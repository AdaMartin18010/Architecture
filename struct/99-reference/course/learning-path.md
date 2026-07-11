# 学习路径：从架构复用新手到专家

> **版本**: 2026-07-08
> **目标**: 为不同背景读者提供 4 条递进式学习路径
> **生成命令**: `python scripts/build-deliverables.py`

---

## 路径总览

| 路径 | 适合人群 | 预计学时 | 关键产出 |
|------|----------|----------|----------|
| 🏗️ 架构师路径 | 企业架构师、技术负责人 | 40h | 可复用架构设计文档 |
| 💻 工程师路径 | 软件工程师、DevOps | 35h | 复用组件/服务设计 |
| 🔒 安全工程师路径 | 安全架构师、合规专员 | 25h | 供应链安全评估报告 |
| 🤖 AI 原生路径 | AI 平台工程师、Agent 开发者 | 30h | MCP/A2A 复用方案 |

---

## 按主题学习索引

### 01 元模型与标准对齐

- [核心标准对齐矩阵](../../01-meta-model-standards/01-iso-420xx-family/alignment-matrix.md)
- [ISO/IEC/IEEE AWI 42030 修订跟踪](../../01-meta-model-standards/01-iso-420xx-family/awi-42030-tracking.md)
- [IEEE 1517-2010 软件生命周期复用过程](../../01-meta-model-standards/01-iso-420xx-family/ieee-1517-reuse-processes.md)
- [ISO/IEC/IEEE 12207:2026 与软件复用过程对齐](../../01-meta-model-standards/01-iso-420xx-family/iso-12207-2026-alignment.md)
- [ISO/IEC 25010:2023 AI/ML 质量特性与复用评估](../../01-meta-model-standards/01-iso-420xx-family/iso-25010-2023-ai-quality.md)
- … 共 26 个文件

### 02 业务架构复用

- [01 业务域复用（Business Domain Reuse）](../../02-business-architecture-reuse/01-business-domain-reuse/README.md)
- [业务能力复用](../../02-business-architecture-reuse/02-business-capability/capability-reuse.md)
- [FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射](../../02-business-architecture-reuse/02-business-capability/fea-brm-togaf-mapping.md)
- [价值流复用的形式化组合](../../02-business-architecture-reuse/03-value-stream/value-stream-composition.md)
- [04 业务流程复用（Business Process Reuse）](../../02-business-architecture-reuse/04-business-process-reuse/README.md)
- … 共 15 个文件

### 03 应用架构复用

- [分层架构复用模式](../../03-application-architecture-reuse/01-layered-architecture/layered-architecture-reuse.md)
- [01 分层架构复用](../../03-application-architecture-reuse/01-layered-architecture/README.md)
- [分层架构复用模式](../../03-application-architecture-reuse/01-layered-architecture/reuse-patterns.md)
- [微服务架构复用模式](../../03-application-architecture-reuse/02-microservices/microservices-reuse-patterns.md)
- [02 微服务架构复用](../../03-application-architecture-reuse/02-microservices/README.md)
- … 共 25 个文件

### 04 组件架构复用

- [组件模型与架构复用](../../04-component-architecture-reuse/01-component-models/component-models-reuse.md)
- [接口契约与架构复用](../../04-component-architecture-reuse/02-interface-contracts/interface-contracts-reuse.md)
- [依赖管理与架构复用](../../04-component-architecture-reuse/03-dependency-management/dependency-management-reuse.md)
- [组件接口契约设计模式](../../04-component-architecture-reuse/04-design-patterns/interface-design-patterns.md)
- [组件设计模式选择指南](../../04-component-architecture-reuse/04-design-patterns/pattern-selection-guide.md)
- … 共 11 个文件

### 05 功能架构复用

- [API 设计模式与功能复用](../../05-functional-architecture-reuse/01-api-design/api-design-reuse-patterns.md)
- [函数即服务（FaaS）与功能复用模式](../../05-functional-architecture-reuse/02-function-as-a-service/faas-reuse-patterns.md)
- [事件驱动函数复用模式](../../05-functional-architecture-reuse/03-event-functions/event-driven-function-reuse.md)
- [领域函数目录](../../05-functional-architecture-reuse/04-domain-functions/domain-function-catalog.md)
- [Temporal 工作流复用模式](../../05-functional-architecture-reuse/04-workflow-orchestration/temporal-reuse-patterns.md)
- … 共 10 个文件

### 06 跨层复用治理与成熟度模型

- [跨层复用治理框架](../../06-cross-layer-governance/01-process-governance/cross-layer-governance.md)
- [02 复用过程治理（Reuse Process Governance）](../../06-cross-layer-governance/02-reuse-process/README.md)
- [软件架构复用成熟度评估问卷（SAR-MAQ v1.0）](../../06-cross-layer-governance/03-maturity-models/assessment-questionnaire.md)
- [ISO/IEC 26565:2026 & 26566:2026 正式版与产品线成熟度/纹理管理对齐](../../06-cross-layer-governance/03-maturity-models/iso-26565-26566-final.md)
- [软件复用成熟度模型：RCMM、RiSE-RM 与行业映射](../../06-cross-layer-governance/03-maturity-models/reuse-maturity-models-rcmm-rise.md)
- … 共 24 个文件

### 07 形式化验证与复用正确性

