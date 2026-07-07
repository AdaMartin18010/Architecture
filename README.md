# 软件工程架构复用视角 · 结构化知识体系

> **版本**: 2026-07-08 Phase 1.5 修复完成 · 质量门控 100%
> **定位**: 将 ~31 万字源文档转化为结构化、可验证、可输出的知识产品；已完成内容深度补齐、模板污染清理、权威来源对齐、可视化图库填充、全局质量验证与 struct/view 同步
> **对齐标准**: ISO/IEC/IEEE 42010:2022, TOGAF 10, SLSA 1.2, IEC 61508, MCP 2025-11-25, A2A v1.0 等 25+ 国际标准
> **健康状态**: `python scripts/health-check.py` 全部通过（struct/ 288/288 · view/ 14/14 · 死链 0 · 交叉索引 0 冲突）

---

## 📊 项目规模

> **统计口径**: 截至 2026-07-07；Markdown 按 `.md` 文件计数；字数按中文字符 + 英文词（连续字母）计数；形式化代码按扩展名计数。

| 指标 | 数据 |
|------|------|
| **Markdown 文件** | **330** 个（`struct/` 307 + `view/` 23，含 14 个聚合卷册与 9 个历史快照） |
| **形式化规约/代码** | **93** 个（TLA+ × 3, Alloy × 4, Coq × 2, Isabelle × 2, Mermaid × 75 + SVG × 75, Python × 7） |
| **累计内容** | **~79.1 万中文字** / **~97.7 万总词** / **~294 万字符**（`struct/` 主知识库） |
| **一级主题** | **13** 个（01-13）+ **99-reference** 参考层 |
| **形式化规约** | TLA+ × 3, Alloy × 4, Coq × 2, Isabelle × 2, 公理-定理体系 × 20+ |
| **权威来源对齐** | 30+ 国际标准与行业框架 |
| **质量门控** | `struct/` 288/288 通过，`view/` 14/14 通过，死链 0，模板重复 0 |
| **交叉索引** | 公理 0 未定义 / 0 重复；标准版本冲突 0；术语定义冲突 0 |

---

## 🗂️ 知识体系结构

