# SBOM 格式对比：SPDX vs CycloneDX vs SWID

> **版本**: 2026-06-06
> **定位**: 对比主流 SBOM 格式的特性、适用场景与复用策略

---

## 1. 三种格式概览

| 特性 | SPDX (ISO/IEC 5962) | CycloneDX (OWASP) | SWID (ISO/IEC 19770-2) |
|------|---------------------|-------------------|------------------------|
| **标准化组织** | Linux Foundation / ISO | OWASP | ISO/IEC / NIST |
| **主要用途** | 许可证合规 + 供应链安全 | 供应链安全 + 漏洞管理 | 软件资产管理 |
| **表达复杂度** | 高 | 中 | 低 |
| **嵌套依赖支持** | 优秀 | 优秀 | 有限 |
| **许可证信息** | 非常丰富 | 支持 | 有限 |
| **漏洞关联** | 通过 VEX 扩展 | 原生支持 | 较弱 |
| **适用场景** | 企业合规、法律咨询 | 安全运营、DevSecOps | 资产清单、ITAM |

---

## 2. SPDX 详解

SPDX (Software Package Data Exchange) 是 Linux Foundation 主导的开放标准，已被 ISO 接纳为 ISO/IEC 5962。

### 核心元素

```
SPDX Document
├── SPDXID: SPDXRef-DOCUMENT
├── name
├── documentNamespace
├── creators
├── packages[]
│   ├── SPDXID, name, downloadLocation
│   ├── licenseConcluded, licenseDeclared
│   └── externalRefs
├── relationships[]
│   ├── DEPENDS_ON
│   ├── CONTAINS
│   └── DESCRIBES
└── files[], snippets[] (optional)
```

### 优势

- 丰富的许可证表达
- 强大的关系模型
- ISO 国际标准
- 生态工具丰富

### 局限

- 学习曲线陡峭
- 文档可能冗长
- 漏洞信息需要 VEX 扩展

---

## 3. CycloneDX 详解

CycloneDX 是 OWASP 主导的标准，专注于软件供应链安全。

### 核心元素

```
bom.json
├── metadata
├── components[]
│   ├── type, name, version, purl
│   ├── licenses[], hashes[]
│   ├── pedigree, externalReferences
│   └── properties
├── dependencies[]
├── vulnerabilities[] (原生)
└── formulations[]
```

### 优势

- 原生漏洞支持
- DevSecOps 友好
- JSON 格式轻量
- 工具生态完善

### 局限

- 许可证表达不如 SPDX 精细
- 国际标准采纳程度较低

---

## 4. SWID 详解

SWID (Software Identification Tags) 是 ISO/IEC 19770-2 标准。

### 核心元素

```xml
<SoftwareIdentity name="MyApp" tagId="..." version="1.0.0">
    <Entity name="Example Inc." role="softwareCreator"/>
    <Payload>
        <File name="core.jar" SHA256:hash="..."/>
    </Payload>
</SoftwareIdentity>
```

### 优势

- NIST 要求对齐
- 软件资产管理原生支持
- 轻量级

### 局限

- 依赖关系表达弱
- 漏洞和许可证信息支持有限

---

## 5. 格式选择决策

```
SBOM 格式选择
│
├── 主要目标？
│   ├── 许可证合规 → SPDX
│   ├── 安全漏洞管理 → CycloneDX
│   └── 软件资产盘点 → SWID
│
├── 输出格式偏好？
│   ├── JSON → CycloneDX
│   ├── RDF/Tag-Value → SPDX
│   └── XML → SWID/SPDX
│
└── 监管要求？
    ├── 美国联邦 → SWID + SPDX/CycloneDX
    └── 欧盟 CRA → SPDX 或 CycloneDX
```

---

## 6. 2026 趋势

| 需求 | 说明 |
|------|------|
| 运行时 SBOM | 记录实际加载的组件 |
| AI 模型 SBOM | 记录训练数据、依赖库、超参数 |
| VEX 自动化 | 自动化漏洞可利用性评估 |
| SBOM 签名 | 使用 cosign 签名 |
| SBOM 复用 | 组件级组合为系统级 |

---

> 最后更新: 2026-06-06