- [T08: A2A Task 状态机的 TLA+ 规约说明](../../07-formal-verification/01-tla-plus/a2a-task-lifecycle.md)
- [TLA+ 案例库总览](../../07-formal-verification/01-tla-plus/case-library.md)
- [T07: MCP Server 能力协商协议的 TLA+ 规约说明](../../07-formal-verification/01-tla-plus/mcp-capability-negotiation.md)
- [T06: 分布式支付服务组件的 TLA+ 规约说明](../../07-formal-verification/01-tla-plus/payment-service.md)
- [T11: 组件依赖无环性验证 (Alloy)](../../07-formal-verification/02-alloy/component-dependency.md)
- … 共 26 个文件

### 08 认知架构与复用决策

- [ACT-R 认知架构与知识复用](../../08-cognitive-architecture/01-act-r-model/act-r-cognitive-reuse.md)
- [BDI 智能体架构与复用模式](../../08-cognitive-architecture/02-bdi-model/bdi-agent-reuse.md)
- [认知负荷理论与架构复用](../../08-cognitive-architecture/03-cognitive-load-theory/cognitive-load-theory.md)
- [DORA 2025 认知负荷与复用采纳率](../../08-cognitive-architecture/03-cognitive-load-theory/dora-2025-cognitive-load.md)
- [开发者复用决策的认知负荷量化模型](../../08-cognitive-architecture/03-cognitive-load-theory/quantitative-model.md)
- … 共 10 个文件

### 09 价值量化与 ROI 模型

- [COCOMO II 复用模型 2026 校准版](../../09-value-quantification/01-cocomo-ii-reuse/cocomo-2026-calibration.md)
- [COCOMO II 复用模型深度解析](../../09-value-quantification/01-cocomo-ii-reuse/cocomo-ii-reuse-model-deep-dive.md)
- [架构复用 ROI 框架](../../09-value-quantification/02-roi-npv-models/roi-framework.md)
- [软件复用的 ROI、实物期权与战略价值量化](../../09-value-quantification/02-roi-npv-models/roi-real-options-strategic-value.md)
- [价值量化碳维度扩展：SCI 复用碳模型](../../09-value-quantification/03-carbon-dimension/sci-reuse-value-extension.md)
- … 共 7 个文件

### 10 供应链安全工程

- [OpenSSF Scorecard + Security Baseline 与复用决策](../../10-supply-chain-security/01-slsa-framework/openssf-scorecard-reuse.md)
- [SLSA 1.2 Multi-Track 深度解析](../../10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md)
- [SLSA L4 分布式构建验证实践](../../10-supply-chain-security/01-slsa-framework/slsa-l4-distributed-builds.md)
- [SLSA v1.2 多轨道复用安全边界详解](../../10-supply-chain-security/01-slsa-framework/slsa-reuse-boundaries.md)
- [SBOM 格式对比：SPDX vs CycloneDX vs SWID](../../10-supply-chain-security/02-sbom-standards/sbom-comparison.md)
- … 共 25 个文件

### 11 工业 IoT / OT-IT 融合复用

- [ISA-95 五层跨层数据流映射](../../11-industrial-iot-otit/01-isa-95-model/cross-layer-matrix/data-flow-mapping.md)
- [ISA-95 资产目录深度清单](../../11-industrial-iot-otit/01-isa-95-model/isa-95-asset-catalog-deep-dive.md)
- [ISO/IEC 30141:2024 IoT 参考架构对齐](../../11-industrial-iot-otit/01-isa-95-model/iso-30141-iot-ra-alignment.md)
- [L0 现场层复用资产目录](../../11-industrial-iot-otit/01-isa-95-model/l0-field/asset-catalog.md)
- [L1 控制层复用资产目录](../../11-industrial-iot-otit/01-isa-95-model/l1-control/asset-catalog.md)
- … 共 39 个文件

### 12 AI 原生复用

- [MCP 2025-11-25 权威规范解读](../../12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-authoritative.md)
- [MCP 2025-11-25 综合更新与复用影响评估](../../12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-comprehensive-update.md)
- [MCP 2025-11-25 规范深度解析](../../12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-deep-dive.md)
- [MCP 2026-07-28 RC 深度解析](../../12-ai-native-reuse/01-mcp-protocol/mcp-2026-deep-dive.md)
- [MCP 2026-07-28 RC → 正式版迁移指南](../../12-ai-native-reuse/01-mcp-protocol/mcp-2026-transition-guide.md)
- … 共 22 个文件

### 13 新兴趋势

- [内部开发者平台 (IDP) 与架构复用](../../13-emerging-trends/01-platform-engineering/idp-reuse.md)
- [平台工程与内部开发者平台（IDP）复用](../../13-emerging-trends/01-platform-engineering/platform-engineering-cncf-2026.md)
- [平台工程深化：CNCF 毕业项目与 IDP AI 集成](../../13-emerging-trends/01-platform-engineering/platform-engineering-deep-dive.md)
- [平台工程成熟度模型（Platform Engineering Maturity Model）](../../13-emerging-trends/01-platform-engineering/platform-maturity-model.md)
- [模块化单体：复用的务实选择](../../13-emerging-trends/02-modular-monolith/modular-monolith-reuse.md)
- … 共 18 个文件

### 99 参考索引

- [Phase C 对齐矩阵与 A+B+C 累计汇总](../../99-reference/alignment-matrix-phase-c.md)
- [2026-06-06 本轮完成统计报告](../../99-reference/audit/2026-06-06-completion-stats.md)
- [《软件工程架构复用视角》全面差距分析报告](../../99-reference/audit/comprehensive-gap-analysis-2026-06-08.md)
- [内容事实勘误与权威来源对齐报告（2026-07-07）](../../99-reference/audit/content-fact-fix-2026-07.md)
- [交叉引用有效性检查报告](../../99-reference/audit/cross-reference-audit.md)
- … 共 54 个文件
