# 09 价值量化与 ROI 模型

## 定位

将复用的价值从"定性认同"转化为"定量度量"，支撑管理层的投资决策。

## 核心内容

- **COCOMO II 复用模型深度**: ESLOC、AAF、RUSE 乘数
  - 对齐 USC COCOMO II Model Definition Manual (Boehm et al.)
  - 2026 校准版：适配 AI 辅助开发、Serverless、低代码平台
- **跨层复用的 FinOps 成本分摊模型**
  - 直接成本 / 间接成本 / 风险成本
  - 按使用量/团队/项目/层级分摊
- **复用投资回报率 (ROI) 完整计算模型**
  - 直接收益 + 间接收益 + 战略收益
  - NPV（净现值）计算（考虑时间价值）
- 复用盈亏平衡点分析

## 权威对齐

- [COCOMO II Manual](https://csse.usc.edu/csse/research/COCOMOII) (USC, Barry Boehm)
- [FinOps Foundation Framework](https://www.finops.org/framework/)
- [AWS FinOps Best Practices](https://aws.amazon.com/finops/)

## 关键定理
>
> **定理 V.1** (ROI Threshold): 复用项目的 ROI 为正的必要条件是：复用资产的改编调整因子 AAF < 0.7。若 AAF ≥ 0.7，复用的直接经济价值消失，仅剩战略价值。

## 当前状态

- [x] COCOMO II 公式与计算示例
- [x] ROI/NPV 完整模型
- [x] COCOMO II 2026 校准版 (`01-cocomo-ii-reuse/cocomo-2026-calibration.md`)
- [x] 可执行的 Python 计算模板 (`tools/cocomo-calculator.py`)
  - 支持官方 COCOMO II Reuse 模型（ASLOC/AAM/AAF/AT/DM/CM/IM/SU/UNFM）、5 个规模因子、17 个成本驱动因子综合乘数、工期估算、JSON/CSV/Markdown 导出、敏感性分析及 YAML 批量场景。
  - `struct/99-reference/tools/cocomo-calculator.py` 为早期旧版/简单版原型，功能已合并到上述主工具中。
- [ ] Excel 计算模板 (P1, 2026-Q4)
- [ ] 跨层 FinOps 成本分摊可执行模板 (P1, 2026-Q4)

## 关联主题

- `06-cross-layer-governance`（FinOps 成本治理）
