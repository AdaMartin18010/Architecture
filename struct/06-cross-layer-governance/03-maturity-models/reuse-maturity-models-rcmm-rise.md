# 软件复用成熟度模型：RCMM、RiSE-RM 与行业映射
>
> 版本: 2026-06-06
> 对齐来源: CMMI (ISACA), RCMM (Jasmine & Vasantla), RiSE-RM (Garcia 2010), Automotive SPICE, Koltun & Hudson (1991)

## 1. 复用成熟度模型谱系

| 模型 | 层级数 | 焦点 | 来源 |
|-----|--------|------|------|
| **CMM / CMMI-DEV** | 5 | 通用软件开发过程 | SEI / ISACA |
| **RCMM** | 5 | 复用导向软件开发 | Jasmine & Vasantla |
| **RiSE-RM** | 7 | 系统化复用采用 | RiSE Labs / Garcia (2010) |
| **Koltun & Hudson** | 5 | 组织 mindset 层面复用 | 1991 |
| **Automotive SPICE** | 6 | 汽车行业过程评估 | VDA QMC |
| **Koltun-Hudson 软件复用** | 5 | 代码/组件/应用/系统复用 | 1991 |

## 2. CMMI 与复用

### 2.1 CMMI 核心信息

- **当前管理方**：ISACA（2016 年从 CMU/SEI 接管）
- **定位**：结果导向的性能改进模型，与 Agile、SAFe、DevSecOps 集成
- **量化收益**（ISACA 数据）：
  - 缺陷减少 30%
  - 开发生产率提升 15%
  - 交付时间偏差减少 43%
  - 客户满意度提升 13%
  - 成本偏差减少 47%

### 2.2 CMMI 成熟度等级

| 等级 | 名称 | 复用含义 |
|-----|------|---------|
| 1 | 初始 | 复用偶然发生，依赖个人英雄主义 |
| 2 | 已管理 | 项目级复用跟踪，基本的配置管理 |
| 3 | 已定义 | 组织级复用过程标准化，领域工程启动 |
| 4 | 量化管理 | 复用率、质量、成本度量驱动决策 |
| 5 | 优化 | 持续过程改进，创新复用技术引入 |

## 3. RCMM（Reuse Capability Maturity Model）

### 3.1 五级定义

| 等级 | 名称 | 特征 | 关键实践 |
|-----|------|------|---------|
| **1** | 初始复用 | 个人级、无计划、临时复制粘贴 | 无 |
| **2** | 可重复复用 | 项目内识别可复用组件；基本的版本控制 | 组件目录、编码标准 |
| **3** | 已定义复用 | 组织级复用过程；领域分析；组件库 | 复用计划、领域工程、质量门 |
| **4** | 已管理复用 | 量化复用指标；投资回报跟踪；供应商管理 | 复用度量、成本模型、资产质量管理 |
| **5** | 优化复用 | 持续改进复用过程；创新技术；跨组织复用 | 基准比较、技术雷达、复用文化 |

### 3.2 与 CMMI 的映射

RCMM 直接基于 CMMI 框架，但增加复用特定过程域：

- **复用计划（Reuse Planning）**
- **资产管理（Asset Management）**
- **领域工程（Domain Engineering）**
- **复用度量（Reuse Measurement）**

## 4. RiSE Reference Model（RiSE-RM）

### 4.1 七级定义

由 RiSE Labs（巴西）通过工业实践与专家验证提出：

| 等级 | 名称 | 核心特征 |
|-----|------|---------|
| **1** | Informal Reuse | 非正式复用；复制粘贴；无管理 |
| **2** | Basic Reuse | 基本复用；识别常见功能；简单库 |
| **3** | Planned Reuse | 计划复用；领域分析；可复用组件设计 |
| **4** | Managed Reuse | 管理复用；组件库管理；版本控制；质量评估 |
| **5** | Family-Oriented Products Reuse | 产品线复用；核心资产库；变体管理 |
| **6** | Measured Reuse | 度量复用；量化指标；ROI 跟踪；过程优化 |
| **7** | Proactive Reuse | 主动复用；预测需求；战略资产投资；跨组织生态 |

