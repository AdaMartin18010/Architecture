# BDI 智能体架构与复用模式
>
> 版本: 2026-06-06
> 对齐来源: Rao & Georgeff (1995), FIPA 规范, JACK/dMARS/PRS 工业系统, 俄罗斯科学院 SFedU 研究, arXiv 智能体语义迁移论文

## 1. BDI 理论基础

### 1.1 心智状态三元组

BDI（Belief-Desire-Intention）理论由 Rao & Georgeff (1995) 提出，基于 Bratman 的哲学行动理论：

| 元素 | 定义 | 在软件中的映射 |
|-----|------|--------------|
| **信念（Belief）** | 智能体对世界状态的认知 | 知识库、传感器输入、内部状态 |
| **愿望（Desire）** | 智能体希望达到的目标状态 | 目标集合、偏好、效用函数 |
| **意图（Intention）** | 智能体承诺执行的行动计划 | 当前执行计划、承诺栈 |

### 1.2 实用推理（Practical Reasoning）

```
信念更新（Belief Revision）
    ↓
愿望生成（Option Generation）
    ↓
过滤（Filtering）→ 意图集合
    ↓
行动计划（Means-End Reasoning）
    ↓
执行与监控（Action Execution & Monitoring）
```

## 2. BDI 架构实现谱系

### 2.1 历史系统

| 系统 | 类型 | 应用领域 |
|-----|------|---------|
| **PRS**（Procedural Reasoning System）| 研究原型 | 航天器控制、机器人 |
| **dMARS**（distributed MARS）| 分布式推理 | 多智能体仿真 |
| **JACK** | 商业平台（AOS Group）| 工业控制、仿真、游戏 |
| **Jason** | 开源解释器 | 教学与研究 |
| **Jadex** | 开源 BDI 框架 | 分布式系统 |

### 2.2 核心特征

- **意图作为承诺**：区别于简单目标栈，意图包含对资源的承诺和时间约束
- **计划库（Plan Library）**：预定义的计划模板，可参数化复用
- **事件驱动**：外部事件触发信念更新，进而触发意图重新评估

## 3. 计划库复用模式

### 3.1 计划作为可复用资产

```
Plan Library
├── Generic Plans（通用计划）
│   ├── move-to-location(X, Y)
│   ├── communicate(message, recipient)
│   └── wait-for-condition(predicate)
├── Domain Plans（领域计划）
│   ├── manufacturing/execute-work-order(order)
│   ├── logistics/optimize-route(waypoints)
│   └── healthcare/patient-monitoring(protocol)
└── Meta Plans（元计划）
    ├── replan-on-failure()
    └── delegate-task(task, agent-pool)
```

### 3.2 复用机制

| 机制 | 描述 |
|-----|------|
| **计划继承** | 子计划继承父计划的触发条件与前提 |
| **计划组合** | 将原子计划组合为复合计划 |
| **参数化实例化** | 同一计划模板用于不同实体 |
| **上下文激活** | 基于当前信念状态动态选择计划 |

## 4. 多智能体 BDI 扩展

### 4.1 协作与协调

- **共享意图（Joint Intention）**：团队级承诺，个体意图需与团队意图一致
- **社会承诺（Social Commitment）**：智能体间的契约式协作
- **对话协议**：通过言语行为（Speech Acts）协商计划分配

### 4.2 BDI 与 FIPA ACL

第一代多智能体系统（1995–2005）以 FIPA 平台为中心：

- **FIPA ACL**：基于言语行为的通信语言
- **目录服务（Directory Facilitator）**：智能体发现与注册
- **局限**：与开放 Web 的基底不匹配，未能在开放互联网规模普及

## 5. 从 BDI 到 Agentic AI 的语义迁移

### 5.1 三代智能体语义演进

| 世代 | 时间 | 焦点 | 关键技术 | 语义位置 |
|-----|------|------|---------|---------|
| **Generation I** | 1995–2005 | 平台 | FIPA ACL, BDI, JADE, DF | **平台中的语义** |
| **Generation II** | 2001–2012 | 数据 | RDF, OWL, SPARQL, DBpedia | **数据中的语义** |
| **Generation III** | 2020s– | 模型 | Transformer, LLMs, MCP, A2A | **模型中的语义** |

### 5.2 每代权衡

- **Gen I（平台）**：强有状态协调，但与开放 Web 基底不匹配
- **Gen II（数据）**：高可验证性，但标注脆弱且经济不可持续
- **Gen III（模型）**：灵活零标注语义，但**可验证性丧失**

### 5.3 预测：下一代语义迁移

> "The next migration will move toward **semantics-in-verified-contracts**, restoring verifiability without sacrificing model flexibility."

- **签名清单（Signed Manifests）**：加密验证的 Agent Card
- **运行时合同执行**：MCP/A2A 能力证明与行为约束
- **教训**：每代迁移以形式化保证换取适应能力；所丧失的成为下一代的主导问题

## 6. BDI 与 MCP/A2A 的映射

| BDI 概念 | MCP/A2A 对应 | 复用含义 |
|---------|-------------|---------|
| 信念（Belief） | MCP Resource / A2A Task context | 共享上下文作为信念基础 |
| 愿望（Desire） | A2A Task goal | 任务目标即愿望状态 |
| 意图（Intention） | MCP Tool call sequence / A2A Artifact plan | 工具调用链作为执行承诺 |
| 计划库 | MCP Tool registry / A2A Agent Card skills | 预注册能力库复用 |
| 实用推理 | LLM-based planning | 生成式规划替代符号过滤 |

## 7. 认知架构对比：ACT-R vs BDI

| 维度 | ACT-R | BDI |
|-----|-------|-----|
| 起源 | 认知心理学 | 哲学行动理论 |
| 目标 | 预测人类行为 | 构建理性智能体 |
| 知识表示 | 产生式规则 + 陈述性块 | 信念库 + 计划库 |
| 学习机制 | 强化学习 + 规则编译 | 计划获取 + 信念更新 |
| 应用领域 | 人机交互、培训仿真 | 自治系统、机器人、游戏 |
| 多智能体 | 间接（个体模型并行）| 原生支持（联合意图）|
| 与 LLM 关系 | 认知约束层 | 规划框架层 |

## 8. 参考索引

- Rao, A.S. & Georgeff, M.P.: "BDI Agents: From Theory to Practice" (ICMAS 1995)
- Bratman, M.E.: "Intention, Plans, and Practical Reason" (1987)
- FIPA Specifications: [fipa.org](http://www.fipa.org)
- JACK Intelligent Agents: AOS Group
- dMARS: distributed Multi-Agent Reasoning System
- Bova, V.V. & Lezhebokov, A.A.: "Development of Cognitive Architecture BDI of the Intellectual Agent" (Izvestiya Kabardino-Balkarskogo Nauchnogo Tsentra RAN)
- ArXiv (2026-05): "From Multi-Agent Systems and the Semantic Web to Agentic AI: A Unified Narrative of the Web of Agents"
