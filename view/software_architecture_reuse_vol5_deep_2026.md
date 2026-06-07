# 软件工程架构复用视角：卷五深化卷——工业IoT/OT-IT融合技术硬核扩展

> **版本**: 2026-06-05
> **定位**: 对卷五《工业IoT/OT-IT融合扩展卷》中五个核心章节进行源码级/形式化级/协议级的递归深化
> **深化方向**: OPC UA FX协议帧结构、ISA-95对象模型形式化、PLCopen功能块接口定义、AAS数字孪生映射、IEC 61508 Proven-in-Use统计验证
> **对齐标准**: OPC UA FX 1.0 (2026), IEC 62541-100, IEC 62264-1:2013, PLCopen Motion Control V2.0, IEC 63278 (AAS), IEC 61508-3-1:2016
> **思维表征**: 协议帧结构图、UML类图、状态机图、时序图、统计公式、配置模板

---

## 卷五深化目录

- [软件工程架构复用视角：卷五深化卷——工业IoT/OT-IT融合技术硬核扩展](#软件工程架构复用视角卷五深化卷工业iotot-it融合技术硬核扩展)
  - [卷五深化目录](#卷五深化目录)
  - [1. OPC UA FX 协议深度：帧结构、TSN门控与FX Connection Manager](#1-opc-ua-fx-协议深度帧结构tsn门控与fx-connection-manager)
    - [1.1 OPC UA FX 帧结构深度解析](#11-opc-ua-fx-帧结构深度解析)
      - [UADP 帧结构（确定性模式）](#uadp-帧结构确定性模式)
      - [C2C vs C2D vs D2D 的帧差异](#c2c-vs-c2d-vs-d2d-的帧差异)
    - [1.2 TSN 门控表（Gate Control List）配置](#12-tsn-门控表gate-control-list配置)
      - [GCL 配置示例：C2D 通信（控制器→伺服驱动）](#gcl-配置示例c2d-通信控制器伺服驱动)
      - [GCL 配置的数学约束](#gcl-配置的数学约束)
    - [1.3 FX Connection Manager 状态机](#13-fx-connection-manager-状态机)
      - [FX Connection Manager 状态机（形式化定义）](#fx-connection-manager-状态机形式化定义)
      - [FX Connection Manager 配置模板（JSON）](#fx-connection-manager-配置模板json)
  - [2. ISA-95 对象模型形式化：UML类图与属性精确定义](#2-isa-95-对象模型形式化uml类图与属性精确定义)
    - [2.1 ISA-95 Part 1 核心对象模型的 UML 形式化](#21-isa-95-part-1-核心对象模型的-uml-形式化)
      - [核心类图：资源（Resources）](#核心类图资源resources)
      - [核心类图：能力（Capabilities）](#核心类图能力capabilities)
    - [2.2 ISA-95 对象属性的精确定义](#22-isa-95-对象属性的精确定义)
      - [人员（Personnel）属性精确定义](#人员personnel属性精确定义)
      - [设备（Equipment）属性精确定义](#设备equipment属性精确定义)
    - [2.3 ISA-95 对象模型的复用约束](#23-isa-95-对象模型的复用约束)
  - [3. PLCopen 运动控制功能块：接口定义与状态机形式化](#3-plcopen-运动控制功能块接口定义与状态机形式化)
    - [3.1 PLCopen Motion Control V2.0 核心功能块接口](#31-plcopen-motion-control-v20-核心功能块接口)
      - [MC\_Power（轴使能）功能块](#mc_power轴使能功能块)
      - [MC\_MoveAbsolute（绝对定位）功能块](#mc_moveabsolute绝对定位功能块)
    - [3.2 PLCopen 状态机的形式化验证](#32-plcopen-状态机的形式化验证)
  - [4. Asset Administration Shell (AAS) 与数字孪生映射](#4-asset-administration-shell-aas-与数字孪生映射)
    - [4.1 AAS 元模型与 OPC UA 信息模型的映射](#41-aas-元模型与-opc-ua-信息模型的映射)
      - [AAS 子模型模板：技术数据（Technical Data）](#aas-子模型模板技术数据technical-data)
      - [AAS 到 OPC UA 的 NodeSet 映射（XML片段）](#aas-到-opc-ua-的-nodeset-映射xml片段)
    - [4.2 AAS 的复用层次](#42-aas-的复用层次)
  - [5. IEC 61508 Proven-in-Use：统计验证方法深度](#5-iec-61508-proven-in-use统计验证方法深度)
    - [5.1 Proven-in-Use 的统计基础](#51-proven-in-use-的统计基础)
      - [故障率估计的统计方法](#故障率估计的统计方法)
      - [PIU 计算示例](#piu-计算示例)
    - [5.2 PIU 的贝叶斯方法扩展](#52-piu-的贝叶斯方法扩展)
    - [5.3 PIU 复用的约束与风险](#53-piu-复用的约束与风险)
  - [附录 M：卷五深化思维表征](#附录-m卷五深化思维表征)
    - [M.1 OPC UA FX 帧结构对比图](#m1-opc-ua-fx-帧结构对比图)
    - [M.2 ISA-95 对象模型层次图](#m2-isa-95-对象模型层次图)
    - [M.3 PLCopen 状态机对比矩阵](#m3-plcopen-状态机对比矩阵)
    - [M.4 AAS 子模型模板清单](#m4-aas-子模型模板清单)
    - [M.5 PIU 统计方法对比矩阵](#m5-piu-统计方法对比矩阵)

---

## 1. OPC UA FX 协议深度：帧结构、TSN门控与FX Connection Manager

### 1.1 OPC UA FX 帧结构深度解析

OPC UA FX 使用 UADP（UA Datagram Protocol）作为传输层，其帧结构在确定性通信中至关重要。

#### UADP 帧结构（确定性模式）

```text
UADP 帧结构（确定性通信，C2C/C2D/D2D）
┌─────────────────────────────────────────────────────────────┐
│ 字段                          │ 长度    │ 说明              │
├─────────────────────────────────────────────────────────────┤
│ UADP Version                  │ 1 byte  │ 0x01 = 当前版本   │
│ UADP Flags                    │ 1 byte  │ 压缩、加密、签名标志│
│ Extended Flags (optional)     │ 1 byte  │ 扩展标志（大帧等） │
│ Publisher ID                  │ 1-8 byte│ 发布者标识符       │
│ Group Header Enabled?          │ flag    │ 是否包含组头       │
│ Group Version                  │ 4 byte  │ 数据集版本（时序） │
│ Network Message Number          │ 2 byte  │ 网络消息序号       │
│ Sequence Number               │ 2 byte  │ 序列号（用于重排） │
│ Payload Header Enabled?          │ flag    │ 是否包含负载头     │
│ Extended Payload Header?         │ flag    │ 扩展负载头（时间戳）│
│ Timestamp (optional)            │ 8 byte  │ 发布者时间戳（ns） │
│ Picoseconds Offset (optional)   │ 2 byte  │ 皮秒级偏移         │
│ Promoted Fields Enabled?         │ flag    │  promoted fields  │
│ DataSet Payload                 │ variable│ 数据集负载（核心） │
│   ├── DataSet Class ID          │ 16 byte │ 数据集类标识（UUID）│
│   ├── DataSet Message Sequence  │ 2 byte  │ 数据集消息序列号   │
│   ├── DataSet Message Timestamp │ 8 byte  │ 数据集时间戳       │
│   ├── Status Code               │ 2 byte  │ 数据状态码         │
│   └── DataSet Fields            │ variable│ 字段值数组         │
│ Signature (optional)            │ variable│ ECDSA签名（安全模式）│
└─────────────────────────────────────────────────────────────┘

关键字段说明:
├── Publisher ID: 全局唯一标识发布者（控制器/设备），用于路由和过滤
├── Group Version: 数据集配置的版本号，变更时订阅者需重新协商
├── Timestamp + Picoseconds: 纳秒级时间戳 + 皮秒偏移，用于TSN时间同步
├── DataSet Class ID: UUID标识数据类型（如"温度传感器读数"、"电机状态"）
└── Status Code: 数据质量状态（Good/Uncertain/Bad + 子状态码）
```

#### C2C vs C2D vs D2D 的帧差异

| 维度 | C2C (Controller-to-Controller) | C2D (Controller-to-Device) | D2D (Device-to-Device) |
|------|--------------------------------|---------------------------|------------------------|
| **周期** | 10-100 ms | 500 μs - 10 ms | 250 μs - 1 ms |
| **帧大小** | 500-1500 bytes | 100-500 bytes | 50-200 bytes |
| **Publisher ID** | 控制器NodeID | 控制器NodeID | 设备NodeID（直接发布） |
| **Group Version** | 高（配置变更频繁） | 中 | 低（设备配置固定） |
| **Timestamp精度** | 微秒级 | 微秒级 | 纳秒级（运动控制） |
| **Payload** | 复杂数据结构（多个DataSet） | 简单IO数据（单个DataSet） | 极简（原始值+状态） |
| **Security** | 签名+加密 | 签名（可选加密） | 签名（性能优先） |
| **冗余** | 802.1CB帧复制 | 802.1CB帧复制 | 802.1CB帧复制 |

### 1.2 TSN 门控表（Gate Control List）配置

TSN 802.1Qbv 的时间感知整形器（Time-Aware Shaper）通过门控表（GCL）控制每个队列的传输窗口，是 OPC UA FX 确定性的核心机制。

#### GCL 配置示例：C2D 通信（控制器→伺服驱动）

```text
TSN 802.1Qbv Gate Control List 配置示例
├── 网络拓扑: 控制器(端口1) → TSN交换机 → 伺服驱动(端口2)
├── 周期: 1 ms (1000 μs)
├── 门控表周期: 1 ms，分为8个时间槽
│
├── 时间槽 0: 0-100 μs (Control Phase)
│   ├── Queue 0 (Best Effort): CLOSED
│   ├── Queue 1 (Video/Audio): CLOSED
│   ├── Queue 2 (Reserved): CLOSED
│   ├── Queue 3 (Reserved): CLOSED
│   ├── Queue 4 (Reserved): CLOSED
│   ├── Queue 5 (Reserved): CLOSED
│   ├── Queue 6 (Reserved): CLOSED
│   └── Queue 7 (Time-Critical/OPC UA FX): OPEN
│       └── 传输: 控制器→驱动器的控制指令（位置设定值、速度设定值）
│
├── 时间槽 1: 100-200 μs (Feedback Phase)
│   ├── Queue 7: OPEN
│   └── 传输: 驱动器→控制器的反馈数据（实际位置、实际速度、转矩）
│
├── 时间槽 2: 200-300 μs (Safety Phase)
│   ├── Queue 7: OPEN
│   └── 传输: 安全相关数据（STO状态、安全门、急停）
│
├── 时间槽 3-6: 300-800 μs (Background Phase)
│   ├── Queue 0-6: OPEN (Best Effort + Reserved)
│   ├── Queue 7: CLOSED
│   └── 传输: 非实时数据（配置、诊断、日志、HMI）
│
└── 时间槽 7: 800-1000 μs (Guard Band)
    ├── 所有队列: CLOSED
    └── 用途: 保护带，防止帧跨越周期边界（Frame Preemption准备）

GCL 配置参数:
├── Cycle Time: 1000 μs (1 ms)
├── Base Time: 起始时间戳（与gPTP同步）
├── Gate Control List Entries: 8个时间槽
├── Gate Control List Length: 8
├── Gate States per Entry: 8-bit (每个队列的开关状态)
└── 802.1Qbu Frame Preemption: 启用（保护带内可被抢占）
```

#### GCL 配置的数学约束

**定理 TSN.1** (GCL Cycle Consistency): 若网络中有 N 个设备参与时间触发通信，则所有设备的 GCL 周期 T 必须满足：

```text
T = k × T_base, 其中 k ∈ ℕ⁺, T_base 为网络最小公约周期

且对于任意设备 i 和 j:
|BaseTimeᵢ - BaseTimeⱼ| < ε, 其中 ε 为 gPTP 同步精度（通常 < 1 μs）

违反此约束将导致时间槽重叠或空闲，破坏确定性。
```

**定理 TSN.2** (Guard Band Necessity): 保护带（Guard Band）长度 G 必须满足：

```text
G ≥ MTU_max / LineRate + PropagationDelay_max + Jitter_max

其中:
- MTU_max: 最大传输单元（通常为 1500 bytes）
- LineRate: 线路速率（如 1 Gbps = 10⁹ bits/s）
- PropagationDelay_max: 最大传播延迟（电缆长度/光速）
- Jitter_max: 最大抖动（时钟漂移 + 处理延迟）

示例: 1 Gbps, MTU=1500B, 电缆100m, Jitter=100ns
G ≥ (1500×8)/10⁹ + 100/((2/3)×3×10⁸) + 100×10⁻⁹
G ≥ 12 μs + 500 ns + 100 ns ≈ 12.6 μs
```

### 1.3 FX Connection Manager 状态机

FX Connection Manager 是 OPC UA FX 的核心组件，负责管理 C2C/C2D/D2D 连接的建立、配置、监控和拆除。

#### FX Connection Manager 状态机（形式化定义）

```text
FX Connection Manager 状态机
├── 状态集合 S = {Idle, Discovery, Configuration, Ready, Operational, Error, Degraded}
│
├── 初始状态: Idle
├── 终止状态: Operational（正常）或 Error（故障）
│
├── 状态转移函数 δ: S × Event → S × Action
│
├── 转移定义:
│   ├── Idle --(DiscoverRequest)--> Discovery
│   │   ├── 动作: 发送发现请求，扫描网络中的FX Agent
│   │   └── 触发: 上层应用请求建立连接
│   │
│   ├── Discovery --(AgentFound)--> Configuration
│   │   ├── 动作: 读取Agent Card，获取能力清单、端点地址、安全要求
│   │   └── 触发: 收到Agent Card响应
│   │
│   ├── Discovery --(Timeout)--> Error
│   │   ├── 动作: 记录错误日志，通知上层应用
│   │   └── 触发: 发现超时（默认5秒）
│   │
│   ├── Configuration --(ConfigureSuccess)--> Ready
│   │   ├── 动作: 配置DataSet、采样率、安全模式、TSN流预留
│   │   └── 触发: 配置协商成功（双方参数兼容）
│   │
│   ├── Configuration --(ConfigureFail)--> Error
│   │   ├── 动作: 记录配置失败原因（参数不匹配、资源不足、安全冲突）
│   │   └── 触发: 配置协商失败
│   │
│   ├── Ready --(Activate)--> Operational
│   │   ├── 动作: 启动数据发布/订阅，激活TSN门控，开始周期性传输
│   │   └── 触发: 上层应用激活连接
│   │
│   ├── Operational --(DataQualityDegraded)--> Degraded
│   │   ├── 动作: 降低采样率、切换到冗余路径、通知上层应用
│   │   └── 触发: 数据质量降级（丢包率>阈值、延迟>阈值）
│   │
│   ├── Degraded --(Recovery)--> Operational
│   │   ├── 动作: 恢复全功能传输，通知上层应用
│   │   └── 触发: 数据质量恢复
│   │
│   ├── Operational --(Deactivate)--> Ready
│   │   ├── 动作: 停止数据发布/订阅，释放TSN资源
│   │   └── 触发: 上层应用停用连接
│   │
│   ├── Operational/Degraded/Ready --(ConnectionLost)--> Error
│   │   ├── 动作: 记录故障、尝试重连、通知上层应用
│   │   └── 触发: 连接丢失（心跳超时、物理断开）
│   │
│   └── Error --(Reset)--> Idle
│       ├── 动作: 清理资源、重置状态、准备重新发现
│       └── 触发: 上层应用重置请求
│
├── 状态不变量（Invariants）:
│   ├── Invariant 1: Operational状态下，PublisherID必须非空且唯一
│   ├── Invariant 2: Operational状态下，GroupVersion必须与对端一致
│   ├── Invariant 3: Operational状态下，TSN流预留必须成功（BandwidthReserved ≥ BandwidthRequired）
│   └── Invariant 4: Degraded状态下，至少一条冗余路径可用（Redundancy ≥ 1）
│
└── 活性性质（Liveness）:
    ├── Liveness 1: 若配置成功，则最终进入Operational状态
    ├── Liveness 2: 若连接丢失，则最终进入Error状态（非无限挂起）
    └── Liveness 3: 若数据质量降级，则最终进入Degraded或Operational状态（非无限降级）
```

#### FX Connection Manager 配置模板（JSON）

```json
{
  "connectionId": "C2D_Servo_Axis1",
  "connectionType": "C2D",
  "publisher": {
    "nodeId": "ns=2;i=1001",
    "endpointUrl": "opc.tcp://controller:4840",
    "securityMode": "SignAndEncrypt",
    "securityPolicy": "http://opcfoundation.org/UA/SecurityPolicy#Basic256Sha256"
  },
  "subscriber": {
    "nodeId": "ns=2;i=2001",
    "endpointUrl": "opc.tcp://servo-drive:4840",
    "agentCardUrl": "http://servo-drive/.well-known/fx-agent.json"
  },
  "dataSet": {
    "dataSetClassId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "samplingRate": 1000,
    "samplingUnit": "microsecond",
    "fields": [
      {"name": "SetPosition", "dataType": "Double", "valueRank": -1},
      {"name": "SetVelocity", "dataType": "Double", "valueRank": -1},
      {"name": "SetTorque", "dataType": "Double", "valueRank": -1}
    ]
  },
  "tsn": {
    "streamId": "FX_C2D_Axis1_Control",
    "cycleTime": 1000,
    "cycleTimeUnit": "microsecond",
    "priority": 7,
    "bandwidth": 100000,
    "bandwidthUnit": "bps",
    "redundancy": {
      "enabled": true,
      "mode": "802.1CB",
      "seqNumLength": 16
    }
  },
  "redundancy": {
    "mode": "RedundantPublisher",
    "redundantPaths": [
      {"pathId": "Path_A", "priority": 1},
      {"pathId": "Path_B", "priority": 2}
    ]
  }
}
```

---

## 2. ISA-95 对象模型形式化：UML类图与属性精确定义

### 2.1 ISA-95 Part 1 核心对象模型的 UML 形式化

ISA-95 Part 1 (IEC 62264-1:2013) 定义了企业-控制系统集成的核心对象模型。以下将其形式化为 UML 类图。

#### 核心类图：资源（Resources）

```text
ISA-95 资源对象模型（UML类图）

┌─────────────────────────────────────────────────────────────┐
│ <<abstract>> Resource                                       │
├─────────────────────────────────────────────────────────────┤
│ + ID: String {id}                                           │
│ + Description: String [0..1]                                │
│ + HierarchyScope: HierarchyScopeEnum [0..1]                 │
│ (Enterprise/Site/Area/ProductionUnit/WorkCell/StorageZone)  │
│ + Status: ResourceStatusEnum [0..1]                         │
│   (Available/Unavailable/Offline/Maintenance)               │
└─────────────────────────────────────────────────────────────┘
                              △
             ┌────────────────┼────────────────────────┐
             │                │                        │
    ┌────────┴────────┐ ┌─────┴─────┐         ┌────────┴──────────┐
    │ Personnel       │ │ Equipment │         │ Material          │
    ├─────────────────┤ ├───────────┤         ├───────────────────┤
    │ + PersonID      │ │ + EquipmentID       │ + MaterialID      │
    │ + Name          │ │ + EquipmentClassID  │ + MaterialClassID │
    │ + Role: RoleEnum│ │ + EquipmentLevel    │ + MaterialLevel   │
    │ + Skill: Skill[]│ │ + Vendor            │ + LotID           │
    │ + Certification │ | + Model             │ + Quantity        │
    │   : Cert[]      │ │ + SerialNumber      │ + UnitOfMeasure   │
    │ + Availability  │ │ + Location          │ + QualityStatus   │
    │   : Schedule[]  │ │ + Capability        │ + StorageLocation │
    └─────────────────┘ │   : Capability[]    │ + ExpirationDate  │
                        │ + MaintenanceStatus│└───────────────────┘
                        │ + OperationalStatus│
                        └───────────────────┘

关系约束:
├── Resource 是抽象类，不可直接实例化
├── Personnel、Equipment、Material 继承 Resource
├── 一个 Resource 可以关联多个 Capability（能力）
├── 一个 Resource 可以关联多个 Schedule（可用性计划）
└── HierarchyScope 决定资源在 ISA-95 层次模型中的位置
```

#### 核心类图：能力（Capabilities）

```text
ISA-95 能力对象模型（UML类图）

┌─────────────────────────────────────────────────────────────┐
│ <<abstract>> Capability                                     │
├─────────────────────────────────────────────────────────────┤
│ + ID: String {id}                                           │
│ + Description: String [0..1]                                │
│ + CapabilityType: CapabilityTypeEnum                        │
│   (Production/Material/Personnel/Equipment)                 │
│ + Reason: String [0..1]                                     │
│ + StartTime: DateTime [0..1]                                │
│ + EndTime: DateTime [0..1]                                  │
│ + HierarchyScope: HierarchyScopeEnum [0..1]                 │
└─────────────────────────────────────────────────────────────┘
                              △
         ┌────────────────────┼────────────────────────┐
         │                    │                        │
┌────────┴────────┐     ┌─────┴─────┐         ┌────────┴────────┐
│ ProductionCapability│ │ MaterialCapability│ │ PersonnelCapability│
├─────────────────────┤ ├───────────────────┤ ├────────────────────┤
│ + ProductionRate    │ │ + MaterialQuantity│ │ + PersonnelCount     │
│ + UnitOfMeasure     │ │ + UnitOfMeasure   │ │ + PersonQualification│
│ + ProductSegmentID  │ │ + MaterialDefinitionID│ + SkillRequirement   │
│ + ProcessSegmentID  │ │ + MaterialLotID   │ + ShiftPattern       │
│ + EquipmentCapability │ │ + QualityStatus   │ + AvailabilitySchedule│
│   : EquipmentCap[]    │ │ + StorageLocation │ └────────────────────┘
│ + PersonnelCapability │ │ + DeliverySchedule│
│   : PersonnelCap[]  │ └───────────────────┘
│ + MaterialCapability│
│   : MaterialCap[]   │
└─────────────────────┘

关系约束:
├── Capability 与 Resource 是多对多关系（一个资源有多个能力，一个能力可被多个资源满足）
├── Capability 与 Segment（过程段）是多对多关系
├── ProductionCapability 包含嵌套的 EquipmentCapability、PersonnelCapability、MaterialCapability
└── 能力的有效时间区间 [StartTime, EndTime] 必须非空（StartTime < EndTime）
```

### 2.2 ISA-95 对象属性的精确定义

#### 人员（Personnel）属性精确定义

| 属性名 | 数据类型 | 基数 | 约束 | 示例 | 复用语义 |
|--------|----------|------|------|------|----------|
| **PersonID** | String | 1 | 全局唯一，格式：组织ID+部门ID+序号 | "ACME-ENG-00123" | 人员标识的复用模板 |
| **Name** | String | 1 | 非空，长度≤100字符 | "张三" | 人员目录的复用单元 |
| **Role** | RoleEnum | 1..* | 枚举值：Operator/Engineer/Supervisor/Maintenance/Manager | ["Operator", "Supervisor"] | 角色定义的复用 |
| **Skill** | Skill[] | 0..* | 每个Skill包含：SkillID、SkillLevel(1-5)、CertificationDate、ExpirationDate | [{"SkillID":"PLC-Prog","Level":4}] | 技能矩阵的复用 |
| **Certification** | Cert[] | 0..* | 每个Cert包含：CertID、IssuingBody、IssueDate、ExpiryDate、Status | [{"CertID":"ISO-9001-IA","Status":"Active"}] | 认证模板的复用 |
| **Availability** | Schedule[] | 0..* | 每个Schedule包含：StartTime、EndTime、ShiftType、Location | [{"ShiftType":"Night","Location":"Line-A"}] | 排班模板的复用 |
| **HierarchyScope** | HierarchyScopeEnum | 0..1 | 枚举：Enterprise/Site/Area/ProductionUnit/WorkCell | "WorkCell" | 层次范围的复用 |
| **Status** | ResourceStatusEnum | 0..1 | 枚举：Available/Unavailable/Offline/Maintenance/Retired | "Available" | 状态机的复用 |

#### 设备（Equipment）属性精确定义

| 属性名 | 数据类型 | 基数 | 约束 | 示例 | 复用语义 |
|--------|----------|------|------|------|----------|
| **EquipmentID** | String | 1 | 全局唯一，符合组织命名规范 | "ACME-PLANT01-LINEA-ROBOT01" | 设备编码的复用模板 |
| **EquipmentClassID** | String | 0..1 | 引用EquipmentClass定义 | "6-Axis-Industrial-Robot" | 设备类别的复用 |
| **EquipmentLevel** | EquipmentLevelEnum | 0..1 | 枚举：Enterprise/Site/Area/ProcessCell/Unit/WorkCenter/WorkUnit | "WorkCenter" | 设备层次的复用 |
| **Vendor** | String | 0..1 | 供应商名称 | "KUKA Robotics" | 供应商目录的复用 |
| **Model** | String | 0..1 | 设备型号 | "KR QUANTEC nano" | 型号目录的复用 |
| **SerialNumber** | String | 0..1 | 制造商序列号 | "1234567890" | 资产追踪的复用 |
| **Location** | Location | 0..1 | 包含：SiteID、AreaID、Coordinates | {"Site":"Plant01","Area":"LineA"} | 位置模型的复用 |
| **Capability** | EquipmentCapability[] | 0..* | 每个Capability包含：CapabilityID、Value、Unit、ValidPeriod | [{"CapabilityID":"MaxPayload","Value":"120","Unit":"kg"}] | 能力模板的复用 |
| **MaintenanceStatus** | MaintenanceStatusEnum | 0..1 | 枚举：Scheduled/InProgress/Completed/Overdue/Deferred | "Scheduled" | 维护状态机的复用 |
| **OperationalStatus** | OperationalStatusEnum | 0..1 | 枚举：Running/Idle/Setup/Changeover/Down/Offline | "Running" | 运营状态机的复用 |

### 2.3 ISA-95 对象模型的复用约束

> **公理 ISA.1** (HierarchyScope Consistency): 若对象 A 的 HierarchyScope = "WorkCell"，则 A 的所有父对象（Site、Area、ProductionUnit）必须存在且已定义。形式化：∃Site, Area, ProductionUnit: Parent(WorkCell) = ProductionUnit ∧ Parent(ProductionUnit) = Area ∧ Parent(Area) = Site。
> **公理 ISA.2** (Capability-Resource Binding): 能力声明（Capability）必须与资源实例（Resource）绑定才具有语义意义。未绑定资源的能力是抽象定义，不可用于调度或执行。形式化：Capability.valid ↔ ∃Resource: Resource.Capability ⊇ Capability。
> **定理 ISA.1** (Object Model Composition): 若企业 E 的 ISA-95 对象模型包含 {Personnelᵢ, Equipmentⱼ, Materialₖ, ProcessSegmentₗ}，则 E 的生产调度问题可分解为：Schedule = argmax f(Personnelᵢ, Equipmentⱼ, Materialₖ, ProcessSegmentₗ)，其中 f 为生产目标函数（产量、成本、时间）。不同企业可复用相同的对象模型结构，但 f 的权重和约束因企业而异。

---

## 3. PLCopen 运动控制功能块：接口定义与状态机形式化

### 3.1 PLCopen Motion Control V2.0 核心功能块接口

PLCopen Motion Control 规范定义了跨厂商可复用的运动控制功能块接口。以下是其核心功能块的形式化定义。

#### MC_Power（轴使能）功能块

```text
MC_Power 功能块接口定义（PLCopen Motion Control V2.0）

┌─────────────────────────────────────────────────────────────┐
│ FUNCTION_BLOCK MC_Power                                     │
├─────────────────────────────────────────────────────────────┤
│ 输入 (Inputs):                                              │
│   Axis        : AXIS_REF    // 轴引用（硬件抽象）            │
│   Enable      : BOOL        // 使能请求（上升沿触发）        │
│   EnablePositive : BOOL   // 正向使能（硬件限位旁路）         │
│   EnableNegative : BOOL   // 负向使能（硬件限位旁路）         │
├─────────────────────────────────────────────────────────────┤
│ 输出 (Outputs):                                              │
│   Status      : BOOL        // 轴已使能且就绪                 │
│   Valid       : BOOL        // 输出数据有效                  │
│   Error       : BOOL        // 错误发生                      │
│   ErrorID     : MC_ERROR    // 错误代码枚举                  │
└─────────────────────────────────────────────────────────────┘

状态机:
├── Idle（初始状态）
│   ├── Enable = FALSE → 保持 Idle
│   └── Enable = TRUE → 转换到 PowerOn
│
├── PowerOn（使能中）
│   ├── 硬件使能成功 → 转换到 PowerOnDone
│   └── 硬件使能失败 → 转换到 Error
│
├── PowerOnDone（使能完成）
│   ├── Status = TRUE, Valid = TRUE
│   ├── Enable = TRUE → 保持 PowerOnDone
│   └── Enable = FALSE → 转换到 PowerOff
│
├── PowerOff（禁用中）
│   ├── 硬件禁用完成 → 转换到 Idle
│   └── 硬件禁用失败 → 转换到 Error
│
└── Error（错误状态）
    ├── Error = TRUE, ErrorID = 具体错误码
    └── Enable = FALSE → 转换到 Idle（错误清除）

时序约束:
├── PowerOn 转换时间 ≤ 500 ms（典型值，厂商可配置）
├── PowerOff 转换时间 ≤ 200 ms（典型值）
├── Error 响应时间 ≤ 50 ms（安全相关）
└── 所有输出在 Enable 变化后 ≤ 1 个 PLC 周期内更新
```

#### MC_MoveAbsolute（绝对定位）功能块

```text
MC_MoveAbsolute 功能块接口定义

┌─────────────────────────────────────────────────────────────┐
│ FUNCTION_BLOCK MC_MoveAbsolute                              │
├─────────────────────────────────────────────────────────────┤
│ 输入 (Inputs):                                              │
│   Axis        : AXIS_REF      // 轴引用                     │
│   Execute     : BOOL          // 执行请求（上升沿触发）       │
│   Position    : REAL          // 目标位置 [单位：轴定义单位]  │
│   Velocity    : REAL          // 目标速度 [单位/秒]          │
│   Acceleration: REAL          // 加速度 [单位/秒²]           │
│   Deceleration: REAL          // 减速度 [单位/秒²]           │
│   Jerk        : REAL          // 加加速度 [单位/秒³]         │
│   Direction   : MC_DIRECTION // 方向：Positive/Negative/Shortest│
│   BufferMode  : MC_BUFFER_MODE // 缓冲模式：Aborting/Buffered/Blending│
└─────────────────────────────────────────────────────────────┘
│ 输出 (Outputs):                                              │
│   Done        : BOOL          // 运动完成                    │
│   Busy        : BOOL          // 运动进行中                  │
│   Active      : BOOL          // 轴被此FB控制                │
│   CommandAborted: BOOL        // 命令被中止                  │
│   Error       : BOOL          // 错误发生                    │
│   ErrorID     : MC_ERROR      // 错误代码                    │
└─────────────────────────────────────────────────────────────┘

状态机:
├── Idle（初始状态）
│   └── Execute = FALSE → 保持 Idle
│
├── Busy（执行中）
│   ├── Execute 上升沿 → 转换到 Busy
│   ├── Busy = TRUE, Active = TRUE
│   ├── 运动完成 → 转换到 Done
│   ├── 命令中止 → 转换到 CommandAborted
│   └── 错误发生 → 转换到 Error
│
├── Done（完成）
│   ├── Done = TRUE, Busy = FALSE, Active = FALSE
│   └── Execute = FALSE → 转换到 Idle
│
├── CommandAborted（中止）
│   ├── CommandAborted = TRUE
│   └── Execute = FALSE → 转换到 Idle
│
└── Error（错误）
    ├── Error = TRUE, ErrorID = 具体错误码
    └── Execute = FALSE → 转换到 Idle

时序约束:
├── Execute 上升沿到 Active = TRUE: ≤ 2 个 PLC 周期
├── 运动完成到 Done = TRUE: ≤ 1 个 PLC 周期
├── 命令中止到 CommandAborted = TRUE: ≤ 1 个 PLC 周期
└── 错误发生到 Error = TRUE: ≤ 1 个 PLC 周期

复用约束:
├── Position 单位必须与 Axis 的单位定义一致（如 mm、deg、inch）
├── Velocity 必须 ≤ Axis.MaxVelocity（轴最大速度限制）
├── Acceleration 必须 ≤ Axis.MaxAcceleration（轴最大加速度限制）
├── Jerk 必须 ≤ Axis.MaxJerk（轴最大加加速度限制）
└── BufferMode = Blending 时，必须与下一个运动命令的速度/加速度兼容
```

### 3.2 PLCopen 状态机的形式化验证

PLCopen 功能块的状态机可以通过形式化方法验证其正确性。以下使用 TLA+ 规约 MC_Power 的核心安全性质。

```tla
(* TLA+ 规约: MC_Power 功能块的安全性质 *)
------------------------------ MODULE MC_Power_Safety ------------------------------
EXTENDS Naturals, Sequences

CONSTANTS AXIS_REF, MC_ERROR
VARIABLES state, enable, status, valid, error, errorId

(* 状态定义 *)
States == {"Idle", "PowerOn", "PowerOnDone", "PowerOff", "Error"}

(* 初始状态 *)
Init ==
    /\ state = "Idle"
    /\ enable = FALSE
    /\ status = FALSE
    /\ valid = FALSE
    /\ error = FALSE
    /\ errorId = "NoError"

(* 状态转移 *)
PowerOnRequest ==
    /\ state = "Idle"
    /\ enable = TRUE
    /\ state' = "PowerOn"
    /\ UNCHANGED <<enable, status, valid, error, errorId>>

PowerOnSuccess ==
    /\ state = "PowerOn"
    /\ state' = "PowerOnDone"
    /\ status' = TRUE
    /\ valid' = TRUE
    /\ error' = FALSE
    /\ UNCHANGED <<enable, errorId>>

PowerOnFailure ==
    /\ state = "PowerOn"
    /\ state' = "Error"
    /\ error' = TRUE
    /\ errorId' = "PowerOnFailed"
    /\ UNCHANGED <<enable, status, valid>>

PowerOffRequest ==
    /\ state = "PowerOnDone"
    /\ enable = FALSE
    /\ state' = "PowerOff"
    /\ status' = FALSE
    /\ valid' = FALSE
    /\ UNCHANGED <<enable, error, errorId>>

PowerOffComplete ==
    /\ state = "PowerOff"
    /\ state' = "Idle"
    /\ UNCHANGED <<enable, status, valid, error, errorId>>

ErrorReset ==
    /\ state = "Error"
    /\ enable = FALSE
    /\ state' = "Idle"
    /\ error' = FALSE
    /\ errorId' = "NoError"
    /\ UNCHANGED <<enable, status, valid>>

(* 下一步关系 *)
Next ==
    /\ PowerOnRequest
    \/ PowerOnSuccess
    \/ PowerOnFailure
    \/ PowerOffRequest
    \/ PowerOffComplete
    \/ ErrorReset

(* 安全性质 *)
SafetyInvariant ==
    (* 性质 1: 若 error = TRUE，则 status 必须为 FALSE *)
    /\ error = TRUE => status = FALSE
    (* 性质 2: 若 state = "Idle"，则 status = FALSE 且 error = FALSE *)
    /\ state = "Idle" => (status = FALSE /\ error = FALSE)
    (* 性质 3: 若 state = "PowerOnDone"，则 status = TRUE 且 valid = TRUE *)
    /\ state = "PowerOnDone" => (status = TRUE /\ valid = TRUE)

(* 活性性质 *)
Liveness ==
    (* 若 enable = TRUE 且无错误，则最终 status = TRUE *)
    /\ (enable = TRUE /\ error = FALSE) ~> status = TRUE

================================================================================
```

---

## 4. Asset Administration Shell (AAS) 与数字孪生映射

### 4.1 AAS 元模型与 OPC UA 信息模型的映射

IEC 63278（Asset Administration Shell）定义了工业数字孪生的标准化元模型。AAS 与 OPC UA 信息模型之间存在标准化的映射关系。

```text
AAS 元模型与 OPC UA 信息模型映射
├── AAS 核心概念
│   ├── AssetAdministrationShell: 数字孪生的顶层容器
│   ├── Asset: 物理资产（设备、系统、产品）
│   ├── Submodel: 资产的某个方面（如"技术数据"、"文档"、"运行数据"）
│   ├── SubmodelElement: 子模型的元素（属性、操作、事件、关系）
│   └── ConceptDescription: 语义定义（引用 IEC CDD、ECLASS、ETIM）
│
├── OPC UA 映射
│   ├── AAS → OPC UA ObjectType: AASType
│   ├── Asset → OPC UA Object: AssetInstance
│   ├── Submodel → OPC UA Object: SubmodelInstance
│   ├── SubmodelElement → OPC UA Variable/Method/Object
│   │   ├── Property → OPC UA Variable
│   │   ├── Operation → OPC UA Method
│   │   ├── Event → OPC UA EventType
│   │   └── Relationship → OPC UA Reference
│   └── ConceptDescription → OPC UA DataType/VariableType
│
└── 映射规则
    ├── 规则 1: AAS 的 idShort 映射到 OPC UA 的 BrowseName
    ├── 规则 2: AAS 的 identification (IRDI/URI) 映射到 OPC UA 的 NodeId
    ├── 规则 3: AAS 的 semanticId 映射到 OPC UA 的 HasTypeDefinition 或 HasProperty
    ├── 规则 4: AAS 的 Submodel 映射到 OPC UA 的 FolderType 或自定义 ObjectType
    └── 规则 5: AAS 的 Qualifier 映射到 OPC UA 的 EUInformation 或 Range
```

#### AAS 子模型模板：技术数据（Technical Data）

```json
{
  "idShort": "TechnicalData",
  "id": "https://example.com/aas/TechnicalData/1/0",
  "semanticId": {
    "type": "ExternalReference",
    "keys": [{
      "type": "GlobalReference",
      "value": "0173-1#01-ADS753#016"
    }]
  },
  "submodelElements": [
    {
      "idShort": "ManufacturerName",
      "modelType": "Property",
      "valueType": "xs:string",
      "value": "Siemens AG",
      "semanticId": {
        "keys": [{"type": "GlobalReference", "value": "0173-1#02-AAO677#002"}]
      }
    },
    {
      "idShort": "SerialNumber",
      "modelType": "Property",
      "valueType": "xs:string",
      "value": "SN123456789",
      "semanticId": {
        "keys": [{"type": "GlobalReference", "value": "0173-1#02-AAW338#001"}]
      }
    },
    {
      "idShort": "MaxOperatingTemperature",
      "modelType": "Property",
      "valueType": "xs:double",
      "value": "85.0",
      "semanticId": {
        "keys": [{"type": "GlobalReference", "value": "0173-1#02-BAA039#008"}]
      }
    },
    {
      "idShort": "TechnicalSpecification",
      "modelType": "File",
      "mimeType": "application/pdf",
      "value": "/aas/files/specification.pdf",
      "semanticId": {
        "keys": [{"type": "GlobalReference", "value": "0173-1#02-AAO738#001"}]
      }
    }
  ]
}
```

#### AAS 到 OPC UA 的 NodeSet 映射（XML片段）

```xml
<!-- AAS TechnicalData Submodel 映射到 OPC UA NodeSet -->
<UAObjectType NodeId="ns=2;i=1001" BrowseName="2:TechnicalDataSubmodelType">
  <DisplayName>TechnicalData Submodel Type</DisplayName>
  <Description>Technical data submodel based on IEC 63278</Description>
  <References>
    <Reference ReferenceType="HasSubtype">i=58</Reference> <!-- BaseObjectType -->
  </References>
</UAObjectType>

<UAVariable NodeId="ns=2;i=1002" BrowseName="2:ManufacturerName"
            ParentNodeId="ns=2;i=1001" DataType="String">
  <DisplayName>Manufacturer Name</DisplayName>
  <Description>Manufacturer name based on ECLASS 0173-1#02-AAO677#002</Description>
  <References>
    <Reference ReferenceType="HasTypeDefinition">i=63</Reference> <!-- PropertyType -->
    <Reference ReferenceType="HasModellingRule">i=78</Reference> <!-- Mandatory -->
  </References>
</UAVariable>

<UAVariable NodeId="ns=2;i=1003" BrowseName="2:SerialNumber"
            ParentNodeId="ns=2;i=1001" DataType="String">
  <DisplayName>Serial Number</DisplayName>
  <Description>Serial number based on ECLASS 0173-1#02-AAW338#001</Description>
  <References>
    <Reference ReferenceType="HasTypeDefinition">i=63</Reference>
    <Reference ReferenceType="HasModellingRule">i=78</Reference>
  </References>
</UAVariable>

<UAVariable NodeId="ns=2;i=1004" BrowseName="2:MaxOperatingTemperature"
            ParentNodeId="ns=2;i=1001" DataType="Double">
  <DisplayName>Max Operating Temperature</DisplayName>
  <Description>Max operating temperature in °C</Description>
  <References>
    <Reference ReferenceType="HasTypeDefinition">i=63</Reference>
    <Reference ReferenceType="HasModellingRule">i=79</Reference> <!-- Optional -->
  </References>
  <Value>
    <Double>85.0</Double>
  </Value>
  <EURange>
    <Low>-40.0</Low>
    <High>150.0</High>
  </EURange>
  <EngineeringUnits>
    <NamespaceUri>http://www.opcfoundation.org/UA/units/un/cefact</NamespaceUri>
    <UnitId>4408652</UnitId> <!-- degree Celsius -->
  </EngineeringUnits>
</UAVariable>
```

### 4.2 AAS 的复用层次

```text
AAS 复用层次
├── Level 1: 子模型模板复用 (Submodel Template Reuse)
│   ├── 定义: 标准化的子模型结构（如"技术数据"、"文档"、"标识"）
│   ├── 来源: IDTA（工业数字孪生协会）发布的标准子模型模板
│   ├── 示例: TechnicalData、Nameplate、Identification、ContactInformation
│   └── 复用方式: 下载模板 → 实例化 → 填充特定值
│
├── Level 2: 概念描述复用 (Concept Description Reuse)
│   ├── 定义: 标准化的语义定义（如"制造商名称"、"序列号"）
│   ├── 来源: ECLASS、IEC CDD、ETIM、PROLIST
│   ├── 示例: ECLASS 0173-1#02-AAO677#002 = ManufacturerName
│   └── 复用方式: 引用 IRDI（International Registration Data Identifier）
│
├── Level 3: AAS 实例复用 (AAS Instance Reuse)
│   ├── 定义: 特定资产的完整数字孪生实例
│   ├── 示例: 某台具体电机的 AAS（包含所有子模型和实际数据）
│   └── 复用方式: 克隆实例 → 修改标识符和特定值 → 部署到新资产
│
└── Level 4: AAS 生态复用 (AAS Ecosystem Reuse)
    ├── 定义: 跨组织的 AAS 交换和互操作
    ├── 示例: 供应商提供产品的 AAS → 集成商导入 AAS → 运营商使用 AAS
    └── 复用方式: AASX 包格式（基于 OPC UA NodeSet + JSON + 文件）
```

---

## 5. IEC 61508 Proven-in-Use：统计验证方法深度

### 5.1 Proven-in-Use 的统计基础

IEC 61508-3-1:2016 的 Proven-in-Use（PIU）方法允许通过运行历史来证明软件组件的安全完整性，而非执行完整的 V 模型生命周期。其统计基础是**置信区间估计**。

#### 故障率估计的统计方法

```text
Proven-in-Use 统计验证方法
├── 目标: 证明软件组件的故障率 λ 低于 SIL 目标要求
│
├── 数据收集
│   ├── 运行时间 T: 组件在所有应用中的累计运行时间（小时）
│   ├── 故障数 N: 在运行时间 T 内观察到的危险故障数
│   └── 环境相似性: 收集数据的应用环境与新应用环境的相似度评估
│
├── 统计模型
│   ├── 假设: 故障服从泊松过程（Poisson Process）
│   ├── 点估计: λ̂ = N / T（故障率的最大似然估计）
│   ├── 置信区间: λ 的 (1-α) 置信上限
│   └── 公式: λ_upper = χ²(2N+2, 1-α) / (2T)
│       ├── χ²: 卡方分布的分位数
│       ├── 2N+2: 自由度
│       └── 1-α: 置信水平（通常 90% 或 95%）
│
├── SIL 目标对比
│   ├── SIL 1: λ < 10⁻⁵ /h (危险故障率)
│   ├── SIL 2: λ < 10⁻⁶ /h
│   ├── SIL 3: λ < 10⁻⁷ /h
│   └── SIL 4: λ < 10⁻⁸ /h
│
└── 判定规则
    ├── 若 λ_upper < SIL_target → 组件满足 PIU 要求，可复用
    ├── 若 λ_upper ≥ SIL_target → 组件不满足 PIU 要求，需补充验证或重新开发
    └── 若 N = 0（零故障）→ λ_upper = χ²(2, 1-α) / (2T) = -ln(α) / T（对于 90% 置信度，λ_upper ≈ 2.3 / T）
```

#### PIU 计算示例

```text
示例：安全联锁逻辑模块的 Proven-in-Use 评估

参数:
├── 组件: 安全联锁逻辑判断模块（SIL 2 目标）
├── 运行历史: 50 个相同应用，每个运行 2 年（17,520 小时）
├── 累计运行时间 T = 50 × 17,520 = 876,000 小时
├── 观察到的危险故障数 N = 0（零故障）
├── 置信水平: 90%（α = 0.1）
├── SIL 2 目标故障率: λ_target = 10⁻⁶ /h
│
计算:
├── 零故障时的 90% 置信上限:
│   λ_upper = -ln(0.1) / 876,000 = 2.3026 / 876,000 ≈ 2.63 × 10⁻⁶ /h
│
├── 判定:
│   λ_upper (2.63 × 10⁻⁶) > λ_target (1.00 × 10⁻⁶)
│   → 不满足 SIL 2 的 PIU 要求！
│
├── 改进方案:
│   方案 A: 延长运行时间至 T = 2,302,600 小时（约 263 年累计）
│           λ_upper = 2.3026 / 2,302,600 ≈ 1.00 × 10⁻⁶ /h ✓
│   方案 B: 降低目标至 SIL 1（λ_target = 10⁻⁵ /h）
│           λ_upper (2.63 × 10⁻⁶) < λ_target (10⁻⁵) ✓
│   方案 C: 补充形式化验证（覆盖关键路径）+ 缩短运行时间要求
│   方案 D: 增加冗余（2oo3 表决）→ 系统级故障率降低，允许模块级 PIU 放宽
│
└── 结论: 单独的 PIU 不足以满足 SIL 2，需要结合其他方法（如冗余、形式化验证）
```

### 5.2 PIU 的贝叶斯方法扩展

```text
Proven-in-Use 的贝叶斯扩展方法
├── 先验分布: 基于类似组件的历史数据或专家判断，设定故障率的先验分布
│   ├── 常用先验: Gamma 分布（共轭先验，便于计算）
│   ├── Gamma(α₀, β₀): α₀ 为先验故障数，β₀ 为先验运行时间
│   └── 无信息先验: α₀ = 0.5, β₀ = 0（Jeffreys 先验）
│
├── 后验分布: 结合先验和观察数据
│   ├── 观察数据: N 故障，T 运行时间
│   ├── 后验: Gamma(α₀ + N, β₀ + T)
│   └── 后验均值: E[λ] = (α₀ + N) / (β₀ + T)
│
├── 贝叶斯置信上限（Credible Interval）
│   ├── 90% 可信上限: λ_upper = Gamma⁻¹(0.9; α₀+N, β₀+T)
│   └── 与经典方法的对比: 贝叶斯方法允许融入先验知识，减少所需运行时间
│
└── 示例（带先验知识）
    ├── 先验: 类似组件的历史故障率 λ_prior ≈ 5 × 10⁻⁷ /h
    ├── 先验分布: Gamma(α₀=1, β₀=2,000,000) → 均值 5 × 10⁻⁷
    ├── 观察: N=0, T=876,000
    ├── 后验: Gamma(α=1, β=2,876,000) → 均值 3.48 × 10⁻⁷
    ├── 90% 可信上限: ≈ 8.5 × 10⁻⁷ /h
    └── 判定: 8.5 × 10⁻⁷ < 10⁻⁶ (SIL 2) → 满足 PIU 要求 ✓

    对比: 经典方法（无先验）需要 T > 2,302,600 小时
          贝叶斯方法（有先验）仅需 T = 876,000 小时
          → 先验知识减少运行时间需求 62%
```

### 5.3 PIU 复用的约束与风险

```text
PIU 复用的约束与风险
├── 约束 1: 环境相似性
│   ├── 要求: 收集 PIU 数据的应用环境必须与新应用环境"足够相似"
│   ├── 评估维度: 硬件平台、操作系统、编译器、输入数据分布、操作模式
│   └── 风险: 环境差异导致故障模式不同，PIU 数据失效
│
├── 约束 2: 变更影响
│   ├── 要求: 组件自 PIU 数据收集以来未发生影响安全性的变更
│   ├── 评估: 变更影响分析（CIA: Change Impact Analysis）
│   └── 风险: 微小变更（如编译器优化选项）可能引入新故障模式
│
├── 约束 3: 数据完整性
│   ├── 要求: 运行时间和故障数据必须完整、准确、可追溯
│   ├── 验证: 日志审计、数据来源确认、统计方法审查
│   └── 风险: 数据遗漏、故障漏报、记录错误
│
├── 约束 4: 统计显著性
│   ├── 要求: 累计运行时间必须足够长，以提供统计显著性
│   ├── 问题: 高 SIL 等级（SIL 3/4）要求极长的运行时间（数十年）
│   └── 风险: 技术迭代速度超过 PIU 数据收集速度，组件在收集完成前已过时
│
└── 约束 5: 监管接受度
    ├── 要求: 目标监管机构必须接受 PIU 作为验证方法
    ├── 差异: 欧洲（ERA）较接受 PIU；美国（FAA）较保守；中国（NFSA）要求结合其他方法
    └── 风险: 监管政策变化导致已接受的 PIU 证据失效
```

---

## 附录 M：卷五深化思维表征

### M.1 OPC UA FX 帧结构对比图

| 字段 | C2C (10-100ms) | C2D (500μs-10ms) | D2D (250μs-1ms) |
|------|----------------|-------------------|-----------------|
| **UADP Version** | 1 byte | 1 byte | 1 byte |
| **Publisher ID** | 4-8 bytes | 2-4 bytes | 1-2 bytes |
| **Group Version** | 4 bytes | 4 bytes | 2 bytes |
| **Sequence Number** | 2 bytes | 2 bytes | 1 byte |
| **Timestamp** | 8 bytes (μs) | 8 bytes (μs) | 8 bytes (ns) |
| **Picoseconds** | 0 bytes | 0 bytes | 2 bytes |
| **DataSet Class ID** | 16 bytes | 16 bytes | 8 bytes (short) |
| **DataSet Fields** | 500-1400 bytes | 50-400 bytes | 20-150 bytes |
| **Signature** | 64-128 bytes | 32-64 bytes | 16-32 bytes |
| **Total Frame** | 600-1500 bytes | 100-500 bytes | 50-200 bytes |

### M.2 ISA-95 对象模型层次图

```text
ISA-95 对象模型层次
├── Enterprise
│   └── Site
│       └── Area
│           ├── ProductionUnit
│           │   └── WorkCell
│           │       └── WorkUnit
│           └── StorageZone
│               └── StorageUnit
│
├── Resource (跨层次)
│   ├── Personnel (绑定到 WorkCell/WorkUnit)
│   ├── Equipment (绑定到 WorkCell/WorkUnit)
│   └── Material (绑定到 StorageUnit/WorkUnit)
│
├── Capability (跨层次)
│   ├── ProductionCapability (绑定到 WorkCell)
│   ├── MaterialCapability (绑定到 StorageUnit)
│   └── PersonnelCapability (绑定到 WorkCell)
│
└── ProductDefinition
    ├── MaterialDefinition
    ├── MaterialClass
    └── ProcessSegment
        └── OperationSegment
```

### M.3 PLCopen 状态机对比矩阵

| 功能块 | 状态数 | 核心状态 | 安全相关 | 时序约束 | 复用等级 |
|--------|--------|----------|----------|----------|----------|
| **MC_Power** | 5 | Idle/PowerOnDone/Error | 是 | <500ms | 极高 |
| **MC_Home** | 6 | Idle/Done/Error | 是 | <10s | 极高 |
| **MC_MoveAbsolute** | 5 | Idle/Done/Error | 否 | <2周期 | 极高 |
| **MC_MoveRelative** | 5 | Idle/Done/Error | 否 | <2周期 | 极高 |
| **MC_MoveVelocity** | 5 | Idle/Done/Error | 否 | <2周期 | 极高 |
| **MC_Stop** | 4 | Idle/Done/Error | 是 | <1周期 | 极高 |
| **MC_CamIn** | 6 | Idle/InSync/Error | 否 | <2周期 | 高 |
| **MC_GearIn** | 6 | Idle/InGear/Error | 否 | <2周期 | 高 |

### M.4 AAS 子模型模板清单

| 子模型模板 | IDTA ID | 适用范围 | OPC UA 映射 | 复用频率 |
|------------|---------|----------|-------------|----------|
| **TechnicalData** | SM_TechnicalData | 所有资产 | ObjectType + Variables | 极高 |
| **Nameplate** | SM_Nameplate | 所有资产 | ObjectType + Variables | 极高 |
| **Identification** | SM_Identification | 所有资产 | ObjectType + Variables | 极高 |
| **Documentation** | SM_Documentation | 所有资产 | ObjectType + FileType | 高 |
| **Service** | SM_Service | 设备资产 | ObjectType + Methods | 中 |
| **CarbonFootprint** | SM_CarbonFootprint | 所有资产 | ObjectType + Variables | 新兴 |
| **HandoverDocumentation** | SM_Handover | 项目交付 | ObjectType + FileType | 中 |
| **ContactInformation** | SM_ContactInfo | 所有资产 | ObjectType + Variables | 高 |

### M.5 PIU 统计方法对比矩阵

| 方法 | 先验知识 | 数据需求 | 计算复杂度 | 保守度 | 适用场景 |
|------|----------|----------|------------|--------|----------|
| **经典置信区间** | 无 | 高（长运行时间） | 低 | 高 | 数据充足、无先验 |
| **贝叶斯（共轭先验）** | 中 | 中 | 中 | 中 | 有类似组件历史 |
| **贝叶斯（专家先验）** | 高 | 低 | 中 | 低 | 专家经验丰富 |
| **层次贝叶斯** | 高 | 中 | 高 | 中 | 多组件共享故障模式 |
| **Bootstrap** | 无 | 高 | 高 | 中 | 非泊松故障过程 |

---

> **卷五深化卷结束**。
> 本卷对卷五《工业IoT/OT-IT融合扩展卷》的五个核心章节进行了源码级/形式化级/协议级的递归深化：OPC UA FX帧结构（UADP确定性模式、TSN门控表、FX Connection Manager状态机）、ISA-95对象模型形式化（UML类图、属性精确定义、复用约束）、PLCopen功能块接口定义（MC_Power/MC_MoveAbsolute形式化、TLA+安全验证）、AAS数字孪生映射（JSON模板、OPC UA NodeSet映射、子模型模板复用）、IEC 61508 PIU统计验证（经典置信区间、贝叶斯方法、约束与风险）。
> 软件工程架构复用视角的完整知识体系至此构建为十二卷本+深化卷+速查手册，总计约260,000字符，26万字。
