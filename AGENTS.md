# AGENTS.md — Hermes 本地规范（项目级 Agent 执行章程）

> 本文件是本项目所有自动化/AI 协作者（agent）的**执行章程**，由项目现状推导（无外部成文规范），与 `CONTRIBUTING.md`（人类贡献规范）、`struct/MASTER_PLAN.md`（阶段计划）、`struct/HERMES-TASKS.md`（执行任务池）配套使用。冲突时以本文件的 R1 真源层级裁决。

## 1. 项目主题（一句话）

《软件工程架构复用视角 · 结构化知识体系》：把 ~31 万字源文档转化为结构化、可验证、可输出的中文知识产品，对齐 30+ 国际标准（ISO 420xx、TOGAF 10、ArchiMate 4.0、SLSA 1.2、MCP/A2A、IEC 61508 等）。

规模与统计数字**一律以 `reports/stats.json` 为唯一真源**（由 `scripts/knowledge-cli.py stats` 机器生成），任何文档不得手写过期的文件数/词数。

## 2. 目录地图与职责

| 路径 | 职责 | 性质 |
| ------ | ------ | ------ |
| `struct/` | 全部知识内容的**唯一真源**（14 个 `NN-主题/` + `99-reference/` + `MASTER_PLAN.md` + `_ARCHIVE/`） | 直接维护 |
| `view/` | 派生卷册层：14 个现役 `volume-NN-*.md`（由 `sync-view-from-struct.py` 按内容哈希生成）+ `_HISTORICAL_/` 8 个只读快照 | **禁止手改** |
| `dist/` | 输出层：`build-deliverables.py` 聚合生成（全书/分卷/课程）+ PDF/slides | **禁止手改** |
| `scripts/` | 质量门控（17）、构建输出（4）、修复批处理与同步（11）共 32 个 Python 脚本 | 直接维护 |
| `reports/` | 门控与审计报告输出口；**脚本生成的文件不手改**，人工报告命名带 `YYYY-MM` 日期 | 混合 |
| `.github/workflows/` | CI：health-check / formal-verification / quarterly-frontier-check / slsa-l4-poc | 直接维护 |
| `struct/HERMES-TASKS.md` | 可执行任务池（本章程配套） | 直接维护 |

## 3. 六大规则

### R1 真源层级（冲突裁决顺序）

| 信息类别 | 真源 | 守护者 |
| --------- | ------ | ------ |
| 知识内容 | `struct/` | `sync-view-from-struct.py`（哈希校验） |
| 统计数据 | `reports/stats.json` | `check-stats-consistency.py` |
| 标准状态/URL | `struct/99-reference/standards-index/authoritative-sources-v2.md` | `authority-source-audit.py` |
| 阈值 | threshold-registry | `threshold-check.py` |
| 术语 | `glossary-master.md` + `terminology-db.yaml` 双库 | `terminology-crosscheck.py` |
| 阶段计划 | `struct/MASTER_PLAN.md` | 人工 |
| 执行任务 | `struct/HERMES-TASKS.md` | 每次会话收口时更新 |

### R2 派生物纪律

禁止手改 `view/` 现役卷册、`dist/` 产物、脚本生成的 `reports/`。发现派生物与 struct/ 不一致时，回 `struct/` 修正后由脚本重新生成。`view/_HISTORICAL_/` 与 `struct/_ARCHIVE/` 正文只读，仅允许在其头部追加"已被现行状态取代"横幅。

### R3 标准工作循环

**场景 A — 修改/新增知识内容**（最常用）：

```bash
# 1. 改 struct/ 下的 Markdown
# 2. 全文质量门（硬门禁，必须全绿）
python scripts/health-check.py
# 3. 重新生成派生物（注意：sync 脚本默认只出报告，必须带 --generate）
python scripts/sync-view-from-struct.py --generate
python scripts/build-deliverables.py
# 4. 产物校验
python scripts/dist-check.py
# 5. 刷新统计真源
python scripts/knowledge-cli.py stats
# 6. 语义化提交
```

