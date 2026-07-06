# SLSA Provenance 可执行示例

> **对齐**：SLSA v1.2 Build Track L3、Sigstore/Cosign、OCI v1.1 Reference Types、GitHub Actions

---

## 1. 示例清单

| 文件 | 说明 |
|------|------|
| `slsa-provenance-github-action.yml` | GitHub Actions 工作流：构建镜像 → 生成 SLSA provenance → Cosign keyless 签名 → SBOM 验证 |

---

## 2. 工作流阶段

```text
Push/Tag
   │
   ▼
[Build] ──► Docker image + OCI provenance/SBOM attestation
   │
   ▼
[Provenance] ──► SLSA Build L3 attestation (slsa-github-generator)
   │
   ▼
[Sign] ──► Cosign keyless sign via Sigstore/Fulcio/Rekor
   │
   ▼
[Verify] ──► Syft SBOM 生成 + Grype 漏洞扫描
```

---

## 3. 关键特性

- **SLSA Build L3**：使用 GitHub Actions SLSA generator，非伪造 provenance
- **Sigstore Keyless**：无需管理长期私钥；Fulcio 短期证书 + Rekor 透明日志
- **OCI v1.1 Reference Types**：SBOM 和 provenance 作为镜像 digest 的 referrers 附加，不修改镜像本身
- **双格式 SBOM**：SPDX 3.0 JSON + CycloneDX 1.7 JSON
- **漏洞门禁**：Grype `--fail-on high` 阻止高危漏洞流入生产

---

## 4. 使用方式

```bash
# 1. 复制到仓库
cp slsa-provenance-github-action.yml .github/workflows/slsa-provenance.yml

# 2. 推送后，在 Actions 标签页查看运行结果

# 3. 本地验证签名
cosign verify \
  --certificate-identity-regexp="https://github.com/你的组织/你的仓库/" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  ghcr.io/你的组织/你的仓库@sha256:...

# 4. 查看 SBOM referrers
regctl manifest get ghcr.io/你的组织/你的仓库@sha256:... --referrers
```

---

## 5. 与项目复用体系的映射

| 项目目录 | 供应链安全角色 |
|----------|----------------|
| `struct/04-component-architecture-reuse/` | 容器镜像 = 可复用组件；OCI provenance = 组件信任护照 |
| `struct/06-cross-layer-governance/` | SLSA L3 + SBOM = 组件目录准入门槛 |
| `struct/10-supply-chain-security/` | SLSA、Sigstore、SBOM 的完整工具链 |

---

*文档生成时间：2026-06-06 · 对齐 SLSA v1.2 / Sigstore / OCI v1.1*


---

## 补充说明：SLSA Provenance 可执行示例

## 概念定义

**定义**：SLSA（Supply-chain Levels for Software Artifacts）是 OpenSSF 提出的框架，通过 Source、Build、Provenance、Common 等 Track 定义软件制品的可验证安全等级。

## 示例

**示例**：使用 Sigstore/cosign 对容器镜像进行签名，配合 GitHub Actions 隔离构建与可复现构建证明，达到 SLSA Build L3。

## 反例

**反例**：项目手动从个人仓库下载二进制依赖且无哈希校验，构建环境未隔离，无法达到 SLSA L1。

## 权威来源

> **权威来源**:
>
> - [SLSA Framework](https://slsa.dev)
> - [OpenSSF SLSA](https://openssf.org/projects/slsa/)
> - 核查日期：2026-07-07

## 分析

**分析**：SLSA 将供应链安全分解为可升级、可审计的等级，是组织渐进式改进的路线图。
