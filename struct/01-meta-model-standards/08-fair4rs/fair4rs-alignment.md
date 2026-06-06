# FAIR4RS 原则与软件架构复用对齐

> **定位**: 将 RDA/FAIR4RS 原则纳入软件架构复用框架，指导研究软件、AI 功能和架构资产的可持续复用
> **对齐来源**: FAIR4RS Principles v1.0 (RDA, 2022), Wilkinson et al. (2016), Barker et al. (2022), ReSA Actionable FAIR4RS TF (2024–2025)
> **状态**: Phase 2（2026-Q4）
> **权威链接**:
>
> - <https://ardc.edu.au/resource/fair-principles-for-research-software-fair4rs/>
> - <https://doi.org/10.15497/RDA00068>
> - <https://github.com/force11/FAIR4RS>

---

## 1. 什么是 FAIR4RS

**FAIR4RS**（FAIR Principles for Research Software）是 FAIR 数据原则在**研究软件**领域的适配版本，由 RDA、FORCE11 和 ReSA 联合制定，于 **2022 年 5 月**正式发布。

与 FAIR 数据不同，FAIR4RS 强调软件是**可执行的、可组合的、持续演进的**，因此将传统的 Reusable 扩展为 **Usable + Reusable**（可执行且可复用）。

| 维度 | FAIR4RS 核心要求 |
|------|-----------------|
| **F — Findable** | 软件及其元数据易被人和机器发现 |
| **A — Accessible** | 通过标准化协议可检索 |
| **I — Interoperable** | 通过 API 和数据标准与其他软件互操作 |
| **R — Reusable / Usable** | 既可执行（usable），又可理解、修改、集成（reusable） |

---

## 2. FAIR4RS 17 条子原则

### F — Findable（可发现）

- **F1**: 软件被分配全局唯一且持久的标识符
  - **F1.1**: 不同粒度级别（库/模块/函数/服务）的组件都有独立标识符
  - **F1.2**: 不同版本有独立标识符
- **F2**: 软件具有丰富的元数据描述
- **F3**: 元数据明确包含软件的标识符
- **F4**: 元数据本身也是 FAIR、可搜索、可索引的

### A — Accessible（可访问）

- **A1**: 通过标准化通信协议按标识符检索软件
  - **A1.1**: 协议开放、免费、通用可实现
  - **A1.2**: 协议支持必要的认证和授权
- **A2**: 即使软件不再可用，元数据仍可访问

### I — Interoperable（互操作）

- **I1**: 软件以符合领域社区标准的方式读写和交换数据
- **I2**: 软件包含对其他对象的限定引用

### R — Reusable / Usable（可复用且可执行）

- **R1**: 软件具有多种准确且相关的属性描述
  - **R1.1**: 软件有明确且可访问的许可证
  - **R1.2**: 软件有详细的来源 provenance
- **R2**: 软件包含对其他软件的限定引用
- **R3**: 软件符合领域相关的社区标准

---

## 3. 与 FAIR 数据的关键区别

| 维度 | FAIR 数据 | FAIR4RS |
|------|----------|---------|
| 对象 | 数据集 | 源代码、二进制、文档、构建脚本 |
| 可执行性 | 数据不可执行 | 软件**必须可执行** |
| 粒度 | 数据集级别 | 多粒度（库/模块/函数/服务） |
| 版本 | 非核心 | **版本必须有独立持久 ID** |
| 互操作 | 共享词汇和格式 | API、数据交换、限定引用 |
| 衰减 | 比特腐烂 | 依赖崩溃、环境腐烂 |

---

## 4. 与软件架构复用框架的映射

### 4.1 对应四层复用架构

