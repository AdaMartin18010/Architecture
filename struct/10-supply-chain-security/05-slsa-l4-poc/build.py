#!/usr/bin/env python3
"""
SLSA Build Level 4 模拟构建脚本。

输入:
    src/main.py

输出:
    dist/app              构建产物（源码的副本，带执行权限）
    dist/provenance.json  来源证明

设计原则（Hermetic）:
    - 不访问外部网络。
    - 输入唯一且声明明确（src/main.py）。
    - 构建脚本自身哈希也被记录，防止构建脚本被篡改后无法发现。
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "main.py"
DIST = ROOT / "dist"
OUTPUT = DIST / "app"
PROVENANCE = DIST / "provenance.json"
BUILD_SCRIPT = Path(__file__).resolve()


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


def copy_with_normalized_newlines(src: Path, dst: Path) -> None:
    """
    以 LF 换行符复制文件，确保 Windows / Linux 构建产出字节一致，
    增强可复现性（Reproducible build）。
    """
    text = src.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n")
    dst.write_text(text, encoding="utf-8", newline="\n")


def build() -> dict[str, str]:
    DIST.mkdir(parents=True, exist_ok=True)

    if not SRC.exists():
        raise FileNotFoundError(f"Source file not found: {SRC}")

    # 1. 生成输出产物（先做内容复制，再设置执行权限，保证可复现）
    copy_with_normalized_newlines(SRC, OUTPUT)
    # 在类 Unix 系统上设置可执行权限；Windows 上 chmod 也会返回成功但不影响 ACL
    os.chmod(OUTPUT, 0o755)

    # 2. 计算各关键输入/输出的哈希
    source_hash = sha256_file(SRC)
    script_hash = sha256_file(BUILD_SCRIPT)
    output_hash = sha256_file(OUTPUT)

    # 3. 收集来源证明
    def rel_posix(path: Path) -> str:
        """返回相对于 ROOT 的正斜杠路径，保证跨平台 provenance 一致。"""
        return path.relative_to(ROOT).as_posix()

    provenance = {
        "version": "1.0.0",
        "builder_id": "slsa-l4-poc-local-builder",
        "build_type": "https://example.com/slsa-l4-poc/build@v1",
        "built_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "build_script_path": rel_posix(BUILD_SCRIPT),
        "build_script_hash": script_hash,
        "source_path": rel_posix(SRC),
        "source_hash": source_hash,
        "output_path": rel_posix(OUTPUT),
        "output_hash": output_hash,
        "slsa_build_level": "L4 (simulated)",
        "invocation": {
            "config_source": {"uri": ROOT.as_posix(), "entry_point": "build.py"},
            "parameters": {},
            "environment": {"os": os.name, "python": sys.version.split()[0]},
        },
    }

    with open(PROVENANCE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(provenance, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return provenance


def main() -> int:
    try:
        provenance = build()
    except Exception as exc:  # noqa: BLE001
        print(f"[build] ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"[build] Source hash:  {provenance['source_hash']}")
    print(f"[build] Script hash:  {provenance['build_script_hash']}")
    print(f"[build] Output hash:  {provenance['output_hash']}")
    print(f"[build] Git commit:   {provenance['git_commit']}")
    print(f"[build] Provenance:   {PROVENANCE.relative_to(ROOT)}")
    print(f"[build] Build complete: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
