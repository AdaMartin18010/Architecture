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

## 10. 正向示例

### 示例 1：汽车焊装车间融合网络

某德系整车厂焊装车间采用 IEC/IEEE 60802 配置文件，将机器人运动控制（硬实时，250 μs 周期）、PLC I/O（软实时，2 ms 周期）与视觉质检（Best Effort）流量复用到同一套 TSN 骨干网。通过复用 802.1AS 时钟域和 802.1Qbv 门控列表模板，新产线网络规划时间从 6 周缩短到 2 周，网关数量减少 40%。

### 示例 2：过程自动化远程 I/O

石化装置将远程 I/O 与 DCS 控制器通过 60802 兼容 TSN 交换机连接，利用 802.1CB 帧复制实现关键控制回路冗余，单链路故障时切换时间 < 1 ms，满足 SIL 2 对应 FTTI 要求。

## 11. 反例 / 失败案例

### 反例 1：直接复制 GCL 模板忽略拓扑差异

某项目将 A 厂房的 802.1Qbv 门控配置原样复制到 B 厂房，未重新计算交换机转发延迟和电缆传播时延，导致时间槽重叠，控制报文周期性丢失，产线抖动超标。

### 反例 2：非 TSN 交换机承载时间触发流量

为节省成本，团队在非 TSN 商用交换机上运行 OPC UA FX C2D 循环数据，结果最佳努力流量挤占时隙，通信延迟从 500 μs 恶化到 10 ms，触发安全联锁误动作。

## 12. 参考索引

| 来源 | URL |
|:---|:---|
| IEC/IEEE 60802 TSN Profile for Industrial Automation | <https://1.ieee802.org/tsn/iec-ieee-60802/> |
| IEEE 802.1 TSN Task Group | <https://1.ieee802.org/tsn/> |
| IEEE 802.1AS-Rev (gPTP) | <https://1.ieee802.org/tsn/802-1as/> |
| IEEE 802.1Qbv (Time-Aware Shaper) | <https://1.ieee802.org/tsn/802-1qbv/> |
| OPC UA FX Part 80 | <https://reference.opcfoundation.org/UAFX/Part80/v100/docs/> |
| IEC 62541 OPC Unified Architecture | <https://webstore.iec.ch/publication/66912> |
| IEC 61784-3 Functional safety fieldbuses | <https://webstore.iec.ch/publication/66912> |
| TSN Industrial Automation Conformance Collaboration (TIACC) | <https://www.tiacc.net/> |

---

> 最后更新: 2026-07-08
> 权威来源: <https://1.ieee802.org/tsn/iec-ieee-60802/>
