# Serverless 架构复用模式

> **版本**: 2026-06-08
> **定位**: 应用架构层（Level 2）—— FaaS 函数复用边界、事件源模式与冷启动权衡
> **对齐标准**: CNCF Serverless Whitepaper v2
> **状态**: ⏳ 框架填充中

---

## 1. 核心概念

Serverless 架构将计算抽象为**事件触发的无状态函数**，开发者无需管理服务器生命周期。从复用视角看，Serverless 的复用单元从"服务"进一步细化为"函数"和"事件处理管道"。

CNCF Serverless Whitepaper v2 定义了 Serverless 的核心特征：**自动伸缩、按调用计费、无服务器管理、事件驱动**。这些特征直接影响复用策略：函数的短暂生命周期要求复用单元必须是**快速初始化、无状态、幂等**的。

### 1.1 函数复用的层次

| 层次 | 复用单元 | 生命周期 | 典型示例 |
|------|---------|---------|---------|
| 函数代码 | 单一处理逻辑 | 毫秒级 | 图片缩略图生成 |
| 函数层/Layer | 共享依赖库 | 部署级 | 认证 SDK、监控 Agent |
| 事件管道 | 触发器→函数→输出 | 流级 | S3 上传 → Lambda → DynamoDB |
| 应用模板 | 完整 Serverless 应用骨架 | 项目级 | SAM / Terraform 模板 |

---

## 2. 核心复用模式

### 2.1 函数即复用单元（Function-as-Reuse-Unit）

单个函数在满足以下条件时可作为跨项目复用单元：

- **纯函数特性**: 输出仅取决于输入事件 + 环境变量，无隐式状态
- **幂等性**: 同一事件多次触发产生相同结果（应对至少一次交付语义）
- **超时可控**: 执行时间 < 平台限制（AWS Lambda: 15 min, Azure Functions: 无默认限制）

> **定理 S.1** (Serverless Reuse Threshold): 一个 Serverless 函数的复用收益为正当且仅当其**冷启动延迟 + 执行时间 < 调用方可容忍的响应时间上限**。

### 2.2 事件源复用模式

Serverless 的复用不仅限于代码，更包括**事件源（Event Source）与事件模式的复用**。

| 事件源类型 | 复用模式 | 典型场景 |
|-----------|---------|---------|
| 对象存储事件 | S3/ Blob 触发器模板 | 文件处理流水线 |
| 消息队列事件 | Kafka / SQS / Event Hubs 触发 | 异步任务消费 |
| HTTP API 事件 | API Gateway → Function 路由 | REST/GraphQL 后端 |
| 定时事件 | Cron 触发器模板 | 批处理、数据同步 |
| 数据库变更事件 | CDC (Change Data Capture) | 数据复制、缓存失效 |

**事件契约复用**: 定义标准的事件 Schema（如 CloudEvents 规范），使同一函数可消费来自不同源的事件。

### 2.3 层（Layer）与镜像复用

- **函数层**: 将公共依赖（如 AWS SDK、数据处理库）打包为层，供多个函数挂载
- **容器镜像**: 对于需要自定义运行时的场景，使用 OCI 镜像作为复用单元（AWS Lambda / Azure Functions / Knative 均支持）

---

## 3. 冷启动与性能权衡

冷启动（Cold Start）是 Serverless 复用决策的核心约束。

| 运行时类型 | 冷启动延迟 | 复用建议 |
|-----------|-----------|---------|
| 原生运行时 (Go, Rust) | 10-100 ms | 高并发场景首选，复用价值最高 |
| JIT 运行时 (Java, .NET) | 1-5 s | 使用 SnapStart / Provisioned Concurrency |
| 解释型 (Node.js, Python) | 100-500 ms | 通用场景，平衡开发效率与性能 |
| 自定义容器 | 2-10 s | 仅当原生运行时无法满足依赖需求时使用 |

### 3.1 预置并发（Provisioned Concurrency）的复用经济学

预置并发通过**保持函数实例常驻**消除冷启动，但将计费模型从"纯按调用"转变为"按调用 + 按容量预留"。

- **决策公式**: 当函数调用频率 > 阈值时，预置并发的单位调用成本低于冷启动的延迟惩罚成本
- **复用启示**: 高频复用的函数应配置预置并发；低频复用的函数接受冷启动

---

## 4. 跨平台复用约束

| 约束维度 | 影响 |
|---------|------|
| 事件格式 | 不同云平台的事件 Schema 差异（需 CloudEvents 抽象层） |
| 执行环境变量 | 密钥管理、配置注入机制各异 |
| 并发限制 | 平台级并发配额影响复用规模 |
| 最大执行时长 | 长任务需拆分为 Step Functions / Durable Functions |

---

> 最后更新: 2026-06-08
> 权威来源:
>
> - <https://github.com/cncf/wg-serverless/blob/master/whitepapers/serverless-overview.md>
> - <https://cloudevents.io/> (CloudEvents Specification)
> - <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html>
