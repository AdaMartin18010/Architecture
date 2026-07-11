# OWASP LLM / MCP 安全对齐

> **版本**: 2026-06-06
> **权威来源**: OWASP Top 10 for LLM Applications 2025, OWASP Top 10 for MCP 2025, OWASP Top 10 for Agentic AI 2026
> **定位**: 对齐 OWASP 最新 AI 安全框架与 MCP/Agent 复用安全

---

## 1. OWASP LLM Top 10 (2025)

| 排名 | 风险 | 说明 | MCP 相关 |
|------|------|------|---------|
| **LLM01** | Prompt Injection | 提示注入攻击 | ✅ 高 |
| **LLM02** | Sensitive Information Disclosure | 敏感信息泄露 | ✅ 中 |
| **LLM03** | Supply Chain Vulnerabilities | 供应链漏洞 | ✅ 高 |
| **LLM04** | Data and Model Poisoning | 数据和模型投毒 | ✅ 中 |
| **LLM05** | Improper Output Handling | 输出处理不当 | ✅ 中 |
| **LLM06** | Excessive Agency | 过度代理 | ✅ 高 |
| **LLM07** | System Prompt Leakage | 系统提示泄露 | ✅ 中 |
| **LLM08** | Vector and Embedding Weaknesses | 向量和嵌入弱点 | ✅ 中 |
| **LLM09** | Misinformation | 错误信息 / 过度依赖 | ✅ 中 |
| **LLM10** | Unbounded Consumption | 无界资源消耗 | ✅ 高 |

---

## 2. OWASP MCP Top 10 (2025)

OWASP 针对 MCP 专门发布了 Top 10：

| 排名 | 风险 | 说明 |
|------|------|------|
| **MCP1** | Prompt Injection via Tool Descriptions | 通过工具描述注入 |
| **MCP2** | Tool Description Poisoning | 工具描述投毒 |
| **MCP3** | Excessive Tool Permissions | 过度工具权限 |
| **MCP4** | Insecure Tool Output Handling | 不安全的工具输出处理 |
| **MCP5** | Command Injection & Execution | 命令注入和执行 |
| **MCP6** | Prompt Injection via Contextual Payloads | 通过上下文负载注入 |
| **MCP7** | Inadequate Authentication & Authorization | 认证授权不足 |
| **MCP8** | Lack of Audit and Telemetry | 缺少审计和遥测 |
| **MCP9** | Shadow MCP Servers | 影子 MCP Server |
| **MCP10** | Context Injection & Over-Sharing | 上下文注入和过度共享 |

---

## 3. OWASP Agentic AI Top 10 (2026)

| 排名 | 风险 | 说明 |
|------|------|------|
| **ASI01** | Agent Goal Hijack | Agent 目标劫持 |
| **ASI02** | Uncontrolled Autonomy | 不受控的自主性 |
| **ASI03** | Identity and Privilege Abuse | 身份和权限滥用 |
| **ASI04** | Cross-Agent Prompt Injection | 跨 Agent 提示注入 |
| **ASI05** | Unexpected Code Execution | 意外代码执行 |
| **ASI06** | Agent-to-Agent Trust Boundary | Agent 间信任边界 |
| **ASI07** | Tool Chain Exploitation | 工具链利用 |
| **ASI08** | Model Drift | 模型漂移 |
| **ASI09** | Insecure Memory | 不安全记忆 |
| **ASI10** | Orchestration Failure | 编排失败 |

---

## 4. MCP 关键攻击向量

### 4.1 Tool Poisoning（工具投毒）

**机制**: MCP Server 在会话之间修改 Schema，添加恶意参数。

**防御**:

- 版本锁定（version pinning）
- Server 代码审计
- 沙箱化运行
- Capability Attestation（即将推出）

### 4.2 Context Bloat（上下文膨胀）

**机制**: 过多 Tool Schema 占用 System Prompt 空间，导致：

- Token 成本飙升
- 模型注意力分散
- 性能下降

**防御**:

- 按需加载工具
- 工具分类和路由
- 限制同时连接的 Server 数量

### 4.3 Prompt Injection via Tool Outputs

**机制**: 恶意网站/文档中的指令通过 MCP Tool 输出返回给模型。

**防御**:

- 输入/输出过滤
- 特权分离
- 人在回路确认高影响操作

---

## 5. 安全设计原则

### 5.1 Defense in Depth

```text
多层防御
├── 网络层: TLS、证书固定
├── 认证层: OAuth 2.1 + PKCE、API Key
├── 应用层: 输入验证、输出过滤
├── 模型层: Prompt 硬化、系统提示隔离
├── 工具层: 权限最小化、沙箱执行
└── 监控层: 审计日志、异常检测
```

### 5.2 Zero Trust for AI Agents

- 不信任任何 Tool 描述
- 不信任任何 Agent Card（除非签名验证）
- 不信任任何用户输入（视为潜在注入）
- 不信任任何模型输出（视为可能受污染）

---

## 6. 复用安全建议

| 复用场景 | 风险 | 建议 |
|---------|------|------|
| 复用第三方 MCP Server | Tool Poisoning | 代码审计 + 版本锁定 + 沙箱 |
| 复用 Agent 角色模板 | 过度代理 | 限制权限范围 + 人在回路 |
| 复用 Prompt 模板 | 提示注入 | 输入验证 + 参数化 |
| 复用多 Agent 编排 | 跨 Agent 注入 | Agent 间认证 + 消息签名 |
| 复用 RAG 组件 | 向量弱点 | 来源验证 + 检索过滤 |

---

## 7. 工具推荐

| 类别 | 工具 |
|------|------|
| MCP 扫描 | MCPScan, MCPGuard, Cisco MCP Scanner |
| Prompt 防护 | Prompt 过滤器、Layered Filtering |
| 监控 | OpenTelemetry GenAI 约定 |
| 沙箱 | Docker, gVisor |

---

> 最后更新: 2026-06-06
> 权威来源:
>
> - <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
> - <https://owasp.org/www-project-mcp-top-10/>
> - OWASP Top 10 for Agentic AI Applications 2026


---

## 补充说明：OWASP LLM / MCP 安全对齐

## 概念定义

**定义**：MCP 是由 Anthropic 主导的开放协议，规范 AI 模型如何发现、调用工具并交换上下文，使工具成为可复用资产。

## 示例

**示例**：代码助手通过 MCP 调用统一代码搜索工具，返回结构化上下文；不同 IDE 插件复用同一工具，无需各自实现代码索引。

## 反例

**反例**：Agent 通过私有 HTTP 端点调用工具，无 Schema 注册与权限控制，工具变更导致所有调用方失效。

## 分析

**分析**：MCP 将工具从“代码片段”提升为“可发现服务”，是 Agent 生态互操作的关键。
