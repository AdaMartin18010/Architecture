# 01 业务域复用（Business Domain Reuse）

> **版本**: 2026-06-12
> **定位**: 02-business-architecture-reuse / 01-business-domain-reuse
> **对齐标准**: TOGAF Standard 10 Business Architecture, BMM (Business Motivation Model), FEA BRM

---

## 核心概念

业务域复用关注**最粗粒度**的业务能力组织：如何在企业层面识别、封装和复用业务域（Business Domain）。它与领域驱动设计（DDD）的战略模式相通，但更强调跨项目、跨系统的业务能力资产化。

| 概念 | 定义 | 复用价值 |
|:---|:---|:---|
| **业务域（Business Domain）** | 企业为达成特定业务目标而需要的一组连贯业务能力 | 作为能力投资组合的边界单元 |
| **业务能力（Business Capability）** | 企业为达成特定成果而具备的能力，通常稳定且独立于组织结构 | 跨系统复用的核心抽象 |
| **业务实体（Business Entity）** | 域内关键信息对象，如客户、订单、产品 | 数据模型复用的基础 |
| **价值流（Value Stream）** | 端到端交付价值的活动序列 | 识别复用机会的过程视图 |

---

## 复用模式

1. **域级参考模型复用**
   - 采用行业参考模型（如 FEA BRM、APQC PCF、BIAN 服务域）作为起点
   - 根据组织特点裁剪，形成企业级业务能力地图

2. **业务能力目录复用**
   - 建立分层能力目录（L1 域 → L2 能力 → L3 子能力 → L4 活动）
   - 通过能力热力图识别重复建设和高复用潜力领域

3. **业务实体共享服务**
   - 将跨域共享的实体（如 Party、Product、Location）上升为 enterprise canonical model
   - 通过主数据管理（MDM）或数据网格实现实体复用

---

## 检查清单

- [ ] 是否绘制了企业级业务能力地图？
- [ ] 业务域边界是否基于稳定的能力而非易变的组织/系统？
- [ ] 关键业务实体是否已识别并定义 canonical model？
- [ ] 是否评估了各能力的复用成熟度和投资回报？
- [ ] 域间依赖是否清晰，避免循环依赖？

---

## 关联主题

- `02-business-architecture-reuse/02-business-capability/` — 业务能力建模细化
- `02-business-architecture-reuse/03-value-stream/` — 价值流驱动的复用机会识别
- `02-business-architecture-reuse/04-business-process-reuse/` — 业务流程级复用
- `03-application-architecture-reuse/` — 业务能力到应用架构的映射


---

## 补充说明：01 业务域复用（Business Domain Reuse）

## 示例

**示例**：BIAN 银行业架构参考模型将银行业务划分为 300+ 业务服务组件，为银行数字化转型提供可复用的领域蓝图。

## 反例

**反例**：将其他行业的“库存管理”模型直接套用于航空维修备件管理，忽视行业法规与生命周期差异，导致模型失真。

## 权威来源

> **权威来源**:
>
> - [BIAN](https://www.bian.org)
> - [The Open Group TOGAF](https://www.opengroup.org/togaf)
> - 核查日期：2026-07-07

## 分析

**分析**：业务域复用强调领域知识的沉淀，过早抽象或过晚抽象都会削弱复用价值。