```text
struct/
├── 01-meta-model-standards/            # 元模型与标准对齐
│   ├── 01-iso-420xx-family/            # ISO 42010/42020/42030 与 12207 族
│   ├── 02-togaf-10-alignment/          # TOGAF 10 企业架构
│   ├── 03-iso-26550-ple/               # ISO 26550 产品线工程
│   ├── 04-archimate-4/                 # ArchiMate 3.2/4.0
│   ├── 05-swebok-v4/                   # SWEBOK V4 知识领域
│   ├── 06-formal-axioms/               # 形式化公理体系
│   ├── 07-omg-ras/                     # OMG RAS 可复用资产
│   ├── 08-fair4rs/                     # FAIR4RS 研究软件复用
│   ├── 09-sysml-v2/                    # SysML v2 对齐
│   ├── 10-mbse-reuse/                  # MBSE 与复用集成
│   └── plans-tasks/                    # plans tasks
├── 02-business-architecture-reuse/     # 业务架构复用
│   ├── 01-business-domain-reuse/       # 01 business domain reuse
│   ├── 02-business-capability/         # 业务能力建模
│   ├── 03-value-stream/                # 价值流映射
│   ├── 04-business-process-reuse/      # 04 business process reuse
│   ├── 05-business-service-reuse/      # 05 business service reuse
│   ├── 06-bpmn-dmn/                    # BPMN 2.0 / DMN 1.5
│   ├── 07-defense-mission-engineering/ # 国防任务工程
│   ├── 08-zachman-reuse-mapping/       # Zachman 框架复用映射
│   └── case-studies/                   # case studies
├── 03-application-architecture-reuse/  # 应用架构复用
│   ├── 01-layered-architecture/        # 分层架构模式
│   ├── 02-microservices/               # 微服务架构
│   ├── 03-app-service/                 # 应用服务复用
│   ├── 04-serverless/                  # Serverless 架构
│   ├── 05-data-architecture/           # 数据架构复用
│   ├── 06-event-driven/                # 事件驱动架构
│   ├── 07-cloud-native-patterns/       # 云原生复用性矩阵 2026
│   ├── 08-service-mesh/                # 服务网格通信模式
│   ├── 09-eda-cqrs/                    # EDA/CQRS 深度
│   ├── 10-tosca-dmn-platform/          # TOSCA v2.0 / DMN 1.6
│   └── 11-idp-practices/               # IDP 复用实践
├── 04-component-architecture-reuse/    # 组件架构复用
│   ├── 01-component-models/            # 组件模型理论
│   ├── 02-interface-contracts/         # 接口契约设计
│   ├── 03-dependency-management/       # 依赖管理策略
│   ├── 04-design-patterns/             # 设计模式与反模式
│   ├── 05-version-strategy/            # 版本策略
│   ├── 06-cloud-native-networking/     # 云原生网络
│   └── 07-language-ecosystems/         # 6 大语言生态深度对比
├── 05-functional-architecture-reuse/   # 功能架构复用
│   ├── 01-api-design/                  # API 设计模式
│   ├── 02-function-as-a-service/       # FaaS 复用模式
│   ├── 03-event-functions/             # 事件函数模式
│   ├── 04-workflow-orchestration/      # Temporal 工作流复用
│   ├── 05-ai-llm-functions/            # AI/LLM 功能复用
│   └── 06-mcp-a2a-protocols/           # MCP + A2A 协议分析
├── 06-cross-layer-governance/          # 跨层治理与量化
│   ├── 01-process-governance/          # 复用过程治理
│   ├── 02-reuse-process/               # 02 reuse process
│   ├── 03-maturity-models/             # 成熟度模型（RCMM/RiSE/SPICE）
│   ├── 04-finops-cost/                 # FinOps 成本分摊模板
│   ├── 05-metrics-kpi/                 # 四级度量指标体系
│   ├── 06-up-downgrade-matrix/         # 升降级决策矩阵
│   ├── 07-policy-automation/           # 07 policy automation
│   ├── 08-reserved/                    # 预留编号
│   └── 09-agentic-governance/          # Agentic 治理
├── 07-formal-verification/             # 形式化验证
│   ├── 01-tla-plus/                    # TLA+ 案例库
│   ├── 02-alloy/                       # Alloy 案例库
│   ├── 03-coq-isabelle/                # Coq / Isabelle
│   ├── 04-rust-type-system/            # Rust 类型系统深化
│   ├── 05-spark-ada/                   # SPARK/Ada 契约验证
│   ├── 06-b-method/                    # B Method / Event-B
│   ├── 07-vv-standards/                # V&V 标准（IEEE 1012）
│   ├── 08-emerging-trends/             # 形式化验证前沿
│   ├── 09-comparative-matrices/        # 方法对比矩阵
│   └── plans-tasks/                    # plans tasks
├── 08-cognitive-architecture/          # 认知架构
│   ├── 01-act-r-model/                 # ACT-R 模型
│   ├── 02-bdi-model/                   # BDI 模型
│   ├── 03-cognitive-load-theory/       # 认知负荷理论
│   ├── 04-decision-making/             # 决策机制
│   └── 05-ai-cognitive-augmentation/   # AI 认知增强
├── 09-value-quantification/            # 价值量化
│   ├── 01-cocomo-ii-reuse/             # COCOMO II 2026 校准
│   ├── 02-roi-npv-models/              # ROI 与 NPV 模型
│   ├── 03-carbon-dimension/            # 碳排维度
│   └── tools/                          # 工具脚本
├── 10-supply-chain-security/           # 供应链安全
│   ├── 01-slsa-framework/              # SLSA 框架
│   ├── 02-sbom-standards/              # SBOM 标准
│   ├── 03-attack-vectors/              # 攻击向量
│   ├── 04-provenance-examples/         # 来源示例
│   ├── 05-zero-trust-supply-chain/     # 零信任供应链
│   ├── 06-case-studies/                # 案例研究
│   ├── 07-owasp-scvs/                  # OWASP SCVS
│   ├── 08-guac-supply-chain/           # GUAC 供应链图
│   ├── 09-owasp-asvs/                  # OWASP ASVS
│   ├── 10-owasp-top10-2025/            # OWASP Top 10 2025
│   ├── 11-osps-baseline/               # OSPS 基线
│   └── 12-nist-ssdf-update/            # NIST SSDF 更新
├── 11-industrial-iot-otit/             # 工业 IoT / OT-IT 融合
│   ├── 01-isa-95-model/                # ISA-95 五层资产目录
│   ├── 02-opc-ua-fx/                   # OPC UA FX 深化
│   ├── 03-tsn-deterministic/           # TSN 确定性网络
│   ├── 04-plcopen-motion/              # PLCopen Motion
│   ├── 05-digital-twin-aas/            # 数字孪生 / AAS
│   ├── 06-functional-safety/           # 功能安全（IEC 61508 / ISO 26262）
│   ├── 07-edge-ai/                     # 工业边缘 AI
│   ├── 08-digital-twin-general/        # 数字孪生通用
│   ├── 09-network-digital-twin/        # 网络数字孪生
│   └── plans-tasks/                    # plans tasks
├── 12-ai-native-reuse/                 # AI 原生复用
│   ├── 01-mcp-protocol/                # MCP 协议
│   ├── 02-a2a-protocol/                # A2A 协议
│   ├── 03-agentic-infrastructure/      # Agentic Infrastructure
│   ├── 04-hybrid-a2a-mcp-poc/          # A2A/MCP 混合 PoC
│   ├── 05-probabilistic-contracts/     # 概率契约
│   ├── 06-ai-governance/               # AI 治理
│   └── 07-conformal-prediction/        # Conformal Prediction
├── 13-emerging-trends/                 # 前沿趋势
│   ├── 01-platform-engineering/        # 平台工程成熟度
│   ├── 02-modular-monolith/            # 模块化单体
│   ├── 03-webassembly-components/      # WASM Component Model
│   ├── 04-green-architecture/          # 绿色架构
│   ├── 05-rust-ecosystem/              # Rust 生态
│   ├── 06-regtech-ai/                  # RegTech AI
│   ├── 07-green-software/              # 绿色软件
│   ├── 08-reserved/                    # 预留编号
│   └── 09-frontier-tracking/           # 前沿跟踪
└── 99-reference/                       # 参考索引
│   ├── audit/                          # 审计报告
│   ├── chapters/                       # 全书章节框架
│   ├── external-links/                 # 外部链接
│   ├── frontier-tracking/              # 前沿跟踪
│   ├── glossary/                       # 术语表
│   ├── knowledge-index/                # 知识索引
│   ├── standards-index/                # 标准索引
│   ├── templates/                      # 模板
│   ├── tools/                          # 工具脚本
│   └── visualizations/                 # 可视化
```

