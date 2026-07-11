# ISA-95 / IEC 62264 企业-控制系统集成复用

> **版本**: 2026-07-09
> **定位**: 将 ISA-95 五层模型转化为可复用的 OT-IT 资产目录与接口契约，支撑跨工厂、跨系统的信息模型复用。
> **对齐标准**: ANSI/ISA-95.00.01-2010 (IEC 62264-1:2013)、ISA-95.00.02-2018、ISA-95.00.03-2013、ISA-95 Part 5 (B2MML)、IEC 61512 (ISA-88)

---

## 1. 概念定义

**ISA-95 / IEC 62264** 是制造企业从企业层（L4）到现场层（L0）的垂直集成参考模型，定义了层级边界、资源模型、活动模型与信息交换对象模型。其核心复用价值在于：将企业的物理资产、活动与数据流抽象为跨厂商、跨项目的标准化语义契约。

| 层级 | 名称 | 时间尺度 | 核心复用资产 |
|------|------|---------|-------------|
| **L0** | 现场设备 | 毫秒–秒 | 传感器/执行器模板、IODD/GSDML/EDS |
| **L1** | 基本控制 | 秒–分 | PLCopen FB、IEC 61131-3 功能块、安全联锁模板 |
| **L2** | 监控层 | 分–小时 | SCADA 画面、报警规则、PackML 状态机 |
| **L3** | 制造运营 | 小时–天 | MES 模块、配方模板、OEE/KPI 计算模型 |
| **L4** | 企业层 | 天–月 | 物料主数据、BOM、业务流程模板 |

> **定义 ISA.1** (ISA-95 层级边界): ISA-95 层级边界是物理过程、实时控制、区域监控、工厂运营和企业业务之间的职责分隔。复用资产时，必须确保其在目标层级的实时性、安全性和语义一致性。

---

## 2. ISA-95 与 AAS / OPC UA 的标准条款映射

ISA-95 的抽象模型需要映射到可执行的信息模型。下表给出关键 ISA-95 概念与 IEC 63278 AAS 子模型、OPC UA 信息模型的对应关系。

| ISA-95 概念 | IEC 62264 条款 | AAS 对应（IEC 63278-1） | OPC UA 对应 | 复用说明 |
|------------|---------------|------------------------|------------|---------|
| Equipment（实例） | Part 1, 5.3.3 | Asset (AssetKind = Instance) + Technical Data / Nameplate / Identification 子模型 | OPC UA DI NodeSet / AASAssetAdministrationShellType | 每台物理设备一个 AAS 实例 |
| EquipmentClass（类型） | Part 1, 5.3.2 | Asset (AssetKind = Type) + Technical Data 子模型 | AASSubmodelType / Companion Spec | 设备族系模板 |
| Personnel | Part 1, 5.3.5 | Asset（无形资产）+ Contact Information / Qualifications | — | 人员能力与资质复用 |
| MaterialLot | Part 1, 5.3.4 | Asset (Instance) + Identification / Carbon Footprint | — | 批次追踪与碳足迹 |
| ProcessSegment | Part 1, 5.3.6 | Submodel（能力描述） | Custom ObjectType | 工序能力定义 |
| ProductionSchedule / Work Order | Part 2, 6.2 / 6.3 | Submodel（计划数据）+ Time Series Data | ISA-95 B2MML / OPC 10030 | ERP-MES 接口复用 |
| MaintenanceRecord | Part 1, 5.3.3 | Submodel + Handover Documentation | OPC UA FileType | 维护记录与文档 |
| OEE / KPI | Part 4 | Submodel + Time Series Data | PackML Counter / OPC UA HDA | 跨工厂绩效对标 |

> **定理 ISA.AAS.1** (AAS 复用单调性): 若 ISA-95 资产 A 被复用于系统 S，则 A 的 AAS 子模型必须在 S 的 AAS 中保持语义等价。任何子模型属性的丢失或语义漂移都会导致复用边界破坏。

---

## 3. 正向示例

### 示例 1：汽车总装线 PackML + OEE 模板复用

某汽车 OEM 在新工厂复制总装线时，复用 L2/L3 的 PackML 状态机模板与 OEE 指标库。新产线在 4 周内达到标准化生产模式，而非以往的 12 周。

