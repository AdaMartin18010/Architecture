# 可执行工具目录

> **定位**: 将知识体系中的理论模型转化为可运行的代码原型
> **开发策略**: 按 `SUBSEQUENT_PLAN_2026.md` 决策 3A，采用 Python CLI + Streamlit 快速原型
> **版本**: 2026-06-12

---

## 工具清单

| 工具 | 路径 | 用途 | 状态 |
|------|------|------|------|
| 术语查询 | `terminology-query.py` | 跨标准术语搜索、对比、版本提示、导出、同步（ISO/Togaf/SLSA/MCP/A2A） | ✅ 可用 |
| COCOMO II 计算器 | `cocomo-calculator.py` | 复用模型工作量估算 | ✅ 可用 |
| 形式化验证环境 | `formal-verification-env/` | Docker 化 TLA+/Alloy/Coq/Isabelle | ✅ 已创建 |
| 复用决策工具 | `reuse-decision-tool/` | 交互式六阶段复用决策（Web/CLI） | 🔄 Phase 6 |

---

## 术语数据库

- 术语数据外部化到同目录的 `terminology-db.yaml`（推荐）或 `terminology-db.json`。
- 文件结构包含三个顶层键：`terms`（术语定义）、`aliases`（标准别名）、`version_hints`（权威版本提示）。
- 脚本启动时优先加载外部文件；若文件不存在，则回退到内置字典，保证单文件可运行。
- 使用 `sync` 命令可从 Markdown 表格自动同步术语别名与标准版本提示到数据库（默认 dry-run，需 `--apply` 才会写入）。

---

## 快速开始

```bash
cd struct/99-reference/tools

# 查询术语
python terminology-query.py search "architecture view"
python terminology-query.py search "复用" --lang zh

# 跨标准对比
python terminology-query.py compare "reusability" --standards iso25010,ieee1517 --lang zh

# 列出某标准下的术语
python terminology-query.py list --standard togaf10 --lang zh

# 权威版本提示
python terminology-query.py version-hint "reusability" --lang zh

# 导出生词表
python terminology-query.py export-glossary --format md --output glossary.md
python terminology-query.py export-glossary --format json --output glossary.json
python terminology-query.py export-glossary --format yaml --output glossary.yaml

# 从 Markdown 来源同步（默认 dry-run）
python terminology-query.py sync \
  --sources ../../99-reference/glossary/terminology-crosswalk.md,../../99-reference/standards-index/authoritative-sources-v2.md \
  --lang zh

# 应用同步到 terminology-db.yaml
python terminology-query.py sync \
  --sources ../../99-reference/glossary/terminology-crosswalk.md,../../99-reference/standards-index/authoritative-sources-v2.md \
  --apply --lang zh

# 运行内置单元测试
python terminology-query.py --test

# COCOMO II 计算
python cocomo-calculator.py --ksloc-reused 50 --aaf 0.4 --em 1.2

# 启动形式化验证环境
cd formal-verification-env
docker compose up -d
bash verify-all.sh
```

---

## 计划中的工具（按 `SUBSEQUENT_PLAN_2026.md`）

- `maturity-assessment-cli.py` — ISO/IEC 26566:2026 复用成熟度评估问卷（Phase 2）
- `finops-allocation.py` — 跨层 FinOps 成本分摊计算器（Phase 2）
- `probabilistic-contract-calibration.py` — AI 概率契约校准工具（Phase 2）
- `piu-bayesian-tool.py` — IEC 61508 Proven-in-Use 统计验证（Phase 3）
- `supply-chain-attack-tree-viz.py` — 供应链攻击树可视化（Phase 4）
- `reuse-decision-tool/` — 交互式复用决策 Web/CLI（Phase 6）

---

> 最后更新: 2026-06-12
