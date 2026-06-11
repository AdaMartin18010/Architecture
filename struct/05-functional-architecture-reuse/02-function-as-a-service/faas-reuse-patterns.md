# 函数即服务（FaaS）与功能复用模式

> **版本**: 2026-06-10
> **定位**: 功能架构层 —— 无服务器函数的复用特征、粒度边界与可移植性实践
> **对齐标准**: CNCF Serverless Workflow, OpenFunction, Knative, AWS Lambda, Azure Functions, Google Cloud Functions
> **状态**: ✅ 已完成

---

## 目录

- [函数即服务（FaaS）与功能复用模式](#函数即服务faas与功能复用模式)
  - [目录](#目录)
  - [1. FaaS 概述](#1-faas-概述)
    - [1.1 主流 FaaS 平台](#11-主流-faas-平台)
    - [1.2 FaaS 核心特征](#12-faas-核心特征)
  - [2. FaaS 函数的复用特征](#2-faas-函数的复用特征)
    - [2.1 函数作为最小复用单元](#21-函数作为最小复用单元)
    - [2.2 函数接口标准化](#22-函数接口标准化)
  - [3. 函数复用的粒度边界](#3-函数复用的粒度边界)
    - [3.1 粒度选择矩阵](#31-粒度选择矩阵)
    - [3.2 CNCF Serverless Workflow](#32-cncf-serverless-workflow)
  - [4. FaaS 函数的可移植性](#4-faas-函数的可移植性)
    - [4.1 可移植性挑战](#41-可移植性挑战)
    - [4.2 跨平台复用策略](#42-跨平台复用策略)
  - [5. FaaS 函数的供应链安全](#5-faas-函数的供应链安全)
    - [5.1 部署包完整性](#51-部署包完整性)
    - [5.2 运行时隔离](#52-运行时隔离)
  - [6. 案例：使用 AWS Lambda Layers 和 Knative 实现跨平台函数复用](#6-案例使用-aws-lambda-layers-和-knative-实现跨平台函数复用)
    - [6.1 场景](#61-场景)
    - [6.2 AWS Lambda 实现](#62-aws-lambda-实现)
    - [6.3 Knative 实现](#63-knative-实现)
    - [6.4 复用价值](#64-复用价值)
  - [7. 权威来源](#7-权威来源)

---

## 1. FaaS 概述

### 1.1 主流 FaaS 平台

| 平台 | 提供商 | 运行时支持 | 冷启动 | 最大执行时间 | 特色功能 |
|:---|:---|:---|:---:|:---:|:---|
| **AWS Lambda** | Amazon | 15+ 语言 | ~100ms | 15 分钟 | Lambda Layers, Provisioned Concurrency |
| **Azure Functions** | Microsoft | .NET, Node, Python, Java, Go | ~200ms | 10 分钟 | Durable Functions, Premium Plan |
| **Google Cloud Functions** | Google | Node, Python, Go, Java, Ruby, PHP | ~200ms | 60 分钟 | CloudEvents 原生支持 |
| **Knative** | CNCF (开源) | 任何容器 | ~500ms | 无限制 | K8s 原生、多云可移植 |
| **OpenFaaS** | 开源 | 任何容器/二进制 | ~1s | 无限制 | 社区活跃、易于部署 |
| **Fission** | 开源 | 任何容器 | ~100ms | 无限制 | K8s 原生、快速启动 |

### 1.2 FaaS 核心特征

| 特征 | 描述 | 复用影响 |
|:---|:---|:---|
| **无状态** | 函数不保存请求间的状态 | 函数可被任意实例执行，天然可复用 |
| **事件驱动** | 由事件触发执行 | 函数可与多种事件源组合复用 |
| **短生命周期** | 执行完成后资源释放 | 快速迭代，版本更新成本低 |
| **自动伸缩** | 从零到多自动扩展 | 复用函数可按需分配资源 |
| **按调用付费** | 仅对实际执行付费 | 降低复用成本门槛 |

---

## 2. FaaS 函数的复用特征

### 2.1 函数作为最小复用单元

```
FaaS 函数复用层次
├── L1: 单个函数复用
│   └── 直接调用部署好的函数端点
│   └── 例：调用文本翻译函数
├── L2: 函数模板复用
│   └── 复用函数的代码框架和配置模板
│   └── 例：复用"HTTP 触发 + 数据库写入"模板
├── L3: 函数编排复用
│   └── 复用预定义的函数工作流
│   └── 例：复用"图片上传 → 缩略图生成 → CDN 分发"流水线
└── L4: 函数平台能力复用
    └── 复用 FaaS 平台的通用能力（认证、日志、监控）
    └── 例：复用平台的 OIDC 认证中间件
```

### 2.2 函数接口标准化

```
标准化函数接口（以 CloudEvents 为例）
{
  "specversion": "1.0",
  "type": "com.example.order.created",
  "source": "/order-service",
  "id": "A234-1234-1234",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "ORD-12345",
    "amount": 99.99
  }
}
```

**复用价值**: 基于 CloudEvents 的函数可在不同云平台间移植。

---

## 3. 函数复用的粒度边界

### 3.1 粒度选择矩阵

| 粒度 | 示例 | 优点 | 缺点 | 复用场景 |
|:---|:---|:---|:---|:---|
| **单函数** | 发送邮件 | 简单、独立 | 功能有限 | 通用工具函数 |
| **函数链** | 验证 → 处理 → 存储 | 模块化 | 编排复杂 | 业务流程 |
| **函数工作流** | 订单处理全流程 | 端到端 | 紧耦合 | 完整业务场景 |

### 3.2 CNCF Serverless Workflow

**定义**: 标准化的无服务器工作流规范，支持 DSL（YAML/JSON）定义函数编排。

```yaml
# Serverless Workflow 示例
id: order-processing
version: '1.0'
functions:
  - name: validateOrder
    operation: http://order-service/validate
  - name: processPayment
    operation: http://payment-service/process
  - name: sendNotification
    operation: http://notification-service/send
states:
  - name: Validate
    type: operation
    actions:
      - functionRef: validateOrder
    transition: ProcessPayment
  - name: ProcessPayment
    type: operation
    actions:
      - functionRef: processPayment
    transition: SendNotification
  - name: SendNotification
    type: operation
    actions:
      - functionRef: sendNotification
    end: true
```

---

## 4. FaaS 函数的可移植性

### 4.1 可移植性挑战

| 维度 | 平台差异 | 可移植方案 |
|:---|:---|:---|
| **触发器** | HTTP / S3 / Kafka / Timer | CloudEvents 抽象 |
| **上下文** | 平台特定的上下文对象 | 标准化上下文接口 |
| **状态管理** | DynamoDB / Cosmos DB / Firestore | 外部状态存储（Redis、数据库） |
| **依赖管理** | Layers / 容器 / 内置 | 容器化部署 |
| **配置** | 环境变量 / Secrets Manager | 标准化配置注入 |

### 4.2 跨平台复用策略

```
跨平台 FaaS 复用策略
├── 容器化
│   └── 使用 OCI 容器打包函数
│   └── 任何支持容器的平台可运行
├── CloudEvents
│   └── 标准化事件格式
│   └── 触发器与函数解耦
├── 无供应商锁定框架
│   └── Serverless Framework
│   └── Pulumi / Terraform
└── Knative（开源标准）
    └── K8s 原生 FaaS
    └── 多云可移植
```

---

## 5. FaaS 函数的供应链安全

### 5.1 部署包完整性

- **签名验证**: 部署包必须经过签名验证
- **SBOM**: 函数依赖必须提供 SBOM
- **最小权限**: 函数执行角色遵循最小权限原则

### 5.2 运行时隔离

| 隔离级别 | 实现 | 安全性 |
|:---|:---|:---:|
| **进程隔离** | 传统容器 | 🟡 中 |
| **沙箱隔离** | gVisor, Firecracker | 🟢 高 |
| **WASM 隔离** | Wasmtime, WasmEdge | 🟢 高 |
| **硬件隔离** | 机密计算（SGX, SEV） | 🟢 极高 |

---

## 6. 案例：使用 AWS Lambda Layers 和 Knative 实现跨平台函数复用

### 6.1 场景

通用日志处理函数，需要在 AWS 和私有 K8s 集群中复用。

### 6.2 AWS Lambda 实现

```python
# app.py
import json
import logging

def handler(event, context):
    """CloudEvents 兼容的日志处理函数"""
    # 解析 CloudEvent
    cloud_event = json.loads(event['body'])

    # 处理日志
    processed = process_log(cloud_event.data)

    # 发送到下游
    send_to_downstream(processed)

    return {
        'statusCode': 200,
        'body': json.dumps({'processed': True})
    }

def process_log(data):
    # 通用日志处理逻辑
    return data.upper()

def send_to_downstream(data):
    # 抽象的发送接口
    pass
```

### 6.3 Knative 实现

```yaml
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: log-processor
spec:
  template:
    spec:
      containers:
        - image: gcr.io/project/log-processor:v1
          env:
            - name: DOWNSTREAM_URL
              value: http://downstream-service
```

### 6.4 复用价值

- 业务逻辑（`process_log`）完全复用
- 通过 CloudEvents 实现触发器抽象
- 通过环境变量实现配置外部化

---

## 7. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| CNCF Serverless Workflow | <https://serverlessworkflow.io/> | 2026-06-10 |
| Knative | <https://knative.dev/> | 2026-06-10 |
| CloudEvents | <https://cloudevents.io/> | 2026-06-10 |
| AWS Lambda | <https://docs.aws.amazon.com/lambda/> | 2026-06-10 |
| Azure Functions | <https://docs.microsoft.com/azure/azure-functions/> | 2026-06-10 |
| OpenFunction | <https://openfunction.dev/> | 2026-06-10 |
