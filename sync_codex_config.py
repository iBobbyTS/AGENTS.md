#!/usr/bin/env python3
"""Sync this repository's Codex instructions into the user Codex home."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


IGNORED_COPY_PATTERNS = shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc")


class SyncError(RuntimeError):
    """Raised when the sync cannot complete safely."""


def run_git(repo: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def print_process_output(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)


def git_head(repo: Path) -> str:
    result = run_git(repo, ["rev-parse", "HEAD"])
    if result.returncode != 0:
        print_process_output(result)
        raise SyncError("Could not read the current git HEAD.")
    return result.stdout.strip()


def pull_repository(repo: Path) -> bool:
    before = git_head(repo)

    result = run_git(repo, ["pull", "--ff-only"])
    print_process_output(result)
    if result.returncode != 0:
        raise SyncError("git pull failed; nothing was synced.")

    after = git_head(repo)
    return before != after


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    if path.is_dir():
        shutil.rmtree(path)
        return
    if path.exists():
        raise SyncError(f"Refusing to remove unsupported path type: {path}")


def replace_file(source: Path, target: Path) -> None:
    if not source.is_file():
        raise SyncError(f"Missing source file: {source}")
    if target.exists() and target.is_dir() and not target.is_symlink():
        raise SyncError(f"Refusing to replace directory with file: {target}")

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_target = target.with_name(f".{target.name}.tmp-{os.getpid()}")
    remove_existing(tmp_target)
    try:
        shutil.copy2(source, tmp_target)
        os.replace(tmp_target, target)
    finally:
        remove_existing(tmp_target)


def replace_directory(source: Path, target: Path) -> None:
    if not source.is_dir():
        raise SyncError(f"Missing source directory: {source}")

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_target = target.with_name(f".{target.name}.tmp-{os.getpid()}")
    remove_existing(tmp_target)
    try:
        shutil.copytree(
            source,
            tmp_target,
            symlinks=True,
            ignore=IGNORED_COPY_PATTERNS,
        )
        remove_existing(target)
        tmp_target.rename(target)
    finally:
        remove_existing(tmp_target)


def iter_skill_sources(skills_dir: Path) -> list[Path]:
    if not skills_dir.is_dir():
        raise SyncError(f"Missing source skills directory: {skills_dir}")
    return sorted(
        child
        for child in skills_dir.iterdir()
        if not child.name.startswith(".") and child.is_dir()
    )


def sync_codex_files(repo: Path, codex_home: Path) -> list[str]:
    repo = repo.resolve()
    codex_home = codex_home.expanduser()

    source_skills_dir = repo / "skills"
    target_skills_dir = codex_home / "skills"
    synced: list[str] = []

    for skill_dir in iter_skill_sources(source_skills_dir):
        replace_directory(skill_dir, target_skills_dir / skill_dir.name)
        synced.append(f"skills/{skill_dir.name}")

    replace_file(repo / "AGENTS.md", codex_home / "AGENTS.md")
    synced.append("AGENTS.md")
    return synced


def deploy_after_pull(repo: Path, codex_home: Path, force: bool = False) -> bool:
    try:
        did_update = pull_repository(repo)
    except SyncError as exc:
        if not force:
            raise
        print(f"git pull did not complete ({exc}); syncing because --force was set.")
    else:
        if not did_update and not force:
            print("No git updates found; exiting without syncing.")
            return False
        if force:
            print("Syncing after git pull because --force was set.")

    synced = sync_codex_files(repo, codex_home)
    print(f"Synced {len(synced)} item(s) into {codex_home.expanduser()}:")
    for item in synced:
        print(f"  - {item}")
    return True


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run git pull for this repository, then sync AGENTS.md and skills/* "
            "into ~/.codex when the pull changed HEAD or --force is set."
        )
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Sync after git pull even when the pull found no update or failed.",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Repository to pull and sync. Defaults to the directory containing this script.",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path.home() / ".codex",
        help="Destination Codex home. Defaults to ~/.codex.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        deploy_after_pull(args.repo, args.codex_home, force=args.force)
    except SyncError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
