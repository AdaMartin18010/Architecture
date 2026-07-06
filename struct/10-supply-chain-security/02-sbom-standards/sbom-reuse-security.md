# SPDX vs CycloneDX vs SWID 复用安全应用对比

> **版本**: 2026-06-06
> **权威来源**: SPDX 3.0.1 (ISO/IEC 5962), CycloneDX 1.6/1.7 (ECMA-424), SWID ISO/IEC 19770-2:2015, NTIA Minimum Elements, CISA SBOM Framing 2024, BSI TR-03183-2
> **定位**: Track D 供应链安全工程深化内容，支撑采购审计与事件响应决策
> **交叉引用**: `struct/10-supply-chain-security/02-sbom-standards/sbom-comparison.md`, `struct/04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md`

---

## 1. 引言：SBOM 作为复用安全的"身份护照"

Software Bill of Materials（SBOM）在架构复用中的角色已从"合规附件"演进为"安全决策基础设施"。
当组织复用一个开源组件或采购一个商业软件时，SBOM 回答了三个根本问题：**这是什么？从哪来？有什么风险？**

然而，并非所有 SBOM 格式在所有场景下都等效。SPDX、CycloneDX 和 SWID 的设计哲学、信息模型和生态工具链存在显著差异，直接影响其在复用安全生命周期中的效用。
本文件基于 2026 年最新规范（SPDX 3.0.1、CycloneDX 1.6/1.7、SWID ISO/IEC 19770-2），建立 **3 标准 x 4 应用场景** 的决策矩阵，并提供可执行的生成示例。

> **定理 SBOM.1** (Format-Scenario Fit): SBOM 的安全价值 = 格式表达能力 x 场景需求匹配度 x 工具链成熟度。格式选择错误会导致信息损失（lossy translation）或合规失效。

---

## 2. 三标准核心特性对比（2026 更新版）

| 特性维度 | SPDX 3.0.1 | CycloneDX 1.6+ | SWID ISO/IEC 19770-2 |
|---------|-----------|---------------|---------------------|
| **标准化组织** | Linux Foundation / ISO/IEC 5962 | OWASP / ECMA-424 | ISO/IEC / NIST |
| **设计哲学** | 许可证合规优先，通用语义模型 | 供应链安全优先，轻量敏捷 | 软件资产管理（ITAM）优先 |
| **数据模型** | 图模型（Element + Relationship） | 层次模型（bom -> components -> dependencies） | 标签模型（SoftwareIdentity + Entity + Payload） |
| **漏洞表达** | 通过 VEX 扩展（独立文件） | **原生支持** vulnerabilities[] | 不支持 |
| **许可证表达** | **非常丰富**（SPDX License Expressions, 400+ 标准标识符） | 支持（SPDX 标识符 + 自定义） | 有限 |
| **依赖关系** | **优秀**（11+ 种 Relationship 类型） | **优秀**（依赖图 + pedigree） | **有限**（Payload 文件清单，无传递依赖） |
| **签名支持** | 支持（通过外部工具） | **原生支持** CDXA（CycloneDX Attestation） | 支持（XML Signature） |
| **AI/ML 支持** | **AI Profile**（数据集、模型、训练参数） | **Formulations**（配方/构建步骤） | 不支持 |
| **生态工具** | Microsoft SBOM Tool, Syft, FOSSology | cdxgen, OWASP Dependency-Track, Syft | SWID Tag Creator（有限） |

> **引用**: "CycloneDX 1.6 added Cryptographic BOM (CBOM) and attestation support (CDXA)... CycloneDX 1.7 added citations for provenance." [^1]
> **引用**: "SPDX 3.0 introduced a profile-based architecture where the core specification defines common elements and optional profiles (Security, Licensing, Build, AI, Dataset) extend the model." [^2]

---

## 3. 3 x 4 应用场景决策矩阵

### 3.1 场景一：开发时安全扫描（DevSecOps Shift-Left）

**场景描述**: 开发者在编码阶段或 CI 构建阶段生成 SBOM，用于即时漏洞扫描和许可证冲突检测。

| 评估维度 | SPDX 3.0.1 | CycloneDX 1.6+ | SWID |
|---------|-----------|---------------|------|
| **生成速度** | 中（模型复杂） | **快**（JSON 轻量） | 慢（XML 冗长） |
| **漏洞关联** | 需 VEX 扩展 | **原生优秀** | 不支持 |
| **IDE 集成** | 有限 | **优秀**（Dependency-Track, Jenkins, GitHub） | 无 |
| **推荐度** | 3/5 | 5/5 | 1/5 |
| **推荐理由** | 许可证分析强，但漏洞需额外步骤 | 原生漏洞支持，DevSecOps 工具链最完善 | 不满足安全扫描需求 |

