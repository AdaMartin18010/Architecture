# 更新日志

> **版本**: 2026-06-06
> **定位**: 记录知识库的重大更新、勘误和权威来源对齐

---

## 2026-06-06 Phase 1.5 修复（用户确认 1A/2A/3A/4A/5A 后执行）

### 修复内容

#### 目录结构与一致性

- 重写 `struct/README.md` — 以实际 `struct/` 目录结构为准，明确标注与早期 MASTER_PLAN 规划树的差异
- 清理 `.vscode/README.md` — 删除约 200 行 PostgreSQL 18+ 残留内容，恢复为 VSCode/Cursor 配置说明
- 更新 `struct/MASTER_PLAN.md` — 修正 FinOps 实际路径、MCP 版本引用（2025-11-25）、SLSA 版本引用（1.1/1.2），添加 `SUBSEQUENT_PLAN_2026.md` 链接和关键决策确认
- 更新 `struct/99-reference/audit/roadmap-consistency-audit.md` — 追加修复记录

#### 形式化验证环境

- 创建 `struct/99-reference/tools/formal-verification-env/`:
  - `README.md` — 环境使用说明
  - `docker-compose.yml` — TLA+/Alloy/Coq/Isabelle 四容器配置
  - `verify-all.sh` — 批量检查脚本
- 创建 `struct/07-formal-verification/03-coq-isabelle/README.md` — Coq/Isabelle 占位与 Phase 2 计划
- 更新 `struct/07-formal-verification/README.md` — 添加验证环境引用和验收标准
- 更新 `struct/07-formal-verification/plans-tasks/roadmap.md` — 修正目录结构声明，移除不存在的 `07-model-checking`

### 关键决策

- **1A**: 目录结构以实际文件为准
- **2A**: Docker 化形式化验证环境，新增规约必须自动验证
- **3A**: 可执行工具采用 Python CLI + Streamlit
- **4A**: 重点补齐 CP+形式化、WASI 0.3、Agentic Governance；暂缓量子计算
- **5A**: 每篇文档列出 1-3 个国际权威来源 URL

---

## Phase 2 持续推进（2026-06）— 国际权威内容对齐

### 新增标准对齐文档

#### 元模型与标准对齐

- `07-omg-ras/ras-alignment.md` — 对齐 OMG RAS v2.2（formal/05-11-02），覆盖 Core RAS 四元组（Classification/Solution/Usage/RelatedAssets）、Profile 扩展、`.ras` 包格式、仓库服务接口，以及与 ISO 42010 / TOGAF 的映射
- `08-fair4rs/fair4rs-alignment.md` — 对齐 FAIR4RS Principles v1.0 (RDA, 2022)，覆盖 F/A/I/R 17 条子原则、与 SBOM/MCP/容器注册表的整合、架构资产 FAIR4RS 合规行动清单
- `01-iso-420xx-family/ieee-1517-reuse-processes.md` — 对齐 IEEE 1517-2010 软件生命周期复用过程，映射 Domain Engineering / Reuse Asset Management / Reuse Program Management 与 ISO 12207 / 42020 / TOGAF ADM

#### AI 原生复用

- `01-mcp-protocol/mcp-2025-11-25-deep-dive.md` — **关键勘误**：将项目中所有 "MCP 2026-07-28 RC" 引用更新为官方当前稳定版 **MCP 2025-11-25**。深度解析 Tasks、Icons、Sampling with Tools、Elicitation URL 模式、OAuth 企业级增强、Linux Foundation Agentic AI Foundation 治理变化

### 新增可执行工具原型

- `99-reference/tools/terminology-query.py` — 跨标准术语查询 CLI（ISO 42010 / ISO 25010 / TOGAF / SLSA / MCP / A2A）
- `99-reference/tools/cocomo-calculator.py` — COCOMO II 复用模型 2026 版计算器
- `12-ai-native-reuse/04-probabilistic-contracts/calibration-tool.py` — 基于 **Conformal Prediction** 的 AI 功能概率契约校准工具，输出 P(correctness) ≥ 1-α 的统计保证
- `06-cross-layer-governance/03-maturity-models/assessment-tool.py` — 基于 **ISO/IEC 26566:2026 / RCMM / RiSE / NASA RRL** 的复用成熟度评估问卷 CLI，生成分维度雷达图和总体成熟度报告

### 更新的 README/状态

