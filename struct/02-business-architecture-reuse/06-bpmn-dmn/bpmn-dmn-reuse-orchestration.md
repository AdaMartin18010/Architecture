# BPMN 2.0 / DMN 业务过程与决策的复用编排
>
> 版本: 2026-06-06
> 对齐来源: OMG BPMN 2.0.2 / DMN 1.5, ISO/IEC 19510:2013, Camunda 2024, Signavio/SAP, 澳大利亚 NSW 交通标准

## 1. 标准体系

| 标准 | 版本状态 | 标准化机构 | 关键特征 |
|-----|---------|-----------|---------|
| **BPMN** | 2.0.2 (2014) | OMG / ISO/IEC 19510:2013 | 人读 + 机执行的双重语义 |
| **DMN** | 1.5 (2024) | OMG | 决策需求图 + 决策表 + FEEL 表达式 |
| **CMMN** | 1.1 | OMG | 案例管理（非结构化流程）|

## 2. BPMN 作为复用载体的独特价值

### 2.1 双重语义

> "A BPMN diagram is simultaneously a visual that any stakeholder can read and an XML specification that an orchestration engine can run."

- **人读**：业务流程图让所有利益相关者理解流程
- **机执行**：BPMN 2.0 XML 可被流程引擎直接执行
- **结果**：业务批准的流程与生产运行的流程完全一致

### 2.2 与 AI 智能体时代的契合

BPMN 在 AI 时代的价值不降反升：

- **确定性骨架**：为非确定性 AI 智能体提供编排、升级、审批、审计的确定性框架
- **Agent 治理**：BPMN 将智能体视为普通参与者（服务、人员、系统），由流程决定何时调用、结果如何处理
- **可审计性**：每一步（无论由代码、智能体或人执行）进入同一审计轨迹

### 2.3 与专有方案的对比

| 维度 | BPMN (开放标准) | 专有低代码 | 纯代码编排器 |
|-----|---------------|-----------|------------|
| 开放标准 | ISO/IEC 19510, OMG 维护 | 厂商私有 | 无，仅代码构造 |
| 业务可读性 | 原生设计 | 受限于厂商 UI | 无，逻辑在代码中 |
| 工具/人才可移植性 | 100+ 工具支持 | 锁定厂商 | 锁定引擎 SDK |
| 人工任务支持 | User Task 为一等公民 | 套件内支持 | 需从零构建 |
| 智能体治理 | 外部+内部（ad-hoc subprocess）| 仅外部 | 仅外部 |
| 审计轨迹 | 自动记录，无需额外插桩 | 套件内；跨系统脆弱 | 仅日志，无端到端视图 |

## 3. BPMN 核心元素族

| 元素族 | 代表元素 | 复用场景 |
|-------|---------|---------|
| **事件（Events）** | Start, End, Timer, Message, Error, Boundary | 流程触发器、超时处理、异常恢复 |
| **任务（Tasks）** | User Task, Service Task, Business Rule Task, Script Task | 人工审批、API 调用、DMN 决策、脚本执行 |
| **网关（Gateways）** | Exclusive, Parallel, Inclusive, Event-based | 条件分支、并行处理、事件等待 |
| **子流程（Subprocesses）** | Embedded, Call Activity, Ad-hoc | 流程模块化、跨流程复用、非结构化 AI Agent 步骤 |
| **边界事件（Boundary Events）** | Timer, Error, Escalation | 步骤级超时、错误捕获、升级处理 |
| **消息流（Message Flows）** | Pool-to-Pool 虚线箭头 | 跨组织/跨系统/跨智能体通信 |

## 4. DMN 决策复用

### 4.1 三层结构

```text
Decision Requirements Diagram (DRD)
├── Decisions（决策节点）
├── Input Data（输入数据）
├── Business Knowledge Models（业务知识模型）
└── Knowledge Sources（知识来源）

Decision Table（决策表）
├── Inputs（条件列）
├── Outputs（结果列）
└── Rules（规则行）

FEEL Expressions（Friendly Enough Expression Language）
└── 上下文中的表达式计算
```

