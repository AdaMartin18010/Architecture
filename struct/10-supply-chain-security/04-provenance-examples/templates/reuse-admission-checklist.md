# 组件复用准入检查单（Component Reuse Admission Checklist）

> **版本**: 2026-06-12
> **定位**: 在将外部/开源/内部组件引入系统前，执行最小可接受的安全与合规检查。
> **适用对象**: 架构师、安全工程师、开发团队、供应链治理团队。

---

## 检查单总览

| 检查项 | 关键交付物 | 合格标准 | 责任人 | 状态 |
|--------|-----------|---------|--------|------|
| 1. SBOM | `sbom-spdx-3.0-template.json` 或 `sbom-cyclonedx-1.6-template.json` | 组件提供 SPDX 2.3/3.0+ 或 CycloneDX 1.4+ SBOM | 组件提供方 / 架构师 | ☐ |
| 2. Provenance | `slsa-provenance-template.intoto.jsonl` | SLSA Build L2+ provenance attestation 存在且可验证 | 安全工程师 | ☐ |
| 3. 签名 | Sigstore/cosign / GPG / HSM 签名 | 制品签名可验证，公钥/证书可信 | 安全工程师 | ☐ |
| 4. 漏洞扫描 | OSV、Snyk、Dependabot、Trivy 等报告 | 无 Critical/High 未修复漏洞；已知漏洞有 VEX 说明 | 开发团队 | ☐ |
| 5. 许可证审查 | FOSSA、Black Duck 或人工审查记录 | 许可证与组织策略兼容；Copyright 清晰 | 合规团队 | ☐ |

---

## 1. SBOM（软件物料清单）

### 1.1 必备字段

- [ ] 组件名称与版本（`name` / `version`）
- [ ] 唯一标识（`purl`、`CPE` 或 `swid`）
- [ ] 供应商/作者信息（`supplier`、`originator`、`manufacture`）
- [ ] 哈希校验值（SHA-256 或 stronger）
- [ ] 许可证结论与声明（`licenseConcluded` / `licenseDeclared`）
- [ ] 依赖关系（直接 + 传递依赖，`dependencies`）
- [ ] SBOM 生成工具与生成时间戳

### 1.2 可接受格式（按优先级）

1. **SPDX 3.0.1**（推荐新项目）
2. SPDX 2.3
3. CycloneDX 1.6
4. SWID ISO/IEC 19770-2:2015（特定合规场景）

### 1.3 拒绝标准

- 缺少版本或 purl/cpe/swid 任一种标识。
- 依赖树未展开或缺失传递依赖。
- 许可证字段为 `NOASSERTION` 且无补充说明。

---

## 2. Provenance（来源证明）

### 2.1 SLSA v1.2 Build Track 要求

- [ ] **Build L1**: Provenance 存在（`https://slsa.dev/provenance/v1` predicate）。
- [ ] **Build L2**: Provenance 由托管构建服务生成并签名；构建服务身份可验证。
- [ ] **Build L3**: Hermetic / Reproducible Build；依赖不可变；构建环境受控。

### 2.2 必含字段

- [ ] `subject` 包含制品名与 digest。
- [ ] `buildDefinition.buildType` 明确。
- [ ] `externalParameters` 记录触发构建的输入。
- [ ] `resolvedDependencies` 列出所有解析后的依赖及其 digest。
- [ ] `runDetails.builder.id` 可验证。

### 2.3 验证命令示例

```bash
# cosign 验证 SLSA provenance
# 需要组件提供方在发布时生成并上传 intoto.jsonl
cosign verify-attestation \
  --type slsaprovenance \
  --certificate-identity-regexp '^https://github.com/example/reuse-component/.github/workflows/.*' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  example/reuse-component:1.0.0
```

---

## 3. 签名（Signature）

### 3.1 可接受签名机制

- [ ] **Sigstore/cosign**: 基于 OIDC 的短期证书 + Rekor 透明日志。
- [ ] **GPG**: 维护者长期公钥，需通过可信渠道分发并校验 fingerprint。
- [ ] **HSM / KMS**: 企业级密钥管理，满足内部合规要求。

### 3.2 验证要求

- [ ] 签名覆盖制品文件本身（jar/wheel/npm tarball 等）。
- [ ] 签名证书/公钥可信且在有效期内。
- [ ] 对于 Sigstore，验证 Rekor entry 存在且未过期。

### 3.3 拒绝标准

- 仅校验 MD5/SHA1（弱哈希）。
- 签名文件与制品文件分开存放且无绑定关系。
- 使用自签名证书且无信任锚。

---