- `struct/01-meta-model-standards/README.md` — 新增 OMG RAS、FAIR4RS、IEEE 1517 内容
- `struct/12-ai-native-reuse/README.md` — 修正 MCP 版本为 2025-11-25，添加 calibration-tool 状态
- `struct/05-functional-architecture-reuse/README.md` — 修正 MCP 版本引用
- `struct/06-cross-layer-governance/README.md` — 标记成熟度评估问卷 CLI 已完成

### 对齐的权威来源

- OMG RAS v2.2 formal/05-11-02: <https://www.omg.org/spec/RAS/2.2/PDF>
- FAIR4RS v1.0 (RDA, 2022): <https://doi.org/10.15497/RDA00068>
- IEEE 1517-2010: <https://standards.ieee.org/standard/1517-2010.html>
- MCP 2025-11-25 Spec: <https://modelcontextprotocol.io/specification/2025-11-25>
- MCP Linux Foundation Governance: <https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation>
- Angelopoulos & Bates, "A Gentle Introduction to Conformal Prediction" (2021): <https://arxiv.org/abs/2107.07511>
- ISO/IEC 26566:2026: <https://www.iso.org/standard/81437.html>

---

## 2026-06-06 本轮更新

### 新增文档

#### 元模型与标准对齐

- `iso-42010-2022-update.md` — 对齐 ISO 42010:2022 第二版关键变更（EoI、ADF、View Component、Aspect、Perspective）
- `iso-25010-2023-update.md` — 对齐 ISO 25010:2023 九大质量特性

#### 供应链安全

- `slsa-1-1-1-2-update.md` — 对齐 SLSA 1.1/1.2 多轨道模型（Build/Source/Attested Build Environments）
- `nist-ssdf-1-2-alignment.md` — 对齐 NIST SSDF 1.2 征求意见稿
- `eu-cra-compliance.md` — 对齐欧盟网络弹性法案（EU CRA）

#### 工业 IoT

- `iec-63278-roadmap.md` — 对齐 IEC 63278 AAS 系列标准路线图
- `iec-ieee-60802-profile.md` — 对齐 IEC/IEEE 60802 TSN 工业自动化配置文件
- `plcopen-motion-control.md` — 对齐 PLCopen Motion Control Part 1–4 + Safety，状态机与功能块复用
- `iec-61508-ed3-reuse.md` — 对齐 IEC 61508 功能安全与 Proven-In-Use 复用路径
- `iso-26262-seooc-reuse.md` — 对齐 ISO 26262 SEooC 与安全合同驱动的软件组件复用
- `tinyml-onnx-edge-ai.md` — 对齐 TinyML / Edge AI 模型复用技术栈

#### AI 原生复用

- `mcp-2025-11-25-authoritative.md` — 基于官方规范解读 MCP 2025-11-25
- `a2a-v1-authoritative.md` — 对齐 A2A v1.0 正式发布版本
- `owasp-llm-mcp-security.md` — 对齐 OWASP LLM/MCP/Agentic AI Top 10

#### 形式化验证

- `spark-ada-do333-industrial.md` — 对齐 SPARK Ada + DO-178C/DO-333 工业形式验证替代测试
- `event-b-railway-refinement.md` — 对齐 Event-B / B Method 铁路信号精化复用

#### 新兴趋势

- `platform-engineering-cncf-2026.md` — 对齐 CNCF 平台工程成熟度模型、Golden Path、IDP
- `wasm-component-model-2026.md` — 对齐 WebAssembly Component Model、WASI 0.3/1.0、wasmCloud
- `rust-wasm-formal-verification.md` — 对齐 Rust 类型系统、Kani/Miri、WASM 组件开发

#### 元模型与标准对齐

- `togaf-enterprise-continuum-reuse.md` — 对齐 TOGAF 10 企业连续体、ABB/SBB、架构仓库与 ISO 42010:2022 映射

#### 应用架构复用

- `nist-sp-800-204-microservices-security.md` — 对齐 NIST SP 800-204 系列微服务安全策略（五种代码类型、MS-SS 策略、DevSecOps）
- `gateway-api-gamma-2026.md` — 对齐 CNCF Gateway API / GAMMA、Istio Ambient Multicluster Beta、AI 推理扩展
- `eda-cqrs-event-sourcing-patterns.md` — 对齐 EDA/CQRS/Event Sourcing/Saga 模式与云原生实现栈
- `data-mesh-data-product-reuse.md` — 对齐 Data Mesh 四原则、数据产品、2026 IDP-for-data 合成模式

#### 业务架构复用

- `bpmn-dmn-reuse-orchestration.md` — 对齐 OMG BPMN 2.0.2 / DMN 1.5 业务过程与决策复用编排