| FAIR4RS 原则 | 本体系对应层次 | 实践方式 |
|-------------|---------------|----------|
| F1.1 多粒度标识 | 02→05 四层架构 | 为业务能力、应用、组件、功能分配 PURL/DOI/SWHID |
| F1.2 版本标识 | 04 组件架构 | SemVer + Git tag + 持久归档 |
| F2 丰富元数据 | 01 元模型 / 06 治理 | CodeMeta/CITATION.cff + README + SPDX |
| I1/I2 互操作 | 03 应用架构 / 05 功能架构 | OpenAPI/gRPC/MQTT/OPC UA/MCP |
| R1.1 许可证 | 10 供应链安全 | SPDX 许可证标识符 |
| R1.2 来源 | 10 供应链安全 | SLSA provenance + Sigstore 签名 |
| R2 限定引用 | 04 组件架构 / 10 供应链安全 | SBOM (SPDX/CycloneDX) |

### 4.2 对应供应链安全

FAIR4RS 的 **I2**（限定引用）和 **R2**（对其他软件的限定引用）本质上就是机器可读的依赖和来源声明。这与 SBOM 完全对应：

- **SPDX** (ISO/IEC 5962:2021): 许可证和合规导向
- **CycloneDX** (ECMA-424): 安全导向，支持 VEX
- 两者都使用 **PURL**、CPE 和哈希进行组件识别

### 4.3 对应容器与包管理生态

| 基础设施 | FAIR4RS 实现 |
|---------|-------------|
| OCI 容器注册表 | A1/A1.1/A1.2 标准化分发 + A2 元数据持久化 |
| npm / PyPI / Cargo / Maven | F1/F4 可搜索索引 + A1 HTTP(S) + I 标准 manifest + R 安装/构建/运行 |
| Software Heritage | F1.2 版本持久 ID (SWHID) + A2 长期归档 |
| Zenodo / Figshare | F1 持久 DOI + A2 元数据存档 |

### 4.4 对应 AI/LLM 功能复用（MCP）

FAIR4RS 对新兴的 **AI Tool 复用** 极具指导意义：

| FAIR4RS 原则 | MCP Tool 复用实践 |
|-------------|------------------|
| F1.1 组件粒度 | 每个 LLM 可调用的 function/tool 有独立版本化标识 |
| I1 互操作 | MCP 协议提供统一接口标准 |
| A1 可访问 | stdio / HTTP(S) with SSE 标准传输 |
| R1 丰富描述 | Tool 名称、自然语言描述、JSON input/output schema |
| R1.1 许可证 | Tool Server 明确声明许可证 |
| R1.2 来源 | Server provenance、签名、供应链审查 |

实际案例：**BioContextAI** 已将 FAIR4RS 作为生物医学 MCP Server 的准入要求。

---

## 5. 使架构资产 FAIR4RS 合规的行动清单

| 原则 | 对架构资产（模式、组件、参考架构、LLM 工具）的实际行动 |
|------|-----------------------------------------------------|
| **F1 / F1.1 / F1.2** | 分配持久 ID：Zenodo/Figshare DOI、Software Heritage SWHID、PURL、SemVer；每个发布版本都归档 |
| **F2 / F3 / F4** | 维护丰富机器可读元数据：`codemeta.json`、`CITATION.cff`、README、SPDX 许可证标识符；注册到可搜索目录 |
| **A1 / A1.1 / A1.2** | 通过 HTTPS/Git/OCI/包管理器 API 分发；需要时支持认证授权 |
| **A2** | 在 Zenodo、Software Heritage、机构库中长期保存元数据和源码快照 |
| **I1** | 采用社区接口标准：OpenAPI/AsyncAPI、gRPC/Protobuf、GraphQL、MQTT、OPC UA、MCP |
| **I2 / R2** | 每个发布版本生成并发布 SPDX 或 CycloneDX SBOM；声明对相关系统、数据集、模型、文档的限定引用 |
| **R1.1** | 使用 SPDX 标识符明确声明许可证；必要时包含 CLA/DCO |
| **R1.2** | 记录来源：作者（ORCID）、资助、项目背景、变更日志；使用签名提交、签名制品、SLSA/Sigstore provenance |
| **R3** | 符合领域标准：编码规范、测试策略、安全扫描、CI/CD、架构决策记录 (ADR) |
| **AI/LLM 工具** | 为每个 tool/function 提供 MCP manifest：名称、版本化 ID、自然语言描述、JSON I/O schema、认证模型、执行环境规范 |

