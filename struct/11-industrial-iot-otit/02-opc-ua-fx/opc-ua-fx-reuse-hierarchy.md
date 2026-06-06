# OPC UA FX 复用层次分析

> **版本**: 2026-06-06
> **对齐标准**: OPC UA FX 1.0 (2026), IEC 62541-100, IEC/IEEE 60802 TSN
> **定位**: 分析 OPC UA FX 在现场级通信中的四层复用模型

---

## 目录

- [OPC UA FX 复用层次分析](#opc-ua-fx-复用层次分析)
  - [目录](#目录)
  - [1. OPC UA FX 的技术栈](#1-opc-ua-fx-的技术栈)
  - [2. 四层复用模型](#2-四层复用模型)
    - [Level 1: 物理硬件复用](#level-1-物理硬件复用)
    - [Level 2: 通信协议复用](#level-2-通信协议复用)
    - [Level 3: 信息模型复用](#level-3-信息模型复用)
    - [Level 4: 应用逻辑复用](#level-4-应用逻辑复用)
  - [3. C2C / C2D / D2D 的复用差异](#3-c2c--c2d--d2d-的复用差异)
  - [4. 2026 厂商支持矩阵](#4-2026-厂商支持矩阵)
  - [5. 现场层复用决策树](#5-现场层复用决策树)
  - [6. 形式化约束](#6-形式化约束)

---

## 1. OPC UA FX 的技术栈

```text
OPC UA FX 技术栈
├── 物理层: 标准以太网 (1GbE/10GbE) + Single-Pair Ethernet (Ethernet-APL)
│   └── 复用: 商用现成以太网芯片，无需专用 ASIC
│
├── 确定性层: TSN (Time-Sensitive Networking) ──→ IEC/IEEE 60802
│   ├── 802.1AS-Rev: 亚微秒级时间同步 (gPTP)
│   ├── 802.1Qbv: 时间感知整形器 (Time-Aware Shaper)
│   ├── 802.1CB: 帧复制与消除 (冗余)
│   ├── 802.1Qcc: 集中式网络配置 (CNC)
│   └── 复用: TSN 配置文件的跨厂商标准化
│
├── 传输层: OPC UA PubSub over UDP
│   ├── UADP: 确定性二进制编码
│   ├── 安全模式: 确定性安全（无握手延迟）
│   └── 复用: OPC UA 信息模型跨层复用
│
└── 应用层: FX 通信配置文件
    ├── C2C (Controller-to-Controller): 控制器间协调，10-100ms 周期
    ├── C2D (Controller-to-Device): 控制器到 IO/驱动，500μs-10ms 周期
    └── D2D (Device-to-Device): 设备间直连，250μs-1ms 周期
```

---

## 2. 四层复用模型

### Level 1: 物理硬件复用

| 复用单元 | 标准组件 | 价值 |
|---------|---------|------|
| 标准以太网交换机 | TSN-capable 商用交换机 | 替代专用现场总线交换机 |
| 标准以太网电缆 | CAT6A, Single-Pair Ethernet (Ethernet-APL) | 降低布线成本和备件库存 |
| 标准以太网 PHY 芯片 | 1GbE/10GbE 商用芯片 | 无需厂商专用 ASIC |

**复用边界**: 硬件复用受 TSN 能力约束。非 TSN 交换机只能用于背景流量，不能用于时间触发通信。

### Level 2: 通信协议复用

| 复用单元 | 内容 | 价值 |
|---------|------|------|
| TSN 配置模板 | 802.1Qbv 门控表、802.1AS 时钟域 | 跨厂商网络规划复用 |
| OPC UA PubSub 配置 | 发布者/订阅者、数据集定义 | 一次配置，多设备部署 |
| UADP 协议栈库 | 编码/解码、序列号管理 | 跨平台软件复用 |

**复用边界**: TSN 配置必须与具体的网络拓扑、设备周期、流量特征绑定。模板需要参数化适配。

### Level 3: 信息模型复用

| 复用单元 | 内容 | 价值 |
|---------|------|------|
| Companion Specifications | 设备类型定义、语义互操作 | 跨厂商语义一致性 |
| FX Connection Manager | 连接配置、流预留、冗余模式 | 连接管理的工程模板 |
| 设备描述文件 | 类型库、配置向导 | 快速设备集成 |

**复用边界**: Companion Specification 的成熟度决定复用深度。新兴设备类型可能缺乏标准化信息模型。

### Level 4: 应用逻辑复用

| 复用单元 | 内容 | 价值 |
|---------|------|------|
| C2C/C2D/D2D 配置模板 | 连接配置文件 | 相同通信模式的快速复制 |
| 控制回路模板 | PID 参数集、运动控制轨迹 | 控制算法的参数化复用 |
| Golden Path | 工程模板、项目模板 | 从设计到部署的标准化路径 |

**复用边界**: 应用逻辑复用必须考虑具体工艺的安全约束和性能要求。模板复用不等于无审查部署。

---

## 3. C2C / C2D / D2D 的复用差异

| 维度 | C2C (Controller-to-Controller) | C2D (Controller-to-Device) | D2D (Device-to-Device) |
|------|--------------------------------|---------------------------|------------------------|
| **周期** | 10-100 ms | 500 μs - 10 ms | 250 μs - 1 ms |
| **帧大小** | 500-1500 bytes | 100-500 bytes | 50-200 bytes |
| **Publisher ID** | 控制器 NodeID | 控制器 NodeID | 设备 NodeID（直接发布） |
| **Group Version** | 高（配置变更频繁） | 中 | 低（设备配置固定） |
| **Timestamp 精度** | 微秒级 | 微秒级 | 纳秒级（运动控制） |
| **Payload** | 复杂数据结构（多个 DataSet） | 简单 IO 数据（单个 DataSet） | 极简（原始值+状态） |
| **Security** | 签名+加密 | 签名（可选加密） | 签名（性能优先） |
| **冗余** | 802.1CB 帧复制 | 802.1CB 帧复制 | 802.1CB 帧复制 |
| **复用成熟度** | 高（2026 已量产） | 中（2026 试点） | 低（规划中） |
| **典型场景** | PLC 间协调、产线同步 | 伺服驱动、IO 模块 | 视觉→机器人、安全扫描→驱动 |

---

## 4. 2026 厂商支持矩阵

| 厂商 | C2C 状态 | C2D 状态 | D2D 状态 | 代表产品 | 复用策略 |
|------|----------|----------|----------|----------|----------|
| **Siemens** | 已发布 (S7-1500 TM) | 2026 试点 (ET 200) | 规划中 | S7-1500, Scalance XCM | 原生 FX + Profinet 共存 |
| **Rockwell** | 2026 Q1 (ControlLogix) | 2026 H2 (FLEXHA 5000) | 规划中 | ControlLogix, Stratix | 固件升级现有平台 |
| **Beckhoff** | 已发布 (TwinCAT 3) | 已发布 (CX TSN 网关) | 规划中 | CX 系列, EK/EL 耦合器 | EtherCAT + FX 混合 |
| **Phoenix Contact** | 已发布 (PLCnext) | 试点 (Axioline F2) | 规划中 | PLCnext, FL SWITCH TSN | 开放多厂商策略 |
| **B&R (ABB)** | 已发布 (X20/X90) | 2026 (ACOPOS M4) | 规划中 | X20, ACOPOS M4 | 伺服驱动原生支持 |

**关键洞察**:

- C2C 在所有厂商中率先落地，因为周期要求宽松（10-100ms），政治价值高（跨厂商互操作）
- C2D 面临现有现场总线（EtherCAT/Profinet）的强竞争，仅在绿地或扩展场景中采用
- D2D 仍处于早期，依赖 Companion Specifications 的成熟度

---

## 5. 现场层复用决策树

```text
现场层通信复用决策树
│
├── 场景: 新建工厂 (Greenfield)
│   ├── 需要运动控制 (<250μs)?
│   │   ├── 是 → 内循环: EtherCAT/Profinet IRT; 外循环: OPC UA FX C2C
│   │   └── 否 → 全厂 OPC UA FX (C2C + C2D)
│   └── 多厂商环境?
│       ├── 是 → OPC UA FX 强制（避免 vendor lock-in）
│       └── 否 → 可选单一厂商总线或 FX
│
├── 场景: 现有工厂改造 (Brownfield)
│   ├── 保留现有现场总线?
│   │   ├── 是 → 网关模式: 现有总线 + FX 网关 + TSN 骨干网
│   │   └── 否 → 完全替换（仅当控制器到期更换时）
│   └── 新增产线/扩展?
│       ├── 是 → 新增单元用 FX，通过网关与现有系统集成
│       └── 否 → 维持现状，仅升级监控层
│
└── 场景: 混合场景 (Hybrid)
    ├── 核心策略: "网关-led 渐进迁移"
    ├── 第一步: FX C2C 连接各现有单元（通过网关）
    ├── 第二步: 新增单元原生 FX
    ├── 第三步: 控制器到期更换时，内循环评估 C2D 迁移
    └── 时间跨度: 10-15 年完整迁移
```

---

## 6. 形式化约束

> **公理 FX.1** (Determinism Preservation): OPC UA FX 的复用必须保持端到端确定性。任何在复用过程中引入的额外协议转换（网关、代理）必须证明其时延上界小于应用容忍阈值。
> **公理 FX.2** (Semantic Compatibility): 跨厂商复用的前提是 Companion Specification 的语义兼容性。仅语法兼容（相同 UADP 帧格式）不足以保证互操作；必须验证信息模型的语义等价性。
> **定理 FX.1** (C2C-C2D Migration Cost): 从 C2C 升级到 C2D 的迁移成本与现有现场总线的生命周期剩余时间成反比。形式化：MigrationCost(t) = K / RemainingLifetime(t)，其中 K 为设备更换和工程重做的固定成本。
> **定理 FX.2** (Gateway Eternity): 在棕地工厂中，协议网关不是临时过渡措施，而是**永久性架构组件**。声称"最终消除网关"的架构愿景违背工业现实。
> **定理 TSN.1** (GCL Cycle Consistency): 若网络中有 N 个设备参与时间触发通信，则所有设备的 GCL 周期 T 必须满足：T = k × T_base，其中 k ∈ ℕ⁺。且 |BaseTimeᵢ - BaseTimeⱼ| < ε，ε 为 gPTP 同步精度（通常 < 1μs）。违反此约束将导致时间槽重叠或空闲。
> **定理 TSN.2** (Guard Band Necessity): 保护带长度 G 必须满足：G ≥ MTU_max / LineRate + PropagationDelay_max + Jitter_max。

---

> 最后更新: 2026-06-06
> 下次更新时机: OPC UA FX C2D/D2D 正式发布 / 新厂商支持声明
