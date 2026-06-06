# 2026 年 OPC UA FX 厂商支持矩阵

> **版本**: 2026-06-06
> **状态**: 基于公开产品发布、展会演示（Hannover Messe 2025/2026, SPS 2025）及厂商路线图整理
> **定位**: 为架构复用决策提供客观的厂商能力基线

---

## 目录

- [1. 矩阵总览](#1-矩阵总览)
- [2. 厂商详情](#2-厂商详情)
- [3. 关键趋势分析](#3-关键趋势分析)
- [4. 选型建议](#4-选型建议)
- [5. 参考文献](#5-参考文献)

---

## 1. 矩阵总览

| 厂商 | 总部 | 代表产品线 | C2C 支持 | C2D 支持 | D2D 支持 | TSN 支持 | 发布时间 | 复用策略 |
|------|------|-----------|:--------:|:--------:|:--------:|:--------:|:--------:|----------|
| **Siemens** | 德国 | S7-1500 TM, ET 200, Scalance XCM | ✅ 已发布 | 🧪 2026 试点 | 📋 规划中 | ✅ 已发布 | 2024 (C2C) / 2026 H2 (C2D) | 原生 FX + Profinet 共存 |
| **Rockwell** | 美国 | ControlLogix 5580, FLEXHA 5000, Stratix | ✅ 2026 Q1 | 🧪 2026 H2 | 📋 规划中 | ✅ 已发布 | 2026 Q1 (C2C) / 2026 H2 (C2D) | 固件升级现有平台 |
| **Beckhoff** | 德国 | CX 系列, TwinCAT 3, EK/EL 耦合器 | ✅ 已发布 | ✅ 已发布 | 📋 规划中 | ✅ 已发布 | 2023 (C2C) / 2025 (C2D) | EtherCAT + FX 混合架构 |
| **B&R (ABB)** | 奥地利 | X20, ACOPOS M4, X90 | ✅ 已发布 | 🧪 2026 试点 | 📋 规划中 | ✅ 已发布 | 2023 (C2C) / 2025 (C2D 原型) | 伺服驱动原生支持 |
| **Phoenix Contact** | 德国 | PLCnext, Axioline F2, FL SWITCH TSN | ✅ 已发布 | 🧪 试点 | 📋 规划中 | ✅ 已发布 | 2023 (C2C) | 开放多厂商策略 |
| **Mitsubishi** | 日本 | iQ-R, iQ-F, CC-Link IE TSN 模块 | ✅ 2026 Q2 | 📋 规划中 | 📋 规划中 | ✅ 已发布 | 2026 Q2 (C2C) | CC-Link IE TSN + FX 桥接 |
| **Schneider Electric** | 法国 | EcoStruxure, Modicon M580, PAC | 🧪 2026 试点 | 📋 规划中 | 📋 规划中 | ✅ 部分 | 2026 (试点) | EcoStruxure OPC UA Server Expert |
| **Hilscher** | 德国 | netX 90 / netX 4000 TSN | ✅ 已发布 | 🧪 试点 | 📋 规划中 | ✅ 已发布 | 2024 (C2C) | 芯片级 FX 协议栈供应 |

> **图例**: ✅ 已发布（量产可用） | 🧪 试点/预览（客户试用） | 📋 规划中（ roadmap 声明）

---

## 2. 厂商详情

### 2.1 Siemens（西门子）

| 项目 | 内容 |
|------|------|
| **C2C 产品** | S7-1500 TM NET 通信模块（固件 V3.0+） |
| **C2D 产品** | ET 200 SP IO-Link FX 预览模块（Hannover Messe 2026） |
| **TSN 交换机** | Scalance XCM-300 / XCM-400 系列，支持 802.1Qbv/AS/CB |
| **工程软件** | TIA Portal V19 + UAFX 插件 |
| **关键里程碑** | 2025 Hannover Messe：S7-1500 与 Beckhoff/Phoenix Contact 控制器实现无网关 C2C 互通 |
| **复用策略** | "原生 FX + Profinet 共存"：现有 Profinet 设备通过 TSN 交换机与 FX C2C 网络融合，ET 200 系列逐步扩展 FX C2D 能力 |

**洞察**: Siemens 是 OPC UA FX 最积极的推动者之一，其策略强调**渐进式融合**而非颠覆替换。S7-1500 TM 模块使现有控制器无需更换主机即可支持 FX，显著降低棕地迁移成本。[Siemens Hannover Messe 2025/2026 Demo]

### 2.2 Rockwell Automation（罗克韦尔）

| 项目 | 内容 |
|------|------|
| **C2C 产品** | ControlLogix 5580 控制器（2026 Q1 固件更新） |
| **C2D 产品** | FLEXHA 5000 I/O（2026 H2 roadmap，Automation Fair 2026 GA） |
| **TSN 交换机** | Stratix 5400/5410 系列（2024 年硬件就绪，2026 年 FX 固件刷新） |
| **工程软件** | FactoryTalk Design Studio + Plex MES 集成 |
| **关键里程碑** | 2026 年 2 月 Berlin IOP：Rockwell 与 Beckhoff、Mitsubishi 完成多厂商 C2C 互操作测试 |
| **复用策略** | "固件升级现有平台"：保护 Americas 地区庞大的 ControlLogix 装机量，通过固件更新而非硬件替换引入 FX |

**洞察**: Rockwell 的 FX 策略与其在北美离散制造业的统治地位深度绑定。FactoryTalk Design Hub 的工程模板复用是关键差异化点。[Rockwell Automation Fair 2026 Roadmap]

### 2.3 Beckhoff（倍福）

| 项目 | 内容 |
|------|------|
| **C2C 产品** | TwinCAT 3（TF6xxx OPC UA FX 功能包） |
| **C2D 产品** | CX TSN 网关（EK/EL 耦合器后挂 FX 接口） |
| **TSN 交换机** | CX7000 系列 IPC 集成 TSN 端口 |
| **工程软件** | TwinCAT XAE + TF6xxx 配置向导 |
| **关键里程碑** | 2026 年 2 月 Berlin IOP 主办方：测试 PubSub Ethernet、优先级映射、AML 离线工程交换 |
| **复用策略** | "EtherCAT + FX 混合"：内循环保留 EtherCAT（<100 μs），外循环/单元间采用 FX C2C/C2D |

**洞察**: Beckhoff 是 2026 年 2 月 Berlin IOP 的主办方，其开放态度表明 FX 不是 EtherCAT 的替代者，而是**向上扩展**的互操作层。CX TSN 网关允许现有 EtherCAT 从站设备通过透明桥接参与 FX 网络。[Beckhoff Berlin IOP 2026]

### 2.4 B&R Industrial Automation（ABB 旗下）

| 项目 | 内容 |
|------|------|
| **C2C 产品** | X20 系列 PLC（X20CP3686 等） |
| **C2D 产品** | ACOPOS M4 伺服驱动（2025 年 SPS 发布，原生 FX 支持） |
| **TSN 交换机** | X20 总线耦合器集成 TSN 端口 |
| **工程软件** | Automation Studio + mapp Technology |
| **关键里程碑** | 2025 年 11 月 SPS：ACOPOS M4 是首批原生支持 OPC UA FX 的伺服驱动之一，消除协议网关需求 |
| **复用策略** | "伺服驱动原生支持"：将 FX 协议栈直接嵌入驱动器固件，实现控制器到驱动的直接确定性通信 |

**洞察**: B&R 的 ACOPOS M4 代表了 OPC UA FX C2D 的**理想形态**——无需网关、无需协议转换，控制器直接通过 UADP 向伺服驱动发送运动指令。这对运动控制领域的棕地迁移具有示范意义。[B&R ACOPOS M4 Launch]

### 2.5 Phoenix Contact（菲尼克斯电气）

| 项目 | 内容 |
|------|------|
| **C2C 产品** | PLCnext 控制器（AXC F 2152 / RFC 4072S） |
| **C2D 产品** | Axioline F2 I/O 模块（FX 预览版） |
| **TSN 交换机** | FL SWITCH TSN 系列 |
| **工程软件** | PLCnext Engineer + Eclipse 插件 |
| **关键里程碑** | 长期参与 OPC Foundation FLC 倡议，强调开放性和多厂商互操作 |
| **复用策略** | "开放多厂商策略"：PLCnext 平台基于 Linux + container，允许第三方 FX 协议栈（如 open62541）直接部署 |

**洞察**: Phoenix Contact 的 PLCnext 是工业控制器中**开放性最高**的平台之一。其容器化架构意味着 FX 能力可通过软件更新持续增强，而无需更换硬件。这延长了设备的复用生命周期。[Phoenix Contact PLCnext]

### 2.6 Mitsubishi Electric（三菱电机）

| 项目 | 内容 |
|------|------|
| **C2C 产品** | iQ-R 系列 PLC（2026 Q2 固件更新） |
| **C2D 产品** | 尚未公布具体产品线 |
| **TSN 交换机** | CC-Link IE TSN 模块（与 FX TSN 底层兼容） |
| **工程软件** | GX Works3 + MELSOFT Navigator |
| **关键里程碑** | 2026 年 2 月 Berlin IOP 参与者，验证 iQ-R 与欧美厂商控制器的 C2C 互通 |
| **复用策略** | "CC-Link IE TSN + FX 桥接"：在亚洲市场保留 CC-Link IE TSN 投资，通过网关与 FX 网络互操作 |

**洞察**: Mitsubishi 的策略反映了亚洲自动化市场的现实——CC-Link IE TSN 已有大量装机，完全迁移至 FX 不经济。Bridge/Gateway 模式是理性选择。[Mitsubishi iQ-R 2026 Update]

### 2.7 Schneider Electric（施耐德电气）

| 项目 | 内容 |
|------|------|
| **C2C 产品** | EcoStruxure OPC UA Server Expert（软件层） |
| **C2D 产品** | Modicon M580 / PAC（FX 能力规划中） |
| **TSN 交换机** | 部分 Industrial Ethernet 交换机支持 802.1AS |
| **工程软件** | EcoStruxure Automation Expert |
| **关键里程碑** | 2026 年 Hannover Messe：展示 EcoStruxure 作为 FX 网络的云端/边缘聚合层 |
| **复用策略** | "EcoStruxure 软件先行"：通过 OPC UA Server Expert 实现现有 Modbus/以太网设备向 FX 网络的软件级接入 |

**洞察**: Schneider 的 FX 策略偏向**软件定义**：不急于在底层控制器全面替换 Modbus/以太网，而是通过 EcoStruxure 软件栈实现上层 FX 兼容。这对过程工业（其传统优势领域）的渐进迁移是务实路径。[Schneider EcoStruxure 2026]

### 2.8 Hilscher（赫优讯）

| 项目 | 内容 |
|------|------|
| **C2C 产品** | netX 90 / netX 4000 TSN 芯片（含 FX 协议栈） |
| **C2D 产品** | netX 芯片 C2D 预览固件 |
| **TSN 交换机** | 芯片级 TSN 支持（供 OEM 集成） |
| **工程软件** | netX Studio + Protocol API |
| **关键里程碑** | 为多家中小型自动化厂商提供 FX 协议栈 IP，降低 FX 准入门槛 |
| **复用策略** | "芯片级 FX 供应"：作为协议栈供应商，使中小型设备厂商无需自研 FX 能力 |

**洞察**: Hilscher 是工业通信芯片领域的"隐形冠军"。其 netX 芯片的 FX 支持意味着**任何设备制造商**（无论规模大小）均可通过芯片升级获得 FX 能力，这是推动 FX 生态扩展的关键基础设施。[Hilscher netX TSN]

---

## 3. 关键趋势分析

### 3.1 C2C：全面量产

截至 2026 年中，所有主要厂商均已完成或即将完成 C2C 产品发布。C2C 周期要求宽松（10–100 ms），技术风险低，政治价值高（跨厂商互操作演示），因此成为首选落地场景。

### 3.2 C2D：分化期

- **已发布**: Beckhoff（CX TSN 网关）、B&R（ACOPOS M4 原生）
- **2026 试点**: Siemens（ET 200）、Rockwell（FLEXHA 5000）
- **规划中**: Phoenix Contact、Mitsubishi、Schneider

C2D 面临现有现场总线（EtherCAT、Profinet IRT）的强烈竞争，仅在绿地或特定升级场景中被采用。

### 3.3 D2D：早期阶段

尚无主流厂商宣布 D2D 量产产品。D2D 要求 Companion Specifications（运动控制、安全、IO）的成熟度和芯片级 UADP 协议栈优化，预计 2027–2028 年才有首批产品。

### 3.4 TSN：基础设施就绪

TSN 交换机（802.1Qbv/AS/CB 支持）在所有主要厂商中已可采购。瓶颈不在于硬件，而在于**GCL 配置工程**和**跨厂商配置互操作**。

---

## 4. 选型建议

| 场景 | 推荐厂商组合 | 理由 |
|------|-------------|------|
| **全西门子生态扩展** | Siemens S7-1500 TM + Scalance XCM | 原生融合 Profinet，工程工具统一 |
| **多厂商混合（欧美）** | Beckhoff CX + B&R X20 + Phoenix Contact PLCnext | 均支持原生 FX C2C，Berlin IOP 验证互通 |
| **运动控制优先** | B&R ACOPOS M4 + Beckhoff TwinCAT | ACOPOS M4 原生 C2D，TwinCAT 运动库成熟 |
| **北美存量升级** | Rockwell ControlLogix 5580 + Stratix | 固件升级保护现有投资 |
| **亚洲混合生态** | Mitsubishi iQ-R + Siemens S7-1500（网关） | CC-Link IE TSN 与 FX 通过网关共存 |
| **小型 OEM 快速 FX 化** | Hilscher netX 芯片 + 自研硬件 | 降低协议栈自研成本 |

---

## 5. 参考文献

1. [OPC Foundation] OPC Foundation Hannover Messe 2026 Booth Demos, https://opcfoundation.org/event-detail/hannover-messe/
2. [OPC Foundation] Berlin IOP 2026 Report (Beckhoff-hosted), February 2026
3. [IoT Digital Twin PLM] "OPC UA FX in 2026: Field-Level Communications Goes Open," May 2026, https://iotdigitaltwinplm.com/opc-ua-fx-field-level-communications-analysis-2026/
4. [Future Market Insights] "OPC UA FX Market Size, Share & Forecast to 2036," March 2026
5. [B&R] "ACOPOS M4 with OPC UA FX," SPS 2025, https://www.br-automation.com/en/technologies/opc-ua-fx/
6. [Siemens] S7-1500 TM NET Product Documentation, 2025
7. [Rockwell] ControlLogix 5580 Firmware Release Notes, Q1 2026
8. [Beckhoff] TwinCAT 3 OPC UA FX Function Documentation, TF6xxx, 2025
9. [Phoenix Contact] PLCnext Technology Portal, https://www.plcnext-community.net
10. [Hilscher] netX TSN Product Brief, 2024

---

> 最后更新: 2026-06-06
> 下次更新时机: SPS 2026（November）后更新 C2D 产品 GA 状态
