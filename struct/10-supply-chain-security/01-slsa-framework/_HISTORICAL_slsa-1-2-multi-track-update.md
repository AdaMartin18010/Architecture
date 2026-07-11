# SLSA v1.1 / v1.2 Multi-Track 权威对齐（2025‑2026）

> **定位**：供应链安全层最新标准状态，指导复用组件的“信任护照”分级。
> **权威来源**：slsa.dev、OpenSSF、CISA、NIST、Sigstore、in-toto。

---

## 1. 关键结论（TL;DR）

| 版本 | 状态 | 核心变化 |
|------|------|----------|
| **SLSA v1.1** | 2025‑04 批准 | 澄清刷新；VSA（Verification Summary Attestation）新增验证器元数据 |
| **SLSA v1.2** | 2025‑11 批准 | **Source Track** 从实验提升为正式；引入 **Multi-Track** 架构 |
| **BuildEnv Track** | 草案 | 构建环境可信：vTPM → TEE（AMD SEV-SNP / Intel TDX） |
| **Dependency Track** | 讨论中 | 第三方依赖风险度量 |

---

## 2. Multi-Track 架构详解

SLSA v1.2 将单一 Build Track 扩展为多条独立可认证的轨道：

```text
SLSA v1.2
├── Build Track      (L1–L3, L4 提议中)
│   L1: Provenance 存在
│   L2: Hosted + signed provenance
│   L3: Hardened + non-forgeable builds
│
├── Source Track     (L1–L3, v1.2 正式化)
│   L1: 稳定不可变标识符
│   L2: 完整历史保存 + VSA
│   L3: 持续强制执行分支保护、签名审查、状态检查
│
├── BuildEnv Track   (L1–L3, 草案)
│   L1: 签名构建镜像 provenance
│   L2: 证明启动时环境实例化 (vTPM/Secure Boot)
│   L3: 硬件证明运行时完整性 (TEE / AMD SEV-SNP / Intel TDX)
│
└── Dependency Track (TBD)
    第三方依赖风险度量与控制
```

### 2.1 Source Track 对复用的影响

**核心洞察**：消费者现在可以**机械验证**被复用组件的每一次提交都经过了强制的代码审查和分支保护，而不仅仅是声明。

| 场景 | Source L3 要求 | 复用价值 |
|------|---------------|----------|
| 内部库复用 | 主分支强制 PR 审查 + 签名提交 + 状态检查 | 防止恶意内部提交污染共享组件 |
| OSS 引入 | 验证上游 Source Track 等级 | 将社区项目按供应链健康度分级 |
| 合规审计 | VSA 声明 Source L2+ | 满足 FedRAMP / NIST 800-161 溯源要求 |

---

## 3. OpenSSF 生态最新

### 3.1 Scorecard v5 (2024‑2025)

- **结构化结果**：19 项聚合检查分解为 **44+ 细粒度 probes**（`archived`、`hasOSVVulnerabilities`、`releasesAreSigned`、`pinsDependencies`）
- **in-toto 输出**：`--format=intoto`
- **实验性 SBOM 检查**：检测项目是否发布 SBOM
- **维护者注释**：可对不适用检查添加上下文

### 3.2 OSPS Security Baseline (2025‑10‑10)

三层最低安全基线：

- **Level 1**：MFA、贡献控制、版本控制、文档（通用底线）
- **Level 2**：安全发布、漏洞响应、依赖管理
- **Level 3**：权限管理、加固发布、测试（面向大规模用户项目）

### 3.3 Protobom

- OpenSSF 维护的格式无关 SBOM 数据表示（Protocol Buffers）
- 实现 SPDX ↔ CycloneDX 无损转换
- 驱动 `bomctl`、`sbom-convert`、GUAC 摄取

### 3.4 GUAC v1.0 (2025‑06)

- 稳定的图化供应链分析
- 认证器插件：OSV、Scorecard、许可证、EOL

---

## 4. SBOM 规范：CycloneDX v1.7 vs SPDX 3.0

| 特性 | CycloneDX v1.7 | SPDX 3.0 |
|------|---------------|----------|
| **标准状态** | ECMA-424 (2024) | ISO/IEC 5962 更新提交中 |
| **AI/ML BOM** | ML-BOM 成熟 | AI Profile (模型元数据、训练数据、评估标准) |
| **生命周期** | `metadata.lifecycles[].phase` | 通过 Annotation / Relationship 表达 |
| **专利/IP** | v1.7 新增专利/IP 元数据 | 较窄 |
| **加密透明** | v1.7 增强 CBOM | Security Profile |

**实践建议**：

- 内部 CI/CD 和广泛工具链 → **CycloneDX**
- 监管合规或供应商强制 → **SPDX 3.0**
- 欧盟 CRA / BSI TR-03183-2 接受两者 → 通过 **Protobom** 双发

---

## 5. CISA SBOM 2025 草案更新

CISA 2025 年 8 月发布 **Minimum Elements Draft** 更新：

- **新增必填字段**：Component Hash、License、Tool Name、Generation Context
- **角色澄清**：SBOM Author vs. Software Producer
- **自动化强调**：API 交付、CI/CD 集成
- **前沿扩展**：SaaS SBOM、AI 系统 SBOM、验证机制
- **VEX / CSAF 集成**：SBOM + Vulnerability Exploitability eXchange 配对

**"Shared Vision of SBOM for Cybersecurity" (2025)**：21 个国际网络安全机构联合背书，四大原则：

