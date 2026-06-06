# LLM Agent 的复用与组合

> **版本**: 2026-06-06
> **定位**: 分析 LLM Agent 作为一种新型复用单元的架构模式

---

## 1. LLM Agent 作为复用单元

**定义 AI.1** (LLM Agent): LLM Agent 是一个由大语言模型驱动、具备感知-推理-行动循环的自主软件实体。其形式为：

```text
Agent := ⟨LLM, Memory, Tools, Planner, EnvironmentInterface⟩
```

其中：

- `LLM`: 核心推理引擎
- `Memory`: 短期/长期记忆
- `Tools`: 可调用的外部能力（MCP Tool / Function Call）
- `Planner`: 任务分解与执行规划
- `EnvironmentInterface`: 与外部世界的交互接口

> **公理 AI.1** (Probabilistic Contract Necessity): LLM Agent 的输出本质上是概率分布 P(output | input, context)。因此，其复用契约不能是确定性的，而必须是**概率性契约**：P(correct | task) ≥ θ。

---

## 2. Agent 复用的层次

### Level 1: Prompt 模板复用

复用经过验证的 Prompt 模板。最轻量的复用形式。

### Level 2: Tool 组合复用

复用一组相关的 MCP Tool / Function Call。

### Level 3: Agent 角色复用

复用预定义的 Agent 角色（如"代码审查员"、"需求分析师"）。

### Level 4: 多 Agent 系统复用

复用整个多 Agent 协作模式（如 A2A 编排、CrewAI 团队结构）。

---

## 3. Agent 组合模式

### 模式 1: 串行管道 (Sequential Pipeline)

```text
Input → Agent A → Agent B → Agent C → Output
```

### 模式 2: 路由分发 (Router)

```text
        ┌→ Agent A
Input → Router →┼→ Agent B
        └→ Agent C
```

### 模式 3: 投票聚合 (Voting / Ensemble)

```text
        ┌→ Agent A ─┐
Input → ┼→ Agent B ─┼→ Aggregator → Output
        └→ Agent C ─┘
```

### 模式 4: 主从协作 (Manager-Worker)

```text
Manager Agent
├── 分解任务
├── 分配给 Worker Agent
├── 收集结果
└── 验证与整合
```

### 模式 5: A2A 跨 Agent 协作

A2A 协议支持不同框架、不同厂商的 Agent 之间协作：

```text
Agent A (Google ADK) --A2A--> Agent B (LangGraph) --A2A--> Agent C (AutoGen)
```

---

## 4. Agent 复用的质量保障

> **公理 AI.2** (Uncertainty Composition): 多个 Agent 组合时，总体不确定性是各 Agent 不确定性的函数。若 Agent 间存在依赖，总体不确定性可能**超线性**增长。

### 质量保障策略

| 策略 | 说明 |
|------|------|
| **一致性采样** | 多次采样，选择最一致的输出 |
| **人在回路** | 关键决策点引入人工确认 |
| **置信度阈值** | 低置信度输出触发降级策略 |
| **对抗验证** | 使用批评 Agent 验证主 Agent 的输出 |
| **结构化输出** | 强制 JSON schema / Pydantic 输出 |
| **追踪与可观测性** | 记录 Agent 的思考链和工具调用 |

---

## 5. 关键定理

> **定理 AI.1** (Calibration Ceiling): 若 Agent 在训练分布 D_train 上校准良好，但在部署分布 D_deploy 上存在显著漂移，则其复用可靠性存在上界。
> **定理 AI.2** (Human-in-the-Loop Optimality): 对于高风险的 Agent 决策，人在回路的成本低于完全自动化的期望错误成本，当且仅当 C_human < P(error) × C_error。

---

> 最后更新: 2026-06-06
