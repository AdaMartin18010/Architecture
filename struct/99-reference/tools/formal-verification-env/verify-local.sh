#!/usr/bin/env bash
# 形式化验证本地 best-effort 运行脚本
# 用法: ./verify-local.sh
#
# 本脚本在不依赖 Docker 的情况下，直接调用本机已安装的 TLA+/Alloy/Coq/Isabelle
# 工具进行验证。缺少的工具会打印 SKIPPED，不会导致整体失败。
#
# 若需要容器化环境，请使用同目录下的 docker-compose.yml：
#   cd struct/99-reference/tools/formal-verification-env
#   docker compose up -d

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 优先尝试使用 WSL 路径（health-check.py 在 Windows 上通过 wsl 调用）
if grep -qi microsoft /proc/version 2>/dev/null && command -v wslpath >/dev/null 2>&1; then
    echo "[INFO] 检测到 WSL 环境，使用本地工具链"
fi

# 形式化验证环境说明
echo "[INFO] 形式化验证本地 best-effort 运行"
echo "[INFO] 脚本位置: $SCRIPT_DIR/verify-local.sh"
echo "[INFO] 实际验证逻辑由 verify-all.sh 执行"
echo ""

# 调用主验证脚本
exec bash "$SCRIPT_DIR/verify-all.sh"
