# MCP 2026-07-28 RC → 正式版迁移指南

> **版本**: 2026-07-08
> **状态**: 基于已发布的 **Release Candidate（2026-05-29）** 编制，最终正式版预计 2026-07-28
> **定位**: `12-ai-native-reuse/01-mcp-protocol/` 的预对齐迁移 checklist

---

## 1. 概念定义

**MCP 迁移** 是指将 MCP Server/Client/Gateway 从既有协议版本（通常为 2025-11-25）升级到新版（2026-07-28）的过程，涉及传输模型、生命周期、路由、缓存、扩展框架与授权机制的调整。

---

## 2. 版本状态

| 版本 | 状态 | 发布日期 | 生产建议 |
|---|---|---|---|
| **2025-11-25** | 现行稳定版 | 2025-11-25 | 生产环境继续使用 |
| **2026-07-28** | **Release Candidate 已发布** | 2026-05-29 | 可评估/试点；正式版发布后逐步迁移 |

官方来源：

- 稳定规范: <https://modelcontextprotocol.io/specification/2025-11-25>
- RC releases: <https://github.com/modelcontextprotocol/modelcontextprotocol/releases>

---

## 3. 2026-07-28 核心变化对复用的影响

| 变化项 | 对复用的影响 | 迁移动作 |
|---|---|---|
| **Stateless 核心** | Server 成为无状态函数，支持任意负载均衡与自动扩缩容 | 网关与基础设施移除粘性会话依赖 |
| **移除 initialize/initialized 握手** | 每请求自包含，降低连接开销 | 客户端/服务端重构生命周期管理 |
| **Mcp-Method 头部路由** | 网关无需解析 JSON-RPC body，可缓存、低延迟 | 更新网关与缓存策略 |
| **ttlMs 缓存语义** | `tools/list` 等可缓存，减少重复发现 | 在工具目录实现中加入 TTL 控制 |
| **Extensions 框架正式化** | 扩展演进标准化 | 评估现有自定义扩展是否需迁移到官方 Extensions |
| **Tasks Extension 毕业** | 长时任务复用有官方支持 | 将异步任务实现迁移到 Tasks Extension |
| **MCP Apps（服务器渲染 UI）** | 交互式工具可复用 | 评估在客服、DevOps 等场景中引入 MCP Apps |
| **OAuth 2.1 + 防 issuer 混淆** | 企业级授权与审计 | 更新认证流程，增加 issuer 校验 |

---

## 4. 迁移 Checklist

### 4.1 基础设施层

- [ ] 移除 MCP 网关对 `Mcp-Session-Id` 的粘性会话依赖
- [ ] 支持基于 `Mcp-Method` 头部的路由与缓存
- [ ] 为无状态 Server 配置负载均衡/自动扩缩容
- [ ] 评估 Serverless/FaaS 部署可行性

### 4.2 服务端实现

- [ ] 移除 `initialize/initialized` 握手逻辑
- [ ] 确保每个请求自包含 capabilities 与上下文
- [ ] 为 `tools/list`、`resources/list` 等响应添加 `ttlMs`
- [ ] 若存在长时任务，迁移到 Tasks Extension

### 4.3 客户端实现

- [ ] 更新版本协商逻辑以支持 2026-07-28
- [ ] 实现 OAuth 2.1 授权流程与 issuer 混淆防护
- [ ] 处理无状态 Server 的每请求独立上下文

### 4.4 安全与治理

- [ ] 更新工具权限模型，支持 Extensions 的独立能力声明
- [ ] 对 MCP Apps 的 UI 输出进行安全审查
- [ ] 在审计日志中记录协议版本、method、issuer

### 4.5 文档与培训

- [ ] 更新内部 MCP Server 开发规范
- [ ] 更新工具目录注册模板
- [ ] 对开发团队进行 stateless 架构与 Extensions 培训

---

## 5. 版本共存策略

| 场景 | 建议 |
|---|---|
| 新 Server | 直接基于 2026-07-28 实现 |
| 现有生产 Server | 保持 2025-11-25，在维护窗口中升级 |
| 网关/中间件 | 同时支持 2025-11-25 与 2026-07-28，通过版本协商路由 |
| 客户端 | 优先使用 2026-07-28，失败时回退到 2025-11-25 |

---

## 6. 正向示例

某 DevOps 智能助手团队将其 MCP 网关升级为 2026-07-28 无状态模式：

- 网关通过 `Mcp-Method` 头部直接路由，无需解析 JSON-RPC body
- `tools/list` 响应加入 `ttlMs=300000`，下游缓存命中提升 40%
- 长时 CI/CD 任务迁移到 Tasks Extension，用户体验从"等待超时"变为"异步通知"

---

## 7. 反例

某团队在未更新授权逻辑的情况下直接升级 MCP Server 到 2026-07-28，未启用 issuer 校验。攻击者通过伪造 issuer 获取了本不应授权的工具调用权限，造成数据泄露。

**教训**: 协议升级必须与安全机制同步升级，不能仅关注功能兼容性。

---

## 8. 分析

MCP 2026-07-28 的 stateless 化是一次架构范式迁移，其本质是复用单元从"会话参与者"变为"无状态函数执行器"。这要求基础设施、安全模型与运维监控同时演进；只升级协议而不升级治理会导致新的风险。

---

## 9. 权威来源

| 来源 | URL | 核查日期 |
|---|---|---|
| MCP 2025-11-25 规范 | <https://modelcontextprotocol.io/specification/2025-11-25> | 2026-07-08 |
| MCP 2026-07-28 RC | <https://github.com/modelcontextprotocol/modelcontextprotocol/releases/tag/2026-07-28-RC> | 2026-07-08 |
| MCP Specification repo | <https://github.com/modelcontextprotocol/specification> | 2026-07-08 |
