#!/usr/bin/env python3
"""
验证 SLSA L4 PoC 的 provenance。

校验项:
    1. 当前 Git HEAD 与 provenance 中的 git_commit 一致。
    2. build.py 的当前哈希与 provenance 中的 build_script_hash 一致。
    3. dist/app 的当前哈希与 provenance 中的 output_hash 一致。
    4. 存在 two-person review 记录（REVIEWERS 文件或 SLSA_REVIEWERS 环境变量）。
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROVENANCE = ROOT / "dist" / "provenance.json"
OUTPUT = ROOT / "dist" / "app"
BUILD_SCRIPT = ROOT / "build.py"
REVIEWERS_FILE = ROOT / "REVIEWERS"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def load_provenance() -> dict:
    if not PROVENANCE.exists():
        raise FileNotFoundError(f"Provenance not found: {PROVENANCE}")
    with open(PROVENANCE, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_git_commit(provenance: dict) -> bool:
    expected = provenance.get("git_commit", "")
    actual = git_commit()
    if actual == "unknown" or expected != actual:
        print(f"[verify] ✘ git commit mismatch: expected={expected}, actual={actual}")
        return False
    print(f"[verify] ✔ git commit matches HEAD: {actual}")
    return True


def verify_script_hash(provenance: dict) -> bool:
    expected = provenance.get("build_script_hash", "")
    if not BUILD_SCRIPT.exists():
        print(f"[verify] ✘ build script not found: {BUILD_SCRIPT}")
        return False
    actual = sha256_file(BUILD_SCRIPT)
    if expected != actual:
        print(
            f"[verify] ✘ build script hash mismatch: expected={expected}, actual={actual}"
        )
        return False
    print("[verify] ✔ build script hash matches")
    return True


def verify_output_hash(provenance: dict) -> bool:
    expected = provenance.get("output_hash", "")
    if not OUTPUT.exists():
        print(f"[verify] ✘ output file not found: {OUTPUT}")
        return False
    actual = sha256_file(OUTPUT)
    if expected != actual:
        print(
            f"[verify] ✘ output hash mismatch: expected={expected}, actual={actual}"
        )
        return False
    print("[verify] ✔ output hash matches provenance")
    return True


def get_reviewers() -> list[str]:
    """
    获取 two-person review 记录。优先级：
        1. SLSA_REVIEWERS 环境变量（逗号分隔）
        2. REVIEWERS 文件（每行一个 reviewer，忽略空行和 # 注释）
    """
    env = os.environ.get("SLSA_REVIEWERS", "").strip()
    if env:
        return [r.strip() for r in env.split(",") if r.strip()]

    if REVIEWERS_FILE.exists():
        reviewers = []
        with open(REVIEWERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if line:
                    reviewers.append(line)
        return reviewers

    return []


def verify_two_person_review(provenance: dict) -> bool:
    reviewers = get_reviewers()
    unique_reviewers = sorted(set(reviewers))
    if len(unique_reviewers) < 2:
        print(
            f"[verify] ✘ two-person review NOT satisfied: only {len(unique_reviewers)} reviewer(s): {unique_reviewers}"
        )
        return False
    print(
        f"[verify] ✔ two-person review confirmed (reviewers: {', '.join(unique_reviewers)})"
    )
    return True


def main() -> int:
    try:
        provenance = load_provenance()
    except Exception as exc:  # noqa: BLE001
        print(f"[verify] ERROR: {exc}", file=sys.stderr)
        return 1

    checks = [
        verify_git_commit(provenance),
        verify_script_hash(provenance),
        verify_output_hash(provenance),
        verify_two_person_review(provenance),
    ]

    if all(checks):
        print("[verify] PASS: SLSA L4 checks succeeded")
        return 0
    else:
        print("[verify] FAIL: one or more SLSA L4 checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
