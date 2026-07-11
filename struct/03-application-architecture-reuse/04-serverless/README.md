# 03 Serverless 架构复用

> **版本**: 2026-07-09
> **定位**: 03 应用架构复用的基础子主题 — Serverless / FaaS 架构的复用模式
> **对齐**: CNCF Serverless Whitepaper v2, AWS/Azure/GCP 官方文档, 12-Factor App, ISO/IEC 25010:2023
> **状态**: ✅ 核心内容已填充

---

## 核心内容

1. **概念定义（CARC 本体）**：Serverless、FaaS、BaaS、事件驱动、自动扩缩容、冷启动。
2. **概念谱系**：从 CGI/PaaS 到 AWS Lambda、EventBridge、Cloud Run、Knative。
3. **核心复用模式**：Lambda Layer、事件源复用、Serverless 工作流、BaaS 复用、Serverless→容器化升级路径。
4. **函数边界与粒度**：单操作函数、单业务步骤、聚合功能函数的取舍。
5. **示例与反例**：图片处理流水线、定时同步、函数中保存会话状态、忽视冷启动成本。
6. **多维矩阵**：Serverless 平台能力对比、Serverless vs 微服务 vs 分层架构。
7. **场景决策树**：根据负载特征、执行时间、延迟要求、成本选择 Serverless 形态。

## 主文档

- **[reuse-patterns.md](reuse-patterns.md)** — Serverless 架构复用模式完整指南
- **[serverless-reuse-patterns.md](serverless-reuse-patterns.md)** — Serverless/FaaS 复用边界、模式与成本优化深度指南

## 关联主题

- `03/02-microservices`（Serverless 作为微服务的极端粒度）
- `05/02-function-as-a-service`（功能层的 FaaS 复用）
- `06/04-finops-cost`（Serverless 成本分摊模型）
- `01-meta-model-standards/06-formal-axioms/four-layer-ontology.md`（四层架构概念本体）

---

## 概念定义

**定义**：Serverless 架构复用是利用函数即服务（FaaS）与托管服务，将无状态计算、事件处理与后端能力封装为可复用函数与模板。Serverless 的复用单元不是源代码文件，而是**函数模板、事件源映射、共享层（Layer）和 BaaS 服务契约**。

**关键属性**：

| 属性 | 说明 | 复用含义 |
|------|------|---------|
| 事件驱动 | 函数由事件触发 | 事件源映射可在多个函数间复用 |
| 自动扩缩容 | 平台根据负载自动扩展到零或无限 | 容量规划模板可复用 |
| 按使用付费 | 按调用次数和执行时间计费 | 成本模型需要被复用方理解 |
| 无状态 | 函数实例不保存本地状态 | 状态外置到 BaaS，实现跨函数状态复用 |
| 冷启动 | 闲置后首次调用存在延迟惩罚 | 需要预置并发等性能复用策略 |

## 示例

**示例 1：图片处理流水线函数模板**

团队将图片压缩、水印、格式转换实现为标准 Lambda/Cloud Function 模板，并通过 Lambda Layer 共享图像处理库（如 Sharp、Pillow）。新项目通过配置环境变量即可部署一条完整的图片处理流水线，无需重复编写核心逻辑。

**示例 2：Knative 标准化事件源映射**

某企业使用 Knative Eventing 将 GitHub Webhook、Cloud Storage 事件、消息队列统一抽象为事件源（Source）与触发器（Trigger）。不同业务线的函数只需订阅标准化事件类型（如 `com.example.object.created`），即可复用同一事件基础设施。

## 反例

**反例 1：在 Serverless 函数中保留大量长连接与本地状态**

某团队在 Lambda 函数中维护数据库连接池和会话状态，导致冷启动时间长、成本高且难以扩展。函数因状态外置失败而丧失 Serverless 的核心收益。

**反例 2：忽视供应商锁定与隐藏成本**

某初创公司大量使用某云厂商专有的事件格式和 SDK，后续迁移时面临高昂的代码改造费用；同时未监控函数调用频次，导致按量计费账单远超预期。

## 标准/框架映射

| 复用场景 | 标准/框架 | 关键映射点 |
|---------|----------|-----------|
| 无状态函数设计 | 12-Factor App (Processes) | 进程无状态、共享 nothing、状态外置到 BaaS |
| 配置管理 | 12-Factor App (Config) | 配置存储在环境变量，函数模板可跨环境复用 |
| 事件格式标准化 | CNCF CloudEvents 1.0.2 | 跨云、跨函数平台的事件互操作 |
| Kubernetes 原生 Serverless | Knative Serving/Eventing | Revision 版本管理、自动扩缩容、事件路由 |
| 质量模型 | ISO/IEC 25010:2023 Reusability | 函数模板与 Layer 作为可移植复用单元 |

## 分析

Serverless 复用的核心价值在于将无状态计算、事件处理与后端能力封装为可复用模板。成功的 Serverless 复用需要同时满足 12-Factor App 的无状态、配置外置原则，以及 CloudEvents 的事件格式标准化。失败往往源于忽视冷启动成本、在函数中保留状态、或过度依赖单一云厂商专有 API。组织应通过 Golden Path 和共享 Layer 固化最佳实践，同时保留跨云迁移能力。

## 权威来源

| 标准/框架 | 权威 URL | 核查日期 |
|----------|----------|----------|
| CNCF Serverless Whitepaper v2 | <https://github.com/cncf/wg-serverless/tree/main/whitepapers/serverless-overview> | 2026-07-09 |
| CNCF CloudEvents 1.0.2 | <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md> | 2026-07-09 |
| Knative (CNCF Graduated) | <https://knative.dev/> | 2026-07-09 |
| AWS Lambda Developer Guide | <https://docs.aws.amazon.com/lambda/> | 2026-07-09 |
| Azure Functions Documentation | <https://learn.microsoft.com/en-us/azure/azure-functions/> | 2026-07-09 |
| Google Cloud Functions | <https://cloud.google.com/functions/docs> | 2026-07-09 |
| 12-Factor App Methodology | <https://12factor.net/> | 2026-07-09 |
| ISO/IEC 25010:2023 | <https://www.iso.org/standard/78176.html> | 2026-07-09 |

---

> **最后更新**: 2026-07-09
