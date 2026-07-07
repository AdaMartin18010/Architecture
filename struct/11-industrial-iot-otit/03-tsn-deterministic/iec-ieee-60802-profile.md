# IEC/IEEE 60802 TSN 工业自动化配置文件

> **版本**: 2026-06-06
> **权威来源**: IEEE 802.1 TSN, IEC SC65C/WG18
> **定位**: 对齐 IEC/IEEE 60802 TSN Profile for Industrial Automation

---

## 1. 标准背景

IEC/IEEE 60802 是 IEC 和 IEEE 的联合项目，旨在为工业自动化定义 TSN（Time-Sensitive Networking）配置文件。
这是一个**双标徽标准**（dual logo standard），同时是 IEC 和 IEEE 标准。

| 项目 | 内容 |
|------|------|
| **标准名称** | IEC/IEEE 60802 TSN Profile for Industrial Automation |
| **发起方** | IEC SC65C/WG18 + IEEE 802.1 TSN Task Group |
| **目标** | 使 IEEE 802 标准能够在工业自动化中部署融合网络 |
| **关键价值** | 同时支持 OT 流量和其他流量 |

---

## 2. TSN 四大支柱

TSN 建立在四个关键技术支柱上：

```text
TSN Four Pillars
├── 1. Time Synchronization（时间同步）
│   └── IEEE 802.1AS - gPTP 精确时间协议
│
├── 2. Guaranteed End-to-End Latency（保证端到端延迟）
│   ├── IEEE 802.1Qbv - 增强流量整形（门控列表）
│   ├── IEEE 802.1Qbu/802.3br - 帧抢占
│   └── IEEE 802.1CB - 帧复制和消除
│
├── 3. Reliability（可靠性）
│   ├── IEEE 802.1CB - 帧复制和消除
│   └── IEEE 802.1Qca - 路径控制和预留
│
└── 4. Resource Management（资源管理）
    ├── IEEE 802.1Qcc - 流预留协议 (SRP)
    └── IEEE 802.1Qcp - YANG 数据模型
```

---

## 3. IEC/IEEE 60802 的核心内容

60802 为工业自动化选择并规定了以下内容：

- **Features（特性）**: 哪些 IEEE 802 TSN 特性必须实现
- **Options（选项）**: 哪些可选特性在工业场景中应启用
- **Configurations（配置）**: 默认参数和推荐配置
- **Defaults（默认值）**: 即插即用的默认行为
- **Protocols（协议）**: 使用的协议栈
- **Procedures（规程）**: 部署和操作程序

---

## 4. 工业自动化流量类型

60802 定义了工业自动化中的典型流量类型：

| 流量类型 | 周期 | 延迟要求 | 示例 |
|---------|------|---------|------|
| **硬实时** | 250 μs - 1 ms | < 100 μs | 运动控制、安全 |
| **软实时** | 1 ms - 10 ms | < 1 ms | PLC I/O |
| **循环数据** | 10 ms - 100 ms | < 10 ms | 过程数据 |
| **事件数据** | 非周期 | < 100 ms | 报警、诊断 |
| **Best Effort** | 非周期 | 无保证 | 配置、Web |

---

## 5. OPC UA FX 与 60802 的关系

OPC UA FX 直接使用 IEC/IEEE 60802 作为其底层网络传输：

```text
OPC UA FX Stack
├── Application Layer: OPC UA PubSub / Client-Server
├── Transport Layer: UDP/IP
├── Network Layer: IEEE 802.3 Ethernet + TSN
└── TSN Profile: IEC/IEEE 60802
```

60802 提供：

- **确定性**: 保证延迟和抖动边界
- **融合网络**: OT 和 IT 流量共享同一物理网络
- **互操作性**: 多厂商设备基于统一配置文件

---

## 6. 时间同步精度

IEC/IEEE 60802 要求的时间同步精度：

| 应用场景 | 精度要求 |
|---------|---------|
| 一般工业自动化 | ±1 μs |
| 高精度运动控制 | ±100 ns |
| 过程自动化 | ±10 ms |

实现机制：

- IEEE 802.1AS gPTP（generalized Precision Time Protocol）
- 边界时钟（Boundary Clock）
- 透明时钟（Transparent Clock）

---

## 7. 门控调度（Gate Control List）

IEEE 802.1Qbv 的门控调度是 TSN 的核心机制：

```text
Gate Control List (GCL)
├── Base Time: 调度开始时间
├── Cycle Time: 循环周期
├── Gate States: 每个队列的开关状态
└── Time Intervals: 每个状态的持续时间
```

### 设计约束

- GCL 周期必须与控制回路周期对齐
- 门控转换时间必须考虑帧传输时间
- 多个流共享队列时需要避免冲突

---

## 8. 部署最佳实践

### 网络拓扑

```text
Star/Ring Topology
├── Central TSN Switch (主时钟)
├── Edge TSN Switches
│   ├── PLC
│   ├── Robot Controller
│   ├── HMI
│   └── IO Modules
└── Converged IT/OT Traffic
```

### 配置流程

1. **识别流量类型**: 分类所有实时和非实时流量
2. **定义 SLA**: 每个流量类型的延迟、抖动、丢包率要求
3. **设计 GCL**: 为关键流量预留时间槽
4. **配置 SRP**: 为流预留网络资源
5. **验证**: 使用网络演算或测量验证

---

## 9. 复用价值

> **定理 TSN.1** (Profile Interoperability): 严格遵循 IEC/IEEE 60802 的设备可以在不需要自定义配置的情况下实现互操作。任何偏离配置文件的行为都会增加集成成本和风险。
> **定理 TSN.2** (Convergence Benefit): 使用 60802 的融合网络可以将 OT 和 IT 基础设施成本降低 30-50%，但前提是流量工程必须正确实施。

---

> 最后更新: 2026-06-06
> 权威来源: <https://1.ieee802.org/tsn/iec-ieee-60802/>


---

## 补充章节
## 概念定义

**定义**：工业 IoT/OT-IT 复用是在制造、能源、交通等运营技术（OT）与信息技术（IT）融合场景中，复用 ISA-95 层级模型、OPC UA 信息模型、功能安全组件与数字孪生资产。

## 示例

**示例**：汽车工厂将 ISA-95 L0-L4 资产目录映射到 IEC 63278 资产管理壳（AAS），通过 OPC UA FX 实现现场设备与 MES/ERP 的即插即用复用。

## 反例

**反例**：将 IT 系统直接补丁策略套用到 PLC 产线，未考虑实时性约束与功能安全认证，导致停机与安全事故。