---

## 6. 与 SBOM、MCP、RAS 的整合视图

```text
┌─────────────────────────────────────────────────────────────┐
│                    FAIR4RS 合规架构资产                      │
├─────────────────────────────────────────────────────────────┤
│  F1/F1.1/F1.2  ──→  DOI + SWHID + SemVer + PURL            │
│  F2/F3/F4      ──→  codemeta.json + CITATION.cff + README  │
│  A1/A1.1/A1.2  ──→  HTTPS / Git / OCI / 包管理器 API       │
│  A2            ──→  Zenodo / Software Heritage 长期归档      │
│  I1            ──→  OpenAPI / gRPC / MQTT / MCP / OPC UA     │
│  I2/R2         ──→  SPDX/CycloneDX SBOM                    │
│  R1.1          ──→  SPDX 许可证标识符                        │
│  R1.2          ──→  SLSA provenance + Sigstore 签名          │
├─────────────────────────────────────────────────────────────┤
│  包装层可选: OMG RAS (rasset.xml) 或现代包管理器 manifest    │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. 批判性评估

### 7.1 优势

- **社区广泛认可**: RDA 官方背书，被多国资助机构采纳（NWO、DFG、加拿大数字研究联盟）
- **行动指南明确**: 17 条子原则可直接转化为工程实践
- **跨领域适用**: 从传统软件到 AI Tool、数字孪生、工业自动化均可应用
- **与现有工具链整合**: 不发明新工具，而是利用 SBOM、包管理器、容器注册表等已有基础设施

### 7.2 局限

- **资助者认知度不足**: 2025 年调查显示仅 70% 国际资助者听说过 FAIR4RS（vs 97% 听说过 FAIR 数据）
- **自动化评估仍在发展中**: FAIR-IMPACT 已发布 17 个自动指标，但工具成熟度参差不齐
- **与商业软件许可证实践有张力**: 开源偏好与专有组件现实的平衡需要领域指导
- **大型系统分解难度**: 为遗留系统分配多粒度持久 ID 成本高

### 7.3 2026 年应用建议

1. **从组件层切入**: 先为 `04-component-architecture-reuse` 中的关键组件建立 CodeMeta + SBOM
2. **为 MCP/A2A 工具增加 FAIR4RS manifest**: 在 `12-ai-native-reuse` 中定义 AI Tool 元数据规范
3. **跟踪 ReSA Actionable FAIR4RS Task Force**: 预计 2025 年末发布跨领域实施指南
4. **与 SLSA/SPDX 工作流整合**: 在 CI/CD 中自动生成 SBOM + provenance，满足 I2/R1.2

---

## 8. 公理映射

> **公理 FAIR.1** (Executable Reusability): 软件的复用价值必须同时满足**可发现**、**可访问**、**可互操作**、**可执行**四个条件，缺一不可。

> **公理 FAIR.2** (Version Persistence): 没有独立持久标识符的版本，不构成可复用的资产单元。

---

## 9. 参考链接

- ARDC FAIR4RS: <https://ardc.edu.au/resource/fair-principles-for-research-software-fair4rs/>
- RDA FAIR4RS WG: <https://www.rd-alliance.org/groups/fair-4-research-software-fair4rs-wg>
- FAIR4RS v1.0 PDF: <https://www.rd-alliance.org/sites/default/files/FAIR%20Principles%20for%20Research%20Software%20(FAIR4RS%20Principles).pdf>
- Zenodo DOI: <https://doi.org/10.15497/RDA00068>
- GitHub: <https://github.com/force11/FAIR4RS>
- ReSA Adoption Update 2024: <https://www.researchsoft.org/blog/2024-03/>
- ReSA Actionable FAIR4RS TF: <https://www.researchsoft.org/tf-actionable-fair4rs/>
- BioContextAI MCP + FAIR4RS: <https://biocontext.ai/docs>
- Barker et al. (2022) Nature Scientific Data: <https://doi.org/10.1038/s41597-022-01710-x>