### 示例 2：制药 ISA-88 / ISA-95 批次管理

制药企业依据 ISA-88（IEC 61512）批处理模型与 ISA-95 L2/L3 边界，建立电子批记录（EBR）模板。批次追溯完整，满足 FDA 21 CFR Part 11 审计要求。

### 示例 3：设备供应商 AAS Digital Nameplate 交付

设备供应商在交付电机与驱动器时附带 IEC 63278 AAS Digital Nameplate 与 OPC UA DI NodeSet。客户 MES/ERP 可自动识别设备参数，工程调试时间缩短约 50%。

---

## 4. 反例 / 失败案例

### 反例 1：ERP 直接写入 PLC 标签

某企业让 ERP 直接写入 PLC 标签，绕过 L2/L3 控制层。破坏了实时控制闭环，导致批次配方被错误覆盖，造成产品污染与停产。

### 反例 2：忽视层级时间尺度复用控制逻辑

将 L2 SCADA 的报警处理逻辑直接下放到 L1 PLC，未考虑毫秒级扫描周期。报警泛滥导致控制回路抖动，产线质量下降。

### 反例 3：跨层级复用 EquipmentClass 忽略工艺差异

将化工反应釜的 EquipmentClass 直接复用到制药生物反应器，未更新安全联锁与洁净度参数，导致认证失败。

---

## 5. 复用策略建议

| 层次 | 复用资产 | 策略 |
|------|---------|------|
| L0 | IODD / GSDML / EDS | 同型号设备 100% 复用同一版设备描述文件 |
| L1 | PLCopen FB / UDT | 建立平台级功能块库，版本化治理 |
| L2 | SCADA 模板 / PackML | 按行业建立画面与状态机模板库 |
| L3 | 配方 / SOP / OEE | 集团级模板，支持多工厂参数化实例化 |
| L4 | 主数据 / BOM / 业务流程 | 企业级 MDM，避免各工厂重复定义 |

---

## 6. 权威来源

> **权威来源**:
>
> - IEC 62264-1:2013 *Enterprise-control system integration — Part 1: Models and terminology*: <https://standards.iteh.ai/catalog/standards/iec/57ebd369-7020-4c85-bb76-5890601d051d/iec-62264-1-2013> （核查日期：2026-07-09）
> - IEC 62264-2:2013 *Object model attributes*: <https://webstore.iec.ch/publication/66912> （核查日期：2026-07-09）
> - IEC 62264-3:2013 *Activity models of manufacturing operations management*: <https://webstore.iec.ch/publication/66912> （核查日期：2026-07-09）
> - IEC 61512-1:1995 *Batch control — Part 1: Models and terminology* (ISA-88): <https://webstore.iec.ch/publication/66912> （核查日期：2026-07-09）
> - ISA-95 / IEC 62264 官方概述： <https://www.isa.org/standards-and-publications/isa-standards/isa-95> （核查日期：2026-07-09）
> - MESA International / B2MML： <https://www.mesa.org/en/B2MML.asp> （核查日期：2026-07-09）
> - IEC 63278-1:2023 *Asset Administration Shell structure*: <https://webstore.iec.ch/publication/65628> （核查日期：2026-07-09）
> - OPC UA for Devices (DI): <https://reference.opcfoundation.org/DI/v105/docs/> （核查日期：2026-07-09）

---

## 7. 交叉引用

- 深度资产清单： [`isa-95-asset-catalog-deep-dive.md`](./isa-95-asset-catalog-deep-dive.md)
- 跨层数据流映射： [`cross-layer-matrix/data-flow-mapping.md`](./cross-layer-matrix/data-flow-mapping.md)
- AAS-OPC UA 映射： [`../05-digital-twin-aas/aas-opcua-mapping.md`](../05-digital-twin-aas/aas-opcua-mapping.md)
- OPC UA FX 复用层次： [`../02-opc-ua-fx/opc-ua-fx-reuse-hierarchy.md`](../02-opc-ua-fx/opc-ua-fx-reuse-hierarchy.md)

---

> 最后更新: 2026-07-09