## 4. 漏洞扫描（Vulnerability Scanning）

### 4.1 扫描范围

- [ ] 组件本身及其所有传递依赖。
- [ ] 容器镜像层（如适用）。
- [ ] 构建时与运行时依赖均需覆盖。

### 4.2 可接受工具

- [ ] OSV / Google OSV-Scanner
- [ ] Snyk Open Source
- [ ] GitHub Dependabot
- [ ] Trivy / Grype
- [ ] 企业内部 SCA 平台

### 4.3 合格标准

| 严重度 | 准入要求 |
|--------|---------|
| Critical | 必须修复或提供经安全团队批准的 VEX 例外 |
| High | 原则上修复；如无法修复需记录缓解措施 |
| Medium | 建议修复，允许带风险引入并制定修复计划 |
| Low | 记录即可 |

### 4.4 VEX 声明

若存在已知未利用漏洞，需提供:

- [ ] VEX 文档（CycloneDX VEX 或 OpenVEX）。
- [ ] 漏洞编号（CVE/GHSA/OSV ID）。
- [ ] 状态（`not_affected` / `affected` / `fixed` / `under_investigation`）。
- [ ] 理由与影响分析。

---

## 5. 许可证审查（License Review）

### 5.1 必查信息

- [ ] 组件主许可证（SPDX 标识符）。
- [ ] 传递依赖的许可证组合。
- [ ] Copyright 声明与归属要求。
- [ ] 专利/商标/出口管制声明（如 GPL、SSPL、CC-NC 等）。

### 5.2 常见风险许可证

| 许可证 | 风险说明 | 建议 |
|--------|---------|------|
| GPL-2.0/3.0 | Copyleft，可能触发衍生作品开源义务 | 法务评审 |
| AGPL-3.0 | 网络使用也触发开源义务 | 通常禁止用于服务端闭源组件 |
| SSPL | 非 OSI 认可，云服务限制 | 通常禁止 |
| CC-NC | 非商业限制 | 商业产品禁止 |
| 自定义 / 未知 | 权利义务不清晰 | 必须法务确认 |

### 5.3 可接受许可证（示例）

- MIT
- Apache-2.0
- BSD-2-Clause / BSD-3-Clause
- ISC
- 经法务批准的企业内部许可

---

## 6. 审批与归档

### 6.1 准入审批

- [ ] 架构师确认组件与目标架构匹配。
- [ ] 安全工程师确认 SBOM、Provenance、签名、漏洞扫描通过。
- [ ] 合规团队确认许可证无冲突。
- [ ] 项目经理/技术负责人最终批准。

### 6.2 归档要求

- [ ] SBOM 文件存入组织制品仓库或 SBOM 管理平台。
- [ ] Provenance attestation 与签名文件随组件版本归档。
- [ ] 漏洞扫描报告与 VEX（如适用）关联到组件版本。
- [ ] 许可证审查记录存入法务/合规系统。

---

## 7. 参考模板

| 模板 | 用途 | 文件 |
|------|------|------|
| SPDX 3.0.1 SBOM | 标准化物料清单 | `sbom-spdx-3.0-template.json` |
| CycloneDX 1.6 SBOM | 标准化物料清单 | `sbom-cyclonedx-1.6-template.json` |
| SLSA v1.2 Provenance | Build Track 来源证明 | `slsa-provenance-template.intoto.jsonl` |

---

> **使用提示**:
>
> - 本检查单为最小集合，金融、政务、关键基础设施等场景应在此基础上增加行业特定要求。
> - 建议将本检查单集成到 CI/CD 门禁（gate）中，未通过的组件禁止进入主分支或生产环境。
>
> 最后更新: 2026-06-12


---

## 补充章节
## 概念定义

**定义**：软件供应链安全关注从源代码、依赖、构建、分发到部署全链路中，复用资产不被篡改、注入漏洞或引入许可证风险；SLSA、SBOM 与签名验证是核心机制。

## 示例

**示例**：组织采用 SLSA L3 构建流程：源码托管、构建环境隔离、构建产物签名并生成SPDX SBOM；Log4j 类事件发生时 2 小时内定位受影响服务。

## 反例

**反例**：XZ Utils 后门事件显示，未对压缩依赖进行来源验证与行为审计，恶意代码可潜伏数年并随复用传播到大量系统。

## 权威来源

> **权威来源**:
>
> - [SLSA Framework](https://slsa.dev)
> - [OpenSSF](https://openssf.org)
> - [SPDX](https://spdx.dev)
> - [CycloneDX](https://cyclonedx.org)
> - 核查日期：2026-07-07