### 4.2 决策即服务（Decision-as-a-Service）

- DMN 决策表可独立于 BPMN 流程部署为可复用服务
- 多个流程共享同一决策逻辑（如信用评分、定价策略、合规检查）
- 决策变更无需修改调用流程，只需更新决策服务版本

### 4.3 与 BPMN 的集成

```text
BPMN Process
├── Business Rule Task
│   └── 调用 DMN Decision Service
└── 根据决策结果路由流程分支
```

## 5. 业务过程分层复用模型

参考澳大利亚 NSW 交通标准实践：

| 层级 | 内容 | 表示法 | 复用粒度 |
|-----|------|--------|---------|
| **Layer 1–3** | 企业地图与价值链 | 上下文/概念/逻辑功能 | 能力域 |
| **Layer 4** | 可执行工作流模型 | BPMN | 流程模板 |
| **Layer 5** | 可执行决策模型 | DMN | 决策服务 |

## 6. 过程资产复用模式

### 6.1 流程模板库

```text
Process Template Library
├── 审批类
│   ├── 请假审批（User Task → Manager Approval → HR Record）
│   ├── 费用报销（OCR → 规则校验 → 多级审批 → 支付）
│   └── 合同审批（Legal Review → Finance Review → Signature）
├── 订单类
│   ├── 电商订单（Create → Payment → Fulfillment → Delivery）
│   └── B2B 订单（Credit Check → Inventory Reserve → Shipping）
├── 客服类
│   ├── 投诉处理（Intake → Categorize → Resolve → Close）
│   └── 退换货（Return Request → Inspection → Refund/Exchange）
└── AI 增强类
    ├── RAG 查询流程（Retrieve → Generate → Human Review → Publish）
    └── 智能体协作（Orchestrator → Agent A → Agent B → Consolidate）
```

### 6.2 Call Activity 跨流程复用

- **定义**：在一个流程中调用另一个独立部署的流程
- **优势**：被调用流程更新不影响调用方定义；多个调用方共享同一子流程
- **典型用例**：通用审批子流程、支付子流程、通知子流程

### 6.3 事件子流程（Event Subprocess）复用

- 定义全局异常处理模式（如超时、升级、补偿）
- 附加于任何流程或子流程，实现横切关注点复用

## 7. 与 CMMN 的互补

| 场景 | BPMN | CMMN |
|-----|------|------|
| 结构化流程 | ✅ 完美适配 | ❌ 过度约束 |
| 知识工作者驱动 | ❌ 难以建模 | ✅ 案例文件 + 自由启动计划项 |
| 规则/事件复杂交织 | 流程图臃肿 | 案例模型清晰 |
| AI Agent 自主决策 | Ad-hoc Subprocess 有限 | 案例目标驱动更适合 |

## 8. 参考索引

- OMG BPMN 2.0.2 Specification
- OMG DMN 1.5 Specification
- ISO/IEC 19510:2013 — BPMN 标准
- Camunda: "BPMN: The open standard for process and agentic orchestration"
- SAP Signavio: BPMN 2.0 for Efficient Process Design
- Australia NSW Transport Standards: BPMN / DMN Layered Approach
- Freund & Rücker: "Practical Process Automation" (O'Reilly)


---

## 补充说明：BPMN 2.0 / DMN 业务过程与决策的复用编排

## 示例

**示例**：信贷审批流程使用 BPMN 定义审批步骤，使用 DMN 决策表管理利率、额度规则，业务人员可直接调整规则而无需修改流程代码。

## 反例

**反例**：将业务规则硬编码在 BPMN 网关条件中，导致规则变更需要重新部署流程，业务人员无法参与。

## 权威来源

> **权威来源**:
>
> - [OMG BPMN](https://www.omg.org/spec/BPMN)
> - [OMG DMN](https://www.omg.org/spec/DMN)
> - 核查日期：2026-07-07

## 分析

**分析**：BPMN/DMN 的分离使流程结构稳定、规则灵活，是业务-IT 对齐的关键实践。
