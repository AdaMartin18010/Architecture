# 可执行工具目录

> **定位**: 将知识体系中的理论模型转化为可运行的代码原型
> **开发策略**: 按 `SUBSEQUENT_PLAN_2026.md` 决策 3A，采用 Python CLI + Streamlit 快速原型
> **版本**: 2026-06-06

---

## 工具清单

| 工具 | 路径 | 用途 | 状态 |
|------|------|------|------|
| 术语查询 | `terminology-query.py` | 跨标准术语搜索（ISO/Togaf/SLSA/MCP/A2A） | ✅ 可用 |
| COCOMO II 计算器 | `cocomo-calculator.py` | 复用模型工作量估算 | ✅ 可用 |
| 形式化验证环境 | `formal-verification-env/` | Docker 化 TLA+/Alloy/Coq/Isabelle | ✅ 已创建 |
| 复用决策工具 | `reuse-decision-tool/` | 交互式六阶段复用决策（Web/CLI） | 🔄 Phase 6 |

---

## 快速开始

```bash
cd struct/99-reference/tools

# 查询术语
python terminology-query.py reusability
python terminology-query.py --standard mcp
python terminology-query.py --list-standards

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

> 最后更新: 2026-06-06
