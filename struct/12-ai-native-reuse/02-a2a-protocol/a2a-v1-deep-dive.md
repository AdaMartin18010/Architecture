# A2A v1.0.0 权威深度解析

> **定位**：Agent-to-Agent 协议的全面技术对齐，明确 MCP 与 A2A 的互补关系，指导多 Agent 架构复用。
> **权威来源**：a2a-protocol.org、Google A2A GitHub、Linux Foundation Agentic AI Foundation (AAIF)、Cloud Next 2026。
> **版本状态**：A2A v1.2 当前稳定版（2026‑03‑12 GA，v1.0 一周年）

---

## 1. 关键结论（TL;DR）

| 维度 | 关键结论 |
|------|----------|
| **A2A 定位** | **水平协议**：Agent ↔ Agent 的协作；与 MCP（垂直：Agent ↔ Tool）互补 |
| **治理** | 2025‑12‑09 捐给 Linux Foundation AAIF，与 MCP 同基金会，中立治理 |
| **v1.0  headline** | **Signed Agent Cards**（JWS 加密域验证）、gRPC 支持、多租户、AP2 支付协议 |
| **核心四元组** | Agent Card（能力发现）→ Task（状态机生命周期）→ Message/Part（多模态通信）→ Artifact（产出物） |
| **与 MCP 关系** | A2A 任务内部可调用 MCP 工具；MCP 不应简单包装 Agent 为 tool |
| **BPMN 集成** | A2A Service Task 已出现在 Camunda 生产模型中；BPMN 治理 + A2A 执行 = 混合架构 |
| **成熟度** | 早期生产级：150+ 组织、22K+ GitHub stars、5 语言 SDK、3 大云原生支持 |

---

## 2. 版本与治理时间线

```text
2025-04-09    Google Cloud Next '25 首发，50+ 合作伙伴
2025-06       捐赠给 Linux Foundation
2025-07-30    v0.3.0：流式传输、Agent Card 能力协商
2025-08       IBM/Cisco ACP 合并入 A2A
2025-12-09    Linux Foundation 成立 AAIF（Agentic AI Foundation），同时托管 MCP + A2A
2026-03-12    v1.0.0 GA（一周年）：Signed Agent Cards、gRPC、多租户
2026-04-09    Cloud Next 2026：ADK 1.0 GA、AP2 支付协议、Latency 广播
2026-Q2       v1.2 当前稳定版
```

---

## 3. 核心概念

### 3.1 Agent Card

```json
{
  "name": "InventoryAgent",
  "description": "Real-time inventory and fulfillment status",
  "url": "https://supplier.example.com/a2a",
  "version": "1.2.0",
  "capabilities": { "streaming": true, "pushNotifications": true },
  "skills": [
    {
      "id": "check_inventory",
      "name": "Check Inventory",
      "description": "Returns stock levels for SKU",
      "tags": ["inventory", "logistics"],
      "examples": ["Check stock for SKU-12345"]
    }
  ],
  "authentication": { "schemes": ["oauth2"] }
}
```

发布于 `/.well-known/agent-card.json`（RFC 8615）。

### 3.2 Task 生命周期状态机

```text
submitted → working → [input-required | auth-required] → completed
   ↓                                              ↓
 rejected                                      failed / canceled
```

**与 MCP 的关键差异**：A2A 将**长时异步工作**作为一等公民；任务可持续分钟、小时乃至天，支持人工介入中断。

### 3.3 Message / Part / Artifact

- **Message**：单轮通信，`role: user | agent`，包含 `parts[]`
- **Part**：最小内容容器
  - `TextPart`：纯文本
  - `FilePart`：内联字节或 URI 引用
  - `DataPart`：结构化 JSON
- **Artifact**：任务产生的有形产出（PDF、JSON、图片）

**多模态原生**：Agent 可在同一会话中交换文本、图片、文档和结构化数据。

---

## 4. 安全模型

| 机制 | 说明 |
|------|------|
| **Signed Agent Cards** | JWS + JCS 签名，绑定发布域；防止 Agent Card 伪造 |
| **OAuth 2.0 / OIDC** | 标准令牌委托 |
| **mTLS** | 证书双向认证 |
| **in-task 授权** | `auth-required` 状态支持 step-up 认证 |
| **已知缺口** | 令牌生命周期控制不足、访问范围过宽、敏感数据同意流缺失、协议级审计日志未规定 |

