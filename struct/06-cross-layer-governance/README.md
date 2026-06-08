# 06 跨层复用治理与成熟度模型

## 定位

横跨业务→应用→组件→功能四层的治理体系，确保复用从"自发行为"提升为"组织能力"。

## 核心内容

- 复用治理的国际标准框架（42020/42030/25010/26566）
- 复用成熟度五级模型（整合 ISO/IEC 26566:2026 / RiSE / RCMM / NASA RRL）
  - Level 1: 初始 (Initial) → Level 5: 优化 (Optimizing)
- 跨层复用的升级/降级决策矩阵
- 复用度量指标体系（资产级/项目级/组织级/生态级）
- FinOps 跨层复用成本模型
- 复用成熟度评估问卷（基于 ISO/IEC 26566:2026）

## 权威对齐

- [ISO/IEC 26566:2026](https://www.iso.org) 成熟度框架
- [NASA RRL (Reuse Readiness Levels)](https://www.nasa.gov)
- [FinOps Foundation](https://www.finops.org)
- [Backstage IDP](https://backstage.io) (内部开发者平台)

## 关键公理
>
> **公理 6.1** (Governance Necessity): 无治理的复用退化为克隆；无度量的治理退化为形式。

## 当前状态

- [x] 五级成熟度模型定义
- [x] 度量指标体系框架
- [x] 复用度量指标体系四级框架 (`05-metrics-kpi/metrics-framework.md`)
- [x] FinOps 跨层成本分摊模板 (Markdown + Python/Excel导出) (`04-finops-cost/cost-allocation-template.md` + `04-finops-cost/templates/finops-exporter.py`)
- [x] 复用成熟度可执行评估问卷 (Python CLI) (`03-maturity-models/reuse-maturity-assessment-cli.py`，基于 ISO/IEC 26566:2026 / RCMM / RiSE / NASA RRL)
- [ ] FinOps 成本分摊工具模板 Python/Excel 实现 (P1, 2026-Q4)

## 关联主题

- 所有层次主题（治理贯穿全部）
- `09-value-quantification`（ROI 与成本模型）