#### 组件架构复用

- `open-source-supply-chain-reuse.md` — 对齐 NIST SP 800-161r1、OWASP SCVS、开源供应链治理与 SBOM 全生命周期

#### 功能架构复用

- `llm-function-reuse-patterns.md` — 对齐 LLM Function Calling、MCP Tool、A2A Agent Card、Microsoft Agent Framework

#### 跨层治理

- `finops-unit-economics-2026.md` — 对齐 FinOps 框架、单位经济学、Cloud COGS、AI 成本管理
- `reuse-maturity-models-rcmm-rise.md` — 对齐 RCMM、RiSE-RM、CMMI、Koltun-Hudson、Automotive SPICE 复用成熟度

#### 价值量化

- `cocomo-ii-reuse-model-deep-dive.md` — 对齐 COCOMO II 复用模型方程、AAM/SU/UNFM 参数、本地校准方法
- `roi-real-options-strategic-value.md` — 对齐软件复用 ROI、实物期权二项式-高斯模型、SaaS 估值倍数

#### 认知架构

- `act-r-cognitive-reuse.md` — 对齐 ACT-R 认知架构与知识复用机制
- `bdi-agent-reuse.md` — 对齐 BDI 智能体架构、计划库复用、MCP/A2A 语义映射

#### 工业 IoT/OT-IT

- `isa-95-asset-catalog-deep-dive.md` — ISA-95 五层资产目录、设备类型/属性/语义模型、OMAC PackML 集成、与 AAS 映射
- `aas-submodel-templates-full-catalog.md` — IDTA 子模型模板全清单（已发布+开发中）、DPP 映射、选择指南

#### 形式化验证

- `spark-ada-vs-rust-verification-matrix.md` — SPARK Ada 与 Rust 安全关键验证方法全面对比（安全属性、工具链、工业生态、决策矩阵）

#### 参考索引

- 更新 `terminology-crosswalk.md` — 增加版本对照表
- 更新 `authoritative-sources.md` — 增加最新权威链接
- 更新 `master-alignment-matrix.md` — 修正 MCP 版本，新增 PLCopen/FinOps/WASM/Gateway API/Data Mesh 等条目
- 新增 `cross-topic-index.md` — 跨主题综合索引与快速查找表
- 新增 `CHANGELOG.md` — 本更新日志

### 重要勘误

| 原内容 | 修正后 | 说明 |
|--------|--------|------|
| MCP 2026-07-28 RC 无状态版本 | MCP 2025-11-25 当前稳定版 | 官方规范仍为 stateful，2026-07-28 版本不存在 |
| A2A v1.0.0 2026-03-12 | A2A v1.0 2026-04 Cloud Next | 官方正式发布时间 |
| SLSA 1.0 单一等级模型 | SLSA 1.2 Multi-Track 模型 | Build/Source/Environment 三轨道 |
| ISO 42010 SoI / AF | ISO 42010 EoI / ADF | 2022 版新术语 |

### 权威来源

本轮更新主要对齐以下权威来源：

- ISO/IEC/IEEE 42010:2022 官方规范
- ISO/IEC 25010:2023 官方规范
- SLSA Specification v1.1 / v1.2 (slsa.dev)
- NIST SP 800-218r1 Initial Public Draft (2025-12-17)
- Regulation (EU) 2024/2847 (EU CRA)
- IEC 63278-1:2023 / IDTA-01001-3-0
- IEC/IEEE 60802 TSN Profile
- Model Context Protocol Specification 2025-11-25
- Google A2A Protocol v1.0 (Cloud Next 2026)
- OWASP Top 10 for LLM Applications 2025
- OWASP Top 10 for MCP 2025
- OWASP Top 10 for Agentic AI Applications 2026

---

### Phase 1 全面深化（本轮新增）

本轮更新按照 `MASTER_PLAN.md` Phase 1（2026-Q3）计划，对 7 条轨道进行了全面深化：

#### Track A: 01 元模型与标准对齐

- `02-togaf-10-alignment/detailed-mapping.md` — TOGAF 10 ABB/SBB 与 ISO 42010:2022 的详细映射（覆盖10个ADM阶段）
- `04-archimate-4/archimate-iso-mapping.md` — ArchiMate 3.2/4.0 元素与 ISO 42010:2022 的对照表（四层全覆盖）
- `03-iso-26550-ple/ple-iso-integration.md` — ISO 26550:2015 与 ISO 42010/42020 的交叉映射（双轨）
- `05-swebok-v4/swebok-alignment.md` — SWEBOK V4 知识领域与本体系 13 个主题的对应关系

