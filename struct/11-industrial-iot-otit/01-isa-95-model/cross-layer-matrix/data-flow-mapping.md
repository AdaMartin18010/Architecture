# ISA-95 五层跨层数据流映射

> **版本**: 2026-06-06
> **范围**: L4 Enterprise ↔ L3 MES ↔ L2 Supervisory ↔ L1 Control ↔ L0 Field
> **对齐来源**: ANSI/ISA-95.00.01-2010 (IEC 62264-1), ISA-95.00.02-2018, ISA-95 Part 5 (B2MML), OPC UA FX, IEC 61131-3

---

## 1. 映射总览

ISA-95 五层模型的核心设计意图之一是**定义清晰的层间接口与数据流**，以避免传统点对点集成导致的"意大利面条式架构"。
本文件系统梳理 ERP↔MES↔SCADA↔PLC↔Field 的数据流映射关系，明确每层的数据对象、传输协议、刷新频率与一致性要求，并给出复用策略建议。

```text
┌─────────────────────────────────────────────────────────────────┐
│  L4 Enterprise (ERP/PLM/CRM/SCM)                                │
│  时间尺度: 天–月  |  数据对象: 工单、BOM、物料主数据、客户订单      │
│  协议: B2MML / REST / OData / EDI                               │
└──────────────────────▼──────────────────────────────────────────┘
                       │ Production Schedule / Work Order / Material Definition
                       │ (下行: 计划→执行)
                       │ Production Performance / Material Actual / Production Response
                       │ (上行: 执行→反馈)
┌──────────────────────▼──────────────────────────────────────────┐
│  L3 MES/MOM (制造运营)                                           │
│  时间尺度: 小时–天  |  数据对象: 配方、SOP、批次记录、OEE、质量报告  │
│  协议: B2MML / OPC UA / MQTT / REST                             │
└──────────────────────▼──────────────────────────────────────────┘
                       │ Control Recipe / Setpoints / SOP Steps
                       │ (下行: 执行指令→监控)
                       │ Process Values / Alarms / Events / Batch Records
                       │ (上行: 过程数据→运营)
┌──────────────────────▼──────────────────────────────────────────┐
│  L2 Supervisory (SCADA/HMI/历史数据库)                            │
│  时间尺度: 分–小时  |  数据对象: 报警、趋势、画面、报表、配方管理    │
│  协议: OPC UA / OPC Classic / MQTT / SQL                        │
└──────────────────────▼──────────────────────────────────────────┘
                       │ Tag Writes / Recipe Parameters / Commands
                       │ (下行: 指令→控制)
                       │ Real-time Data / Alarm Events / Historical Batches
                       │ (上行: 实时数据→监控)
┌──────────────────────▼──────────────────────────────────────────┐
│  L1 Control (PLC/DCS/CNC/运动控制器)                              │
│  时间尺度: 秒–分  |  数据对象: 功能块实例、UDT、I/O 映像、状态机   │
│  协议: Profinet / EtherCAT / EtherNet/IP / Modbus TCP / OPC UA   │
└──────────────────────▼──────────────────────────────────────────┘
                       │ I/O Signals / Device Commands / Setpoints
                       │ (下行: 控制→现场)
                       │ Sensor Values / Actuator Status / Drive Feedback
                       │ (上行: 现场反馈→控制)
┌──────────────────────▼──────────────────────────────────────────┐
│  L0 Field (传感器/执行器/驱动器/智能仪表)                         │
│  时间尺度: 毫秒–秒  |  数据对象: 过程变量、诊断数据、设备描述       │
│  协议: IO-Link / 4-20mA / 0-10V / 24V DC / HART                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 逐层数据流映射

### 2.1 L4 ↔ L3：企业层与制造运营层

| 方向 | 数据对象 | 协议/格式 | 频率 | 一致性要求 | 复用策略 |
|-----|---------|----------|------|-----------|---------|
| L4 → L3 | Production Schedule (生产计划) | B2MML XML / REST JSON / OData | 批次/日/周 | 强一致性（事务型） | 复用 ISA-95 Part 2 对象模型；B2MML Schema 一次定义，多 MES 复用 |
| L4 → L3 | Work Order (工单) | B2MML / REST | 工单级 | 强一致性 | 复用标准工单模板，避免各 MES 自定义字段 |
| L4 → L3 | Material Definition / BOM | B2MML / REST / OData | 主数据变更时 | 最终一致性（分钟级同步） | 主数据模型模板全局复用，见 [L4 企业层](../l4-enterprise/asset-catalog.md) E4/E5 |
| L4 → L3 | Personnel / Equipment Master | B2MML / HR 接口 | 日同步 | 最终一致性 | 人员/设备主数据复用 ISA-95 资源模型 |
| L3 → L4 | Production Performance (生产绩效) | B2MML XML / REST | 工单完工/班报 | 强一致性 | 复用 ISA-95 Part 4 绩效对象；OEE/KPI 模板复用见 [L3 MES 层](../l3-mes/asset-catalog.md) M4 |
| L3 → L4 | Material Actual (物料实绩) | B2MML / REST | 批次完工 | 强一致性 | 复用标准物料消耗/产出报文 |
| L3 → L4 | Production Response (生产响应) | B2MML | 工单事件 | 强一致性 | 复用标准响应消息模板 |

**关键复用决策**: B2MML Schema 是 L4↔L3 跨层复用的核心资产。
建议在集团层面建立统一的 B2MML 扩展规范（基于 ISA-95 Part 5），所有工厂 MES 与 ERP 集成必须遵循，避免各项目重复设计报文结构。

### 2.2 L3 ↔ L2：制造运营层与监控层

| 方向 | 数据对象 | 协议/格式 | 频率 | 一致性要求 | 复用策略 |
|-----|---------|----------|------|-----------|---------|
| L3 → L2 | Control Recipe (控制配方) | OPC UA / MQTT / 专有 API | 批次启动时 | 强一致性 | 复用 ISA-88 配方模板，见 [L3 MES 层](../l3-mes/asset-catalog.md) M1 |
| L3 → L2 | SOP Steps (工作指令步骤) | OPC UA / REST / JSON | 步骤触发 | 强一致性 | 复用 SOP 数字化模板 M2 |
| L3 → L2 | Setpoints / Parameters | OPC UA / MQTT | 秒–分级 | 强一致性 | 复用 UDT 模板，见 [L1 控制层](../l1-control/asset-catalog.md) C3 |
| L2 → L3 | Process Values (过程值聚合) | OPC UA HDA / MQTT / SQL | 秒–分级聚合 | 最终一致性 | 复用 OPC UA DI / PA-DIM 信息模型 |
| L2 → L3 | Alarm Events (报警事件) | OPC UA A&C / MQTT / REST | 事件驱动 | 强一致性（时序） | 复用 ISA-18.2 报警分级模板，见 [L2 监控层](../l2-supervisory/asset-catalog.md) S2 |
| L2 → L3 | Batch Records / EBR | OPC UA / REST / 数据库 | 批次完成 | 强一致性 | 复用电子批记录模板 S6 |

**关键复用决策**: OPC UA Companion Specifications（DI、PA-DIM、ISA-95 CS）是 L3↔L2 语义互操作的关键。
建议将 L3 MES 的数据对象直接映射为 OPC UA 信息模型节点，SCADA 通过订阅复用同一语义层，避免传统"标签映射表"的重复维护。

### 2.3 L2 ↔ L1：监控层与控制层

| 方向 | 数据对象 | 协议/格式 | 频率 | 一致性要求 | 复用策略 |
|-----|---------|----------|------|-----------|---------|
| L2 → L1 | Tag Writes / Commands | OPC UA / Profinet / EtherCAT / Modbus | 毫秒–秒 | 硬实时/确定型 | 复用 UDT 模板与 PLCopen FB 接口 |
| L2 → L1 | Recipe Parameters (配方参数) | OPC UA / 专有 PLC 协议 | 秒级 | 强一致性 | 复用 ISA-88 Control Recipe 绑定规则 |
| L2 → L1 | Mode/State Commands (PackML) | OPC UA / MQTT | 秒级 | 强一致性 | 复用 OMAC PackML 状态机模板 S5 |
| L1 → L2 | Real-time Tags (实时标签) | OPC UA / Profinet / EtherCAT / MQTT | 毫秒–秒 | 硬实时 | 复用 GSDML/EDS/IODD 自动生成的标签结构 |
| L1 → L2 | Alarm Events (报警事件) | OPC UA A&C / 专有报警协议 | 事件驱动 | 强一致性（时序） | 复用 ISA-18.2 报警泛滥管理规则 |
| L1 → L2 | Historical Batches (历史批次) | OPC HDA / SQL / CSV | 批次完成 | 最终一致性 | 复用批次归档模板 |

**关键复用决策**: L2↔L1 的数据流复用重点在于**设备描述→标签→信息模型**的自动化链路。
通过复用 L0 层的 IODD/GSDML/EDS（见 [L0 现场层](../l0-field/asset-catalog.md) E1–E4），工程工具可自动生成 OPC UA 信息模型与 PLC 标签，SCADA 直接订阅复用。

### 2.4 L1 ↔ L0：控制层与现场层

| 方向 | 数据对象 | 协议/格式 | 频率 | 一致性要求 | 复用策略 |
|-----|---------|----------|------|-----------|---------|
| L1 → L0 | Analog Outputs (4-20mA / 0-10V) | 模拟信号 / IO-Link / 总线 | 毫秒级 | 硬实时 | 复用 IODD/GSDML 过程数据映射 |
| L1 → L0 | Digital Outputs (24V DC) | 数字信号 / 总线 | 毫秒级 | 硬实时 | 复用设备描述文件中的通道定义 |
| L1 → L0 | Drive Setpoints (转速/位置/扭矩) | Profinet / EtherCAT / CANopen | 毫秒级 | 硬实时/同步 | 复用 PLCopen AXIS_REF + 驱动器 Profile |
| L1 → L0 | Device Parameters (参数下装) | IO-Link / Profinet / HART | 启动/维护 | 强一致性 | 复用 IODD/EDS 参数集模板 |
| L0 → L1 | Analog Inputs (AI) | 模拟信号 / IO-Link / 总线 | 毫秒级 | 硬实时 | 复用设备描述文件中的量程与单位定义 |
| L0 → L1 | Digital Inputs (DI) | 数字信号 / 总线 | 毫秒级 | 硬实时 | 复用设备描述文件中的通道定义 |
| L0 → L1 | Diagnostic Data (诊断数据) | IO-Link / Profinet / EtherNet/IP | 秒–分级 | 最终一致性 | 复用 IODD/GSDML 诊断事件定义 |
| L0 → L1 | Device Identification (设备标识) | IO-Link / 总线 | 启动时 | 强一致性 | 复用设备描述文件中的 Identification 参数 |

**关键复用决策**: L1↔L0 的复用核心是**设备描述文件的标准化**。
同一型号的传感器/执行器在不同项目中应 100% 复用同一版 IODD/GSDML/EDS，确保 PLC 工程、SCADA 标签、MES 信息模型的自动化生成。

---

## 3. 复用策略矩阵：跨层 vs 层内

### 3.1 跨层复用资产（Multi-Layer Reuse）

以下数据模型与接口契约应在全企业范围内标准化，实现一次定义、多层复用：

| 跨层复用资产 | 贯穿层级 | 复用机制 | 标准化来源 |
|-------------|---------|---------|-----------|
| **物料主数据模型** | L4→L3→L2 | ERP MDM → MES Material Definition → SCADA 配方参数 | ISA-95 Part 2, GS1 GDSN |
| **设备/资产信息模型** | L0→L1→L2→L3 | IODD/GSDML → UDT → OPC UA DI → AAS 子模型 | OPC UA DI, PA-DIM, IEC 63278 (AAS) |
| **OEE/KPI 计算模型** | L1→L2→L3→L4 | PackML 计数器 → SCADA 聚合 → MES 计算 → ERP 成本核算 | OMAC PackML, ISA-95 Part 4, ISO 22400 |
| **配方/产品定义** | L4→L3→L2→L1 | ERP BOM → MES Master Recipe → SCADA Control Recipe → PLC 参数 | ISA-88 / IEC 61512, ISA-95 Part 2 |
| **报警分级与响应规则** | L1→L2→L3 | PLC 报警位 → SCADA 报警管理 → MES 事件记录 | ISA-18.2 / IEC 62682 |
| **人员资质模型** | L4→L3 | HR 系统 → MES 操作员权限与电子签名 | ISA-95 Part 2, FDA 21 CFR Part 11 |

### 3.2 层内复用资产（Intra-Layer Reuse）

以下资产在同一层级内部复用，以降低同层多系统/多项目间的重复开发：

| 层 | 层内复用资产 | 复用范围 | 效果 |
|---|-------------|---------|------|
| L0 | IODD/GSDML/EDS 族系模板 | 同厂商同族设备 | 工程配置时间 ↓ 50% |
| L1 | PLCopen FB 库 / UDT 模板 | 同平台多项目 | 代码复用率 ↑ 60% |
| L1 | 安全关断逻辑 FB | 同 SIL 等级多系统 | 认证成本 ↓ 40% |
| L2 | HMI 画面模板库 | 同行业多产线 | HMI 开发工作量 ↓ 60% |
| L2 | 报警管理规则库 | 全厂/全集团 | 报警合理化一致性 ↑ |
| L3 | 配方模板 / SOP 模板 | 同集团多工厂 | 合规审计准备时间 ↓ 70% |
| L3 | OEE/KPI 模板 | 全集团对标 | 绩效数据可比性 ↑ |
| L4 | 业务流程模板 (P2P/计划到生产) | 集团多法人实体 | ERP 推广成本 ↓ 50% |
| L4 | 主数据编码规则 | 全球组织 | 数据清洗成本 ↓ 80% |

---

## 4. 一致性要求与架构模式

### 4.1 一致性等级定义

| 等级 | 名称 | 说明 | 适用场景 |
|-----|------|------|---------|
| **强一致性 (Strong)** | 事务型一致性 | ACID 保证，实时同步，失败即回滚 | L4→L3 工单下达、L3→L2 配方参数、财务过账 |
| **顺序一致性 (Sequential)** | 时序一致性 | 事件按发生顺序处理，允许短暂延迟 | L1→L2 报警事件、批次状态变更 |
| **最终一致性 (Eventual)** | 最终一致性 | 允许分钟级延迟，最终状态收敛 | L4↔L3 主数据同步、L2→L3 历史数据归档 |
| **软实时 (Soft-RT)** | 确定性延迟 | 毫秒–秒级确定性延迟，允许偶发丢包 | L2→L1 监控命令 |
| **硬实时 (Hard-RT)** | 严格实时 | 微秒–毫秒级严格时限，不允许超时 | L1→L0 运动控制、安全关断 |

### 4.2 推荐架构模式

1. **北向聚合、南向分发**: L3 作为数据汇聚中枢，将 L1/L2 高频数据聚合为 L4 所需的低频业务事件；L4 计划通过 L3 分解为 L2/L1 可执行的指令。
2. **语义层统一**: 在 L2-L3 边界建立 OPC UA 信息模型作为企业级语义层，替代传统的"点表映射"，实现跨层语义复用。
3. **边缘计算卸载**: 对于 L0-L1 的高频数据（振动、视觉），在 L2 边缘节点进行预聚合与特征提取，仅将结果推送至 L3，降低网络负载与存储成本。

---

## 5. 权威来源

1. ANSI/ISA-95.00.01-2010 / IEC 62264-1:2013 — Enterprise-Control System Integration Part 1: Models and Terminology
2. ANSI/ISA-95.00.02-2018 / IEC 62264-2 — Part 2: Object Model Attributes
3. ISA-95 Part 5 / B2MML (Business To Manufacturing Markup Language) — WBF XML Schemas
4. OPC Foundation — OPC Unified Architecture for Devices (DI), OPC 10000-100
5. OPC Foundation / FieldComm Group — PA-DIM Companion Specification
6. ISA-88 / IEC 61512-1,-2,-3 — Batch Control (Models, Data Structures, Recipes)
7. ISA-18.2 / IEC 62682:2022 — Management of Alarm Systems
8. OMAC PackML — State Model and Tag Naming Guideline V4.0
9. IEC 61131-3:2013 — Programmable controllers – Part 3: Programming languages
10. IEC 63278 — Asset Administration Shell for industrial applications (AAS)

---

> 最后更新: 2026-06-06