> **架构建议**：生产部署应在 Agent 流量前部署 **A2A Gateway**，强制执行白名单、提示注入防护、结构化日志和 OAuth 2.0 + RFC 8707 资源指示器。

---

## 5. A2A vs MCP：互补而非竞争

### 5.1 根本区分

| 维度 | **MCP 2025-11-25** | **A2A v1.2** |
|------|---------------------|--------------|
| **层级** | 垂直：Agent → Tool | 水平：Agent → Agent |
| **交互模型** | 无状态结构化函数调用 | 有状态多轮任务委托 |
| **发现机制** | Tool registry / Server list | Agent Card @ well-known URI |
| **不透明性** | Tool 暴露 schema；Agent "看到内部" | Agent 保持不透明；仅广告能力 |
| **生命周期** | 短、同步 | 长时、异步优先 |
| **治理** | Linux Foundation AAIF | Linux Foundation AAIF |

### 5.2 选型指南

| 场景 | 推荐 |
|------|------|
| 单 Agent + 内部工具 | **仅 MCP** |
| 多 Agent、同框架（全 LangGraph） | 框架原生消息 + A2A Agent Card 兼容 |
| 跨框架 Agent（LangGraph ↔ CrewAI ↔ ADK） | **A2A 是务实默认** |
| 跨云 / 跨组织 Agent | **A2A 必需** |
| 长时工作流 + 人工交接 | **A2A** — MCP 缺乏任务生命周期语义 |
| Agent 中介支付 / 商务 | **A2A + AP2** |
| BPMN 管理的业务流程内嵌 AI | **BPMN + A2A 混合** |

### 5.3 生产最佳实践：两者共用

> A2A Client Agent 将复杂任务委托给 A2A Server Agent；Server Agent **内部使用 MCP** 与其工具、API 和数据源交互以完成 A2A 任务。
>
> 将 Agent 简单包装为 MCP tool 是本质上的限制 —— Agent 应以 Agent 身份暴露，而非 tool。

---

## 6. 与 BPMN/DMN 的集成

### 6.1 A2A → BPMN 映射

| A2A 概念 | BPMN 等价物 |
|----------|-------------|
| Task | Service Task / Call Activity |
| 生命周期状态 | Boundary events（timer、error、message） |
| Artifact | Data Object / Message |
| Agent Card 发现 | Process Engine connector |
| 多轮交互 | 展开式 Subprocess |

### 6.2 生产示例：贷款审批 BPMN

```text
Start Event → Service Task(欺诈检测 A2A Agent)
   → Gateway(风险过高?)
   → Subprocess(贷款报价准备 — A2A 多轮客户交互)
   → Subprocess(核保)
   → User Task(人工审批 — 法律要求)
   → End Event
```

**洞察**：BPMN 提供**外部编排**（序列、网关、超时、人工审批）；A2A Agent 在此结构**内部**执行工作。BPMN 强制执行护栏；A2A 启用其中的 Agentic 工作。

### 6.3 DMN 驱动 Agent 选择

DMN 决策表可用于**基于任务类型、SLA、成本或信任评分选择调用哪个 A2A Agent**。BPMN Business Rule Task 可引用 DMN 模型评估 Agent Card 元数据（如 `signed: true` 且 `trustScore > 0.8`）。

---

## 7. 多 Agent 编排模式

| 模式 | A2A 用法 | 适用场景 |
|------|----------|----------|
| **Hub-and-Spoke** | 协调器发现专家 Agent，委托子任务，聚合产出 | 财务报表生成、代码审查流水线 |
| **Peer-to-Peer** | 任意 Agent 直接调用其他 Agent；动态能力匹配 | 领域边界松散、专家不确定 |
| **Pipeline** | 顺序链接：`tasks/send` + Artifact 交接 | 起草 → 审核 → 排版 → 发布 |
| **Competitive** | 并行发送多个候选 Agent，比较产出 | 欺诈检测、投资分析 |
| **Swarm** | Agent 通过共享状态自组织；A2A 提供线协议 | 需要编排层（ADK、AutoGen）之上 |

---