---

## 🚀 快速导航

| 你想了解... | 从这儿开始 |
|------------|-----------|
| 整个体系的逻辑基础 | [`01-meta-model-standards/06-formal-axioms/axiom-system.md`](struct/01-meta-model-standards/06-formal-axioms/axiom-system.md) |
| 6 大编程语言生态怎么选 | [`04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md`](struct/04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md) |
| MCP / A2A 协议深度分析 | [`05-functional-architecture-reuse/06-mcp-a2a-protocols/`](struct/05-functional-architecture-reuse/06-mcp-a2a-protocols/) |
| 云原生架构模式对比 | [`03-application-architecture-reuse/07-cloud-native-patterns/reusability-matrix-2026.md`](struct/03-application-architecture-reuse/07-cloud-native-patterns/reusability-matrix-2026.md) |
| 软件供应链攻击与防御 | [`10-supply-chain-security/03-attack-vectors/attack-tree.md`](struct/10-supply-chain-security/03-attack-vectors/attack-tree.md) |
| ISA-95 + OPC UA 工业资产 | [`11-industrial-iot-otit/01-isa-95-model/`](struct/11-industrial-iot-otit/01-isa-95-model/) |
| TLA+ / Alloy 形式化案例 | [`07-formal-verification/`](struct/07-formal-verification/) |
| 可视化图库总览 | [`99-reference/visualizations/README.md`](struct/99-reference/visualizations/README.md) |
| 学习路径与课程 | [`99-reference/course/`](struct/99-reference/course/) |
| 全书聚合稿 | 运行 `python scripts/build-deliverables.py` 生成 `dist/book-full.md` |
| 复用成熟度评估问卷 | [`06-cross-layer-governance/03-maturity-models/assessment-questionnaire.md`](struct/06-cross-layer-governance/03-maturity-models/assessment-questionnaire.md) |
| 国际标准对齐总览 | [`99-reference/standards-index/master-alignment-matrix.md`](struct/99-reference/standards-index/master-alignment-matrix.md) |
| 术语中英文对照 | [`99-reference/glossary/terminology-crosswalk.md`](struct/99-reference/glossary/terminology-crosswalk.md) |
| 主术语表 | [`99-reference/glossary/glossary-master.md`](struct/99-reference/glossary/glossary-master.md) |