### 4.2 过程域结构

RiSE-RM 包含以下过程域（Process Areas）：

- 复用战略与规划
- 领域工程
- 应用工程
- 资产管理
- 变型管理
- 组织培训与推广
- 度量与分析
- 过程质量保证

## 5. Koltun & Hudson 复用框架（1991）

### 5.1 组织 Mindset 层面

| 层级 | 名称 | 描述 |
|-----|------|------|
| **0** | No Reusability | 复制粘贴；所有实例手动更新 |
| **1** | Object & Function Reuse | 小规模单一对象或函数复用 |
| **2** | Component Reuse | 子系统到单个对象的组件复用 |
| **3** | Application Reuse | 完整应用复用；应用家族 |
| **4** | System Reuse | 完整系统复用；多应用组合 |

### 5.2 与 RCMM/RiSE 的关系

Koltun-Hudson 框架侧重于**技术复用粒度**，而 RCMM/RiSE 侧重于**组织过程成熟度**。两者互补：

- Koltun-Hudson 回答"复用什么"
- RCMM/RiSE 回答"如何系统化地复用"

## 6. 汽车行业：Automotive SPICE

### 6.1 与复用的关联

- **SUP.1: Quality Assurance** — 复用资产的质量保证
- **SUP.8: Configuration Management** — 复用组件的版本与变体管理
- **SUP.9: Problem Resolution Management** — 复用组件缺陷的跨项目影响分析
- **SYS.3 / SWE.2: Architectural Design** — 软件产品线架构设计
- **REU: Reuse Management** (特定扩展) — 复用工程管理

### 6.2 ASPICE 与 ISO 26262 的交叉

- ASPICE 过程能力等级与 ISO 26262 ASIL 等级共同决定复用证据的充分性
- SEooC 开发需同时满足 ASPICE Level 3+ 和对应 ASIL 的过程要求

## 7. 成熟度评估问卷设计原则

### 7.1 维度设计

| 维度 | 权重 | 评估要点 |
|-----|------|---------|
| **战略与治理** | 15% | 复用战略、预算、治理委员会 |
| **过程与方法** | 20% | 领域工程、应用工程、变体管理 |
| **资产与基础设施** | 20% | 资产库、搜索、质量门、SBOM |
| **度量与激励** | 15% | 复用率、成本节约、开发者激励 |
| **文化与技能** | 15% | 培训、社区、Golden Path 采用率 |
| **工具与自动化** | 15% | CI/CD 集成、SCA、SBOM、平台工程 |

### 7.2 评估方法

- **自评估**：在线问卷，快速定位
- **第三方评估**：类似 CMMI Appraisal，由授权评估师执行
- **持续监控**：平台工程工具自动收集度量数据

## 8. 参考索引

- ISACA: CMMI Performance Solutions (2026)
- Jasmine & Vasantla: Reuse Capability Maturity Model (RCMM)
- Garcia (2010): RiSE Reference Model (RiSE-RM)
- Koltun & Hudson (1991): Software Reuse Maturity Framework
- VDA QMC: Automotive SPICE v4.0
- Frakes & Terry (1996): Software Reuse: Metrics and Models
- Lim (1998): Managing Software Reuse
- Schweigert et al.: Maturity models for agile development assessment


---

## 补充说明：软件复用成熟度模型：RCMM、RiSE-RM 与行业映射

## 示例

**示例**：组织采用 NASA RRL 评估可复用资产，从 RRL 1（概念）到 RRL 9（已在多任务中验证），决定是否将资产推广到全组织。

## 反例

**反例**：未评估成熟度便将实验室原型直接作为组织级资产推广，导致生产环境中出现严重缺陷。

## 权威来源

> **权威来源**:
>
> - [NASA RRL](https://www.nasa.gov)
> - [ISO/IEC 26566:2026](https://www.iso.org)
> - 核查日期：2026-07-07

## 分析

**分析**：成熟度模型将复用能力量化，为投资优先级与改进路径提供依据。
