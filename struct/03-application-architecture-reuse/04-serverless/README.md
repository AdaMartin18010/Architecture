# 03 Serverless 架构复用

> **版本**: 2026-07-07
> **定位**: 03 应用架构复用的基础子主题 — Serverless / FaaS 架构的复用模式
> **对齐**: CNCF Serverless Whitepaper v2, AWS/Azure/GCP 官方文档
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

## 关联主题

- `03/02-microservices`（Serverless 作为微服务的极端粒度）
- `05/02-function-as-a-service`（功能层的 FaaS 复用）
- `06/04-finops-cost`（Serverless 成本分摊模型）
- `01-meta-model-standards/06-formal-axioms/four-layer-ontology.md`（四层架构概念本体）

---

> **权威来源**:
>
> - CNCF. *Serverless Whitepaper v2*.
> - AWS. *AWS Lambda Developer Guide*.
> - Microsoft. *Azure Functions Documentation*.
> - Roberts, M. (2018). *Serverless Architectures*.
>
> **核查日期**: 2026-07-07


---

## 补充说明：03 Serverless 架构复用

## 概念定义

**定义**：Serverless 架构复用是利用函数即服务（FaaS）与托管服务，将无状态计算、事件处理与后端能力封装为可复用函数与模板。

## 示例

**示例**：团队将图片处理、PDF 生成、Webhook 转换实现为标准 Lambda/Cloud Function 模板，新项目通过配置环境变量即可部署。

## 反例

**反例**：在 Serverless 函数中保留大量长连接与本地状态，导致冷启动时间长、成本高且难以扩展。

## 分析

**分析**：Serverless 复用适合事件驱动、短时无状态任务，需警惕供应商锁定与隐藏成本。