---

## 📐 标准对齐总览

本知识体系对齐以下国际标准与行业框架：

**架构标准**

- ISO/IEC/IEEE 42010:2022（架构描述）
- ISO/IEC/IEEE 42020:2019（架构过程）
- ISO/IEC 25010:2023（系统与软件质量模型）
- TOGAF® Standard, 10th Edition
- ArchiMate® 3.2 / 4.0 Specification（4.0 于 2026-04-27 正式发布）

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
| 6 | 2027-Q4 | 整合与输出：全书框架、课程、工具链 | 🔄 进行中 |

---

## 📖 使用方式

1. **按需查阅**：通过上方「快速导航」定位感兴趣的主题
2. **系统学习**：按 `01` → `13` 顺序阅读，建立完整知识框架
3. **验证实践**：参考 `07-formal-verification/` 中的 TLA+/Alloy 规约进行模型检查
4. **评估改进**：使用 `06-cross-layer-governance/` 中的成熟度问卷自评
5. **写作引用**：遵循 `99-reference/book-format-guide.md` 的格式规范

---

## ⚠️ 已知限制

- Docker 形式化验证环境已配置（`struct/99-reference/tools/formal-verification-env/docker-compose.yml`），但当前运行环境的 Docker daemon 未启动，无法在本地实际执行 TLC / Alloy / Rocq / Isabelle 验证；CI 工作流 `.github/workflows/formal-verification.yml` 已就绪，将在 GitHub Actions 中 best-effort 执行
- MCP 官方当前稳定版为 **2025-11-25**；项目中仍存在个别历史文档引用 "2026-07-28 RC"，已逐步清理

---

## 📄 许可

见 [`LICENSE`](LICENSE)

---

> **最后更新**: 2026-07-08（Phase 1.5 收尾：health-check 100% 通过、报告路径统一、view 同步刷新）
> **本轮目标**: 全面修复质量门控、完成可视化图库、统一报告输出、确保 struct/view 一致性
> **维护者**: 软件工程架构复用知识体系项目组
>
## 反例：知识体系项目常见的失败模式

- **失败模式 1：标准引用不更新**。将 ISO/IEC 25010:2011 或草案版本当作当前有效版引用，导致架构决策基于过时质量模型。
- **失败模式 2：权威来源仅列标准号而无 URL**。无法快速核查的引用在工程实践中难以取信，也容易因记忆偏差产生勘误。
- **失败模式 3：view/ 与 struct/ 两层内容不同步**。长文档更新后未同步到结构化主题，造成读者获得矛盾信息。

---

## 权威来源

> **权威来源**:
>
> - ISO/IEC/IEEE 42010:2022. *Systems and software engineering — Architecture description*. <https://www.iso.org/standard/74296.html>
> - The Open Group. *TOGAF® Standard, 10th Edition*. <https://www.opengroup.org/togaf>
> - The Open Group. *ArchiMate® 4 Specification*. <https://www.opengroup.org/archimate>
> - ISO/IEC 26550:2015. *Software engineering — Reference model for product line engineering and management*. <https://www.iso.org/standard/69529.html>
>
> **核查日期**: 2026-07-07

---

> **2026-06-12 重要勘误**: 经与国际权威来源复核，修正以下标准状态：ISO/IEC 25010 正式版为 **:2023**（非 :2024）；ArchiMate 4.0 已于 **2026-04-27 正式发布**；ISO/IEC/IEEE 12207:2026 已于 **2026-04-29 发布**；ISO/IEC 30141:2024 已确认存在；NIST SSDF 1.2 仍为 **Initial Public Draft**（非正式版）。详见 `struct/99-reference/standards-index/authoritative-sources-v2.md`。
