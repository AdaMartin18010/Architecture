# HERMES-TASKS — 可执行任务池

> **定位**: 本文件是 Hermes 本地规范的**执行任务池**（见根目录 `AGENTS.md` R6）。`struct/MASTER_PLAN.md` 管阶段里程碑，本文件管可执行任务：每条任务带「动作 / 涉及文件 / 验证命令 / 完成标准」四要素，完成即勾选 `[x]`。
> **沉淀规则**: 新 backlog 从报告型检查的告警中沉淀（`reports/errata-lint.md`、`terminology-crosscheck.md`、`authority-source-audit.md`、`standard-version-audit.md`、`cross-index-report.md`、`figure-check.md`），按 P0/P1/P2 定级。
> **同步状态**: T0 批次随 Hermes 本地规范落地（2026-07-12）；T1 依据 `reports/authority-alignment-errata.md` 与 `reports/critical-analysis-authority-alignment-2026-08.md`；T2/T3 依据各专项检查报告。
> **核查日期**: 2026-07-12

---

## 概念定义：任务池的运作方式

**任务池（Task Pool）**是"报告型检查告警 → 可执行工作项"的转化器。门控脚本只负责发现问题，本文件负责把问题变成有人执行、可验证、可收口的工作项。执行纪律：开工前先跑 R 循环的开工检查；每个完成的任务必须留下验证命令的输出证据（粘贴或引用报告路径）；每批收口时同步刷新统计真源并语义化提交。

## R 循环巡检规程（每次会话）

| 时点 | 动作 | 命令 |
| ---- | ---- | ---- |
| 开工 | 确认基线 | `git status` |
| 开工 | 全量健康检查（红则先修复再开工） | `python scripts/health-check.py` |
| 收口 | 重新生成派生物 | `python scripts/sync-view-from-struct.py && python scripts/build-deliverables.py` |
| 收口 | 产物校验 + 统计刷新 | `python scripts/dist-check.py && python scripts/knowledge-cli.py stats` |
| 收口 | 勾选本文件已完成任务，语义化提交 | `git add -p && git commit` |

### 反例

- 直接改 `view/volume-*.md` 或 `dist/` 完成任务——违反 AGENTS.md R2，下次生成即丢失。
- 任务完成却不跑验证命令就勾选——任务池失去可信度。
- 把报告型 warning 当"门禁失败"反复重跑——报告型检查只沉淀任务，不阻断流程（见 AGENTS.md R4）。

---

## T1 · P0 事实修复批（优先级最高，全部有报告依据）

| # | 状态 | 动作 | 涉及文件 | 验证命令 | 完成标准 | 依据 |
| - | - | - | - | - | - | - |
| T1.1 | [ ] | SWEBOK V4 知识领域 15→18 修正，补 3 个新增 KA 映射 | `struct/01-meta-model-standards/05-swebok-v4/` 及相关引用处 | `python scripts/cross-index-check.py` | 全文无"15 个知识领域"残留，新增 KA 有映射 | critical-analysis-2026-08 :71 |
| T1.2 | [ ] | `ArchiMate 4.2` 错误版本号全文清理为 4.0 | 全库 grep 定位 | `grep -r "4\.2" struct/ --include="*.md" \| grep -i archimate` 无命中 | 零残留 | authority-alignment-errata A2 |
| T1.3 | [ ] | 修复 IEC 62443-4-2 标题错年：原误标为 2025（正确为 2019）；更新要点挂 IEC TS 62443-6-2:2025 | `struct/11-industrial-iot-otit/06-functional-safety/` 及引用处 | `python scripts/standard-version-audit.py` | 版本串审计无该错项 | 同上 A3 |
| T1.4 | [ ] | SSDF 1.2 统一表述为 Initial Public Draft（消除同文件"已发布/IPD"自相矛盾） | `struct/10-supply-chain-security/12-nist-ssdf-update/` 等 | `python scripts/errata-lint.py` + 人工复核 B1 | 全文表述一致 | 同上 B1 |
| T1.5 | [ ] | MCP "2026-07-28 RC" 残留引用统一为"稳定版 2025-11-25"措辞（现役文档；历史快照除外） | 现役 struct/ 文档 | `grep -rn "2026-07-28" struct/` 仅 _ARCHIVE/历史声明处命中 | 现役文档零残留 | 同上 B2 |
| T1.6 | [ ] | KG 中不存在版本实体（ISO/IEC 25010:2024 等）清理：修正源登记或重跑 kg-builder | `struct/99-reference/knowledge-graph/` 产物 | `python scripts/kg-shacl-validate.py` + `reports/stats.json` KG 段 | 不存在版本实体不再作为活实体 | 同上 A1 |
| T1.7 | [ ] | dist/ 全链路重建并校验 | `dist/`、`view/` | `python scripts/sync-view-from-struct.py && python scripts/build-deliverables.py && python scripts/dist-check.py` | dist-check 通过，view 14/14 哈希一致 | dist-check.md |

## T2 · P1 内容深化批

