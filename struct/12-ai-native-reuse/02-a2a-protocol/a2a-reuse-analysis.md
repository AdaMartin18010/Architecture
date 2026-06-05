# A2A v1.0.0 协议复用分析

> **版本**: 2026-06-06
> **对齐标准**: A2A v1.0.0 (2026-03-12 发布), Linux Foundation 治理
> **定位**: Agent 间协作协议的复用流程与价值分析

---

## 目录

- [A2A v1.0.0 协议复用分析](#a2a-v100-协议复用分析)
  - [目录](#目录)
  - [1. 核心对象](#1-核心对象)
  - [2. 协议流程的复用分析](#2-协议流程的复用分析)
    - [五阶段复用流程](#五阶段复用流程)
  - [3. Agent Card 模板](#3-agent-card-模板)
  - [4. Task 状态机](#4-task-状态机)
  - [5. 多模态 Artifact](#5-多模态-artifact)
  - [6. 安全增强：Signed Agent Cards](#6-安全增强signed-agent-cards)
  - [7. 协作模式](#7-协作模式)

---

## 1. 核心对象

| 对象 | 定义 | 复用语义 | 安全机制 |
|------|------|----------|----------|
| **Agent Card** | Agent 的能力广告 JSON 文档 | 能力发现、技能目录、服务契约 | 签名验证（v1.0 新增） |
| **Task** | 委托的工作单元 | 任务复用、状态追踪、生命周期管理 | OAuth 2.1 / mTLS |
| **Artifact** | 结构化输出 | 结果复用、流式传输、多模态 | 传输加密 |
| **Message** | 对话消息 | 交互模式复用、澄清、确认 | 端到端加密 |
| **Part** | 消息的内容片段 | 多模态内容复用（文本/图像/音频/视频） | 内容验证 |

---

## 2. 协议流程的复用分析

### 五阶段复用流程

```text
A2A 协议复用流程
│
├── 1. 能力发现 (Discovery)
│   ├── 客户端读取服务器 Agent Card (/.well-known/agent.json)
│   ├── Agent Card 包含: 名称、描述、能力、认证要求、端点
│   └── 复用单元: Agent Card 模板、能力描述 Schema、发现机制
│
├── 2. 任务委托 (Task Delegation)
│   ├── 客户端 POST /tasks 创建任务
│   ├── 任务状态: submitted → working → input-required → completed/failed/canceled
│   └── 复用单元: 任务模板、状态机定义、超时策略、重试策略
│
├── 3. 消息交互 (Message Exchange)
│   ├── 任务执行期间的双向消息流
│   ├── 消息类型: 澄清请求、部分输出、确认、错误
│   └── 复用单元: 消息模式、对话协议、协商策略
│
├── 4. 结果交付 (Result Delivery)
│   ├── Artifact 作为结构化输出
│   ├── 支持流式 (SSE)、推送、轮询
│   └── 复用单元: 输出 Schema、格式化模板、验证规则
│
└── 5. 安全验证 (Security Verification)
    ├── v1.0 新增: Signed Agent Cards（加密签名）
    ├── 防止: 伪造 Agent、中间人攻击、能力欺骗
    └── 复用单元: 签名验证库、信任锚、证书链
```

---

## 3. Agent Card 模板

```json
{
  "name": "code-review-agent",
  "description": "Specialist agent for reviewing code quality and security",
  "url": "https://code-review.example.com",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true
  },
  "skills": [
    {
      "id": "rust-review",
      "name": "Rust Code Review",
      "description": "Review Rust code for safety, idiomatic patterns, and performance",
      "tags": ["rust", "safety", "performance"],
      "examples": [
        "Review this Rust function for memory safety issues",
        "Check if this async code is cancellation-safe"
      ],
      "inputModes": ["text"],
      "outputModes": ["text", "file"]
    },
    {
      "id": "security-scan",
      "name": "Security Vulnerability Scan",
      "description": "Scan code for common security vulnerabilities",
      "tags": ["security", "vulnerability"],
      "examples": [
        "Scan this Python code for SQL injection risks"
      ],
      "inputModes": ["text", "file"],
      "outputModes": ["text", "structured"]
    }
  ],
  "authentication": {
    "schemes": ["OAuth2"]
  },
  "signature": {
    "algorithm": "Ed25519",
    "publicKey": "base64-encoded-public-key",
    "certificate": "https://code-review.example.com/cert.pem"
  }
}
```

**复用价值**: Agent Card 将 Agent 的能力外化为可机器读取的服务契约，支持：

- 自动化 Agent 市场/目录
- 动态任务路由
- 跨组织 Agent 互操作

---

## 4. Task 状态机

```
Task 状态机（形式化定义）
├── 状态集合 S = {submitted, working, input-required, completed, failed, canceled}
├── 初始状态: submitted
├── 终止状态: completed, failed, canceled
│
├── 状态转移:
│   ├── submitted --(accept)--> working
│   ├── submitted --(reject)--> failed
│   ├── working --(need_input)--> input-required
│   ├── input-required --(provide_input)--> working
│   ├── working --(complete)--> completed
│   ├── working --(error)--> failed
│   ├── working --(cancel)--> canceled
│   └── input-required --(cancel)--> canceled
│
└── 不变量:
    ├── 终止状态下不再有消息交互
    ├── completed 状态必须包含至少一个 Artifact
    └── failed 状态必须包含错误信息
```

---

## 5. 多模态 Artifact

```json
{
  "id": "artifact-001",
  "taskId": "task-001",
  "parts": [
    {
      "type": "text",
      "text": "Code review completed. Found 2 issues:"
    },
    {
      "type": "file",
      "file": {
        "name": "review-report.md",
        "mimeType": "text/markdown",
        "bytes": "base64-encoded-content"
      }
    },
    {
      "type": "data",
      "data": {
        "mimeType": "application/json",
        "schema": {
          "type": "object",
          "properties": {
            "issues": { "type": "array" },
            "severity": { "type": "string" }
          }
        }
      }
    }
  ]
}
```

**复用价值**: Artifact 的结构化输出使 Agent 的结果可被其他 Agent 或系统直接消费，无需人工解析。

---

## 6. 安全增强：Signed Agent Cards

A2A v1.0.0 新增 Signed Agent Cards，防止能力欺骗和中间人攻击。

```
签名验证流程
├── 1. 获取 Agent Card
│   └── GET https://agent.example.com/.well-known/agent.json
│
├── 2. 解析签名字段
│   ├── algorithm: Ed25519 / ECDSA P-256
│   ├── publicKey: Base64 编码的公钥
│   └── signature: 对 Agent Card 内容的数字签名
│
├── 3. 验证签名
│   ├── 使用公钥验证签名有效性
│   ├── 验证公钥来自可信 CA 或信任锚
│   └── 可选：证书透明度日志检查
│
└── 4. 信任决策
    ├── 签名有效 + 信任锚可信 → 信任能力声明
    └── 签名无效或不可信 → 拒绝连接 / 人工审核
```

---

## 7. 协作模式

| 模式 | 描述 | 适用场景 | A2A 实现 |
|------|------|---------|---------|
| **串行** | Agent A → Agent B → Agent C | 流水线处理 | 顺序 Task 委托 |
| **并行** | Agent A 同时委托给 B, C, D | 多角度分析 | 并发 Task 创建 |
| **竞争** | 多个 Agent 同时处理，取最优结果 | 需要高可靠性 | 多 Task + 结果选择 |
| **协商** | Agent 间多轮消息交互达成共识 | 冲突消解 | Message Exchange |
| **主从** | 编排 Agent 协调多个专业 Agent | 复杂任务分解 | Orchestrator 模式 |

---

> 最后更新: 2026-06-06
> 下次更新: A2A v1.1 发布后