**推荐格式**: **CycloneDX JSON**

**理由**:
CycloneDX 的原生 vulnerabilities[] 数组和 dependency 图结构使 OWASP Dependency-Track、Snyk、Grype 等工具能够直接消费，无需格式转换。
其 JSON 序列化在 CI 环境中解析速度比 SPDX RDF/XML 快 3-5 倍。

---

### 3.2 场景二：采购审计（Vendor Due Diligence）

**场景描述**: 组织在采购商业软件或评估开源组件时，要求供应商提供 SBOM 以进行安全、合规和供应链风险评估。

| 评估维度 | SPDX 3.0.1 | CycloneDX 1.6+ | SWID |
|---------|-----------|---------------|------|
| **许可证深度** | **优秀**（400+ 标准标识符，文件级归因） | 良好 | 有限 |
| **合规认可度** | **高**（ISO 标准，美国 FDA 引用） | **高**（ECMA 标准，OWASP 背书） | 中（NIST 要求，但工具生态弱） |
| **供应商信息** | 丰富（supplier, originator, downloadLocation） | 丰富（supplier, publisher, author） | 基础（Entity role） |
| **审计可追溯性** | **优秀**（CreationInfo, verifiedUsing 哈希链） | 良好（metadata.timestamp, tools[]） | 基础 |
| **推荐度** | 5/5 | 4/5 | 2/5 |
| **推荐理由** | ISO 标准 + 许可证深度 = 法律审计最优 | 安全分析强，但许可证不如 SPDX 精细 | 仅适用于资产盘点场景 |

**推荐格式**: **SPDX 3.0.1 JSON**（法律/合规主导）或 **CycloneDX 1.6 JSON**（安全主导）

**理由**:
采购审计通常由法务和安全团队联合执行。SPDX 的许可证表达能力（SPDX License Expressions、文件级版权文本）使其成为法务审计的首选；
CycloneDX 1.6 的 CDXA（CycloneDX Attestation）支持"合规即代码"，可将审计证据直接嵌入 SBOM。若需满足欧盟 CRA（Cyber Resilience Act），BSI TR-03183-2 明确接受 SPDX 3.0.1+ 和 CycloneDX 1.6+ [^3]。

---

### 3.3 场景三：事件响应（Incident Response）

**场景描述**: 新漏洞（如 Log4Shell、XZ Utils）爆发时，组织需要快速回答"我是否受影响？影响范围多大？"

| 评估维度 | SPDX 3.0.1 | CycloneDX 1.6+ | SWID |
|---------|-----------|---------------|------|
| **快速查询** | 中（需遍历 Relationship 图） | **快**（扁平组件列表 + PURL/CPE 索引） | 慢 |
| **漏洞匹配** | 需外部 VEX | **原生**（vulnerabilities + VEX 内嵌） | 不支持 |
| **影响范围分析** | **优秀**（DESCRIBES/DEPENDS_ON/CONTAINS 关系） | **优秀**（dependency 图传递分析） | 差（无依赖关系） |
| **运行时 SBOM** | 支持（通过外部扩展） | **原生支持**（formulations + 运行时组件） | 不支持 |
| **推荐度** | 4/5 | 5/5 | 1/5 |
| **推荐理由** | 关系模型强，但需额外工具解析 | 原生漏洞+依赖图 = 事件响应最快路径 | 完全不适用 |

**推荐格式**: **CycloneDX 1.6 JSON + VEX**

**理由**:
事件响应的核心是速度。CycloneDX 的原生漏洞支持和清晰的 dependencies 图使安全团队能够在数分钟内完成全系统影响分析。
2026 年的最佳实践是将 VEX（Vulnerability Exploitability eXchange）直接嵌入 CycloneDX BOM，而非作为独立文件分发，减少查询时的文件关联开销。

> **引用**: "CISA Framing Software Component Transparency (2024) elevates SBOMs from simple component lists to verifiable security assets." [^4]

---

### 3.4 场景四：合规报告（Regulatory Compliance）

**场景描述**: 向监管机构（欧盟 BSI、美国 CISA、FDA）提交软件成分透明性证明，满足 EO 14028、EU CRA、FDA 预市场指导等要求。

| 评估维度 | SPDX 3.0.1 | CycloneDX 1.6+ | SWID |
|---------|-----------|---------------|------|
| **EO 14028 / NTIA** | 满足 | 满足 | 满足 |
| **EU CRA / BSI TR-03183-2** | **明确要求 3.0.1+** | **明确要求 1.6+** | 未列入 |
| **FDA 医疗器械** | 引用 SPDX | 引用 CycloneDX | 未引用 |
| **NIST SP 800-53** | 格式无关 | 格式无关 | 格式无关 |
| **NTIA 最小要素覆盖** | **完整** | **完整** | 基础 |
| **推荐度** | 5/5 | 5/5 | 2/5 |
| **推荐理由** | 国际标准 = 全球合规 | 安全聚焦 = 监管机构认可 | 仅满足美国部分联邦要求 |

