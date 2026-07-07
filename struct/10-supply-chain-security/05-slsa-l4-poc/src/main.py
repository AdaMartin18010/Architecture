#!/usr/bin/env python3
"""
SLSA L4 PoC: 示例应用源码。
构建后会被复制为 dist/app，并打印构建来源信息。
"""
import json
import os
import sys


def main() -> int:
    provenance_path = os.path.join(
        os.path.dirname(__file__), "..", "dist", "provenance.json"
    )
    provenance = {"builder_id": "local", "git_commit": "unknown"}
    if os.path.exists(provenance_path):
        try:
            with open(provenance_path, "r", encoding="utf-8") as f:
                provenance = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    print(f"SLSA L4 PoC App")
    print(f"  version:    {provenance.get('version', 'unknown')}")
    print(f"  builder:    {provenance.get('builder_id', 'unknown')}")
    print(f"  git_commit: {provenance.get('git_commit', 'unknown')}")
    print(f"  built_at:   {provenance.get('built_at', 'unknown')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