1. 模块化架构
2. 信任与溯源
3. 可操作情报
4. 开放治理

---

## 6. Sigstore / OCI v1.1 / S2C2F

### 6.1 Sigstore 生产就绪

- OpenSSF **Graduated** 项目（2024‑03）
- **后量子密码路线**：ML-DSA (FIPS 204) 实验性支持，等待 Go crypto 包（Go 1.25/1.26）
- **扩展 OIDC**：Fulcio 识别 CircleCI OIDC tokens（2025‑12）
- **企业级**：支持私有 Sigstore 实例

### 6.2 OCI v1.1 Reference Types

- `subject` 字段：将签名、SBOM、证明附加到镜像 digest，**无需修改镜像本身**
- Referrers API：`GET /v2/<name>/referrers/<digest>`
- Artifact Manifest 原生支持非可运行制品
- Docker Hub、ACR、ECR、GAR、Harbor 均已支持

### 6.3 S2C2F（Secure Supply Chain Consumption Framework）

Microsoft 捐赠给 OpenSSF，四级消费成熟度：

| 级别 | 主题 | 关键要求 |
|------|------|----------|
| **L1** | 摄入控制 | 包管理器、本地副本、漏洞扫描、许可证扫描、SBOM 清单 |
| **L2** | 安全消费 / MTTR | 自动更新、PR 级 CVE 告警、EOL 扫描、事件响应、完整性验证 |
| **L3** | 恶意软件 / 零日防御 | 拒绝列表、源码克隆、恶意软件扫描、主动安全审查、**来源强制执行** |
| **L4** | 高级威胁防御 | 验证消费 SBOM、**在可信基础设施上重建 OSS**、签名重建产物、为重建组件生成 SBOM |

> **S2C2F 与 SLSA 互补**：S2C2F 是**消费侧**；SLSA 是**生产侧**。S2C2F L3 的来源要求可由 SLSA Build L3 / Source L3 满足。

---

## 7. 供应链安全 ↔ 软件复用 governance

### 7.1 安全如何**促进**复用

| 机制 | 说明 |
|------|------|
| **信任即元数据** | SLSA Source L3 + Build L3 证明作为组件的“信任护照” |
| **SBOM 即复用契约** | SBOM 记录依赖足迹、许可证兼容性、已知漏洞 |
| **Scorecard 预筛选** | 分支保护、签名发布、固定依赖等 probes 自动评估候选库 |
| **S2C2F 消费治理** | L2–L4 定义安全引入 OSS 的精确控制 |

### 7.2 安全如何**约束**复用

| 约束 | 缓解 |
|------|------|
| 来源门槛 | 高安全环境要求 SLSA Build L2+，缩小候选池 |
| SBOM 向下传递 | NIST 800-161r2 预期要求 SBOM 沿依赖链传播 |
| AI/ML 来源空白 | 需 ML-BOM 记录训练数据、能耗、伦理考量 |
| 事件通知链 | 72 小时内通知所有消费者 → 无健全库存 = 合规风险 |

### 7.3 架构建议

| 层级 | 推荐控制 |
|------|----------|
| **组件目录** | “Approved” 层级要求 SLSA Build L2+ 且 Scorecard ≥ 7；显示 Source Track 等级 |
| **摄入管道** | S2C2F L2 底线：代理所有公共注册表、入站扫描、生成 SBOM |
| **构建管道** | GitHub Actions / GitLab CI 生成 SLSA provenance；Sigstore/Cosign 签名 |
| **制品注册表** | OCI v1.1 reference types 存储 SBOM 和证明 |
| **漏洞运营** | GUAC 或等效工具关联 SBOM + VEX + CSAF；PR 级告警自动化 |
| **AI 组件** | 输出 CycloneDX ML-BOM 或 SPDX 3.0 AI Profile；验证 EU AI Act Annex IV |

---

## 8. 权威来源

| 标准/项目 | URL |
|-----------|-----|
| SLSA Spec | <https://slsa.dev> |
| OpenSSF Scorecard | <https://scorecard.dev> |
| OpenSSF Protobom | <https://github.com/protobom/protobom> |
| OpenSSF S2C2F | <https://github.com/ossf/s2c2f> |
| NIST SP 800-161 Rev. 1 | <https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final> |
| CycloneDX | <https://cyclonedx.org> |
| SPDX | <https://spdx.dev> |
| Sigstore | <https://sigstore.dev> |
| CISA SBOM | <https://www.cisa.gov/sbom> |
| OCI Image Spec | <https://github.com/opencontainers/image-spec> |
| in-toto | <https://in-toto.io> |

---

*文档生成时间：2026-06-06 · 对齐 SLSA v1.2 (2025-11) / OpenSSF Scorecard v5 / CISA SBOM 2025 Draft / OCI v1.1*


---

## 补充章节

## 概念定义

**定义**：SLSA（Supply-chain Levels for Software Artifacts）是 OpenSSF 提出的框架，通过 Source、Build、Provenance、Common 等 Track 定义软件制品的可验证安全等级。

## 示例

**示例**：使用 Sigstore/cosign 对容器镜像进行签名，配合 GitHub Actions 隔离构建与可复现构建证明，达到 SLSA Build L3。

## 反例

**反例**：项目手动从个人仓库下载二进制依赖且无哈希校验，构建环境未隔离，无法达到 SLSA L1。

## 分析

**分析**：SLSA 将供应链安全分解为可升级、可审计的等级，是组织渐进式改进的路线图。