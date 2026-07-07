#!/usr/bin/env bash
# 形式化验证批量检查脚本（best-effort）
# 用法: ./verify-all.sh
# 返回: 当且仅当某个工具实际运行并失败时返回非 0；工具未安装或无法运行时返回 0
#
# 设计原则:
# - 本地没有安装 TLA+/Alloy/Coq/Isabelle 工具时，打印 [SKIPPED] 并退出 0
# - 检测到工具存在时，尽量实际执行验证
# - 对 TLA+/Alloy 额外尝试通过 java -jar 调用发行版 jar
# - 使用 set -euo pipefail，并通过条件判断捕获预期内的失败

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

# 在候选目录中查找指定 jar
find_jar() {
    local jar_name="$1"
    shift
    for dir in "$@"; do
        if [ -f "$dir/$jar_name" ]; then
            printf '%s/%s' "$dir" "$jar_name"
            return 0
        fi
    done
    return 1
}

# 运行单个检查；失败时设置 FAIL=1 但不退出
run_tool() {
    local name="$1"
    shift
    echo "    执行: $*"
    if "$@" >"$VERIFY_LOG" 2>&1; then
        echo "    [PASS] $name"
    else
        echo "    [FAILED] $name"
        sed 's/^/      /' "$VERIFY_LOG" || true
        FAIL=1
    fi
}

# --- TLA+ 检查 ---
echo "[TLA+] 检查 01-tla-plus 目录..."
TLA_DIR="$ROOT_DIR/struct/07-formal-verification/01-tla-plus"
cd "$TLA_DIR"

TLA_RUNNER=""
declare -a TLA_CMD=()
if has_cmd sany; then
    TLA_RUNNER="sany"
elif has_cmd tlc; then
    TLA_RUNNER="tlc"
else
    TLA_JAR="$(find_jar tla2tools.jar "$TLA_DIR" "$ENV_DIR" "$ROOT_DIR" 2>/dev/null || true)"
    if has_cmd java && [ -n "${TLA_JAR:-}" ]; then
        TLA_RUNNER="java"
        TLA_CMD=(java -cp "$TLA_JAR" tlc2.TLC)
    fi
fi

if [ -z "$TLA_RUNNER" ]; then
    echo "  [SKIPPED] TLA+ 工具未安装 (tlc/sany) 且未找到 tla2tools.jar"
else
    for spec in *.tla; do
        [ -f "$spec" ] || continue
        echo "  - 检查: $spec"
        if [ "$TLA_RUNNER" = "sany" ]; then
            run_tool "$spec" sany "$spec"
        else
            cfg="${spec%.tla}.cfg"
            if [ -f "$cfg" ]; then
                if [ "$TLA_RUNNER" = "tlc" ]; then
                    run_tool "$spec" tlc "$spec"
                else
                    run_tool "$spec" "${TLA_CMD[@]}" "$spec"
                fi
            else
                echo "    [SKIPPED] $spec (tlc 需要同名的 .cfg 配置文件)"
            fi
        fi
    done
fi
echo ""

# --- Alloy 检查 ---
echo "[Alloy] 检查 02-alloy 目录..."
ALLOY_DIR="$ROOT_DIR/struct/07-formal-verification/02-alloy"
cd "$ALLOY_DIR"

ALLOY_RUNNER=""
declare -a ALLOY_CMD=()
if has_cmd alloy; then
    ALLOY_RUNNER="alloy"
elif has_cmd alloy5; then
    ALLOY_RUNNER="alloy5"
else
    ALLOY_JAR="$(find_jar org.alloytools.alloy.dist.jar "$ALLOY_DIR" "$ENV_DIR" "$ROOT_DIR" 2>/dev/null || true)"
    if has_cmd java && [ -n "${ALLOY_JAR:-}" ]; then
        ALLOY_RUNNER="java"
        ALLOY_CMD=(java -jar "$ALLOY_JAR")
    fi
fi

if [ -z "$ALLOY_RUNNER" ]; then
    echo "  [SKIPPED] Alloy 未安装 (alloy/alloy5) 且未找到 org.alloytools.alloy.dist.jar"
else
    for model in *.als; do
        [ -f "$model" ] || continue
        echo "  - 检查: $model"
        if [ "$ALLOY_RUNNER" = "java" ]; then
            # Alloy jar 的 CLI 入口可能支持 exec 子命令或直接跟模型文件；依次尝试
            if "${ALLOY_CMD[@]}" exec "$model" >"$VERIFY_LOG" 2>&1; then
                echo "    [PASS] $model"
            elif "${ALLOY_CMD[@]}" "$model" >"$VERIFY_LOG" 2>&1; then
                echo "    [PASS] $model"
            else
                echo "    [FAILED] $model"
                sed 's/^/      /' "$VERIFY_LOG" || true
                FAIL=1
            fi
        else
            if "$ALLOY_RUNNER" exec "$model" >"$VERIFY_LOG" 2>&1; then
                echo "    [PASS] $model"
            elif "$ALLOY_RUNNER" "$model" >"$VERIFY_LOG" 2>&1; then
                echo "    [PASS] $model"
            else
                echo "    [FAILED] $model"
                sed 's/^/      /' "$VERIFY_LOG" || true
                FAIL=1
            fi
        fi
    done
fi
echo ""

# --- Coq / Rocq 检查 ---
echo "[Coq/Rocq] 检查 03-coq-isabelle/coq-examples 目录..."
COQ_DIR="$ROOT_DIR/struct/07-formal-verification/03-coq-isabelle/coq-examples"
cd "$COQ_DIR"

COQ_RUNNER=""
if has_cmd coqc; then
    COQ_RUNNER="coqc"
elif has_cmd rocq; then
    COQ_RUNNER="rocq"
fi

if [ -z "$COQ_RUNNER" ]; then
    echo "  [SKIPPED] Coq/Rocq 未安装 (coqc/rocq)"
else
    for proof in *.v; do
        [ -f "$proof" ] || continue
        echo "  - 证明检查: $proof"
        if [ "$COQ_RUNNER" = "coqc" ]; then
            run_tool "$proof" coqc "$proof"
        else
            run_tool "$proof" rocq compile "$proof"
        fi
    done
fi
echo ""

# --- Isabelle 检查 ---
echo "[Isabelle] 检查 03-coq-isabelle/isabelle-theories 目录..."
ISA_DIR="$ROOT_DIR/struct/07-formal-verification/03-coq-isabelle/isabelle-theories"
cd "$ISA_DIR"

if has_cmd isabelle; then
    echo "  - 运行 isabelle build -D ."
    run_tool "Isabelle theories" isabelle build -D .
else
    echo "  [SKIPPED] Isabelle 未安装 (isabelle)"
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
