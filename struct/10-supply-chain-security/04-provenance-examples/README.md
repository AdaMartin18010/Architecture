# SLSA Provenance 可执行示例

> **对齐**：SLSA v1.2 Build Track L3、Sigstore/Cosign、OCI v1.1 Reference Types、GitHub Actions

---

## 1. 概念定义

**Provenance（来源证明）**：以密码学方式记录软件制品如何被构建、由谁构建、基于哪些输入的元数据。在 SLSA（Supply-chain Levels for Software Artifacts）框架中，provenance 是 Build Track 的核心交付物，用于回答"这个制品从哪来、是否被篡改"的问题。

**Attestation（证明）**：对某一声明（如"此镜像由某 CI 工作流构建"）的密码学签名文档。SLSA provenance 是一种特定类型的 attestation，遵循 in-toto 证明格式。

**OCI Reference Types**：OCI v1.1 引入的机制，允许将 SBOM、provenance、签名等元数据作为 artifact 的 referrers 附加到注册表，无需修改原镜像内容即可实现信任元数据的统一检索。

## 2. 示例清单

| 文件 | 说明 |
|------|------|
| `slsa-provenance-github-action.yml` | GitHub Actions 工作流：构建镜像 → 生成 SLSA provenance → Cosign keyless 签名 → SBOM 验证 |

---

## 3. 工作流阶段

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

## 4. 关键特性

- **SLSA Build L3**：使用 GitHub Actions SLSA generator，非伪造 provenance
- **Sigstore Keyless**：无需管理长期私钥；Fulcio 短期证书 + Rekor 透明日志
- **OCI v1.1 Reference Types**：SBOM 和 provenance 作为镜像 digest 的 referrers 附加，不修改镜像本身
- **双格式 SBOM**：SPDX 2.3 JSON + CycloneDX 1.6 JSON
- **漏洞门禁**：Grype `--fail-on high` 阻止高危漏洞流入生产

---

## 5. 使用方式

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

# 5. 验证 SLSA provenance（使用 slsa-verifier 或 GitHub CLI）
gh attestation verify <artifact> --owner 你的组织
```

---

## 6. 与项目复用体系的映射

| 项目目录 | 供应链安全角色 |
|----------|----------------|
| `struct/04-component-architecture-reuse/` | 容器镜像 = 可复用组件；OCI provenance = 组件信任护照 |
| `struct/06-cross-layer-governance/` | SLSA L3 + SBOM = 组件目录准入门槛 |
| `struct/10-supply-chain-security/` | SLSA、Sigstore、SBOM 的完整工具链 |

---

## 7. 正向示例：容器镜像端到端来源证明

### 示例 A：使用 GitHub Artifact Attestations 验证容器镜像

某 DevOps 团队在构建容器镜像时使用以下模式：

```yaml
- name: Build and push image
  id: build
  uses: docker/build-push-action@v6
  with:
    push: true
    tags: ghcr.io/org/app:${{ github.sha }}

- name: Attest provenance
  uses: actions/attest-build-provenance@v1
  with:
    subject-name: ghcr.io/org/app
    subject-digest: ${{ steps.build.outputs.digest }}
    push-to-registry: true
```

发布后在部署流水线中强制验证：

```bash
gh attestation verify \
  --owner org \
  --predicate-type https://slsa.dev/provenance/v1 \
  ghcr.io/org/app@sha256:<digest>
```

该模式使部署系统只接受由特定 GitHub 工作流、特定源码 commit 构建的镜像，阻断被入侵开发者本地构建的未授权镜像。

### 示例 B：OCI v1.1 Referrers 聚合 SBOM 与签名

通过 OCI v1.1 的 referrers API，镜像消费者无需修改原镜像即可获取其 SBOM 和 provenance：

```bash
# 查询镜像的所有 referrers（SBOM、provenance、signature）
regctl artifact list ghcr.io/org/app@sha256:<digest>

# 拉取 SPDX SBOM
regctl artifact get --subject ghcr.io/org/app@sha256:<digest> \
  --filter-artifact-type application/spdx+json
```

该模式已被 Docker Hub、GitHub Container Registry、Azure Container Registry 等主流注册表支持。

---

## 8. 反例 / 反模式

### 反例 A：curl | bash 执行未签名脚本

2021 年 Codecov 事件中，大量 CI 流水线使用 `bash <(curl -s https://codecov.io/bash)` 执行 Codecov Bash Uploader。攻击者修改该脚本后，在数万个 CI 环境中窃取了环境变量和密钥。根本原因是：没有 provenance、没有完整性校验、没有最小权限隔离。

### 反例 B：静态维护 provenance 文件

某团队将 `provenance.json` 作为静态文件提交到仓库，并声称符合 SLSA L2。实际上该文件未与构建产物绑定，无法防止构建后篡改；且签名使用长期个人 GPG 密钥，密钥泄露后无法追溯。正确的 provenance 必须由构建平台在构建时动态生成并签名。

---

## 9. 控制点映射：SLSA Build Track L2/L3 → 工作流实现

| SLSA 要求 | 工作流实现 | 验证命令 |
|----------|-----------|---------|
| L1：自动化 provenance | `.github/workflows/slsa-provenance.yml` 触发构建 | 检查 Actions 运行日志 |
| L2：托管构建 + 签名 | `slsa-github-generator` 生成 provenance；`actions/attest-build-provenance` 签名 | `gh attestation verify` |
| L2：来源可验证 | provenance 中 `resolvedDependencies` 包含 commit SHA | `slsa-verifier --source-uri` |
| L3：临时/隔离构建 | GitHub-hosted runner；构建步骤禁用外部网络 | 审计 runner 配置与网络策略 |
| L3：非伪造 provenance | OIDC 联邦身份签名，签名密钥对构建者不可见 | 验证 certificate-identity 与 oidc-issuer |
| SBOM 关联 | Syft 生成 SPDX/CycloneDX 并作为 OCI referrer | `regctl artifact list` |

---

## 10. 权威来源

| 来源 | URL | 说明 | 核查日期 |
|------|-----|------|----------|
| SLSA Specification v1.2 | <https://slsa.dev/spec/v1.2/> | Multi-Track 架构与 Build Track L1-L3 | 2026-07-08 |
| SLSA Provenance v1 | <https://slsa.dev/spec/v1.2/provenance> | Provenance predicate 格式 | 2026-07-08 |
| Sigstore / cosign | <https://docs.sigstore.dev/cosign/overview/> | 无密钥签名与验证 | 2026-07-08 |
| GitHub Artifact Attestations | <https://docs.github.com/en/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds> | 原生 provenance 生成与验证 | 2026-07-08 |
| OCI v1.1 Reference Types | <https://github.com/opencontainers/image-spec/blob/main/manifest.md> | OCI referrers 规范 | 2026-07-08 |
| SLSA GitHub Generator | <https://github.com/slsa-framework/slsa-github-generator> | 自动生成 SLSA provenance | 2026-07-08 |
| slsa-verifier | <https://github.com/slsa-framework/slsa-verifier> | Provenance 验证 CLI | 2026-07-08 |

---

*文档生成时间：2026-07-08 · 对齐 SLSA v1.2 / Sigstore / OCI v1.1*
