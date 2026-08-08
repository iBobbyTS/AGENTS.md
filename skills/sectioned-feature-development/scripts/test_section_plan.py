#!/usr/bin/env python3
"""Dependency-free forward tests for section_plan.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("section_plan.py")
TEMPLATE = Path(__file__).parents[1] / "assets" / "PLAN-FULL.template.md"


def run(*args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"command {args} returned {result.returncode}, expected {expected}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def expect_invalid(path: Path, expected_fragment: str) -> None:
    result = run("validate", str(path), expected=2)
    if expected_fragment not in result.stderr:
        raise AssertionError(
            f"expected {expected_fragment!r} in validation error\n{result.stderr}"
        )


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        plan = tmp_path / "PLAN-FULL.md"
        template = TEMPLATE.read_text(encoding="utf-8")
        plan.write_text(template, encoding="utf-8")

        valid = run("validate", str(plan)).stdout
        assert "2 sections" in valid
        listed = run("list", str(plan)).stdout
        assert "S01" in listed and "S02" in listed

        fingerprint = run("fingerprint", str(plan)).stdout.strip()
        assert len(fingerprint) == 64 and all(c in "0123456789abcdef" for c in fingerprint)

        current = tmp_path / "PLAN.md"
        run("extract", str(plan), "S01", "--output", str(current))
        extracted = current.read_text(encoding="utf-8")
        assert "Source SHA-256" in extracted
        assert "## Feature Contract" in extracted
        assert "## S01" in extracted
        assert "## S02" not in extracted
        run("extract", str(plan), "S01", "--output", str(current), expected=2)
        run("extract", str(plan), "S99", "--output", str(tmp_path / "missing.md"), expected=2)

        hierarchical = tmp_path / "HIERARCHICAL.md"
        hierarchical_text = template.replace("S02", "S03.1")
        hierarchical.write_text(hierarchical_text, encoding="utf-8")
        hvalid = run("validate", str(hierarchical)).stdout
        assert "2 sections" in hvalid
        hlisted = run("list", str(hierarchical)).stdout
        assert "S03.1" in hlisted
        hcurrent = tmp_path / "PLAN-HIERARCHICAL.md"
        run("extract", str(hierarchical), "S03.1", "--output", str(hcurrent))
        hextracted = hcurrent.read_text(encoding="utf-8")
        assert "## S03.1" in hextracted

        archive_dir = tmp_path / "plans"
        run(
            "archive",
            str(plan),
            "--dest-dir",
            str(archive_dir),
            "--timestamp",
            "20990101-0000",
        )
        assert (archive_dir / "20990101-0000_FULL.md").exists()
        assert plan.exists(), "safe archive default should copy"
        run(
            "archive",
            str(plan),
            "--dest-dir",
            str(archive_dir),
            "--timestamp",
            "20990101-0000",
            expected=2,
        )

        missing_section_heading = tmp_path / "MISSING-SECTION-HEADING.md"
        missing_section_heading.write_text(
            template.replace("### 验收标准", "### Missing", 1), encoding="utf-8"
        )
        expect_invalid(missing_section_heading, "missing required heading: 验收标准")

        missing_feature_heading = tmp_path / "MISSING-FEATURE-HEADING.md"
        missing_feature_heading.write_text(
            template.replace("### 一句话目标", "### Missing", 1), encoding="utf-8"
        )
        expect_invalid(
            missing_feature_heading,
            "FEATURE-CONTEXT is missing required heading: 一句话目标",
        )

        unknown_dependency = tmp_path / "UNKNOWN-DEPENDENCY.md"
        unknown_dependency.write_text(
            template.replace("- Requires: `S01`", "- Requires: `S99`", 1),
            encoding="utf-8",
        )
        expect_invalid(unknown_dependency, "unknown dependency IDs: S99")

        self_dependency = tmp_path / "SELF-DEPENDENCY.md"
        self_dependency.write_text(
            template.replace("- Requires: `none`", "- Requires: `S01`", 1),
            encoding="utf-8",
        )
        expect_invalid(self_dependency, "S01 cannot depend on itself")

        cyclic = tmp_path / "CYCLIC.md"
        cyclic.write_text(
            template.replace("- Requires: `none`", "- Requires: `S02`", 1),
            encoding="utf-8",
        )
        expect_invalid(cyclic, "dependency cycle:")

    print("section_plan.py tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
