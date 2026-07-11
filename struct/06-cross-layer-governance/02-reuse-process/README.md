# 02 复用过程治理（Reuse Process Governance）

> **版本**: 2026-06-12
> **定位**: 06-cross-layer-governance / 02-reuse-process
> **对齐标准**: ISO/IEC/IEEE 1517:2010-2010, ISO/IEC/IEEE 12207:2026, ISO/IEC 26550:2015

---

## 核心概念

复用过程治理定义组织如何**系统化地生产、管理和消费可复用资产**。它不是单一活动，而是贯穿四层复用架构（业务→应用→组件→功能）的过程体系。

IEEE 1517 将复用过程分为三大过程组：

| 过程组 | 核心活动 | 对应本体系 |
|:---|:---|:---|
| **领域工程（Domain Engineering）** | 识别、构建、维护可复用资产 | `02-business` / `03-application` / `04-component` |
| **应用工程（Application Engineering）** | 消费和适配可复用资产 | `03-application` / `04-component` / `05-functional` |
| **复用管理（Reuse Management）** | 计划、监控、改进复用活动 | `06-cross-layer-governance` / `09-value-quantification` |

---

## 治理框架

```text
复用策略
    │
    ├── 领域工程 ──► 资产生产
    │       ├── 领域分析
    │       ├── 领域设计
    │       ├── 领域实现
    │       └── 资产管理
    │
    ├── 应用工程 ──► 资产消费
    │       ├── 需求分析（含复用机会识别）
    │       ├── 设计（含资产选择）
    │       ├── 实现（含适配）
    │       └── 验证（含集成边界验证）
    │
    └── 复用管理 ──► 资产治理
            ├── 复用计划
            ├── 复用监控
            └── 复用改进
```

---

## 关键治理机制

1. **复用决策门（Reuse Decision Gate）**
   - 在项目立项、设计评审、发布评审中增加复用视角
   - 使用“自制/购买/复用”决策矩阵

2. **资产全生命周期治理**
   - 规划 → 开发 → 发布 → 推广 → 监控 → 退役
   - 每个阶段定义质量门禁和责任人

3. **复用度量体系**
   - 复用率、适配成本、资产质量分、ROI
   - 详见 `06-cross-layer-governance/05-metrics-kpi/`

---

## 检查清单

- [ ] 是否有明确的复用策略和资产路线图？
- [ ] 领域工程和应用工程是否有清晰的职责分离？
- [ ] 复用机会是否在需求分析阶段被系统识别？
- [ ] 资产是否有统一的管理、分类和版本控制？
- [ ] 复用指标是否被跟踪并用于持续改进？

---

## 关联主题

- `01-meta-model-standards/01-iso-420xx-family/ieee-1517-reuse-processes.md` — ISO/IEC/IEEE 1517:2010 与 12207:2026 的对照
- `06-cross-layer-governance/03-maturity-models/` — 复用成熟度评估
- `06-cross-layer-governance/05-metrics-kpi/` — 复用度量指标


---

## 补充说明：02 复用过程治理（Reuse Process Governance）

## 示例

**示例**：产品线工程团队执行 26550 的领域工程过程，建立领域模型、可复用资产与配置机制，应用工程团队基于这些资产定制具体产品。

## 反例

**反例**：只有应用工程没有领域工程，团队不断从头开发相似功能，无法积累可复用资产。

## 权威来源

> **权威来源**:
>
> - [ISO/IEC 26550:2015](https://www.iso.org/standard/69529.html)
> - [IEEE Standards](https://standards.ieee.org)
> - 核查日期：2026-07-07

## 分析

**分析**：复用过程的双轨模型（领域工程 + 应用工程）是系统化复用的核心组织模式。