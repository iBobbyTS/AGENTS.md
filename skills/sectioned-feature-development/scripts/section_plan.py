#!/usr/bin/env python3
"""Validate, list, extract, fingerprint, and archive sectioned feature plans.

The parser is deliberately strict around durable markers and section headings so
that orchestration does not silently run the wrong section after context resets.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

FEATURE_RE = re.compile(
    r"<!--\s*FEATURE-CONTEXT:START\s*-->(.*?)"
    r"<!--\s*FEATURE-CONTEXT:END\s*-->",
    re.DOTALL | re.IGNORECASE,
)
SECTION_ID_PATTERN = r"S\d{2,}(?:\.\d+)*"
SECTION_RE = re.compile(
    rf"<!--\s*SECTION:({SECTION_ID_PATTERN}):START\s*-->(.*?)"
    rf"<!--\s*SECTION:\1:END\s*-->",
    re.DOTALL | re.IGNORECASE,
)
SECTION_MARKER_RE = re.compile(
    rf"<!--\s*SECTION:({SECTION_ID_PATTERN}):(START|END)\s*-->", re.IGNORECASE
)
ID_RE = re.compile(rf"\b{SECTION_ID_PATTERN}\b", re.IGNORECASE)

REQUIRED_HEADING_GROUPS: tuple[tuple[str, ...], ...] = (
    ("目标", "Goal"),
    ("行为增量", "Observable Behavior Increment", "Behavior Increment"),
    ("依赖", "Dependencies"),
    ("预计范围", "Expected Scope", "Scope"),
    ("非目标", "Non-goals", "Non-Goals"),
    ("全局不变量", "Global Invariants", "Feature-level Invariants"),
    ("验收标准", "Acceptance Criteria"),
    ("验证命令", "Validation Commands", "Verification"),
    ("发布与恢复", "Release and Recovery", "Rollout and Recovery"),
    ("延后项", "Deferred Work"),
)

FEATURE_HEADING_GROUPS: tuple[tuple[str, ...], ...] = (
    ("一句话目标", "One-sentence Goal", "Goal"),
    (
        "用户/操作者可观察行为",
        "User/Operator Observable Behavior",
        "Observable Behavior",
    ),
    ("非目标", "Non-goals", "Non-Goals"),
    ("全局不变量", "Global Invariants"),
    ("硬约束与权威来源", "Hard Constraints and Authorities"),
    ("完整功能验收标准", "Full-feature Acceptance Criteria"),
    ("完整功能验证命令", "Full-feature Validation Commands"),
    ("Ownership / State Boundary", "Ownership and State Boundary"),
    (
        "Compatibility / Migration / Rollout / Rollback",
        "Compatibility, Migration, Rollout, and Rollback",
    ),
)

REQUIRES_LINE_RE = re.compile(
    r"(?mi)^\s*[-*]?\s*(?:Requires|依赖于|前置(?:依赖)?)\s*:\s*(.+?)\s*$"
)


@dataclass(frozen=True)
class Section:
    section_id: str
    title: str
    body: str


@dataclass(frozen=True)
class ParsedPlan:
    path: Path
    text: str
    feature_context: str
    sections: tuple[Section, ...]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"plan not found: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"plan is not valid UTF-8: {path}") from exc


def _heading_present(body: str, aliases: Iterable[str]) -> bool:
    for alias in aliases:
        pattern = rf"(?mi)^###\s+{re.escape(alias)}\s*$"
        if re.search(pattern, body):
            return True
    return False


def _title_for(section_id: str, body: str) -> str:
    match = re.search(
        rf"(?mi)^##\s+{re.escape(section_id)}\s*(?:[—–-]\s*)?(.+?)\s*$", body
    )
    if not match:
        return "<missing title>"
    return match.group(1).strip()


def _marker_errors(text: str) -> list[str]:
    errors: list[str] = []
    stack: list[str] = []
    for marker in SECTION_MARKER_RE.finditer(text):
        section_id = marker.group(1).upper()
        kind = marker.group(2).upper()
        if kind == "START":
            if stack:
                errors.append(
                    f"nested section marker {section_id} inside {stack[-1]} is not allowed"
                )
            stack.append(section_id)
        else:
            if not stack:
                errors.append(f"orphan END marker for {section_id}")
            else:
                started = stack.pop()
                if started != section_id:
                    errors.append(
                        f"mismatched marker: started {started}, ended {section_id}"
                    )
    if stack:
        errors.extend(f"missing END marker for {section_id}" for section_id in stack)
    return errors


def _find_dependency_cycle(graph: dict[str, set[str]]) -> list[str] | None:
    """Return one dependency cycle with the start node repeated, if present."""

    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in visited:
            return None
        if node in visiting:
            start = stack.index(node)
            return stack[start:] + [node]

        visiting.add(node)
        stack.append(node)
        for dependency in sorted(graph.get(node, set())):
            cycle = visit(dependency)
            if cycle:
                return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in sorted(graph):
        cycle = visit(node)
        if cycle:
            return cycle
    return None


def parse_plan(path: Path) -> ParsedPlan:
    text = _read(path)
    errors = _marker_errors(text)

    feature_matches = list(FEATURE_RE.finditer(text))
    if len(feature_matches) != 1:
        errors.append(
            "plan must contain exactly one FEATURE-CONTEXT START/END block"
        )
        feature_context = ""
    else:
        feature_context = feature_matches[0].group(1).strip()
        if not feature_context:
            errors.append("FEATURE-CONTEXT block is empty")

    sections: list[Section] = []
    seen: set[str] = set()
    for match in SECTION_RE.finditer(text):
        section_id = match.group(1).upper()
        body = match.group(2).strip()
        if section_id in seen:
            errors.append(f"duplicate section ID: {section_id}")
        seen.add(section_id)
        if not body:
            errors.append(f"{section_id} block is empty")
        title = _title_for(section_id, body)
        if title == "<missing title>":
            errors.append(f"{section_id} is missing a '## {section_id} — title' heading")
        for aliases in REQUIRED_HEADING_GROUPS:
            if not _heading_present(body, aliases):
                errors.append(
                    f"{section_id} is missing required heading: {aliases[0]}"
                )
        sections.append(Section(section_id=section_id, title=title, body=body))

    if not sections:
        errors.append("plan contains no complete SECTION blocks")

    if feature_context:
        for aliases in FEATURE_HEADING_GROUPS:
            if not _heading_present(feature_context, aliases):
                errors.append(
                    f"FEATURE-CONTEXT is missing required heading: {aliases[0]}"
                )

    known = {section.section_id for section in sections}
    dependency_graph: dict[str, set[str]] = {section_id: set() for section_id in known}
    for section in sections:
        dependency_block = re.search(
            r"(?mis)^###\s+(?:依赖|Dependencies)\s*$\s*(.*?)"
            r"(?=^###\s+|\Z)",
            section.body,
        )
        if not dependency_block:
            continue

        block_text = dependency_block.group(1)
        requires_lines = REQUIRES_LINE_RE.findall(block_text)
        if requires_lines:
            refs = {
                item.upper()
                for line in requires_lines
                for item in ID_RE.findall(line)
            }
        else:
            # Backward-compatible fallback for plans that list dependency IDs
            # directly under the heading without a `Requires:` label.
            refs = {item.upper() for item in ID_RE.findall(block_text)}

        if section.section_id in refs:
            errors.append(f"{section.section_id} cannot depend on itself")
            refs.discard(section.section_id)

        unknown = sorted(refs - known)
        if unknown:
            errors.append(
                f"{section.section_id} references unknown dependency IDs: "
                + ", ".join(unknown)
            )
        dependency_graph[section.section_id] = refs & known

    cycle = _find_dependency_cycle(dependency_graph)
    if cycle:
        errors.append("dependency cycle: " + " -> ".join(cycle))

    raw_starts = len(
        re.findall(rf"<!--\s*SECTION:{SECTION_ID_PATTERN}:START\s*-->", text, re.IGNORECASE)
    )
    raw_ends = len(
        re.findall(rf"<!--\s*SECTION:{SECTION_ID_PATTERN}:END\s*-->", text, re.IGNORECASE)
    )
    if raw_starts != len(sections) or raw_ends != len(sections):
        errors.append(
            "one or more section marker pairs could not be parsed; check IDs and matching END markers"
        )

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))

    return ParsedPlan(
        path=path,
        text=text,
        feature_context=feature_context,
        sections=tuple(sections),
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def command_validate(args: argparse.Namespace) -> int:
    plan = parse_plan(Path(args.plan))
    print(
        f"valid: {plan.path} ({len(plan.sections)} sections, "
        f"sha256={sha256_text(plan.text)})"
    )
    return 0


def command_list(args: argparse.Namespace) -> int:
    plan = parse_plan(Path(args.plan))
    for section in plan.sections:
        print(f"{section.section_id}\t{section.title}")
    return 0


def command_extract(args: argparse.Namespace) -> int:
    plan = parse_plan(Path(args.plan))
    requested = args.section.upper()
    selected = next(
        (section for section in plan.sections if section.section_id == requested), None
    )
    if selected is None:
        available = ", ".join(section.section_id for section in plan.sections)
        raise ValueError(f"unknown section {requested}; available: {available}")

    output = Path(args.output)
    if output.exists() and not args.force:
        raise ValueError(f"output exists: {output}; pass --force to replace it")
    output.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    content = (
        "# 当前 Section 实施计划\n\n"
        "> 本文件由 `section_plan.py extract` 生成；权威来源仍为完整计划。\n\n"
        f"- Source plan: `{plan.path}`\n"
        f"- Source SHA-256: `{sha256_text(plan.text)}`\n"
        f"- Section: `{selected.section_id}`\n"
        f"- Generated at: `{timestamp}`\n\n"
        "## Feature Context\n\n"
        f"{plan.feature_context}\n\n"
        "## Current Section\n\n"
        f"{selected.body}\n"
    )
    output.write_text(content, encoding="utf-8")
    print(f"extracted {selected.section_id} -> {output}")
    return 0


def command_fingerprint(args: argparse.Namespace) -> int:
    path = Path(args.plan)
    text = _read(path)
    print(sha256_text(text))
    return 0


def command_archive(args: argparse.Namespace) -> int:
    source = Path(args.plan)
    parse_plan(source)
    dest_dir = Path(args.dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M")
    destination = dest_dir / f"{timestamp}_FULL.md"
    if destination.exists():
        raise ValueError(f"archive exists: {destination}")
    if args.move:
        shutil.move(str(source), str(destination))
        action = "moved"
    else:
        shutil.copy2(source, destination)
        action = "copied"
    print(f"{action} {source} -> {destination}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage sectioned feature PLAN-FULL.md artifacts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="validate a full plan")
    validate_parser.add_argument("plan")
    validate_parser.set_defaults(func=command_validate)

    list_parser = subparsers.add_parser("list", help="list section IDs and titles")
    list_parser.add_argument("plan")
    list_parser.set_defaults(func=command_list)

    extract_parser = subparsers.add_parser(
        "extract", help="extract feature context and one section"
    )
    extract_parser.add_argument("plan")
    extract_parser.add_argument("section")
    extract_parser.add_argument("--output", required=True)
    extract_parser.add_argument(
        "--force", action="store_true", help="replace an existing output file"
    )
    extract_parser.set_defaults(func=command_extract)

    fingerprint_parser = subparsers.add_parser(
        "fingerprint", help="print the plan SHA-256"
    )
    fingerprint_parser.add_argument("plan")
    fingerprint_parser.set_defaults(func=command_fingerprint)

    archive_parser = subparsers.add_parser(
        "archive", help="copy or move a validated plan to a timestamped archive"
    )
    archive_parser.add_argument("plan")
    archive_parser.add_argument("--dest-dir", required=True)
    archive_parser.add_argument(
        "--timestamp", help="override YYYYMMDD-HHMM archive timestamp"
    )
    archive_parser.add_argument(
        "--move", action="store_true", help="move instead of the safe default copy"
    )
    archive_parser.set_defaults(func=command_archive)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(f"error:\n{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