**推荐格式**: **SPDX 3.0.1 JSON**（全球合规首选）或 **CycloneDX 1.6 JSON**（安全合规一体化）

**理由**:
2026 年，欧盟 CRA 的实施指导 BSI TR-03183-2 是全球最严格的 SBOM 合规框架，它明确要求 SPDX 3.0.1+ 或 CycloneDX 1.6+，JSON 或 XML 格式，且强制要求密码学哈希、许可证标识符和签名机制 [^3]。
SWID 未被 BSI 列入认可格式，其工具生态系统也无法满足 CRA 的深度要求 [^5]。

---

## 4. 综合决策矩阵

| 应用场景 | 首选格式 | 次选格式 | 避免使用 | 关键理由 |
|---------|---------|---------|---------|---------|
| **开发时安全扫描** | CycloneDX JSON | SPDX JSON | SWID | 原生漏洞支持，DevSecOps 工具链完善 |
| **采购审计** | SPDX 3.0.1 JSON | CycloneDX 1.6 JSON | SWID | ISO 标准 + 许可证深度 = 法律审计最优 |
| **事件响应** | CycloneDX + VEX | SPDX + 外部 VEX | SWID | 速度优先，原生漏洞+依赖图 |
| **合规报告** | SPDX 3.0.1 JSON | CycloneDX 1.6 JSON | SWID | BSI TR-03183-2 明确要求 SPDX 3.0+ 或 CycloneDX 1.6+ |

---

## 5. SBOM 生成示例

### 5.1 SPDX 3.0.1 JSON 示例

```json
{
  "spdxVersion": "SPDX-3.0.1",
  "SPDXID": "SPDXRef-DOCUMENT",
  "name": "acme-payment-gateway-sbom",
  "documentNamespace": "https://acme.com/sbom/payment-gateway/v2.1.0",
  "creationInfo": {
    "created": "2026-06-06T10:30:00Z",
    "createdBy": ["Tool: syft-1.21.0", "Organization: Acme Security Team"],
    "specVersion": "3.0.1"
  },
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-log4j-core",
      "name": "log4j-core",
      "downloadLocation": "https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/",
      "filesAnalyzed": false,
      "licenseConcluded": "NOASSERTION",
      "licenseDeclared": "Apache-2.0",
      "copyrightText": "NOASSERTION",
      "versionInfo": "2.17.1",
      "packageVerificationCode": {
        "packageVerificationCodeValue": "a3f2b8c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t"
      },
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:maven/org.apache.logging.log4j/log4j-core@2.17.1"
        },
        {
          "referenceCategory": "SECURITY",
          "referenceType": "cpe23Type",
          "referenceLocator": "cpe:2.3:a:apache:log4j:2.17.1:*:*:*:*:*:*:*"
        }
      ],
      "supplier": "Organization: Apache Software Foundation"
    },
    {
      "SPDXID": "SPDXRef-Package-spring-boot",
      "name": "spring-boot",
      "versionInfo": "3.2.0",
      "downloadLocation": "https://repo.maven.apache.org/maven2/org/springframework/boot/spring-boot/3.2.0/",
      "licenseDeclared": "Apache-2.0",
      "supplier": "Organization: VMware, Inc.",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:maven/org.springframework.boot/spring-boot@3.2.0"
        }
      ]
    }
  ],
  "relationships": [
    {
      "spdxElementId": "SPDXRef-DOCUMENT",
      "relatedSpdxElement": "SPDXRef-Package-log4j-core",
      "relationshipType": "DESCRIBES"
    },
    {
      "spdxElementId": "SPDXRef-Package-spring-boot",
      "relatedSpdxElement": "SPDXRef-Package-log4j-core",
      "relationshipType": "DEPENDS_ON"
    }
  ]
}
```

> **说明**: 此示例符合 NTIA 最小要素要求（Supplier Name, Component Name, Version, Unique Identifier, Dependency Relationship, Author, Timestamp），并包含 CISA Framing 2024 推荐的 packageVerificationCode 和 externalRefs（PURL/CPE）用于自动化漏洞关联。

