---
name: feishu-message-sender
description: Send signed Feishu custom-bot text notifications for Codex task starts, periodic progress, and completion using a bundled reporter template. Use only when the user explicitly asks to use $feishu-message-sender, feishu-message-sender, or this Feishu notification skill to send them messages.
---

# Feishu Message Sender

Use this skill only for explicit user requests to send Feishu progress messages.

## Hard Rules

- Do not read, print, summarize, copy, or inspect `~/.config/feishu-message-sender/secret.json`.
- Do not include webhook URLs, secrets, or secret-file contents in chat, logs, patches, or test output.
- Do not modify the protected sending utilities in `scripts/feishu_reporter_template.py`.
- Modify only the agent-editable reporter behavior block after copying the template.
- Do not send a real test message unless the user explicitly asks for one.

## Workflow

1. Copy `scripts/feishu_reporter_template.py` to:

   ```bash
   /tmp/codex-feishu-message-sender/<project-slug>/feishu_reporter.py
   ```

2. If that target file already exists, stop before overwriting it:
   - Check whether a process is running that script path.
   - Inspect only the copied reporter script, not the secret file.
   - Read `PROJECT_NAME`, `REPORT_CREATED_AT`, and `PROGRESS_INTERVAL_SECONDS` from the copied script when present.
   - Use the file mtime to estimate when it was created or last changed.
   - Tell the user what you found and ask whether to delete it, overwrite it, or copy to a new path.

3. Edit only the agent-editable block in the copied reporter:
   - `PROJECT_NAME`
   - `REPORT_CREATED_AT`
   - `START_MESSAGE`
   - `PROGRESS_INTERVAL_SECONDS`
   - log or JSON paths used by progress extraction
   - `extract_progress_message()`
   - `is_task_finished()`
   - `format_final_message()`

4. Start the reporter in the background, then end the current assistant turn:

   ```bash
   nohup python3 /tmp/codex-feishu-message-sender/<project-slug>/feishu_reporter.py >> /tmp/codex-feishu-message-sender/<project-slug>/feishu_reporter.log 2>&1 &
   echo $! > /tmp/codex-feishu-message-sender/<project-slug>/feishu_reporter.pid
   ```

## Existing Reporter Check

Use commands like these, replacing the path:

```bash
pgrep -af '/tmp/codex-feishu-message-sender/<project-slug>/feishu_reporter.py' || true
python3 - <<'PY'
from pathlib import Path
from datetime import datetime

p = Path("/tmp/codex-feishu-message-sender/<project-slug>/feishu_reporter.py")
if p.exists():
    print("mtime:", datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"))
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(("PROJECT_NAME =", "REPORT_CREATED_AT =", "PROGRESS_INTERVAL_SECONDS =")):
            print(line)
PY
```

## Message Format

The protected template sends plain text through Feishu custom bot webhook requests. It formats messages as:

```text
{configured_name} - {MM-DD HH:MM:SS} - {PROJECT_NAME}:
{message_body}
```

The template signs each request with `timestamp` and `sign` as documented in Feishu custom bot docs: <https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot.md>.