#### Track B1: 02 业务架构复用

- `02-business-capability/fea-brm-togaf-mapping.md` — FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射
- `06-bpmn-dmn/bpmn-dmn-executable-cases.md` — BPMN 2.0 / DMN 1.5 可执行语义案例集（3个生产级案例）
- `case-studies/industry-vertical-cases.md` — 行业垂直场景案例库（金融开放银行、医疗 FHIR、制造 ISA-95）

#### Track B2: 03 应用架构复用

- `05-cloud-native-patterns/reusability-matrix-2026.md` — 云原生架构模式复用性矩阵 2026 版（9种模式 × 8维度）
- `06-service-mesh/service-mesh-communication-patterns.md` — 服务网格通信模式复用（Istio/Envoy/Cilium）

#### Track B3: 04 组件架构复用

- `07-language-ecosystems/comparison-matrix-2026.md` — 6大语言生态复用成熟度深度对比 2026
- `04-design-patterns/interface-design-patterns.md` — 设计模式与接口设计模式复用（跨语言对比 + 反模式）
- `07-language-ecosystems/open-source-supply-chain-reuse.md` — 依赖管理策略深度对比（PubGrub/MVS/SAT + 供应链安全）

#### Track B4: 05 功能架构复用

- `06-mcp-a2a-protocols/protocol-analysis.md` — MCP 2026-07-28 RC + A2A v1.0.0 协议架构复用分析
- `04-workflow-orchestration/temporal-reuse-patterns.md` — Temporal 工作流复用模式（Saga/Parallel/Child/Schedule）
- `decision-tree-granularity-cost-roi.md` — 功能复用的粒度-成本-收益决策树

#### Track C: 06 治理与量化 + 09 价值量化

- `05-metrics-kpi/metrics-framework.md` — 复用度量指标体系四级框架（资产/项目/组织/生态级）
- `04-finops-cost/cost-allocation-template.md` — FinOps 跨层复用成本分摊模型（含 Excel/Python 模板）
- `01-cocomo-ii-reuse/cocomo-2026-calibration.md` — COCOMO II 2026 校准版（AI辅助开发/Serverless/低代码适配）

#### Track D: 10 供应链安全

- `03-attack-vectors/attack-tree.md` — 软件供应链攻击树（7条路径 + 典型案例映射 + 防御矩阵）

#### Track E: 11 工业 IoT/OT-IT

- `01-isa-95-model/l0-field/asset-catalog.md` — ISA-95 L0 现场层复用资产目录
- `01-isa-95-model/l1-control/asset-catalog.md` — ISA-95 L1 控制层复用资产目录
- `01-isa-95-model/l2-supervisory/asset-catalog.md` — ISA-95 L2 监控层复用资产目录
- `01-isa-95-model/l3-mes/asset-catalog.md` — ISA-95 L3 MES 层复用资产目录
- `01-isa-95-model/l4-enterprise/asset-catalog.md` — ISA-95 L4 企业层复用资产目录
- `01-isa-95-model/cross-layer-matrix/data-flow-mapping.md` — 跨层数据流映射（ERP↔MES↔SCADA↔PLC↔Field）

#### Track F: 07 形式化验证

- `04-rust-type-system/cargo-sat-resolution.md` — Cargo 依赖解析的 SAT 求解详细说明（PubGrub 算法）
- `04-rust-type-system/polonius-vs-nll.md` — Rust Polonius 借用检查器 vs NLL 对比（4个代码示例）
- `04-rust-type-system/unsafe-verification.md` — unsafe 边界验证策略（7工具对比矩阵 + 4级检查清单）

#### Track 认知架构: 08 认知架构

- `03-cognitive-load-theory/quantitative-model.md` — 开发者复用决策认知负荷量化模型（NASA-TLX 适配版）
- `05-ai-cognitive-augmentation/augmentation-architecture.md` — AI 辅助复用决策的认知增强架构设计（RAG+LLM）

#### 参考索引: 99 参考索引

- `glossary/axiom-theorem-tree.md` — 公理-定理推理树（24条已确立，目标20+公理30+定理）
- `visualizations/standard-family-tree.mmd` — 国际标准族谱图（Mermaid）
- `visualizations/concept-mapping.mmd` — 核心概念映射图（Mermaid）
- `templates/document-template.md` — 文档写作统一模板
- `templates/quick-reference-card.md` — 快速参考卡（一页纸速查）

---

> 最后更新: 2026-06-06