### 5.2 CycloneDX 1.6 XML 示例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bom xmlns="http://cyclonedx.org/schema/bom/1.6"
     serialNumber="urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79"
     version="1">
  <metadata>
    <timestamp>2026-06-06T10:30:00Z</timestamp>
    <tools>
      <tool>
        <vendor>OWASP</vendor>
        <name>Dependency-Track</name>
        <version>4.12.0</version>
      </tool>
    </tools>
    <authors>
      <author>
        <name>Acme Security Team</name>
        <email>security@acme.com</email>
      </author>
    </authors>
    <supplier>
      <name>Acme Corporation</name>
      <url>https://acme.com</url>
    </supplier>
  </metadata>
  <components>
    <component type="library" bom-ref="pkg:maven/org.apache.logging.log4j/log4j-core@2.17.1">
      <group>org.apache.logging.log4j</group>
      <name>log4j-core</name>
      <version>2.17.1</version>
      <description>Apache Log4j Core</description>
      <scope>required</scope>
      <hashes>
        <hash alg="SHA-256">a3f2b8c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f</hash>
      </hashes>
      <licenses>
        <license>
          <id>Apache-2.0</id>
        </license>
      </licenses>
      <purl>pkg:maven/org.apache.logging.log4j/log4j-core@2.17.1</purl>
      <cpe>cpe:2.3:a:apache:log4j:2.17.1:*:*:*:*:*:*:*</cpe>
    </component>
    <component type="library" bom-ref="pkg:maven/org.springframework.boot/spring-boot@3.2.0">
      <group>org.springframework.boot</group>
      <name>spring-boot</name>
      <version>3.2.0</version>
      <description>Spring Boot</description>
      <scope>required</scope>
      <licenses>
        <license>
          <id>Apache-2.0</id>
        </license>
      </licenses>
      <purl>pkg:maven/org.springframework.boot/spring-boot@3.2.0</purl>
    </component>
  </components>
  <dependencies>
    <dependency ref="pkg:maven/org.springframework.boot/spring-boot@3.2.0">
      <dependency ref="pkg:maven/org.apache.logging.log4j/log4j-core@2.17.1"/>
    </dependency>
  </dependencies>
</bom>
```

> **说明**: 此示例展示了 CycloneDX XML 格式的核心结构：metadata（创建信息）、components（组件清单，含哈希、许可证、PURL、CPE）、dependencies（依赖关系图）。该格式可直接被 OWASP Dependency-Track 消费，实现自动化漏洞告警。

---

## 6. 与依赖治理的交叉引用

`struct/04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md` 提出了 Lockfile 安全性和分层防御策略。SBOM 是这一策略的输出证明：

| 防御层 | 依赖治理措施 | SBOM 角色 | 推荐格式 |
|-------|-------------|----------|---------|
| Layer 1: Proxy Registry | 缓存公共 registry，自动漏洞扫描 | 记录代理来源和扫描结果 | CycloneDX JSON |
| Layer 2: 审批工作流 | 新包/新版本需安全团队审批 | 审批决策的证据基线 | SPDX JSON |
| Layer 3: Lockfile + 哈希 | 精确版本锁定，密码学哈希验证 | 验证 SBOM 中的 hashes[] 与 lockfile 一致性 | CycloneDX JSON |
| Layer 4: Vendoring | 关键系统完全离线构建 | 离线构建的组件清单和许可证报告 | SPDX JSON |

> **定理 SBOM.2** (SBOM-Lockfile Consistency): 若 SBOM 中组件的哈希值与 lockfile 中记录的哈希值不一致，则表明构建过程或 SBOM 生成过程存在篡改，该资产应被禁止复用。

---

## 7. 参考索引

[^1]: CycloneDX.org, "Authoritative Guide to SBOM - Use Cases", <https://cyclonedx.org/guides/sbom/use_cases/>
[^2]: SPDX Specification v3.0, "Using SPDX to comply with Norms, Standards and Regulation", <https://spdx.github.io/spdx-spec/v3.0/pdf/combined.pdf>
[^3]: CRA Decoded, "CRA SBOM Requirements: What is Mandated, What is Optional, and What is Still Unclear", 2026-05-12
[^4]: OpenSSF SPDX/CycloneDX Standards TAG, "Cross-Industry SBOM Quality Guide", 2025
[^5]: SBOMify, "SBOM Formats Compared: CycloneDX vs SPDX", 2026-01-15

---

> 最后更新: 2026-06-06
> 关联文件: sbom-comparison.md, struct/04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md


---

## 补充说明：SPDX vs CycloneDX vs SWID 复用安全应用对比

## 概念定义

**定义**：SBOM（Software Bill of Materials）以机器可读格式（SPDX、CycloneDX、SWID）枚举软件组件、版本、许可证与来源，是复用资产透明化的基础。

## 示例

**示例**：在 CI 中为每个服务生成 CycloneDX SBOM，漏洞数据库匹配后自动生成影响范围报告，复用组件升级决策从数周缩短到数小时。

## 反例

**反例**：组织复用开源库多年却从未维护 SBOM，许可证冲突与安全漏洞只能在诉讼或事件爆发后被动发现。
