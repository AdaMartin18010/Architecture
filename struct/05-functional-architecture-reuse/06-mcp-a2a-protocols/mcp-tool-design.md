# MCP Tool 的可复用设计

> **版本**: 2026-06-06
> **对齐标准**: Model Context Protocol (MCP) 2025-11-25（当前稳定版）
> **定位**: 设计可复用、可发现、可验证的 MCP Tool

---

## 1. MCP Tool 的本质

**定义 5.1** (MCP Tool): MCP Tool 是一个**语义化函数签名**，其形式为：

```text
Tool := ⟨Name, Description, InputSchema, OutputSchema, Annotations, ErrorModel, ExampleSet⟩
```

其中：

- `Name`: 全局唯一标识符
- `Description`: LLM 可理解的自然语言语义描述
- `InputSchema`: JSON Schema，描述输入参数结构
- `OutputSchema`: JSON Schema，描述输出结构
- `Annotations`: 运行时元数据（readOnlyHint, openWorld, title, etc.）
- `ErrorModel`: 错误分类与重试策略
- `ExampleSet`: 少样本示例集，用于 LLM 调用优化

> **定理 5.1** (Tool Reuse Equivalence): MCP Tool 的复用等价于其**语义描述**与**模式约束**在目标 LLM 上下文中的可传递性。形式化：Reuse(Tool) ⟺ LLM 能够基于 Description + ExampleSet 正确生成符合 InputSchema 的调用，并正确消费 OutputSchema。

---

## 2. Tool 设计的 SOLID-T 原则

为 MCP Tool 设计的扩展原则：

| 原则 | 说明 | 实践 |
|------|------|------|
| **S - Single Responsibility** | 每个 Tool 做一件事 | Tool 粒度应等同于单一业务操作 |
| **O - Open/Closed** | 对扩展开放，对修改关闭 | 新增可选参数而非修改现有参数结构 |
| **L - Literal Clarity** | 描述必须字面准确 | 避免歧义动词，使用领域术语 |
| **I - Interface Cohesion** | 输入/输出模式应内聚 | 避免 God Schema，使用引用的嵌套结构 |
| **D - Deterministic Defaults** | 默认行为必须可预测 | 明确说明未提供参数时的行为 |
| **T - Testable Examples** | 每个 Tool 必须有可执行的示例 | 示例集覆盖正常、边界、错误三种场景 |

---

## 3. Tool 分类与复用策略

```text
MCP Tool 分类
├── 数据访问类 (Data Access)
│   ├── 数据库查询、文档检索、API 调用
│   └── 复用策略：Schema 标准化、连接池共享、查询模板化
│
├── 计算类 (Computation)
│   ├── 数学计算、字符串处理、数据转换
│   └── 复用策略：纯函数化、幂等性保证、结果缓存
│
├── 状态操作类 (State Mutation)
│   ├── 订单创建、配置更新、用户状态变更
│   └── 复用策略：幂等键、乐观锁、事件溯源
│
├── 外部集成类 (External Integration)
│   ├── 邮件发送、支付调用、Slack 通知
│   └── 复用策略：适配器模式、重试退避、熔断降级
│
└── 复合编排类 (Composition)
    ├── 工作流触发、报告生成、多步骤审批
    └── 复用策略：状态机驱动、子 Tool 组合、A2A Agent 委托
```

---

## 4. Tool 复用的层次

### Level 1: 语法复用

复制 Tool 定义的 JSON Schema 到新的 MCP Server。风险：语义漂移。

### Level 2: 语义复用

复用 Tool 的业务语义，允许实现变化。要求 Description 精确，ExampleSet 完整。

### Level 3: 行为复用

复用 Tool 的行为契约（前置条件、后置条件、幂等性、错误模型）。

### Level 4: 组合复用

将多个 Tool 组合为更高层的能力模板，通过 A2A 在 Agent 间编排。

---

## 5. Tool 注册与发现示例

```json
{
  "tools": [
    {
      "name": "order.create",
      "description": "创建新订单。幂等操作，使用 clientOrderId 避免重复。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "clientOrderId": { "type": "string" },
          "items": { "type": "array" },
          "customerId": { "type": "string" }
        },
        "required": ["clientOrderId", "items", "customerId"]
      },
      "annotations": {
        "title": "Create Order",
        "readOnlyHint": false,
        "destructiveHint": false,
        "idempotentHint": true,
        "openWorld": false
      }
    }
  ]
}
```

---

## 6. Tool 复用质量指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| **Tool Clarity Score** | 描述清晰度和示例覆盖度 | ≥ 0.85 |
| **Schema Completeness** | JSON Schema 的约束完整性 | ≥ 0.90 |
| **Example Coverage** | 示例覆盖正常/边界/错误场景 | ≥ 3 个/Tool |
| **Idempotency Rate** | 幂等 Tool 的比例 | ≥ 80%（状态变更类） |
| **Reuse Count** | Tool 在多少场景中被复用 | 跟踪指标 |
| **Failure Rate** | LLM 调用失败的比率 | < 5% |

---

> 最后更新: 2026-06-06


---

## 补充说明：MCP Tool 的可复用设计

## 概念定义

**定义**：MCP（Model Context Protocol）规范 Agent 与工具/上下文源之间的交互，A2A（Agent-to-Agent Protocol）规范 Agent 之间的协作；二者共同构成 AI 原生复用的协议基础。

## 示例

**示例**：企业构建 MCP 工具目录，将数据库查询、文档检索、代码分析等能力暴露为标准化工具，不同 Agent 可按能力清单调用。

## 反例

**反例**：各 Agent 使用私有 RPC 协议与工具交互，导致工具无法在 Agent 之间共享，形成新的孤岛。

## 权威来源

> **权威来源**:
>
> - [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25)
> - [A2A Protocol](https://a2a-protocol.org/latest/)
> - 核查日期：2026-07-07
