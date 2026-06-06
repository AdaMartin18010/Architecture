# 软件工程架构复用视角 · 结构化知识体系

> **版本**: 2026-06-06 Phase 1 完成
> **定位**: 将 31 万字源文档转化为结构化、可验证、可输出的知识产品
> **对齐标准**: ISO/IEC/IEEE 42010:2022, TOGAF 10, SLSA 1.2, IEC 61508, MCP 2025-11-25, A2A v1.0 等 25+ 国际标准

---

## 📊 项目规模

| 指标 | 数据 |
|------|------|
| **Markdown 文件** | **157** 个 |
| **形式化规约/代码** | **12** 个（TLA+ × 4, Alloy × 4, Mermaid × 3, Python × 1） |
| **累计内容** | **~50.2 万字** / **~150 万字符** |
| **一级主题** | **14** 个（01-13 + 99-reference） |
| **形式化规约** | TLA+ × 4, Alloy × 4, 公理-定理体系 × 29 |
| **权威来源对齐** | 25+ 国际标准与行业框架 |

---

## 🗂️ 知识体系结构

```
struct/
├── 01-meta-model-standards/          # 元模型与标准对齐
│   ├── 01-iso-42010-2022/            # ISO 42010:2022 架构描述
│   ├── 02-togaf-10-alignment/        # TOGAF 10 企业架构
│   ├── 03-iso-26550-ple/             # ISO 26550 产品线工程
│   ├── 04-archimate-4/               # ArchiMate 3.2/4.0
│   ├── 05-swebok-v4/                 # SWEBOK V4 知识领域
│   └── 06-formal-axioms/             # 形式化公理体系（15 公理 + 29 定理）
├── 02-business-architecture-reuse/   # 业务架构复用
│   ├── 01-business-capability-model/ # 业务能力建模
│   ├── 02-business-process-reuse/    # 业务流程复用
│   ├── 03-domain-driven-design/      # 领域驱动设计
│   ├── 04-business-rules/            # 业务规则与决策
│   ├── 05-value-stream/              # 价值流映射
│   ├── 06-bpmn-dmn/                  # BPMN 2.0 / DMN 1.5 可执行案例
│   └── case-studies/                 # 行业垂直场景库
├── 03-application-architecture-reuse/# 应用架构复用
│   ├── 01-layered-architecture/      # 分层架构模式
│   ├── 02-microservices/             # 微服务架构
│   ├── 03-serverless/                # Serverless 架构
│   ├── 04-event-driven/              # 事件驱动架构
│   ├── 05-cloud-native-patterns/     # 云原生复用性矩阵 2026
│   └── 06-service-mesh/              # 服务网格通信模式
├── 04-component-architecture-reuse/  # 组件架构复用
│   ├── 01-component-models/          # 组件模型理论
│   ├── 02-interface-contracts/       # 接口契约设计
│   ├── 03-dependency-management/     # 依赖管理策略
│   ├── 04-design-patterns/           # 设计模式与反模式
│   └── 07-language-ecosystems/       # 6 大语言生态深度对比
├── 05-functional-architecture-reuse/ # 功能架构复用
│   ├── 01-api-design/                # API 设计模式
│   ├── 02-function-as-a-service/     # FaaS 复用模式
│   ├── 03-event-functions/           # 事件函数模式
│   ├── 04-workflow-orchestration/    # Temporal 工作流复用
│   └── 06-mcp-a2a-protocols/         # MCP + A2A 协议分析
├── 06-cross-layer-governance/        # 跨层治理与量化
│   ├── 01-governance-framework/      # 治理框架
│   ├── 02-reuse-process/             # 复用过程模型
│   ├── 03-policy-automation/         # 策略自动化
│   ├── 04-finops-cost/               # FinOps 成本分摊模板
│   └── 05-metrics-kpi/               # 四级度量指标体系
├── 07-formal-verification/           # 形式化验证
│   ├── 01-tla-plus/                  # TLA+ 案例库（4 规约）
│   ├── 02-alloy/                     # Alloy 案例库（4 模型）
│   ├── 03-coq-isabelle/              # Coq / Isabelle 方向
│   └── 04-rust-type-system/          # Rust 类型系统深化
├── 08-cognitive-architecture/        # 认知架构
│   ├── 01-human-factors/             # 人因工程
│   ├── 02-knowledge-representation/  # 知识表示
│   ├── 03-cognitive-load-theory/     # NASA-TLX 认知负荷模型
│   ├── 04-decision-making/           # 复用决策机制
│   └── 05-ai-cognitive-augmentation/ # AI 认知增强架构
├── 09-value-quantification/          # 价值量化
│   ├── 01-cocomo-ii-reuse/           # COCOMO II 2026 校准
│   ├── 02-roi-models/                # ROI 与实物期权模型
│   ├── 03-finops-allocation/         # FinOps 单位经济学
│   └── 04-risk-adjusted-value/       # 风险调整价值
├── 10-supply-chain-security/         # 供应链安全
│   ├── 01-threat-model/              # 威胁建模
│   ├── 02-sbom-standards/            # SPDX / CycloneDX / SWID
│   ├── 03-attack-vectors/            # 攻击树与案例
│   ├── 04-zero-trust/                # 零信任 5 层模板
│   └── 05-compliance/                # 合规映射
├── 11-industrial-iot-otit/           # 工业 IoT / OT-IT 融合
│   ├── 01-isa-95-model/              # ISA-95 五层资产目录
│   ├── 02-opc-ua-fx/                 # OPC UA FX 深化
│   ├── 03-plcopen/                   # PLCopen Motion + TLA+
│   ├── 04-aas/                       # 资产管理壳 AAS
│   └── 05-safety-standards/          # IEC 61508 / ISO 26262
├── 12-ai-native-reuse/               # AI 原生复用
│   ├── 01-llm-prompt-reuse/          # 提示工程复用
│   ├── 02-model-reuse/               # 模型复用与微调
│   ├── 03-ai-agent-reuse/            # Agent 架构复用
│   ├── 04-rag-patterns/              # RAG 模式库
│   └── 05-conformal-prediction/      # 共形预测代码生成
├── 13-emerging-trends/               # 前沿趋势
│   ├── 01-platform-engineering/      # 平台工程成熟度
│   ├── 02-webassembly/               # WASM Component Model
│   ├── 03-edge-computing/            # 边缘计算复用
│   ├── 04-quantum-computing/         # 量子计算架构
│   └── 05-sustainable-software/      # 可持续软件工程
└── 99-reference/                     # 参考索引
    ├── standards-index/              # 标准对齐多维矩阵
    ├── terminology-crosswalk/        # 术语交叉对照
    ├── cross-topic-index.md          # 跨主题快速查找表
    ├── CHANGELOG.md                  # 更新日志与勘误
    ├── chapters/                     # 全书章节框架（ch01-ch06）
    └── book-format-guide.md          # 写作与排版规范
```

