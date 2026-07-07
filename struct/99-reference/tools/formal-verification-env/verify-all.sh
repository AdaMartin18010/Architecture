#!/usr/bin/env bash
# 形式化验证批量检查脚本
# 用法: ./verify-all.sh
# 返回: 所有检查通过则退出码 0，否则非 0
#
# 设计原则:
# - 本地没有安装 TLA+/Alloy/Coq/Isabelle 工具时，打印 SKIPPED 并退出 0
# - 检测到工具存在时，尽量实际执行验证
# - 使用 set -euo pipefail，但通过条件判断与 || 捕获预期内的失败

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
ENV_DIR="$ROOT_DIR/struct/99-reference/tools/formal-verification-env"
FAIL=0

# 临时日志文件，用于在命令失败时展示详情
VERIFY_LOG="$(mktemp -t verify-all.XXXXXX)"
trap 'rm -f "$VERIFY_LOG"' EXIT

echo "========================================"
echo "形式化验证批量检查"
echo "========================================"
echo ""

# 检查命令是否存在
has_cmd() {
    command -v "$1" >/dev/null 2>&1
}

# 运行单个检查；失败时设置 FAIL=1 但不退出
run_check() {
    local name="$1"
    shift
    echo "    执行: $*"
    if "$@" >"$VERIFY_LOG" 2>&1; then
        echo "    ✅ 通过: $name"
    else
        echo "    ❌ 失败: $name"
        sed 's/^/      /' "$VERIFY_LOG" || true
        FAIL=1
    fi
}

# --- TLA+ 检查 ---
echo "[TLA+] 检查 01-tla-plus 目录..."
TLA_DIR="$ROOT_DIR/struct/07-formal-verification/01-tla-plus"
if has_cmd tlc || has_cmd sany; then
    cd "$TLA_DIR"
    for spec in *.tla; do
        [ -f "$spec" ] || continue
        echo "  - 检查: $spec"
        # 优先使用 SANY 做纯语法检查；它比 TLC 更适合无 .cfg 的场景
        if has_cmd sany; then
            run_check "$spec" sany "$spec"
        elif has_cmd tlc; then
            cfg="${spec%.tla}.cfg"
            if [ -f "$cfg" ]; then
                run_check "$spec" tlc "$spec"
            else
                echo "    SKIPPED: $spec (tlc 需要同名的 .cfg 配置文件)"
            fi
        fi
    done
else
    echo "  SKIPPED: TLA+ 工具未安装 (tlc/sany)"
fi
echo ""

# --- Alloy 检查 ---
echo "[Alloy] 检查 02-alloy 目录..."
ALLOY_DIR="$ROOT_DIR/struct/07-formal-verification/02-alloy"
if has_cmd alloy; then
    cd "$ALLOY_DIR"
    for model in *.als; do
        [ -f "$model" ] || continue
        echo "  - 检查: $model"
        # Alloy 发行版的 CLI 参数不尽相同，优先尝试最常见的 exec 子命令
        if alloy exec "$model" >"$VERIFY_LOG" 2>&1; then
            echo "    ✅ 通过: $model"
        elif alloy "$model" >"$VERIFY_LOG" 2>&1; then
            echo "    ✅ 通过: $model"
        else
            echo "    ❌ 失败: $model"
            sed 's/^/      /' "$VERIFY_LOG" || true
            FAIL=1
        fi
    done
else
    echo "  SKIPPED: Alloy 未安装 (alloy)"
fi
echo ""

# --- Coq / Rocq 检查 ---
echo "[Coq/Rocq] 检查 03-coq-isabelle/coq-examples 目录..."
COQ_DIR="$ROOT_DIR/struct/07-formal-verification/03-coq-isabelle/coq-examples"
if has_cmd rocq || has_cmd coqc; then
    cd "$COQ_DIR"
    for proof in *.v; do
        [ -f "$proof" ] || continue
        echo "  - 证明检查: $proof"
        if has_cmd rocq; then
            run_check "$proof" rocq compile "$proof"
        else
            run_check "$proof" coqc "$proof"
        fi
    done
else
    echo "  SKIPPED: Coq/Rocq 未安装 (rocq/coqc)"
fi
echo ""

# --- Isabelle 检查 ---
echo "[Isabelle] 检查 03-coq-isabelle/isabelle-theories 目录..."
ISA_DIR="$ROOT_DIR/struct/07-formal-verification/03-coq-isabelle/isabelle-theories"
if has_cmd isabelle; then
    cd "$ISA_DIR"
    echo "  - 运行 isabelle build -D ."
    run_check "Isabelle theories" isabelle build -D .
else
    echo "  SKIPPED: Isabelle 未安装 (isabelle)"
fi
echo ""

# 清理 Coq/Rocq 生成的中间文件，避免污染仓库
find "$ROOT_DIR/struct/07-formal-verification" -type f \
    \( -name '*.vo' -o -name '*.vok' -o -name '*.vos' -o -name '*.glob' -o -name '*.aux' \) \
    -delete 2>/dev/null || true

echo "========================================"
if [ $FAIL -eq 0 ]; then
    echo "所有形式化检查通过（或暂无需检查项）"
else
    echo "部分形式化检查失败，请查看上文日志"
fi
echo "========================================"

exit $FAIL
