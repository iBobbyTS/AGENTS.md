#!/usr/bin/env python3
"""Template reporter for signed Feishu custom-bot progress messages."""

from __future__ import annotations

import base64
from datetime import datetime
import hashlib
import hmac
import json
from pathlib import Path
import time
from typing import Any, Dict, Optional


# === Agent-editable reporter behavior. Modify only this section after copying. ===

PROJECT_NAME = "REPLACE_WITH_PROJECT_NAME"
REPORT_CREATED_AT = "REPLACE_WITH_COPY_TIME"
PROGRESS_INTERVAL_SECONDS = 60 * 60

START_MESSAGE = "Task started."

TASK_LOG_PATH = Path("/tmp/replace-with-task.log")
LATEST_JSON_PATH = Path("/tmp/replace-with-latest.json")
TASK_DONE_MARKER_PATH = Path("/tmp/replace-with-task.done")
FINAL_LOG_PATH = TASK_LOG_PATH


def extract_progress_message() -> Optional[str]:
    """Return the progress text to send on each interval, or None to skip."""
    if LATEST_JSON_PATH.exists():
        try:
            data = json.loads(LATEST_JSON_PATH.read_text(encoding="utf-8"))
        except Exception as exc:
            return f"Could not parse latest JSON: {type(exc).__name__}: {exc}"
        return json.dumps(data, ensure_ascii=False, indent=2)[:4000]

    if TASK_LOG_PATH.exists():
        lines = TASK_LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
        return "\n".join(lines[-40:])[-4000:] or None

    return "Task is still running; no progress log or latest JSON was found."


def is_task_finished() -> bool:
    """Return True when the task is complete and the final message should be sent."""
    return TASK_DONE_MARKER_PATH.exists()


def format_final_message() -> str:
    """Return the final completion message."""
    if FINAL_LOG_PATH.exists():
        lines = FINAL_LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
        tail = "\n".join(lines[-60:])[-6000:]
        return f"Task finished.\n\nFinal log tail:\n{tail}"
    return "Task finished."


# === End agent-editable reporter behavior. ===


# === Protected Feishu sending utilities. Agents must not modify this section. ===

def gen_sign(timestamp: str, secret: str) -> str:
    # 拼接timestamp和secret
    string_to_sign = "{}\n{}".format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode("utf-8")

    return sign


def secret_config_path() -> Path:
    return Path.home() / ".config" / "feishu-message-sender" / "secret.json"


def _load_secret_config() -> Dict[str, str]:
    path = secret_config_path()
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("secret config must be a JSON object")

    required = ("webhook", "secret", "name")
    config: Dict[str, str] = {}
    for key in required:
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"secret config missing non-empty string field: {key}")
        config[key] = value.strip()
    return config


def _redact(value: str, config: Dict[str, str]) -> str:
    redacted = value
    for key in ("webhook", "secret"):
        secret_value = config.get(key, "")
        if secret_value:
            redacted = redacted.replace(secret_value, "[redacted]")
    return redacted


def _truncate(value: str, limit: int = 2000) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + "...[truncated]"


def format_message(configured_name: str, project_name: str, message_body: str) -> str:
    timestamp = datetime.now().strftime("%m-%d %H:%M:%S")
    return f"{configured_name} - {timestamp} - {project_name}:\n{message_body}"


def send_message(project_name: str, message_body: str, timeout_seconds: int = 10) -> Dict[str, Any]:
    try:
        config = _load_secret_config()
    except Exception as exc:
        return {
            "ok": False,
            "stage": "load_config",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }

    timestamp = str(int(time.time()))
    payload = {
        "timestamp": timestamp,
        "sign": gen_sign(timestamp, config["secret"]),
        "msg_type": "text",
        "content": {
            "text": format_message(config["name"], project_name, message_body),
        },
    }

    try:
        import requests

        response = requests.post(
            config["webhook"],
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=timeout_seconds,
        )
    except Exception as exc:
        return {
            "ok": False,
            "stage": "post",
            "error_type": type(exc).__name__,
            "error": _truncate(_redact(str(exc), config)),
        }

    try:
        response_body: Any = response.json()
    except Exception:
        response_body = _truncate(_redact(getattr(response, "text", ""), config))

    status_code = int(getattr(response, "status_code", 0) or 0)
    api_code = response_body.get("code") if isinstance(response_body, dict) else None
    ok = 200 <= status_code < 300 and (api_code in (None, 0))
    return {
        "ok": ok,
        "stage": "post",
        "status_code": status_code,
        "response": response_body,
    }


def _print_result(label: str, result: Dict[str, Any]) -> None:
    print(json.dumps({"event": label, "result": result}, ensure_ascii=False), flush=True)


def _safe_extract_progress_message() -> Optional[str]:
    try:
        return extract_progress_message()
    except Exception as exc:
        return f"Progress extraction failed: {type(exc).__name__}: {exc}"


def _safe_format_final_message() -> str:
    try:
        return format_final_message()
    except Exception as exc:
        return f"Final message formatting failed: {type(exc).__name__}: {exc}"


def _sleep_seconds() -> int:
    try:
        interval = int(PROGRESS_INTERVAL_SECONDS)
    except Exception:
        interval = 60 * 60
    return max(60, interval)


def run_reporter() -> int:
    _print_result("start", send_message(PROJECT_NAME, START_MESSAGE))

    while True:
        if is_task_finished():
            _print_result("final", send_message(PROJECT_NAME, _safe_format_final_message()))
            return 0

        time.sleep(_sleep_seconds())

        if is_task_finished():
            _print_result("final", send_message(PROJECT_NAME, _safe_format_final_message()))
            return 0

        progress_message = _safe_extract_progress_message()
        if progress_message:
            _print_result("progress", send_message(PROJECT_NAME, progress_message))


if __name__ == "__main__":
    raise SystemExit(run_reporter())

# === End protected Feishu sending utilities. ===