---

## 🚀 快速导航

| 你想了解... | 从这儿开始 |
|------------|-----------|
| 整个体系的逻辑基础 | [`01-meta-model-standards/06-formal-axioms/axiom-system.md`](struct/01-meta-model-standards/06-formal-axioms/axiom-system.md) |
| 6 大编程语言生态怎么选 | [`04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md`](struct/04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md) |
| MCP / A2A 协议深度分析 | [`05-functional-architecture-reuse/06-mcp-a2a-protocols/`](struct/05-functional-architecture-reuse/06-mcp-a2a-protocols/) |
| 云原生架构模式对比 | [`03-application-architecture-reuse/05-cloud-native-patterns/reusability-matrix-2026.md`](struct/03-application-architecture-reuse/05-cloud-native-patterns/reusability-matrix-2026.md) |
| 软件供应链攻击与防御 | [`10-supply-chain-security/03-attack-vectors/attack-tree.md`](struct/10-supply-chain-security/03-attack-vectors/attack-tree.md) |
| ISA-95 + OPC UA 工业资产 | [`11-industrial-iot-otit/01-isa-95-model/`](struct/11-industrial-iot-otit/01-isa-95-model/) |
| TLA+ / Alloy 形式化案例 | [`07-formal-verification/`](struct/07-formal-verification/) |
| 复用成熟度评估问卷 | [`06-cross-layer-governance/05-metrics-kpi/maturity-assessment-questionnaire.md`](struct/06-cross-layer-governance/05-metrics-kpi/maturity-assessment-questionnaire.md) |
| 国际标准对齐总览 | [`99-reference/standards-index/master-alignment-matrix.md`](struct/99-reference/standards-index/master-alignment-matrix.md) |
| 术语中英文对照 | [`99-reference/terminology-crosswalk/terminology-crosswalk.md`](struct/99-reference/terminology-crosswalk/terminology-crosswalk.md) |