| # | 状态 | 动作 | 涉及文件 | 验证命令 | 完成标准 |
| - | - | - | - | - | - |
| T2.1 | [ ] | 26 个高频未收录标准分批补入权威来源表（先 ISO/IEC 类） | `struct/99-reference/standards-index/authoritative-sources-v2.md` | `python scripts/errata-lint.py`（CHK-BASELINE-GAP 清零） | 26 条全部补录并带官方 URL |
| T2.2 | [ ] | 术语双库 16 项缺口补全（YAML 有/glossary 缺 3 + glossary 有/YAML 缺 13） | `struct/99-reference/glossary/glossary-master.md` + `terminology-db.yaml` | `python scripts/terminology-crosscheck.py` | 双向缺口清零 |
| T2.3 | [ ] | FinOps Framework 2025 Scopes/AI/SaaS/DC 成本分摊吸收 | `struct/06-cross-layer-governance/04-finops-cost/` | `python scripts/quality-gate-v2.py struct/` | 新内容过七要素，含 2025 Scopes |
| T2.4 | [ ] | Platform Engineering 2025/2026 实证数据 + 组织设计/ROI 模板 | `struct/13-emerging-trends/01-platform-engineering/` | 同上 | 含 CNCF 成熟度实证与可复用模板 |
| T2.5 | [ ] | DAMA-DMBOK 2R 数据治理映射专题 | `struct/03-application-architecture-reuse/05-data-architecture/` | 同上 | 新增专题文档过门控 |
| T2.6 | [ ] | EU AI Act GPAI Code of Practice 映射 | `struct/12-ai-native-reuse/06-ai-governance/` | 同上 | 映射表完整、来源可核查 |
| T2.7 | [ ] | ISO 23247-5/-6 数字线程/组合内容补充 | `struct/11-industrial-iot-otit/05-digital-twin-aas/` | 同上 | 两分部内容齐备 |
| T2.8 | [ ] | 图文绑定率提升：14 个主题 README/正文各绑定 ≥1 张核心图 | 各主题 README + `struct/99-reference/visualizations/` | `python scripts/figure-check.py` | 绑定率 ≥ 50%（现状 12/75=16%） |
| T2.9 | [ ] | MCP/A2A 跨主题重复收敛：`05/06-mcp-a2a-protocols` 等处改为引用 `12-ai-native-reuse/` 单一事实源 | `struct/05-functional-architecture-reuse/06-mcp-a2a-protocols/` 等 | `python scripts/link-checker.py` + quality-gate | 单一事实源落地，无内容级重复 |

## T3 · P2 机制建设批（长期滚动）

| # | 状态 | 动作 | 涉及文件 | 验证命令 | 完成标准 |
| - | - | - | - | - | - |
| T3.1 | [ ] | 月度跨主题一致性审查脚本（沉淀 cross-index/terminology/authority 报告型检查为月度工件） | `scripts/` + `.github/workflows/` | 试运行产生月度报告 | 报告可生成、含趋势对比 |
| T3.2 | [ ] | 形式化公理机器验证：2026-Q4 前完成 3 条核心公理 TLA+/Alloy 规约 | `struct/01-meta-model-standards/06-formal-axioms/`、`struct/07-formal-verification/` | CI formal-verification best-effort | 3 条公理有机器可检规约 |
| T3.3 | [ ] | 标准别名残留 1,931 处按风险分批人工复核 | 全库 | `python scripts/standard-name-normalizer.py`（报告模式） | 高风险的清零，其余有 backlog 记录 |
| T3.4 | [ ] | standard-status-checker 对 ISO 403 改"反爬受限"分类 | `scripts/standard-status-checker.py` | 模拟 403 场景测试 | 不再误记"失效" |
| T3.5 | [ ] | KG 同义实体归一 + dangling 约束清理 | `scripts/kg-relation-enricher.py` + KG 产物 | `python scripts/kg-shacl-validate.py` | SHACL 自定义约束告警下降 |

---

## 任务来源与优先级分析

任务来源全部为机器可核查的报告（非主观判断），优先级按"事实错误 > 内容缺口 > 机制建设"排序：T1 不修复会持续传播错误事实（如 SWEBOK KA 数量被外部引用）；T2 决定知识体系对 2025–2026 新标准的覆盖度；T3 是降低未来维护成本的机制性投资。每批收口后按 R 循环刷新统计真源并在 MASTER_PLAN 对应 Phase 更新进度。

## 权威来源

> **权威来源**:
>
> - `reports/authority-alignment-errata.md`（T1.2–T1.6 依据）
> - `reports/critical-analysis-authority-alignment-2026-08.md`（T1.1、T2.3–T2.7 依据）
> - `reports/errata-lint.md`、`reports/terminology-crosscheck.md`、`reports/figure-check.md`（T2.1/T2.2/T2.8 依据）
> - `reports/critical-review-round2-2026-07.md`（T3.3 依据）
> - 根目录 `AGENTS.md`（执行纪律与真源层级）
>
> **核查日期**: 2026-07-12