**场景 B — 修改标准引用**：先核 `authoritative-sources-v2.md`（严格区分 已发布 / 草案(DIS/CD) / 征求意见稿(IPD/AWI) / 路线图），改全文 → `standard-version-audit.py` + `errata-lint.py` → 接场景 A 第 2 步起。

**场景 C — 新增主题/子目录**：`NN-kebab-case` 连续编号（`08-reserved` 式预留号除外）→ 七要素齐全（见 R4）→ 术语双库登记 → 主题 README → 接场景 A。

**场景 D — 批量修复**：`batch-fix-quality-gate.py` 等批处理脚本**默认只报告**，必须人工复核后才允许 `--apply`；禁止批量注入模板段落（历史"补充说明"污染教训）。

### R4 质量门分级

硬门禁（exit 非零，必须 100%）：`quality-gate-v2.py`（七要素：概念定义 / 正向示例 / 反例反模式 / 权威来源 / 交叉引用 / 思维表征 / 论证分析）、`link-checker.py`、`cross-index-check.py`（公理引用闭合）、`threshold-check.py`、`structure-lint.py`、`figure-check.py`、`kg-shacl-validate.py`、`sync-view-from-struct.py`、`policy-check.py`。

报告型（exit 0，warning 只报告不阻断）：`errata-lint.py`、`terminology-crosscheck.py`、`authority-source-audit.py`、`standard-version-audit.py` 的 warning 级。报告型检查的告警是 backlog 来源，按 `struct/HERMES-TASKS.md` 分优先级消化。

### R5 目录与命名

- `struct/` 子目录：`NN-kebab-case`；`view/` 卷册：`volume-NN-主题名.md`；编号不得重复或跳空（`structure-lint.py` 硬校验）。
- 人工撰写的分析报告：`reports/*-YYYY-MM.md`；脚本报告用脚本默认输出名。
- 新文档正文 ≥ 300 字/词；Markdown 用 ATX 标题、层级 ≤ 4、表格前后空行（详见 `CONTRIBUTING.md`）。

### R6 任务池制度

- `struct/MASTER_PLAN.md` 管阶段与里程碑，低频修改；
- `struct/HERMES-TASKS.md` 管可执行任务：每条任务必须带「动作 / 涉及文件 / 验证命令 / 完成标准」四要素，完成即勾选，新 backlog 从各报告型检查的告警沉淀。

## 4. 每次会话的巡检规程（R 循环）

- **开工**：`git status` 确认基线 → `python scripts/health-check.py`（红则先修复再开工）。
- **收口**：场景 A 的第 3–5 步 → 在 `HERMES-TASKS.md` 勾选已完成任务 → 语义化提交。
- 提交按 struct / view+dist / scripts / reports / 文档分组，禁止一句"update"打天下。

## 5. 已知环境约束（不要反复踩坑）

- SSH push 被阻塞（github.com:443 不通）：CI 仅在本地可跑；本地 `main` 领先 origin，属预期状态。
- Docker daemon 未启动：TLA+/Alloy/Coq/Isabelle 本地不可执行，只维护文档与规约，验证靠 `.github/workflows/formal-verification.yml` best-effort。
- `standard-status-checker.py` 对 ISO 官网 403 会误判"失效"，引用其结论前先人工复核（见 HERMES-TASKS T3.4）。
- MCP 当前稳定版为 **2025-11-25**；历史快照中 "2026-07-28 RC" 类表述禁止再写入新内容。

## 6. 指向

- 人类贡献细节（格式、审查清单、PR 流程）：`CONTRIBUTING.md`
- 阶段与里程碑：`struct/MASTER_PLAN.md`
- 任务执行清单：`struct/HERMES-TASKS.md`
- 写作模板与格式：`struct/99-reference/templates/`、`struct/99-reference/book-format-guide.md`

---

> **核查日期**: 2026-07-12 · 本章程随项目演进更新，版本记录见 git 历史
