#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目健康综合检查脚本

一键运行：
- quality-gate-v2.py struct/
- quality-gate-v2.py view/
- cross-index-check.py
- sync-view-from-struct.py
- bash verify-all.sh

用法：python scripts/health-check.py
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list, cwd: Path = PROJECT_ROOT, timeout: int = 300) -> tuple:
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def main():
    checks = [
        ("struct/ 质量门控 V2", [sys.executable, "scripts/quality-gate-v2.py", "struct/"]),
        ("view/ 质量门控 V2", [sys.executable, "scripts/quality-gate-v2.py", "view/"]),
        ("交叉索引一致性", [sys.executable, "scripts/cross-index-check.py"]),
        ("struct/view 同步", [sys.executable, "scripts/sync-view-from-struct.py"]),
    ]

    all_ok = True
    print("=" * 60)
    print("项目健康综合检查")
    print("=" * 60)

    for name, cmd in checks:
        rc, stdout, stderr = run(cmd)
        ok = rc == 0
        all_ok = all_ok and ok
        status = "✅ 通过" if ok else "❌ 失败"
        print(f"\n{name}: {status}")
        if not ok:
            print(stderr or stdout)
        else:
            # 打印关键摘要行
            for line in (stdout or "").splitlines()[-3:]:
                print(f"  {line}")

    # 形式化验证 shell 脚本（best-effort；Windows 优先使用 wsl）
    verify_script = PROJECT_ROOT / "struct" / "99-reference" / "tools" / "formal-verification-env" / "verify-all.sh"
    if sys.platform == "win32":
        # 将 Windows 路径转换为 WSL 路径 /mnt/<drive>/...
        drive = PROJECT_ROOT.drive.lower().rstrip(":") if PROJECT_ROOT.drive else "e"
        rest = PROJECT_ROOT.as_posix()[2:]  # 去掉 "E:" 等盘符前缀
        wsl_path = f"/mnt/{drive}{rest}"
        wsl_script = f"{wsl_path}/struct/99-reference/tools/formal-verification-env/verify-all.sh"
        rc, stdout, stderr = run(["wsl", "bash", wsl_script])
    else:
        rc, stdout, stderr = run(["bash", str(verify_script)])
    ok = rc == 0
    all_ok = all_ok and ok
    status = "✅ 通过" if ok else "❌ 失败"
    print(f"\n形式化验证脚本: {status}")
    if not ok:
        print(stderr or stdout)
    else:
        print(f"  {stdout.strip().splitlines()[-1]}")

    print("\n" + "=" * 60)
    if all_ok:
        print("综合结论：所有检查通过，项目健康度 100%")
        return 0
    else:
        print("综合结论：部分检查失败，请查看上文日志")
        return 1


if __name__ == "__main__":
    sys.exit(main())
