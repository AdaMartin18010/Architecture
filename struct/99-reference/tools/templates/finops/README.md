# FinOps 工具模板聚合入口

> **版本**: 2026-06-12
> **定位**: 汇总并索引 `struct/06-cross-layer-governance/04-finops-cost/templates/` 下的 FinOps 治理落地模板，方便快速查找与复用。
> **关系说明**: 本目录为工具模板聚合入口；各主题模板的权威版本与可执行脚本统一维护在对应主题目录下，本 README 仅提供链接与使用导航。

---

## 目录

- [FinOps 工具模板聚合入口](#finops-工具模板聚合入口)
  - [目录](#目录)
  - [1. 模板清单](#1-模板清单)
  - [2. 快速导航](#2-快速导航)
    - [治理策略类](#治理策略类)
    - [运营与审查类](#运营与审查类)
    - [成本分摊与量化类](#成本分摊与量化类)
    - [自动化工具](#自动化工具)
  - [3. 入口目录与主题目录的关系](#3-入口目录与主题目录的关系)
  - [4. 使用建议](#4-使用建议)
  - [5. 可执行脚本](#5-可执行脚本)
  - [6. 版本与更新](#6-版本与更新)
  - [补充说明：FinOps 工具模板聚合入口](#补充说明finops-工具模板聚合入口)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [权威来源](#权威来源)
  - [分析](#分析)

---

## 1. 模板清单

| 序号 | 模板名称 | 文件名 | 主题目录路径 | 说明 |
|------|---------|--------|-------------|------|
| 1 | 标签治理策略模板 | `tagging-policy.md` | [`struct/06-cross-layer-governance/04-finops-cost/templates/tagging-policy.md`](../../../../06-cross-layer-governance/04-finops-cost/templates/tagging-policy.md) | Mandatory/Recommended/Optional 标签、命名规范、自动 enforcement、缺失处理流程 |
| 2 | FinOps 审查会议模板 | `finops-review.md` | [`struct/06-cross-layer-governance/04-finops-cost/templates/finops-review.md`](../../../../06-cross-layer-governance/04-finops-cost/templates/finops-review.md) | 月度/季度 FinOps Review 议程、检查项、AAI/RCSR 等指标、行动项 |
| 3 | FinOps 仪表盘指标与视图定义模板 | `finops-dashboard.md` | [`struct/06-cross-layer-governance/04-finops-cost/templates/finops-dashboard.md`](../../../../06-cross-layer-governance/04-finops-cost/templates/finops-dashboard.md) | Showback/Chargeback、单位成本、异常检测、数据源与视图定义 |
| 4 | 单位经济学计算模板 | `unit-economics.md` | [`struct/06-cross-layer-governance/04-finops-cost/templates/unit-economics.md`](../../../../06-cross-layer-governance/04-finops-cost/templates/unit-economics.md) | Cloud COGS、每用户/每交易/每 token 成本、分层毛利率计算表 |
| 5 | 承诺折扣策略模板 | `commitment-discount-policy.md` | [`struct/06-cross-layer-governance/04-finops-cost/templates/commitment-discount-policy.md`](../../../../06-cross-layer-governance/04-finops-cost/templates/commitment-discount-policy.md) | RI/Savings Plans/Spot/按需决策流程、风险分析、覆盖率目标、回购策略 |
| 6 | AI 场景成本分摊模板 | `ai-cost-allocation.md` | [`struct/06-cross-layer-governance/04-finops-cost/templates/ai-cost-allocation.md`](../../../../06-cross-layer-governance/04-finops-cost/templates/ai-cost-allocation.md) | LLM token、GPU 共享、RAG 检索、模型微调成本分摊方法与示例 |

---

## 2. 快速导航

### 治理策略类

- 需要规范云资源标签 → [标签治理策略模板](../../../../06-cross-layer-governance/04-finops-cost/templates/tagging-policy.md)
- 需要制定 RI/SP/Spot 购买规则 → [承诺折扣策略模板](../../../../06-cross-layer-governance/04-finops-cost/templates/commitment-discount-policy.md)

### 运营与审查类

- 需要召开 FinOps Review → [FinOps 审查会议模板](../../../../06-cross-layer-governance/04-finops-cost/templates/finops-review.md)
- 需要设计 FinOps 仪表盘 → [FinOps 仪表盘指标与视图定义模板](../../../../06-cross-layer-governance/04-finops-cost/templates/finops-dashboard.md)

### 成本分摊与量化类

- 需要计算 Cloud COGS 与单位成本 → [单位经济学计算模板](../../../../06-cross-layer-governance/04-finops-cost/templates/unit-economics.md)
- 需要分摊 AI/GPU/LLM/RAG/微调成本 → [AI 场景成本分摊模板](../../../../06-cross-layer-governance/04-finops-cost/templates/ai-cost-allocation.md)

### 自动化工具

- 需要导出四级分摊 Excel/CSV 报告 → [`struct/06-cross-layer-governance/04-finops-cost/templates/finops-exporter.py`](../../../../06-cross-layer-governance/04-finops-cost/templates/finops-exporter.py)

---

## 3. 入口目录与主题目录的关系

```text
struct/99-reference/tools/templates/finops/   ← 聚合入口（本目录）
    └── README.md                              ← 索引与导航

struct/06-cross-layer-governance/04-finops-cost/templates/   ← 主题目录（权威源）
    ├── tagging-policy.md
    ├── finops-review.md
    ├── finops-dashboard.md
    ├── unit-economics.md
    ├── commitment-discount-policy.md
    ├── ai-cost-allocation.md
    ├── finops-allocation.md
    ├── finops-exporter.py
    └── example-costs.yaml
```

**设计原则**:

| 原则 | 说明 |
|------|------|
| **单一事实源** | 所有 Markdown 模板与可执行脚本统一维护在 `04-finops-cost/templates/`，避免多版本漂移。 |
| **聚合入口只读** | `99-reference/tools/templates/finops/` 仅存放 `README.md` 索引，不复制模板正文。 |
| **相对链接** | 本 README 使用相对路径 `../../../../06-cross-layer-governance/04-finops-cost/templates/` 指向主题目录，确保在仓库内任意 Markdown 渲染器中可正常跳转。 |
| **按需扩展** | 未来新增 FinOps 模板时，先在主题目录创建文件，再在本 README 中补充一行索引。 |

---

## 4. 使用建议

1. **首次使用**: 从本 README 选择对应模板，复制到项目 Wiki/Confluence/飞书文档后填写 `{{占位符}}`。
2. **保持同步**: 若发现主题目录模板更新，应及时刷新复用副本中的链接与内容。
3. **自定义占位符**: 各模板使用 `{{VARIABLE}}` 标记可填写字段，建议团队统一一套变量命名规范。
4. **与工具结合**: 分摊计算可配合 [`finops-exporter.py`](../../../../06-cross-layer-governance/04-finops-cost/templates/finops-exporter.py) 自动生成 Excel/CSV 报告。

---

## 5. 可执行脚本

| 脚本 | 路径 | 功能 |
|------|------|------|
| `finops-exporter.py` | [`../../../../06-cross-layer-governance/04-finops-cost/templates/finops-exporter.py`](../../../../06-cross-layer-governance/04-finops-cost/templates/finops-exporter.py) | L1–L4 四级成本分摊计算与 Excel/CSV 导出 |
| `finops-allocation.py` | [`../../../../06-cross-layer-governance/04-finops-cost/templates/finops-allocation.py`](../../../../06-cross-layer-governance/04-finops-cost/templates/finops-allocation.py) | 跨层成本分摊计算（按 CSV 输入） |

---

## 6. 版本与更新

| 日期 | 更新内容 | 更新人 |
|------|---------|--------|
| 2026-06-12 | 新建 FinOps 工具模板聚合入口与 6 个 Markdown 模板索引 | {{UPDATER}} |

> **交叉引用**:
>
> - FinOps 主题目录: [`struct/06-cross-layer-governance/04-finops-cost/`](../../../../06-cross-layer-governance/04-finops-cost/)
> - FinOps 四级成本分摊模型: [`struct/06-cross-layer-governance/04-finops-cost/finops-allocation-template.md`](../../../../06-cross-layer-governance/04-finops-cost/finops-allocation-template.md)
> - FinOps 单位经济学: [`struct/06-cross-layer-governance/04-finops-cost/finops-unit-economics-2026.md`](../../../../06-cross-layer-governance/04-finops-cost/finops-unit-economics-2026.md)

> 最后更新: 2026-06-12


---

## 补充说明：FinOps 工具模板聚合入口

## 概念定义

**定义**：参考层是结构化知识体系的“地图”，汇总权威来源、术语表、标准索引、课程对标与审计报告，为各主题提供可追溯的引用与一致性校验。

## 示例

**示例**：维护 authoritative-sources.md 登记所有 ISO/IEC、IEEE、NIST、CNCF 来源 URL 与核查日期，确保全书引用可验证。

## 反例

**反例**：参考层链接长期不更新，术语表与正文定义冲突，读者无法确认内容准确性与时效性。

## 权威来源

> **权威来源**:
>
> - [ISO](https://www.iso.org)
> - [IEEE Standards](https://standards.ieee.org)
> - [NIST](https://www.nist.gov)
> - [CNCF](https://www.cncf.io)
> - 核查日期：2026-07-07

## 分析

**分析**：参考层的价值不在于内容本身，而在于建立知识之间的信任锚点；必须随标准演进定期审计与更新。