## 8. 企业采用与壁垒

### 8.1 活跃生产领域（2026 Q2）

| 行业 | 用例 | 代表部署 |
|------|------|----------|
| 金融服务 | 交易对账、KYC、监管报告、欺诈检测 | Deutsche Bank (40+ A2A agents) |
| 保险 | 理赔分类、保单审核、风险评估 | 多家经 Accenture 实施 |
| 供应链 | 库存协调、需求预测、物流 | SAP Joule + 合作伙伴 Agent |
| IT 运维 | 事件分类、自动修复、变更管理 | ServiceNow Now Assist |
| 企业 SaaS | CRM↔ERP 交接、跨平台工作流 | Salesforce Agentforce → SAP |

### 8.2 成熟度评估

| 维度 | 评级 | 说明 |
|------|------|------|
| 规范稳定性 | ⭐⭐⭐⭐☆ | v1.0 稳定；v1.2 当前；已定义废弃政策 |
| 企业安全 | ⭐⭐⭐⭐☆ | Signed Agent Cards、OAuth、mTLS；审计流和同意流仍有缺口 |
| 生态广度 | ⭐⭐⭐⭐⭐ | 150+ 组织、3 大云、5 SDK、6+ 框架 |
| 生产加固 | ⭐⭐⭐☆☆ | 真实部署存在；BigTech 外多数仍为 PoC 或早期生产 |
| 语义互操作 | ⭐⭐☆☆☆ | 协议使 Agent 能"通话"；含义一致仍需领域 schema |
| 工具/可观测性 | ⭐⭐⭐☆☆ | SDK 可用；企业级追踪、监控、成本管理工具仍在涌现 |

**总体成熟度**：**早期生产级** — 超越实验阶段，适合 greenfield 多 Agent 项目，但需要自定义治理和可观测层。

---

## 9. 架构复用意义

A2A 将 Agent 转变为**可组合、可发现的发现服务**：

1. **能力广告**：Agent 技能以机器可读的 Agent Card 声明
2. **不透明封装**：内部工具、提示、记忆、推理隐藏 —— 仅暴露能力契约
3. **框架解耦**：LangGraph Agent 可委托给 CrewAI Agent，双方无需了解对方实现
4. **跨边界信任**：Signed Agent Cards + 标准认证方案实现组织间委托，无需自定义联邦

### 复用模式

| 模式 | 复用收益 |
|------|----------|
| **能力市场** | 策展 Agent Card 注册表；Agent 一次发布，多部门/供应商消费 |
| **专家 Agent 池** | 水平专家（法律、财务、安全）跨垂直工作流复用 |
| **供应商抽象** | Agent Card 作为接口契约；更换底层供应商/Agent 无需更改消费端代码 |
| **联邦编排** | 业务流程跨越组织边界，无需定制集成 |

---

## 10. 权威来源

1. A2A Official Docs: <https://a2a-protocol.org/latest/>
2. A2A Specification: <https://a2a-protocol.org/latest/specification/>
3. Google A2A GitHub: <https://github.com/google/A2A>
4. AAIF (Linux Foundation): <https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation>
5. A2A vs MCP (Official): <https://a2a-protocol.org/latest/topics/a2a-and-mcp/>
6. AP2 (Agent Payments Protocol): <https://github.com/google-agentic-commerce/AP2>
7. Microsoft Semantic Kernel + A2A: <https://devblogs.microsoft.com/foundry/semantic-kernel-a2a-integration/>
8. Camunda Agentic Orchestration: <https://camunda.com/de/solutions/agentic-orchestration/>

---

*文档生成时间：2026-06-06 · 对齐 A2A v1.2 / Cloud Next 2026 / Linux Foundation AAIF*


---

## 补充说明：A2A v1.0.0 权威深度解析

## 示例

**示例**：旅行规划 Agent 通过 A2A 调用酒店预订 Agent 与航班查询 Agent，基于能力清单与信任凭证自动协商，无需硬编码集成。

## 反例

**反例**：各 Agent 使用私有消息格式与认证机制，跨团队协作时需要为每对 Agent 写适配器，形成 N² 集成问题。

## 分析

**分析**：A2A 关注 Agent 之间的协作语义，与 MCP 形成“工具-代理”双层协议体系。
