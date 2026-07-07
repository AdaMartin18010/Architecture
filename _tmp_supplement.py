#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对 02-business-architecture-reuse 下的五个核心文件进行深度补全。
不删除原有内容，仅在特定锚点前插入新增章节。
"""
import os

ROOT = os.path.abspath(os.path.dirname(__file__))


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def insert_before(text, marker, insertion):
    if marker not in text:
        raise ValueError(f"Marker not found: {marker[:80]}")
    return text.replace(marker, insertion + "\n\n" + marker, 1)


def insert_after(text, marker, insertion):
    if marker not in text:
        raise ValueError(f"Marker not found: {marker[:80]}")
    return text.replace(marker, marker + "\n\n" + insertion, 1)


# ============================================================
# 1. Zachman 复用性评估矩阵
# ============================================================

ZACHMAN_TOC_ADDITION = """    - [8. Zachman 复用性评估矩阵](#8-zachman-复用性评估矩阵)
      - [8.1 评估维度与量化模型](#81-评估维度与量化模型)
      - [8.2 六维度属性表](#82-六维度属性表)
      - [8.3 复用性评估决策树](#83-复用性评估决策树)
      - [8.4 行业案例](#84-行业案例)
    - [9. 反例与常见失败模式](#9-反例与常见失败模式)
    - [10. 与其他概念的关系](#10-与其他概念的关系)
    - [11. 权威来源与交叉引用](#11-权威来源与交叉引用)
"""

ZACHMAN_SECTION = """## 8. Zachman 复用性评估矩阵

### 8.1 评估维度与量化模型

**定义**：Zachman 复用性评估矩阵（Zachman Reusability Assessment Matrix, ZRAM）是基于 [Zachman Framework](https://en.wikipedia.org/wiki/Zachman_Framework) 的 6×6 单元结构，对每个架构描述单元（cell）中的复用资产从**稳定性、通用性、封装性、可组合性、可观测性、可治理性**六个维度进行量化评分的方法。

形式化：

```text
Reusability(cell) = Σ(wᵢ × scoreᵢ),  i ∈ {稳定性, 通用性, 封装性, 可组合性, 可观测性, 可治理性}

其中：
- scoreᵢ ∈ [0, 5]，由复用治理委员会评定
- wᵢ 为维度权重，默认各 1/6
- Reusability(cell) ∈ [0, 5]，≥4 视为"高复用性"，2-4 为"中复用性"，<2 为"低复用性"
```

### 8.2 六维度属性表

| 维度 | 说明 | 评分依据 | 重要性 |
|---|---|---|---|
| 稳定性 | 资产在过去 12-24 个月内的变更频率 | 变更次数越少得分越高 | 高 |
| 通用性 | 资产适用于 ≥2 个业务上下文的能力 | 适用场景越多得分越高 | 高 |
| 封装性 | 内部实现对使用者不可见的程度 | 接口契约清晰度、依赖隔离度 | 高 |
| 可组合性 | 与其他复用资产组合形成更大单元的难易度 | 接口标准化程度、文档完整性 | 高 |
| 可观测性 | 运行时行为与使用数据可被度量的程度 | 日志、指标、追踪覆盖度 | 中 |
| 可治理性 | 资产生命周期、版本、责任主体明确程度 | Owner、SLA、路线图完备度 | 中 |

### 8.3 复用性评估决策树

```mermaid
flowchart TD
    A[开始：评估复用资产] --> B{是否有明确的<br/>Zachman 坐标？}
    B -- 否 --> C[归入待分类资产<br/>需补全元数据]
    B -- 是 --> D{覆盖 Which 维度？}
    D -- What --> E[检查实体/功能/组件清单<br/>是否完整]
    D -- How --> F[检查流程/服务/代码<br/>使用指南是否清晰]
    D -- Where --> G[检查部署环境<br/>与多态变体]
    D -- Who --> H[检查 Owner 与<br/>治理主体]
    D -- When --> I[检查版本策略与<br/>生命周期]
    D -- Why --> J[检查战略/架构<br/>决策理由]
    E --> K{复用性评分 ≥ 4？}
    F --> K
    G --> K
    H --> K
    I --> K
    J --> K
    K -- 是 --> L[批准入库<br/>作为高复用性资产]
    K -- 否 --> M[有条件入库<br/>或返回改进]
```

**36 Cell 复用性分布规律**：

| 区域 | 典型 Cell | 复用性 | 原因 |
|---|---|---|---|
| 高复用区 | C2-1, C2-2, C2-6, C3-1, C3-2 | 4-5 | 业务对象、流程模板、服务契约抽象程度高、变更频率低 |
| 中复用区 | C3-3, C3-4, C3-5, C4-2, C4-3 | 2-4 | 部署拓扑、权限模型、调度策略与具体环境相关，需适配 |
| 低复用区 | C1-1~C1-6, C6-1~C6-6 | 1-2 | Scope 行过于抽象，Actual 行过于具体，通常不能直接复用 |

### 8.4 行业案例：三大行业的 Zachman 复用坐标

#### 银行业（基于 BIAN）

| Zachman Cell | 复用资产示例 | 复用价值 |
|---|---|---|
| C2-1 (What, Business) | Party / Customer / Account 业务对象 | 跨核心银行、CRM、渠道系统统一客户语义 |
| C2-2 (How, Business) | 开户、支付、贷款审批流程模板 | 加速新产品上市，降低合规成本 |
| C3-2 (How, System) | 标准化服务契约（OpenAPI） | 支持核心银行系统替换时的流程不变性 |
| C4-3 (Where, Technology) | 高可用部署拓扑模板 | 满足监管对灾备、RTO/RPO 的要求 |

#### 电信业（基于 TM Forum）

| Zachman Cell | 复用资产示例 | 复用价值 |
|---|---|---|
| C2-1 (What, Business) | Product / Service / Resource 业务实体 | 支撑 BSS/OSS 一体化 |
| C2-2 (How, Business) | 订单编排、服务保障流程 | 跨有线/无线/云业务复用 |
| C3-1 (What, System) | SID 数据模型 | 降低运营商系统集成成本 |
| C4-2 (How, Technology) | NFV MANO 组件模板 | 加速网络功能虚拟化部署 |

#### 制造业

| Zachman Cell | 复用资产示例 | 复用价值 |
|---|---|---|
| C2-1 (What, Business) | 物料清单（BOM）、产品配置器 | 支持按订单装配（ATO） |
| C2-2 (How, Business) | 订单到交付（OTD）流程模板 | 缩短供应链响应时间 |
| C4-2 (How, Technology) | 工业物联网边缘组件 | 跨工厂设备接入标准化 |
| C5-1 (What, Subcontractor) | OPC UA 数据契约 | 跨厂商设备互操作 |

---

## 9. 反例与常见失败模式

### 9.1 反例一：把 Zachman 当成方法论而非分类学

**场景**：某大型企业要求所有项目按照 Zachman 的 36 cell 顺序依次交付架构文档，导致在简单微服务改造项目中产生大量无价值的文档。

**问题**：
- Zachman 是**本体论分类框架（taxonomy）**，不是 ADM 式的方法论。
- 强制按 cell 顺序执行会制造流程官僚，而非架构价值。

**后果**：项目进度延迟 30%，开发团队对架构工作产生抵触，复用目录沦为"僵尸文档库"。

**避免建议**：
- 将 Zachman 用作**资产分类和盲区检查**工具，而非项目执行流程。
- 根据项目规模和风险选择性填充相关 cell。

### 9.2 反例二：跨抽象层次复用导致语义坍塌

**场景**：某银行将 C2-1（业务对象"客户"）直接映射为 C5-1（数据库表结构），省略了 C3-1（逻辑数据模型）和 C4-1（物理数据模型）。

**问题**：
- 业务对象的丰富语义（如法律关系、风险偏好、营销偏好）被压缩为几张数据库表。
- 当业务需求变化时，底层表结构被迫大改，影响所有依赖系统。

**后果**：核心系统改造周期从预计 6 个月延长至 18 个月，数据迁移成本超预算 200%。

**避免建议**：
- 坚持**纵向穿透链**完整性：C2-1 → C3-1 → C4-1 → C5-1。
- 每一层只向下层传递必要信息，保留本层的抽象语义。

### 9.3 反例三：为复用而复用——忽视 Why 维度

**场景**：某公司建立企业级组件库，强制所有团队复用通用"工作流引擎组件"，即使某些团队只需要简单的状态机。

**问题**：
- 缺少 C1-6/C2-6 的战略 Why 和业务 Why 论证。
- 组件与具体业务场景的匹配度低，引入不必要的复杂度。

**后果**：部分团队为规避强制复用，私下复制代码并改头换面，形成"影子组件库"，反而增加技术债务。

**避免建议**：
- 每个复用资产入库时必须提供**战略 Why + 架构 Why**。
- 允许团队在证明"替代方案总拥有成本更低"时申请豁免。

### 9.4 反例四：忽视 Where 维度导致"开发可用、生产不可用"

**场景**：某团队复用了 C4-2 的"缓存组件"，但未声明其仅适用于单数据中心部署。该组件被用于多区域部署后，出现跨区缓存一致性问题。

**问题**：
- 组件复用资产的 C4-3（Where）和 C4-6（Why）描述缺失。
- 复用者无法判断组件的运行环境约束。

**后果**：生产环境出现数据不一致，导致交易回滚和客户投诉。

**避免建议**：
- 将**部署拓扑约束**作为组件复用资产的强制元数据。
- 建立多态部署变体（云/本地/边缘）和兼容性矩阵。

---

## 10. 与其他概念的关系

### 10.1 与四层复用模型的关系
Zachman Framework 为四层复用模型（业务→应用→组件→功能）提供**元模型分类坐标**。四层复用模型回答"复用什么"，Zachman 回答"从哪些视角、在哪些抽象层描述复用资产"。

### 10.2 与 GERAM / ISO 15704 的关系
GERAM 是元-元框架，定义企业参考架构需要满足的需求；Zachman 是满足这些需求的一种具体分类学实现；四层复用模型则是在 Zachman 基础上的领域特化。

### 10.3 与 TOGAF / ArchiMate 的关系
TOGAF ADM 提供架构开发方法论，ArchiMate 提供建模语言，Zachman 提供分类框架。三者在复用治理中形成"方法-语言-分类"的互补。

### 10.4 与 BPMN / DMN 的关系
[BPMN](https://en.wikipedia.org/wiki/Business_process_modeling) 主要填充 Zachman 的 C2-2（How, Business）和 C3-2（How, System）；[DMN](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) 填充 C2-6（Why, Business）中可执行业务规则部分。二者共同支撑 How 和 Why 维度的复用。

---

## 11. 权威来源与交叉引用

### 11.1 权威来源

> **权威来源**:
>
> - [Zachman Framework - Wikipedia](https://en.wikipedia.org/wiki/Zachman_Framework) — 概述、历史、六视角六疑问词结构
> - [Zachman International 官方网站](https://www.zachman.com/) — 2020 扩展版与认证
> - [ISO 15704:2019 - GERAM](https://www.iso.org/standard/64207.html) — 企业参考架构方法论需求
> - [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74296.html) — 系统与软件工程架构描述
> - [Business process modeling - Wikipedia](https://en.wikipedia.org/wiki/Business_process_modeling) — 与 BPMN 的关联
>
> **核查日期**: 2026-07-07

### 11.2 交叉引用

- 本主题内：[BIAN 金融服务域复用案例](../case-studies/bian-banking-reuse-case.md) — 银行业的 Zachman 复用坐标实践
- 本主题内：[BPMN 2.0 / DMN 业务过程与决策的复用编排](../06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md) — 填充 Zachman How/Why 维度的可执行标准
- 本主题内：[业务能力复用](../02-business-capability/capability-reuse.md) — 业务复用层核心资产定义
- 上层标准：[FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射](../02-business-capability/fea-brm-togaf-mapping.md) — 业务能力框架映射
- 跨层治理：[复用成熟度模型](../06-cross-layer-governance/03-maturity-models/README.md) — Zachman 成熟度评估
- 元模型：[ISO/IEC/IEEE 42010:2022 对齐](../01-meta-model-standards/01-iso-420xx-family/README.md)

"""


# ============================================================
# 2. BPMN/DMN 复用编排
# ============================================================

BPMN_SECTION = """## 9. BPMN/DMN 复用编排模式

### 9.1 概念定义

**定义**：BPMN/DMN 复用编排（BPMN/DMN Reuse Orchestration）是指利用 BPMN 2.0 的流程可执行语义与 DMN 1.5 的决策服务语义，将稳定的过程结构、可变的决策规则与可复用的服务任务解耦，使流程模板、流程片段与决策服务能够在多个业务上下文、多个系统中重复组合与执行。

形式化：

```text
ReuseOrchestration := ⟨P, D, S, I, V⟩

P: 可复用流程模板集合（Process Templates）
D: 可复用决策服务集合（Decision Services）
S: 可复用服务任务集合（Service Tasks）
I: 流程-决策-服务之间的接口契约集合
V: 版本与兼容性规则集合
```

### 9.2 核心属性

| 属性 | 说明 | 重要性 |
|---|---|---|
| 结构稳定性 | 流程控制流（顺序、分支、并行）变更频率低 | 高 |
| 规则可变性 | 决策规则可独立于流程结构演进 | 高 |
| 服务可替换性 | 服务任务实现可替换，不影响流程定义 | 高 |
| 接口契约化 | 流程、决策、服务之间通过显式契约交互 | 高 |
| 版本兼容性 | 支持多版本流程/决策服务共存 | 中 |
| 执行可观测性 | 流程实例与决策执行可被追踪和审计 | 中 |

### 9.3 复用编排模式

#### 模式 1：流程模板库（Process Template Library）
将同类业务场景抽象为标准 [BPMN](https://en.wikipedia.org/wiki/Business_process_modeling) 模板，通过参数化适配不同上下文。

```mermaid
flowchart TB
    subgraph Library [流程模板库]
        A[审批类模板]
        B[订单类模板]
        C[客服类模板]
        D[AI 增强类模板]
    end
    subgraph Instance [上下文实例化]
        A --> A1[请假审批]
        A --> A2[费用报销]
        A --> A3[合同审批]
        B --> B1[电商订单]
        B --> B2[B2B 订单]
    end
```

#### 模式 2：调用活动跨流程复用（Call Activity Reuse）
独立部署的子流程被多个主流程调用，实现流程片段级复用。

```mermaid
flowchart LR
    P1[主流程：贷款申请] --> CA[[调用活动]]
    P2[主流程：信用卡申请] --> CA
    P3[主流程：开户申请] --> CA
    CA --> SP[子流程：信用评估]
    SP --> DS{DMN 决策服务}
```

#### 模式 3：决策服务复用（Decision-as-a-Service）
[DMN](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) 决策表封装为独立 REST/gRPC 服务，供多个流程和系统共享。

```mermaid
flowchart LR
    subgraph Clients [调用方]
        C1[BPMN 流程]
        C2[移动 App]
        C3[客服系统]
    end
    Clients --> DS[DMN 决策服务]
    DS --> DT1[定价决策表]
    DS --> DT2[信用评分表]
    DS --> DT3[合规检查表]
```

#### 模式 4：事件子流程横切关注点复用
将超时、异常、升级等横切关注点抽象为事件子流程，附加于任意主流程。

### 9.4 流程片段复用

流程片段（Process Fragment）是 BPMN 中可独立识别、命名和版本化的子结构，包括：
- **子流程（Subprocess）**：嵌入式或可调用的流程模块
- **调用活动（Call Activity）**：调用独立流程定义的复用机制
- **全局任务（Global Task）**：跨流程共享的人工任务定义

**流程片段复用的最佳实践**：
1. 识别高频出现的流程结构（如"审批"、"通知"、"支付"）
2. 将高频结构提取为独立子流程或调用活动
3. 定义清晰的输入/输出契约和数据对象
4. 通过语义化版本控制管理变更

### 9.5 决策服务复用

**决策服务复用的层次**：

| 层次 | 复用内容 | 典型示例 |
|---|---|---|
| 决策表结构 | 输入/输出变量、命中策略、规则骨架 | 信用评分表结构 |
| 业务知识模型 | 可跨决策复用的计算逻辑 | 客户终身价值计算 |
| 完整决策服务 | 已部署的 DMN 服务 | 利率定价服务 |

**决策服务复用的反模式警示**：
- 将业务流程条件直接硬编码在 DMN 中，导致决策服务知道过多流程上下文。
- 将 DMN 决策表作为通用规则引擎，执行非决策类逻辑（如数据转换）。

### 9.6 版本管理反例

**反例：无版本隔离的决策服务复用**

**场景**：某金融机构将"信用评分"DMN 决策服务部署为单一版本，供贷款审批、信用卡审批、保险核保三个业务线共享。当贷款业务要求调整评分规则时，直接修改了共享决策服务。

**问题**：
- 三个业务线共享同一决策服务版本，未建立多版本并存机制。
- 修改未进行影响分析，信用卡审批和保险核保的规则被意外改变。

**后果**：
- 信用卡审批通过率异常下降 12%，客户投诉增加。
- 保险核保出现风险漏判，导致后续赔付率上升。
- 回滚困难，因为无法区分三个业务线各自的规则历史版本。

**避免建议**：
- 对共享决策服务实施**语义化版本控制**（Semantic Versioning）。
- 采用**蓝绿部署**或**金丝雀发布**进行决策服务版本切换。
- 在 BPMN 流程中通过版本参数显式指定调用的 DMN 版本。
- 建立决策服务消费者影响分析（Consumer Impact Analysis）流程。

### 9.7 与其他概念的关系

- **与业务复用层的关系**：BPMN 流程模板是业务复用资产中"How"维度的主要载体。
- **与应用复用层的关系**：BPMN 服务任务调用应用层服务契约（OpenAPI/gRPC）。
- **与组件复用层的关系**：DMN 引擎、BPMN 引擎本身是技术组件复用对象。
- **与价值流的关系**：价值流定义"端到端价值创造"，BPMN 定义"价值流的可执行编排"。

### 9.8 权威来源与交叉引用

> **权威来源**:
>
> - [Business process modeling - Wikipedia](https://en.wikipedia.org/wiki/Business_process_modeling) — BPMN 在业务过程建模中的定位
> - [Decision Model and Notation - Wikipedia](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) — DMN 概述
> - [OMG BPMN 2.0.2 Specification](https://www.omg.org/spec/BPMN) — OMG 官方 BPMN 规范
> - [OMG DMN 1.5 Specification](https://www.omg.org/spec/DMN) — OMG 官方 DMN 规范
> - [ISO/IEC 19510:2013](https://www.iso.org/standard/62652.html) — BPMN 国际标准
>
> **核查日期**: 2026-07-07

**交叉引用**：
- [BPMN 2.0 / DMN 1.5 可执行语义案例集](./bpmn-dmn-executable-cases.md) — 具体可执行案例
- [BIAN 金融服务域复用案例](../case-studies/bian-banking-reuse-case.md) — BPMN/DMN 在金融场景的结合
- [业务能力复用](../02-business-capability/capability-reuse.md) — 业务复用层定义
- [价值流复用的形式化组合](../03-value-stream/value-stream-composition.md) — 端到端价值流与 BPMN 编排的关系

"""


# ============================================================
# 3. 业务能力复用
# ============================================================

CAPABILITY_SECTION = """## 6. 业务能力复用的形式化定义与属性

### 6.1 概念定义

**定义**：业务能力复用（Business Capability Reuse）是指将企业中**稳定、通用、可度量**的业务能力单元作为可复用资产，在多个业务线、产品、流程或系统中共享其定义、行为、数据契约和价值度量，从而避免重复建设、加速业务创新并降低架构复杂度的实践。

形式化：

```text
CapabilityReuse(C) := ⟨C, M(C), V(C), Gov(C)⟩

C: 业务能力单元
M(C): C 的成熟度模型（Level 1-5）
V(C): C 的价值度量集合（成本节约、上市时间、质量提升）
Gov(C): C 的治理主体、生命周期与版本策略
```

### 6.2 业务能力复用核心属性

| 属性 | 说明 | 可观察指标 | 重要性 |
|---|---|---|---|
| 稳定性 | 能力边界和核心语义随时间变化的程度 | 过去 24 个月结构性变更次数 | 高 |
| 通用性 | 能力在多个业务上下文中的适用程度 | 使用业务线/系统数量 | 高 |
| 原子性 | 能力粒度的适中性 | 能力分解到子能力的层级数 | 高 |
| 价值可度量性 | 能力成果可被量化评估的程度 | KPI 覆盖率、ROI 可追溯性 | 高 |
| 独立性 | 能力实现与组织结构、技术栈解耦程度 | 组织变更时的影响范围 | 中 |
| 可组合性 | 能力与其他能力组合形成价值流的能力 | 接口契约标准化程度 | 中 |

### 6.3 业务能力成熟度模型

| 成熟度等级 | 特征 | 复用表现 |
|---|---|---|
| L1 初始级 | 能力以职能或项目形式存在，无统一目录 | 复用靠个人关系，无治理 |
| L2 已管理级 | 部门级能力地图建立，但跨部门不一致 | 部门内复用，跨部门重复建设 |
| L3 已定义级 | 企业级统一能力地图，与价值流、IT 服务映射 | 跨部门复用，有标准接口 |
| L4 量化管理级 | 能力有明确 KPI、成本、质量度量 | 基于数据决策复用投资 |
| L5 优化级 | 能力持续演进，驱动业务创新 | 能力资产化，可对外输出 |

### 6.4 与 TOGAF / FEA BRM 的映射

| 框架 | 对应概念 | 映射说明 |
|---|---|---|
| TOGAF 10 | Business Capability / Organization Unit / Function | 业务能力映射到 TOGAF 内容元模型中的 Business Capability，组织单元映射到 Organization Unit，功能函数映射到 Function |
| TOGAF ABB/SBB | 业务能力为 ABB，具体 IT 实现为 SBB | 业务能力定义"做什么"，SBB 定义"怎么做" |
| FEA BRM 2.0 | Line of Business / Sub-function | FEA BRM 的业务线与子功能可映射为业务能力组（Level 1）和具体能力（Level 2-3） |
| ArchiMate 4 | Capability / Resource / Value | ArchiMate 的 Capability 与本概念等价，Resource 为能力实现，Value 为能力创造的价值 |

### 6.5 正例：跨国零售企业的能力复用

**背景**：某跨国零售企业在亚太、欧洲、北美三大区域运营，各区域独立建设"订单管理"系统，导致：
- 同一促销规则需在三个系统分别实现
- 客户体验不一致
- 系统集成成本高

**复用实践**：
1. 建立企业级"订单管理"业务能力（BC-SCM-005），定义统一的能力边界和成果。
2. 将"订单捕获"、"订单校验"、"库存预留"、"订单履约"等子能力标准化。
3. 各区域保留"区域税务计算"、"本地支付方式"等变体能力。
4. 统一能力通过 API 目录暴露给各区域系统。

**效果**：
- 新促销规则上线时间从 6 周缩短至 1 周
- 跨区域客户体验一致性评分提升 35%
- 订单相关 IT 维护成本降低 28%

### 6.6 反例：将组织职能直接建模为业务能力

**场景**：某公司将"市场部审批"、"财务部复核"、"法务部审核"直接建模为业务能力。

**问题**：
- 能力边界随组织架构调整而频繁变化。
- 当市场部拆分为"品牌市场"和"数字市场"后，原"市场部审批"能力失效。
- 能力复用性极低，因为每个能力都绑定了特定组织单元。

**后果**：
- 业务能力地图每半年需大规模重构
- 基于能力的 IT 规划无法稳定执行
- 团队对能力建模失去信心

**避免建议**：
- 业务能力命名应采用**动词+名词**（如"审批营销方案"），而非"部门+动作"。
- 能力定义应聚焦**业务成果**（outcome），而非执行主体。
- 组织角色应映射到能力的 Who 维度，而非能力本身。

### 6.7 与其他概念的关系

- **与价值流的关系**：价值流是业务能力的有序组合，业务能力复用是价值流复用的基础。
- **与业务流程的关系**：业务流程是能力的"时序化执行"，一个能力可由多个流程调用。
- **与业务服务的关系**：业务服务是能力的接口化封装，稳定的服务契约使能力复用跨越技术边界。
- **与应用架构的关系**：应用组件和微服务实现业务能力，通过服务契约向上暴露能力。
- **与 [Zachman Framework](https://en.wikipedia.org/wiki/Zachman_Framework) 的关系**：业务能力主要映射到 Zachman 的 C2-1（What, Business）和 C2-2（How, Business）。

### 6.8 权威来源与交叉引用

> **权威来源**:
>
> - [Business process modeling - Wikipedia](https://en.wikipedia.org/wiki/Business_process_modeling) — 业务过程建模与能力的关系
> - [Zachman Framework - Wikipedia](https://en.wikipedia.org/wiki/Zachman_Framework) — 企业架构分类框架
> - [The Open Group TOGAF Standard, 10th Edition](https://www.opengroup.org/togaf) — TOGAF 业务能力定义
> - [FEA BRM 2.0](https://www.whitehouse.gov/omb/management/federal-enterprise-architecture/) — 联邦企业架构业务参考模型
> - [ArchiMate 4 Specification](https://pubs.opengroup.org/architecture/archimate4-doc/) — ArchiMate 能力元模型
>
> **核查日期**: 2026-07-07

**交叉引用**：
- [FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射](./fea-brm-togaf-mapping.md) — 业务能力与标准框架的详细映射
- [价值流复用的形式化组合](../03-value-stream/value-stream-composition.md) — 能力如何组合为价值流
- [Zachman Framework 与软件架构复用映射](../08-zachman-reuse-mapping/zachman-reusability-matrix.md) — 能力在 Zachman 矩阵中的位置
- [BIAN 金融服务域复用案例](../case-studies/bian-banking-reuse-case.md) — 银行业能力复用实践

"""


# ============================================================
# 4. 价值流组合
# ============================================================

VALUESTREAM_SECTION = """## 7. 价值流组合模式与映射关系

### 7.1 概念定义

**定义**：价值流组合（Value Stream Composition）是指根据端到端价值交付目标，将一组业务能力按照特定的顺序、接口契约和变异规则进行编排，形成可在不同业务场景、产品线或组织中复用的价值交付模式。

形式化：

```text
ValueStreamComposition := ⟨VS, C, I, R, M⟩

VS: 目标价值流
C = {C₁, ..., Cₙ}: 组成价值流的业务能力集合
I = {I₁₂, ..., Iₙ₋₁ₙ}: 阶段间接口契约集合
R: 组合规则（顺序、并行、条件、循环）
M: 变性管理规则（适配、替换、扩展）
```

### 7.2 价值流复用核心属性

| 属性 | 说明 | 可观察指标 | 重要性 |
|---|---|---|---|
| 端到端完整性 | 价值流覆盖从触发到价值交付的全过程 | 首尾阶段是否对应价值主张 | 高 |
| 能力可替换性 | 单个阶段能力可被等效能力替换 | 接口契约稳定性 | 高 |
| 阶段可组合性 | 多个价值流可共享相同阶段 | 阶段复用次数 | 高 |
| 变性可控性 | 能适应不同场景的差异而不破坏主干 | 变体数量与管理成本比 | 中 |
| 价值可度量性 | 每个阶段和端到端价值可被度量 | KPI 定义覆盖率 | 高 |
| 可视化程度 | 价值流可被业务和技术人员共同理解 | 建模工具覆盖率 | 中 |

### 7.3 价值流组合模式

#### 模式 1：线性顺序组合
最基本的组合模式，阶段按严格顺序执行。

```mermaid
flowchart LR
    A[触发事件] --> S1[阶段1：能力 C1]
    S1 --> I1[接口 I12]
    I1 --> S2[阶段2：能力 C2]
    S2 --> I2[接口 I23]
    I2 --> S3[阶段3：能力 C3]
    S3 --> V[价值交付]
```

#### 模式 2：并行-汇聚组合
多个阶段可同时执行，全部完成后汇聚到下一阶段。

```mermaid
flowchart LR
    A[触发事件] --> S1[阶段1]
    S1 --> S2[阶段2a]
    S1 --> S3[阶段2b]
    S2 --> S4[汇聚阶段3]
    S3 --> S4
    S4 --> V[价值交付]
```

#### 模式 3：条件分支组合
根据阶段输出或外部条件选择不同路径。

#### 模式 4：可插拔阶段组合
主干价值流保持不变，某些阶段根据场景插入或跳过。

### 7.4 价值流与业务能力/业务流程的映射

| 概念 | 关注点 | 与价值流的关系 |
|---|---|---|
| 业务能力 | "能做什么" | 价值流的阶段由业务能力实现 |
| 业务流程 | "怎么做" | 业务流程是价值流中各阶段的执行细节 |
| 业务服务 | "如何调用" | 业务服务是能力与流程的接口化封装 |
| 价值主张 | "为何做" | 价值流的起点和终点由价值主张定义 |

**映射规则**：
1. 每个价值流阶段对应一个或多个业务能力。
2. 阶段间的接口契约由业务服务定义。
3. 业务流程负责将能力实例化为具体步骤。
4. 价值度量 KPI 贯穿价值流全过程。

### 7.5 正例：保险公司的理赔价值流复用

**背景**：某保险公司在财产险、健康险、车险三条产品线分别建设了理赔系统，流程差异大但核心价值创造路径相似。

**复用实践**：
1. 定义统一理赔价值流：报案 → 查勘 → 定损 → 核赔 → 赔付。
2. 将每条产品线特定的阶段抽象为"可插拔变体"：
   - 车险：查勘阶段包含现场查勘和远程视频查勘
   - 健康险：查勘阶段包含医疗费用审核
   - 财产险：定损阶段包含第三方评估
3. 统一接口契约（报案号、理赔状态、赔付金额）。
4. 建立价值流模板库，新产品线只需选择变体。

**效果**：
- 新产品理赔流程设计时间从 3 个月缩短至 3 周
- 理赔处理成本降低 22%
- 客户满意度提升 18%

### 7.6 反例：价值流与系统边界错位

**场景**：某电商公司将"订单到收款"价值流按现有系统边界切分为：前端系统负责"下单"、OMS 负责"订单处理"、WMS 负责"发货"、财务系统负责"开票收款"。

**问题**：
- 价值流在系统边界处断裂，每个系统只关注自己的"完成"。
- 客户退货时，需要在四个系统中分别操作，状态不一致。
- 端到端价值（客户满意、现金回笼）无人负责。

**后果**：
- 退货处理周期长达 7-10 天
- 客户投诉中 40% 与"状态不透明"相关
- 财务对账困难，应收账款账龄延长

**避免建议**：
- 价值流设计应**以价值交付为中心**，而非以系统边界为中心。
- 建立端到端价值流 Owner，跨越系统边界协调。
- 使用统一事件总线保持跨系统状态一致性。

### 7.7 与其他概念的关系

- **与业务能力的关系**：价值流是业务能力的有序组合，能力是价值流的"砖块"。
- **与 [BPMN](https://en.wikipedia.org/wiki/Business_process_modeling) 的关系**：BPMN 是价值流可执行编排的主要语言。
- **与 [DMN](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) 的关系**：DMN 定义价值流中条件分支和决策规则的逻辑。
- **与服务网格/编排的关系**：技术层面的服务编排实现价值流中的阶段调用。

### 7.8 权威来源与交叉引用

> **权威来源**:
>
> - [Value-stream mapping - Wikipedia](https://en.wikipedia.org/wiki/Value-stream_mapping) — 价值流图与精益思想
> - [Business process modeling - Wikipedia](https://en.wikipedia.org/wiki/Business_process_modeling) — 业务流程建模
> - [The Open Group TOGAF Series Guide: Value Streams](https://www.opengroup.org/togaf) — TOGAF 价值流指南
> - [SAFe Value Streams](https://scaledagileframework.com/value-streams/) — SAFe 价值流框架
>
> **核查日期**: 2026-07-07

**交叉引用**：
- [业务能力复用](../02-business-capability/capability-reuse.md) — 价值流组合的能力单元
- [BPMN 2.0 / DMN 业务过程与决策的复用编排](../06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md) — 价值流的可执行编排
- [Zachman Framework 与软件架构复用映射](../08-zachman-reuse-mapping/zachman-reusability-matrix.md) — 价值流在 Zachman Why/What/How 维度的映射
- [BIAN 金融服务域复用案例](../case-studies/bian-banking-reuse-case.md) — 金融服务价值流复用

"""


# ============================================================
# 5. BIAN 银行案例
# ============================================================

BIAN_TOC_ADDITION = """  - [8. BIAN 服务景观与复用边界](#8-bian-服务景观与复用边界)
    - [8.1 BIAN Service Landscape 的形式化定义](#81-bian-service-landscape-的形式化定义)
    - [8.2 BIAN 服务域核心属性](#82-bian-服务域核心属性)
    - [8.3 BIAN Service Landscape 12.0 结构图](#83-bian-service-landscape-120-结构图)
    - [8.4 复用边界](#84-复用边界)
    - [8.5 复用边界的决策树](#85-复用边界的决策树)
  - [9. 反例：BIAN 复用的常见失败模式](#9-反例bian-复用的常见失败模式)
  - [10. 与其他概念的关系](#10-与其他概念的关系)
  - [11. 权威来源与交叉引用更新](#11-权威来源与交叉引用更新)
"""

BIAN_DEFINITION_INSERT = """### 1.4 BIAN 服务域的复用定义

**定义**：BIAN 服务域复用（BIAN Service Domain Reuse）是指金融机构基于 BIAN Service Landscape 中标准化的服务域（Service Domain）、业务对象（Business Object）、行为（Behavior）和信息交换规范（Information Exchange），将银行业务能力封装为自治、可组合、可替换的架构资产，并在内部系统、合作伙伴生态和跨银行协作中重复使用的实践。

形式化：

```text
BIAN_Reuse := ⟨SD, BO, B, IX, Gov, Adapt⟩

SD: BIAN 服务域集合
BO: 业务对象模型集合
B: 行为定义集合
IX: 信息交换规范集合
Gov: 服务域治理与版本管理规则
Adapt: 本地化适配规则（监管、税务、渠道等）
```

"""

BIAN_SECTION = """## 8. BIAN 服务景观与复用边界

### 8.1 BIAN Service Landscape 的形式化定义

**定义**：BIAN Service Landscape（银行业服务景观）是 BIAN 组织维护的一套标准化银行业务能力参考模型，通过业务场景（Business Scenario）、业务领域（Business Area）、业务子领域（Sub-domain）、服务域（Service Domain）四级结构，将银行业务分解为 300+ 自治、可组合、可复用的服务域，每个服务域包含业务对象、行为、状态模型和标准化 API 接口。

形式化：

```text
BIAN_SL := ⟨BA, SD, BO, B, I, CP⟩

BA: 业务领域集合
SD: 服务域集合
BO: 业务对象集合
B: 行为集合
I: 信息交换规范集合
CP: 服务域协作模式集合
```

### 8.2 BIAN 服务域核心属性

| 属性 | 说明 | 可观察指标 | 重要性 |
|---|---|---|---|
| 自治性 | 服务域拥有独立业务目标和数据主权 | 外部依赖数量、数据共享范围 | 高 |
| 标准化接口 | 通过统一 API 规范对外服务 | OpenAPI 覆盖率、接口变更频率 | 高 |
| 业务聚焦 | 边界按业务能力划分，而非技术系统 | 是否包含非相关业务功能 | 高 |
| 可组合性 | 可与其他服务域编排成业务场景 | 被引用次数、协作模式数量 | 高 |
| 语义稳定性 | 业务对象和行为的定义长期稳定 | 版本变更中破坏性变更比例 | 高 |
| 实现无关性 | 规范独立于具体技术实现 | 是否规定特定数据库/中间件 | 中 |

### 8.3 BIAN Service Landscape 12.0 结构图

```mermaid
flowchart TB
    BS[业务场景<br/>Business Scenario] --> BA1[客户管理与支持]
    BS --> BA2[产品与服务管理]
    BS --> BA3[销售与分销]
    BS --> BA4[账户管理与交易处理]
    BS --> BA5[支付与清算]
    BS --> BA6[风险管理与合规]
    BS --> BA7[财务管理与报告]

    BA1 --> SD1[服务域：客户信息管理]
    BA1 --> SD2[服务域：客户关系管理]
    BA5 --> SD3[服务域：支付发起]
    BA5 --> SD4[服务域：支付执行]
    BA6 --> SD5[服务域：信用风险管理]

    SD1 --> BO1[业务对象：Customer Profile]
    SD1 --> BO2[业务对象：Customer Consent]
    SD4 --> BO3[业务对象：Payment Order]
    SD4 --> BO4[业务对象：Payment Execution]

    SD1 --> B1[行为：Create Customer Profile]
    SD1 --> B2[行为：Validate Customer Identity]
    SD4 --> B3[行为：Execute Payment]
    SD4 --> B4[行为：Track Payment Status]
```

### 8.4 复用边界

**应该复用的内容**：

| 边界内 | 说明 |
|---|---|
| 服务域规范 | 业务定义、边界、行为清单 |
| 业务对象模型 | 核心实体及其属性、关系 |
| 信息交换规范 | API 请求/响应结构、数据类型 |
| 协作模式 | 服务域之间的标准交互模式 |
| 参考实现 | 经社区验证的开源参考代码 |

**不应该强制复用的内容**：

| 边界外 | 说明 |
|---|---|
| 具体技术栈 | 服务域不强制 Java/.NET/特定数据库 |
| 本地化规则 | 各国监管、税务、合规变体 |
| 非功能性配置 | 性能参数、部署拓扑、容量规划 |
| 遗留系统封装细节 | 适配器实现因银行而异 |
| 用户界面 | 渠道特定的 UI/UX |

### 8.5 复用边界的决策树

```mermaid
flowchart TD
    A[评估潜在复用内容] --> B{是否在 BIAN 服务域规范中?}
    B -- 是 --> C{是否与技术实现无关?}
    B -- 否 --> D[不建议作为 BIAN 资产复用]
    C -- 是 --> E[适合跨银行/跨系统复用]
    C -- 否 --> F{是否可通过参数化适配?}
    F -- 是 --> G[作为可配置复用资产]
    F -- 否 --> H[作为本地扩展，不归入核心复用资产]
```

---

## 9. 反例：BIAN 复用的常见失败模式

### 9.1 反例一：机械照搬 BIAN 服务域，忽视遗留系统现实

**场景**：某中型银行决定全面采用 BIAN，要求所有新系统严格按照 BIAN 服务域拆分，并计划两年内替换核心银行系统。

**问题**：
- 忽视遗留核心系统的复杂性和数据耦合。
- 服务域拆分过细，导致大量分布式事务和集成点。
- 团队对 BIAN 理解不足，将"服务域"简单等同于"微服务"。

**后果**：
- 项目延期 18 个月，预算超支 160%。
- 数据一致性问题和性能问题频发。
- 部分服务域因过度拆分而难以独立交付价值。

**避免建议**：
- 采用**渐进式对齐**策略，先对新增业务能力采用 BIAN，遗留系统通过 facade 模式渐进暴露 BIAN 接口。
- 服务域不等于微服务，一个微服务可实现多个服务域，一个服务域也可由多个微服务实现。

### 9.2 反例二：忽视本地监管变体，强制全球统一接口

**场景**：某全球银行集团要求所有区域使用完全一致的"客户信息管理"API，包括数据字段和验证规则。

**问题**：
- 不同国家/地区对 KYC、数据隐私、身份证件类型的要求不同。
- 强制统一导致各地系统在 API 之上增加大量"变通层"。
- 原本的标准化接口反而增加了系统复杂度。

**后果**：
- 区域系统交付周期延长。
- API 变通层造成数据质量和审计追踪问题。
- 集团无法准确掌握各区域实际数据模型。

**避免建议**：
- 区分**核心标准数据元素**和**本地扩展数据元素**。
- 在信息交换规范中明确定义扩展点（extension points）和本地化适配机制。

### 9.3 反例三：复用接口但语义不一致

**场景**：两家银行都采用 BIAN "Payment Order" 业务对象，但一家将"收款人"定义为账户持有人，另一家定义为实际受益人。

**问题**：
- 虽然 API 字段名称相同，但业务语义存在细微差异。
- 在跨银行集成时，资金被错误路由。

**后果**：
- 跨境支付测试阶段发现错误，险些造成资金损失。
- 两家银行被迫进行昂贵的接口重新映射。

**避免建议**：
- 复用 BIAN 规范时，必须进行**语义对齐验证**。
- 建立业务术语表（Business Glossary）和数据血统（Data Lineage）治理。
- 在集成测试中增加语义断言，而非仅验证字段格式。

### 9.4 反例四：只复用规范不复用治理

**场景**：某银行引入 BIAN 服务域目录，但未建立相应的服务域 Owner、版本管理和变更影响分析流程。

**问题**：
- 多个团队随意修改"共享"服务域接口。
- 版本管理混乱，消费者无法及时了解变更。
- 服务域之间的协作关系无人维护。

**后果**：
- 接口频繁破坏性变更，下游系统反复返工。
- 团队开始绕过标准接口直接访问数据库。
- BIAN 复用计划名存实亡。

**避免建议**：
- 建立**服务域 Owner 制度**，每个服务域有明确的业务和技术负责人。
- 实施语义化版本控制和消费者影响分析。
- 将 BIAN 规范纳入架构评审和质量门禁。

---

## 10. 与其他概念的关系

### 10.1 与业务能力的关系
BIAN 服务域是银行业务能力的标准化表达，可映射到通用业务能力模型。参见 [业务能力复用](../02-business-capability/capability-reuse.md)。

### 10.2 与 TOGAF/FEA 的关系
BIAN 提供银行业特定的 ABB（架构构建块），TOGAF 提供 ABB 的管理方法论，FEA BRM 提供跨行业业务能力分类参考。详细映射见 [FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射](../02-business-capability/fea-brm-togaf-mapping.md)。

### 10.3 与 BPMN/DMN 的关系
BIAN 定义"做什么"（服务域和能力），[BPMN](https://en.wikipedia.org/wiki/Business_process_modeling) 定义"怎么做"（流程编排），[DMN](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) 定义"怎么决定"（业务规则）。

### 10.4 与 ISO 20022 的关系
BIAN 业务对象与 [ISO 20022](https://en.wikipedia.org/wiki/ISO_20022) 报文元素存在映射，共同支撑金融报文互操作。

### 10.5 与 Zachman 的关系
BIAN 服务域可映射到 Zachman 矩阵的 C2-1（What, Business）、C2-2（How, Business）和 C3-2（How, System）等 cell。参见 [Zachman Framework 与软件架构复用映射](../08-zachman-reuse-mapping/zachman-reusability-matrix.md)。

---

## 11. 权威来源与交叉引用更新

### 11.1 新增权威来源

> **权威来源**:
>
> - [Banking Industry Architecture Network - Wikipedia](https://en.wikipedia.org/wiki/Banking_Industry_Architecture_Network) — BIAN 组织概述
> - [ISO 20022 - Wikipedia](https://en.wikipedia.org/wiki/ISO_20022) — 金融报文标准
> - [Business process modeling - Wikipedia](https://en.wikipedia.org/wiki/Business_process_modeling) — BPMN 关联
> - [Decision Model and Notation - Wikipedia](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) — DMN 关联
> - [BIAN 官方网站](https://bian.org/) — Service Landscape 12.0 与服务域规范
> - [The Open Group TOGAF](https://www.opengroup.org/togaf) — 架构开发方法
> - [FEA Framework](https://www.whitehouse.gov/omb/management/federal-enterprise-architecture/) — 联邦企业架构框架
>
> **核查日期**: 2026-07-07

### 11.2 交叉引用

- [Zachman Framework 与软件架构复用映射](../08-zachman-reuse-mapping/zachman-reusability-matrix.md) — BIAN 服务域在 Zachman 矩阵中的坐标
- [BPMN 2.0 / DMN 业务过程与决策的复用编排](../06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md) — BIAN 与 BPMN/DMN 的结合
- [业务能力复用](../02-business-capability/capability-reuse.md) — 服务域作为银行业务能力单元
- [价值流复用的形式化组合](../03-value-stream/value-stream-composition.md) — 金融服务价值流组合
- [FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射](../02-business-capability/fea-brm-togaf-mapping.md) — BIAN 与 FEA/TOGAF 的映射基础

"""


def main():
    files = {
        "zachman": "struct/02-business-architecture-reuse/08-zachman-reuse-mapping/zachman-reusability-matrix.md",
        "bpmn": "struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md",
        "capability": "struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md",
        "valuestream": "struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md",
        "bian": "struct/02-business-architecture-reuse/case-studies/bian-banking-reuse-case.md",
    }

    # 1. Zachman
    path = os.path.join(ROOT, files["zachman"])
    text = read(path)
    # 更新 TOC：在第 7 章后面追加新增章节
    text = text.replace("    - [7. 权威来源与参考文献](#7-权威来源与参考文献)\n", "    - [7. 权威来源与参考文献](#7-权威来源与参考文献)\n" + ZACHMAN_TOC_ADDITION)
    text = insert_before(text, "## 7. 权威来源与参考文献", ZACHMAN_SECTION)
    write(path, text)
    print(f"Updated: {files['zachman']}")

    # 2. BPMN
    path = os.path.join(ROOT, files["bpmn"])
    text = read(path)
    text = insert_before(text, "## 补充说明：BPMN 2.0 / DMN 业务过程与决策的复用编排", BPMN_SECTION)
    write(path, text)
    print(f"Updated: {files['bpmn']}")

    # 3. Capability
    path = os.path.join(ROOT, files["capability"])
    text = read(path)
    text = insert_before(text, "## 补充说明：业务能力复用", CAPABILITY_SECTION)
    write(path, text)
    print(f"Updated: {files['capability']}")

    # 4. Value Stream
    path = os.path.join(ROOT, files["valuestream"])
    text = read(path)
    text = insert_before(text, "## 补充说明：价值流复用的形式化组合", VALUESTREAM_SECTION)
    write(path, text)
    print(f"Updated: {files['valuestream']}")

    # 5. BIAN
    path = os.path.join(ROOT, files["bian"])
    text = read(path)
    # 在 1.3 后面插入定义
    text = text.replace("### 1.3 300+ 服务域的精确分类\n", "### 1.3 300+ 服务域的精确分类\n\n" + BIAN_DEFINITION_INSERT)
    # 更新 TOC
    text = text.replace("  - [7. 实施建议与路线图](#7-实施建议与路线图)\n", "  - [7. 实施建议与路线图](#7-实施建议与路线图)\n" + BIAN_TOC_ADDITION)
    # 在附录前插入
    text = insert_before(text, "## 附录：权威来源", BIAN_SECTION)
    write(path, text)
    print(f"Updated: {files['bian']}")


if __name__ == "__main__":
    main()
