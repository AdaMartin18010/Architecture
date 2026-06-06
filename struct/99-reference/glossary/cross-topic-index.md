# 跨主题综合索引
>
> 版本: 2026-06-06
> 定位: 全知识库 13 个主题的交叉引用枢纽

## 1. 按标准组织的交叉引用

### ISO/IEC/IEEE 42010:2022

- `01-meta-model-standards/01-iso-420xx-family/iso-42010-2022-update.md` — 术语变更
- `01-meta-model-standards/02-togaf-10-alignment/togaf-enterprise-continuum-reuse.md` — TOGAF 与 ISO 42010 映射

### ISO/IEC 25010:2023

- `01-meta-model-standards/01-iso-420xx-family/iso-25010-2023-update.md` — 九大特性
- `06-cross-layer-governance/02-quality-governance/` — 质量门禁映射

### ISO 26550 系列（软件产品线）

- `01-meta-model-standards/03-iso-26550-ple/` — 参考模型
- `04-component-architecture-reuse/` — 组件复用实践
- `06-cross-layer-governance/03-maturity-models/reuse-maturity-models-rcmm-rise.md` — 成熟度评估

### NIST SP 800-204 系列

- `03-application-architecture-reuse/05-cloud-native-patterns/nist-sp-800-204-microservices-security.md` — 微服务安全
- `10-supply-chain-security/05-case-studies/nist-ssdf-1-2-alignment.md` — SSDF 1.2

### MCP / A2A

- `12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-authoritative.md` — MCP 规范
- `12-ai-native-reuse/02-a2a-protocol/a2a-v1-authoritative.md` — A2A 规范
- `05-functional-architecture-reuse/05-ai-llm-functions/llm-function-reuse-patterns.md` — 函数复用模式
- `08-cognitive-architecture/02-bdi-model/bdi-agent-reuse.md` — BDI 与 MCP/A2A 语义映射

## 2. 按技术领域的交叉引用

### 微服务与服务网格

- `03-application-architecture-reuse/05-cloud-native-patterns/nist-sp-800-204-microservices-security.md`
- `03-application-architecture-reuse/06-service-mesh/gateway-api-gamma-2026.md`
- `03-application-architecture-reuse/07-eda-cqrs/eda-cqrs-event-sourcing-patterns.md`
- `13-emerging-trends/01-platform-engineering/platform-engineering-cncf-2026.md`

### 事件驱动与 CQRS

- `03-application-architecture-reuse/07-eda-cqrs/eda-cqrs-event-sourcing-patterns.md`
- `02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md` — BPMN 事件子流程
- `11-industrial-iot-otit/04-plcopen-motion/plcopen-motion-control.md` — 工业事件驱动

### 数据架构

- `03-application-architecture-reuse/04-data-architecture/data-mesh-data-product-reuse.md`
- `01-meta-model-standards/02-togaf-10-alignment/togaf-enterprise-continuum-reuse.md` — 数据架构交付物

### 功能安全

- `11-industrial-iot-otit/06-functional-safety/iec-61508/iec-61508-ed3-reuse.md`
- `11-industrial-iot-otit/06-functional-safety/iso-26262/iso-26262-seooc-reuse.md`
- `07-formal-verification/05-spark-ada/spark-ada-do333-industrial.md`
- `07-formal-verification/06-b-method/event-b-railway-refinement.md`

### AI 与智能体

- `12-ai-native-reuse/` — 全部子主题
- `05-functional-architecture-reuse/05-ai-llm-functions/llm-function-reuse-patterns.md`
- `08-cognitive-architecture/` — ACT-R / BDI
- `11-industrial-iot-otit/07-edge-ai/tinyml-onnx-edge-ai.md` — 边缘 AI

### 供应链安全

- `10-supply-chain-security/` — 全部子主题
- `04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md`

## 3. 按复用层次的交叉引用

| 复用层次 | 代表文档 |
|---------|---------|
| **元模型/标准** | `01-meta-model-standards/` 全部 |
| **业务架构** | `02-business-architecture-reuse/` + BPMN/DMN 文件 |
| **应用架构** | `03-application-architecture-reuse/` + Data Mesh + EDA/CQRS + Service Mesh |
| **数据架构** | `03-application-architecture-reuse/04-data-architecture/data-mesh-data-product-reuse.md` |
| **组件架构** | `04-component-architecture-reuse/` + 开源供应链 |
| **功能架构** | `05-functional-architecture-reuse/` + LLM 函数 |
| **跨层治理** | `06-cross-layer-governance/` + FinOps + 成熟度模型 |
| **形式化验证** | `07-formal-verification/` — SPARK + Event-B + Rust |
| **认知架构** | `08-cognitive-architecture/` — ACT-R + BDI |
| **价值量化** | `09-value-quantification/` + COCOMO II + ROI/Real Options |
| **供应链安全** | `10-supply-chain-security/` — SLSA + SBOM + EU CRA |
| **工业 IoT** | `11-industrial-iot-otit/` — OPC UA + TSN + PLCopen + AAS + 功能安全 + Edge AI |
| **AI 原生复用** | `12-ai-native-reuse/` — MCP + A2A + 智能体基础设施 |
| **新兴趋势** | `13-emerging-trends/` — Platform Engineering + WASM + Rust |

## 4. 快速查找表：常见问题 → 文档

| 问题 | 推荐文档 |
|-----|---------|
| "ISO 42010:2022 改了什么术语？" | `iso-42010-2022-update.md` |
| "如何评估复用成熟度？" | `reuse-maturity-models-rcmm-rise.md` |
| "MCP 官方稳定版是哪个？" | `mcp-2025-11-25-authoritative.md` |
| "SLSA 1.2 的多轨道是什么意思？" | `slsa-1-1-1-2-update.md` |
| "EU CRA 的合规时间表？" | `eu-cra-compliance.md` |
| "A2A v1.0 什么时候发布的？" | `a2a-v1-authoritative.md` |
| "IEC 63278 AAS 路线图？" | `iec-63278-roadmap.md` |
| "PLCopen 运动控制状态机？" | `plcopen-motion-control.md` |
| "SPARK Ada 如何替代 DO-178C 测试？" | `spark-ada-do333-industrial.md` |
| "Event-B 在铁路信号中的应用？" | `event-b-railway-refinement.md` |
| "FinOps 单位经济学怎么算？" | `finops-unit-economics-2026.md` |
| "平台工程成熟度模型？" | `platform-engineering-cncf-2026.md` |
| "WASM Component Model 进展？" | `wasm-component-model-2026.md` |
| "COCOMO II 复用模型方程？" | `cocomo-ii-reuse-model-deep-dive.md` |
| "NIST 微服务安全策略？" | `nist-sp-800-204-microservices-security.md` |
| "Gateway API 替代 Ingress？" | `gateway-api-gamma-2026.md` |
| "Data Mesh 2026 实践模式？" | `data-mesh-data-product-reuse.md` |
| "BPMN 如何编排 AI Agent？" | `bpmn-dmn-reuse-orchestration.md` |
| "开源供应链怎么治理？" | `open-source-supply-chain-reuse.md` |
| "软件复用的实物期权方法？" | `roi-real-options-strategic-value.md` |

## 5. 参考索引

- `struct/README.md` — 主索引
- `struct/MASTER_PLAN.md` — 实施路线图
- `struct/99-reference/standards-index/master-alignment-matrix.md` — 标准对齐矩阵
- `struct/99-reference/glossary/terminology-crosswalk.md` — 术语交叉对照
- `struct/99-reference/CHANGELOG.md` — 更新日志与勘误
