# 06 跨层复用治理与成熟度模型

## 定位

横跨业务→应用→组件→功能四层的治理体系，确保复用从“自发行为”提升为“组织能力”。

## 核心内容

- 复用治理与产品线纹理的国际标准框架（ISO/IEC/IEEE 42020 / 42030 / 25010 / 26565 / 26566）
- 复用成熟度五级模型（以 ISO/IEC 26565 产品线成熟度框架为基准，整合 RiSE / RCMM / NASA RRL；26566 提供产品线纹理方法/工具能力支撑）
  - Level 1: 初始 (Initial) → Level 5: 优化 (Optimizing)
- 跨层复用的升级/降级决策矩阵
- 复用度量指标体系（资产级/项目级/组织级/生态级）
- FinOps 跨层复用成本模型
- 复用成熟度评估问卷（基于 ISO/IEC 26565 产品线成熟度框架）

## 概念定义

**定义**：跨层复用治理是将业务层、应用层、组件层与功能层中的可复用资产，在战略、流程、质量、价值与风险维度上进行统一规范、度量与持续改进的组织能力集合。

## 示例：某制造企业跨层复用治理

**背景**：某跨国制造企业在 12 个区域工厂部署了独立的 MES 与质量追溯系统，功能重复率高达 60%。

**治理措施**：

1. 依据 ISO/IEC/IEEE 42020 建立架构治理过程，成立企业架构委员会（EAC）；
2. 以业务能力目录映射到统一的产品线纹理（ISO/IEC 26566），识别 40+ 可复用业务组件；
3. 引入 RCMM/RiSE 成熟度评估，将复用能力从 L2 提升至 L4；
4. 通过 FinOps 四级成本分摊模型，把共享平台成本透明分摊到各工厂。

**效果**：三年内重复功能减少 45%，新工厂系统上线周期缩短 30%，共享组件缺陷率下降 50%。

## 反例：无治理的“复制粘贴”

某互联网公司在早期扩张阶段鼓励各业务线“快速复制”代码库。由于缺乏统一资产目录与质量门禁，同一支付网关逻辑在 6 个团队中出现 9 个版本，API 契约不一致、安全补丁滞后，最终导致一次重大交易故障，直接损失超过 200 万美元。

**根因**：

- 没有资产 Owner 与生命周期管理；
- 没有跨层一致性检查与质量门禁；
- 缺少度量指标，无法量化复用价值与风险。

## 关键公理

> **公理 6.1** (Governance Necessity): 无治理的复用退化为克隆；无度量的治理退化为形式。

## 权威对齐与条款映射

| 权威来源 | URL | 对应条款/能力 | 本主题映射 | 核查日期 |
|:---|:---|:---|:---|:---|
| ISO/IEC/IEEE 42020:2019 Architecture processes | <https://www.iso.org/standard/68982.html> | Clause 6 Architecture Governance process；Clause 7 Architecture Management process | 跨层复用治理组织、决策与生命周期管理 | 2026-07-08 |
| ISO/IEC/IEEE 42030:2019 Architecture evaluation framework | <https://www.iso.org/standard/73436.html> | Clause 5.2 Concerns & stakeholders；Clause 6 Evaluation synthesis & value assessment | 复用资产评估、成熟度评价与价值判定 | 2026-07-08 |
| COBIT 2019 | <https://www.isaca.org/resources/cobit> | EDM01 Ensure governance framework；APO12 Manage risk；MEA01 Monitor, evaluate and assess performance | IT 治理、风险与绩效评估 | 2026-07-08 |
| ITIL 4 | <https://www.axelos.com/certifications/itil-service-management> | Service Value System；Architecture management；Continual improvement；Service level management | 服务化治理、持续改进与 SLA 管理 | 2026-07-08 |
| ISO/IEC 26565 / 26566 | <https://www.iso.org/standard/81436.html>；<https://www.iso.org/standard/81437.html> | 26565 产品线成熟度框架；26566 产品线纹理方法 | 复用成熟度评估与产品线纹理支撑 | 2026-07-08 |

## 子目录导航

| 子目录 | 主题 | 状态 |
|:---|:---|:---:|
| `01-process-governance/` | 复用过程治理 | ✅ |
| `02-reuse-process/` | 复用过程治理（IEEE 1517 / 12207 / 26550 视角） | 🆕 已创建 |
| `03-maturity-models/` | 成熟度模型（RCMM/RiSE/SPICE） | ✅ |
| `04-finops-cost/` | FinOps 成本分摊模板 | ✅ |
| `05-metrics-kpi/` | 四级度量指标体系 | ✅ |
| `06-up-downgrade-matrix/` | 升级/降级决策矩阵 | ✅ |
| `07-policy-automation/` | 策略自动化（OPA/Sentinel/Cedar） | 🆕 已创建 |
| `09-agentic-governance/` | Agentic 治理 | ✅ |

## 当前状态

- [x] 五级成熟度模型定义
- [x] 度量指标体系框架
- [x] 复用度量指标体系四级框架 (`05-metrics-kpi/metrics-framework.md`)
- [x] FinOps 跨层成本分摊模板 (Markdown + Python/Excel导出) (`04-finops-cost/cost-allocation-template.md` + `04-finops-cost/templates/finops-exporter.py`)
- [x] 复用成熟度可执行评估问卷 (Python CLI) (`03-maturity-models/reuse-maturity-assessment-cli.py`，基于 ISO/IEC 26565 / RCMM / RiSE / NASA RRL)
- [ ] FinOps 成本分摊工具模板 Python/Excel 实现 (P1, 2026-Q4)

## 关联主题

- 所有层次主题（治理贯穿全部）
- [`09-value-quantification`](../09-value-quantification/README.md)（ROI 与成本模型）
- [`01-meta-model-standards/01-iso-420xx-family`](../01-meta-model-standards/01-iso-420xx-family/alignment-matrix.md)（ISO 42020/42030 标准族）

> 最后更新：2026-07-08
