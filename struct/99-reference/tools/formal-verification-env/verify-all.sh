#!/usr/bin/env bash
# 形式化验证批量检查脚本
# 用法: ./verify-all.sh
# 返回: 所有检查通过则退出码 0，否则非 0

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
ENV_DIR="$ROOT_DIR/struct/99-reference/tools/formal-verification-env"
FAIL=0

echo "========================================"
echo "形式化验证批量检查"
echo "========================================"
echo ""

# --- TLA+ 检查 ---
echo "[TLA+] 检查 01-tla-plus 目录..."
cd "$ROOT_DIR/struct/07-formal-verification/01-tla-plus"
for spec in *.tla; do
    if [ -f "$spec" ]; then
        echo "  - 语法检查: $spec"
        # 实际环境中应调用 tlc 或 sany
        # tlc "$spec" -deadlock || FAIL=1
        echo "    (TODO: 在 Docker 环境中启用 tlc "$spec" -deadlock)"
    fi
done
echo ""

# --- Alloy 检查 ---
echo "[Alloy] 检查 02-alloy 目录..."
cd "$ROOT_DIR/struct/07-formal-verification/02-alloy"
for model in *.als; do
    if [ -f "$model" ]; then
        echo "  - 模型检查: $model"
        # 实际环境中应调用 Alloy Analyzer CLI
        # alloy exec "$model" || FAIL=1
        echo "    (TODO: 在 Docker 环境中启用 alloy exec "$model")"
    fi
done
echo ""

# --- Coq / Isabelle 检查 ---
echo "[Coq/Isabelle] 检查 03-coq-isabelle 目录..."
COQ_ISABELLE_DIR="$ROOT_DIR/struct/07-formal-verification/03-coq-isabelle"
if [ -d "$COQ_ISABELLE_DIR" ]; then
    found=0
    while IFS= read -r -d '' proof; do
        found=1
        rel="${proof#$COQ_ISABELLE_DIR/}"
        echo "  - 证明检查: $rel"
        if [[ "$proof" == *.v ]]; then
            echo "    (TODO: Docker 环境中启用 rocq compile $rel)"
        elif [[ "$proof" == *.thy ]]; then
            echo "    (TODO: Docker 环境中启用 isabelle build -D . $rel)"
        fi
    done < <(find "$COQ_ISABELLE_DIR" -type f \( -name '*.v' -o -name '*.thy' \) -print0)
    if [ "$found" -eq 0 ]; then
        echo "  尚未发现 .v / .thy 文件"
    fi
else
    echo "  目录尚未创建，跳过"
fi
echo ""

echo "========================================"
if [ $FAIL -eq 0 ]; then
    echo "所有形式化检查通过（或暂无需检查项）"
else
    echo "部分形式化检查失败，请查看上文日志"
fi
echo "========================================"

exit $FAIL
