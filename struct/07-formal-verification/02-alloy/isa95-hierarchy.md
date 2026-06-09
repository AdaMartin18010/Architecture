# T14: ISA-95 资源层次一致性验证 (Alloy)

> **版本**: 2026-06-06
> **对应规约**: `isa95-hierarchy.als`
> **交叉引用**: `struct/11-industrial-iot-otit/01-isa-95-model/`
> **对齐标准**: ANSI/ISA-95.00.01-2010 (IEC 62264-1); ISA-95.00.02-2018
> **理论来源**: Jackson, D. *Software Abstractions*; ISA-95 Standard; Purdue Enterprise Reference Architecture

---

## 目录

- [T14: ISA-95 资源层次一致性验证 (Alloy)](#t14-isa-95-资源层次一致性验证-alloy)
  - [目录](#目录)
  - [1. 建模背景](#1-建模背景)
  - [2. 签名设计与 ISA-95 映射](#2-签名设计与-isa-95-映射)
    - [2.1 ISA95Layer（五层模型）](#21-isa95layer五层模型)
    - [2.2 Resource（资源层次）](#22-resource资源层次)
    - [2.3 InterfaceDef（接口定义）](#23-interfacedef接口定义)
  - [3. 核心约束解析](#3-核心约束解析)
    - [F2: ParentChildAdjacency（父子相邻层约束）](#f2-parentchildadjacency父子相邻层约束)
    - [F4: CrossLayerInterfaceRequired（跨层接口强制）](#f4-crosslayerinterfacerequired跨层接口强制)
  - [4. 断言与验证](#4-断言与验证)
  - [5. 反例教学：跳层引用的危害](#5-反例教学跳层引用的危害)
  - [6. 与工业 IoT/OT-IT 的交叉引用](#6-与工业-iotot-it-的交叉引用)
  - [7. 权威来源](#7-权威来源)

## 1. 建模背景

ISA-95（IEC 62264）是制造运营管理与企业系统集成的国际标准，定义了从 L0（现场设备层）到 L4（企业管理层）的五层功能层次模型。每一层具有不同的时间尺度、责任域和技术栈。在工业物联网（IIoT）和数字孪生系统中，ISA-95 的资源层次结构是数据流、控制流和安全边界的基础。

然而，在实际工程中，违反 ISA-95 层次约束的情况屡见不鲜：

- **跳层引用**：ERP（L4）直接读取传感器数据（L0），绕过了 L1-L3 的控制逻辑和安全检查。
- **跨层无接口通信**：L3 的 MES 系统直接调用 L1 的 PLC 寄存器，没有通过 OPC UA 等标准接口。
- **层级循环**：某个资源在层次上同时是另一个资源的父节点和子节点（如配置错误导致的逻辑环）。

本 Alloy 规约将 ISA-95 的资源层次模型形式化，验证两项核心约束：父子相邻层关系和跨层接口强制性。

---

## 2. 签名设计与 ISA-95 映射

### 2.1 ISA95Layer（五层模型）

```alloy
abstract sig ISA95Layer {}
one sig L0_Field extends ISA95Layer {}
one sig L1_Control extends ISA95Layer {}
one sig L2_Supervisory extends ISA95Layer {}
one sig L3_MES extends ISA95Layer {}
one sig L4_Enterprise extends ISA95Layer {}
```

使用 `one sig` 表示每层恰好只有一个实例，这是 ISA-95 标准的本体论承诺：无论工厂规模多大，功能层次始终是这五层。`abstract sig` 确保不存在不属于这五层的"游离"层级。

### 2.2 Resource（资源层次）

ISA-95 标准定义了七级设备层次结构（Equipment Hierarchy）：

```
Enterprise -> Site -> Area -> Production Line -> Work Cell -> Equipment Module -> Control Module
```

本规约将其映射为七个子签名，每个子签名严格绑定到对应的 ISA-95 层级：

| Alloy 签名 | ISA-95 概念 | 层级 |
|-----------|------------|------|
| `EnterpriseResource` | Enterprise | L4 |
| `SiteResource` | Site | L4 |
| `AreaResource` | Area | L3 |
| `ProductionLineResource` | Production Line / Work Center | L3 |
| `WorkCellResource` | Work Cell / Process Cell | L2 |
| `EquipmentModuleResource` | Equipment Module | L1 |
| `ControlModuleResource` | Control Module / Sensor / Actuator | L0 |

### 2.3 InterfaceDef（接口定义）

`InterfaceDef` 是 ISA-95 标准第二部分（IEC 62264-2）的核心概念。标准规定了企业层与制造层之间的对象和属性交换格式（如 B2MML）。在 Alloy 中，接口被建模为具有 `definedBy`、`consumedBy`、`protocol` 等属性的独立签名，支持 OPC UA、MQTT、REST API、Modbus TCP 等工业协议。

---

## 3. 核心约束解析

### F2: ParentChildAdjacency（父子相邻层约束）

```alloy
fact ParentChildAdjacency {
    all r: Resource |
        some r.parent implies
            AdjacentLayers[r.level, r.parent.level] and
            HigherLayer[r.parent.level, r.level]
}
```

这是 ISA-95 层次模型的结构核心。`AdjacentLayers` 谓词定义了五层模型中的相邻关系（L0↔L1, L1↔L2, L2↔L3, L3↔L4）。`HigherLayer` 确保父节点始终位于更高的功能层。这一约束排除了如下违规：

- L0 传感器直接作为 L3 MES 的子节点（跳过了 L1 控制器和 L2 SCADA）。
- L4 ERP 直接包含 L2 监控资源（跳过了 L3 MES）。

### F4: CrossLayerInterfaceRequired（跨层接口强制）

```alloy
fact CrossLayerInterfaceRequired {
    all r1, r2: Resource |
        (r1 != r2 and r2 in r1.~children.~parent) implies
            (AdjacentLayers[r1.level, r2.level] or
             some i: InterfaceDef |
                 i.definedBy = r2 and r1 in i.consumedBy)
}
```

这一约束形式化了 ISA-95 标准中的"接口标准化"原则。在现代 IIoT 架构中，跨层数据交换必须通过标准化接口（如 OPC UA、MQTT）进行。若两个资源不在相邻层，且它们之间存在数据流或控制流，则必须存在一个显式定义的 `InterfaceDef` 作为契约。

这与 `struct/11-industrial-iot-otit/01-isa-95-model/isa-95-asset-catalog-deep-dive.md` 中列出的"支持协议"（OPC UA, MQTT, Profinet, EtherCAT）直接对应。

---

## 4. 断言与验证

| 断言 | 验证目标 | 对应 ISA-95 条款 |
|------|---------|-----------------|
| `AllParentsAreAdjacent` | 父子节点必须相邻 | IEC 62264-1 第 5.3 节功能层次 |
| `CrossLayerRequiresInterface` | 非相邻层引用必须有接口 | IEC 62264-2 对象与属性交换 |
| `AcyclicResourceHierarchy` | 资源层次无环 | 层次模型的基本公理 |
| `ProcessCellAtL2OrL3` | ProcessCell 只能在 L2/L3 | IEC 62264-1 过程单元定义 |

所有断言通过 `check` 命令在有限 scope 内验证。ISA-95 模型的好处在于其层次深度固定（5 层），因此小 scope（如每层 3 个资源实例）就能覆盖绝大多数结构性错误。

---

## 5. 反例教学：跳层引用的危害

若要观察跳层引用的反例，可临时注释掉 `F2`，执行：

```alloy
run { some r: Resource | SkipLevelParent[r] } for 3
```

Alloy 可能生成如下反例：

```
Resource: "ERP_SAP" (EnterpriseResource, L4)
  └── parent: "Siemens_S7_1500" (EquipmentModuleResource, L1)
```

在此反例中，L4 的企业资源直接以 L1 的 PLC 为父节点，跳过了 L3（MES）和 L2（SCADA）。在真实工业系统中，这种跳层会导致：

1. **安全风险**：ERP 直接访问 PLC 绕过了 MES 的安全策略和审计日志，违反了 IEC 62443 的 zone/conduit 模型。
2. **语义失配**：ERP 的时间尺度是"天-月"，PLC 的时间尺度是"毫秒-秒"。直接引用会导致数据聚合逻辑缺失。
3. **运维不可追踪**：当 PLC 数据异常时，无法通过 MES 和 SCADA 的上下文追溯问题根因。

这与 `struct/11-industrial-iot-otit/01-isa-95-model/cross-layer-matrix/data-flow-mapping.md` 中强调的"数据流必须沿层次逐层传递"原则一致。

---

## 6. 与工业 IoT/OT-IT 的交叉引用

- `11-industrial-iot-otit/01-isa-95-model/isa-95-asset-catalog-deep-dive.md`：详细列出了 L0-L4 各层的资产类型、关键属性和语义模型。本 Alloy 规约中的七级资源签名直接对应于该目录中的资产分类。
- `11-industrial-iot-otit/01-isa-95-model/l0-field/asset-catalog.md` 至 `l4-enterprise/asset-catalog.md`：各层资产目录提供了本规约中 `Resource` 签名的实例化数据。
- `11-industrial-iot-otit/02-opc-ua-fx/connection-manager/tla-specification.md`：OPC UA FX 连接管理器的 TLA+ 规约与本 Alloy 规约互补——TLA+ 验证时序行为，Alloy 验证静态层次结构。
- `01-meta-model-standards/06-formal-axioms/axiom-system.md` 公理 S.4（Abstraction Layering）：ISA-95 的五层模型是"抽象分层"公理在工业控制领域的最佳实践。

---

## 7. 权威来源

1. Jackson, D. (2012). *Software Abstractions: Logic, Language, and Analysis* (Revised ed.). MIT Press. —— Alloy 建模方法论。
2. ANSI/ISA-95.00.01-2010 / IEC 62264-1. *Enterprise-Control System Integration — Part 1: Models and Terminology*. —— ISA-95 功能层次模型与资源层次结构的权威定义。
3. ANSI/ISA-95.00.02-2018 / IEC 62264-2. *Enterprise-Control System Integration — Part 2: Objects and Attributes*. —— 跨层接口对象与属性的标准规范。
4. ISA. (2010). *ISA-95 Standard on Enterprise-Control System Integration*. —— Purdue 企业参考架构的 ISA-95 实现。

---

> 最后更新: 2026-06-06