---

## 📐 标准对齐总览

本知识体系对齐以下国际标准与行业框架：

**架构标准**
- ISO/IEC/IEEE 42010:2022（架构描述）
- ISO/IEC/IEEE 42020:2023（架构过程）
- ISO/IEC 25010:2023（系统与软件质量模型）
- TOGAF® Standard, 10th Edition
- ArchiMate® 3.2 / 4.0 Specification

**软件工程**
- ISO/IEC 26550:2015（产品线工程）
- ISO/IEC 26564:2022（复用过程评估）
- SWEBOK V4（软件工程知识体系）

**安全与供应链**
- SLSA 1.2（Supply-chain Levels for Software Artifacts）
- NIST SP 800-218 / SSDF 1.2
- EU CRA（网络弹性法案）
- OWASP SCVS / LLM Top 10 / MCP Top 10

**工业自动化**
- ISA-95（企业-控制系统集成）
- IEC 61508（功能安全）
- ISO 26262（道路车辆功能安全）
- IEC 63278（资产管理壳 AAS）
- PLCopen Motion Control Part 1-4

**新兴协议**
- Model Context Protocol 2025-11-25
- Google A2A Protocol v1.0
- WebAssembly Component Model

---

## 🗓️ 推进计划

详见 [`struct/MASTER_PLAN.md`](struct/MASTER_PLAN.md)

| Phase | 时间 | 目标 | 状态 |
|-------|------|------|------|
| 0 | 2026-Q2 | 基础奠基：源文档结构化 | ✅ 完成 |
| 1 | 2026-Q3 | 核心层次深化：业务→应用→组件→功能 | ✅ **本轮完成** |
| 2 | 2026-Q4 | 形式化与量化：TLA+/Alloy/Coq + COCOMO II | 🔄 预热中 |
| 3 | 2027-Q1 | 垂直领域扩展：工业 IoT 深化 | 🔄 预热中 |
| 4 | 2027-Q2 | 安全与供应链：攻击面建模、合规自动化 | 🔄 预热中 |
| 5 | 2027-Q3 | AI 原生与前沿：Agent 架构、WASM、量子 | 待启动 |
| 6 | 2027-Q4 | 整合与输出：全书框架、课程、工具链 | 待启动 |

---

## 📖 使用方式

1. **按需查阅**：通过上方「快速导航」定位感兴趣的主题
2. **系统学习**：按 `01` → `13` 顺序阅读，建立完整知识框架
3. **验证实践**：参考 `07-formal-verification/` 中的 TLA+/Alloy 规约进行模型检查
4. **评估改进**：使用 `06-cross-layer-governance/` 中的成熟度问卷自评
5. **写作引用**：遵循 `99-reference/book-format-guide.md` 的格式规范

---

## ⚠️ 已知限制

- TLA+ 规约未经 SANY/TLC 自动化验证（环境无 Java），依赖人工语法审查
- Alloy 模型未经 Alloy Analyzer 自动执行，建议后续补跑约束求解
- 部分前沿标准（如 MCP 2026-07-28 RC）在官方发布后将触发更新

---

## 📄 许可

见 [`LICENSE`](LICENSE)

---

> **最后更新**: 2026-06-06  
> **本轮规模**: 新增/更新 ~120 个文件，~46.5 万字  
> **维护者**: 软件工程架构复用知识体系项目组
