# SLSA Build Level 4 概念验证（PoC）

> 位置：`struct/10-supply-chain-security/13-slsa-l4-poc/`
> 版本：2026-07-08
> 对齐来源：SLSA Specification v1.2, Sigstore/cosign, GitHub Actions

---

## 1. 概念定义

**SLSA**（Supply-chain Levels for Software Artifacts，软件制品供应链等级）是由 OpenSSF 提出的框架，用于评估软件供应链安全成熟度。**SLSA Build Level 4** 是构建可信度的最高等级，要求：

- **Two-Person Review（双人审查）**：关键源码变更需至少两名独立审批者，降低单点篡改风险。
- **Hermetic Builds（密封构建）**：构建过程声明并固定所有输入，禁止未声明的外部网络或依赖。
- **Reproducible Builds（可复现构建）**：相同输入（源码、构建脚本、环境）应产生位对位相同的输出。
- **可验证的来源证明（Provenance）**：以不可伪造的方式记录构建者身份、源码版本、构建脚本哈希、输出哈希等元数据。

> **本 PoC 定位**：用最小可运行代码演示上述四个控制点，便于本地验证与教学；未集成真实 Sigstore/cosign 签名或 GitHub OIDC，但字段与校验逻辑已覆盖 L4 关键要素。

---

## 2. PoC 目标

本 PoC 演示 SLSA Build Level 4 核心控制点：

| 控制点 | PoC 中的体现 |
|--------|-------------|
| **双人审查** | `verify-provenance.py` 检查 `REVIEWERS` 记录或 `SLSA_REVIEWERS` 环境变量中至少包含两名审批者。 |
| **密封构建** | `build.py` 显式声明输入文件（`src/main.py`），不访问外部网络，构建脚本自身哈希也被记录。 |
| **可复现构建** | 多次运行 `build.py`（同 commit、同脚本）产生的 `dist/app` 字节相同，`verify-provenance.py` 校验 SHA-256。 |
| **来源证明** | `provenance.json` 包含 `git_commit`、`builder_id`、`build_script_hash`、`source_hash`、`output_hash`。 |

---

## 3. 文件结构

```text
13-slsa-l4-poc/
├── README.md                 # 本说明
├── build.py                  # 模拟构建脚本，生成 dist/app 与 provenance.json
├── verify-provenance.py      # 验证 provenance 与当前环境一致性
├── REVIEWERS                 # 双人审查记录（示例）
├── src/
│   └── main.py               # 待构建的示例源码
└── dist/
    ├── app                   # 构建产物（由 build.py 生成）
    └── provenance.json       # 来源证明（由 build.py 生成）
```

---

## 4. 运行步骤

### 4.1 进入目录

```bash
cd struct/10-supply-chain-security/13-slsa-l4-poc/
```

### 4.2 执行构建

```bash
python build.py
```

输出示例：

```text
[build] Source hash:  e770709c...
[build] Script hash:  65d931be...
[build] Output hash:  e770709c...
[build] Git commit:   e65ffb8...
[build] Provenance:   dist/provenance.json
[build] Build complete: dist/app
```

### 4.3 验证来源证明

```bash
python verify-provenance.py
```

成功时：

```text
[verify] ✔ git commit matches HEAD: e65ffb8...
[verify] ✔ build script hash matches
[verify] ✔ output hash matches provenance
[verify] ✔ two-person review confirmed (reviewers: alice, bob)
[verify] PASS: SLSA L4 checks succeeded
```

失败时（例如源码或构建脚本被篡改）：脚本会明确指出哪一项校验失败。

---

## 5. 正向示例

**场景**：团队发布一个供下游消费的命令行工具。通过本 PoC：

1. 每次构建由 CI 触发，`build.py` 固定读取 `src/main.py`，不访问外部 PyPI。
2. `REVIEWERS` 中登记了 `alice` 和 `bob`，`verify-provenance.py` 确认至少两名审批者。
3. 同一 commit 在本地与 CI runner 上分别运行 `build.py`，输出 `dist/app` 的 SHA-256 一致。
4. `provenance.json` 被上传到制品仓库，下游团队可用 `verify-provenance.py` 校验构建来源。

该流程满足 SLSA Build L4 的最低可运行演示，并可在真实场景中替换为 Sigstore/cosign 签名。

### 行业正向案例：Chainguard Images / Wolfi

Chainguard 基于 Wolfi 发行版构建的容器镜像追求可复现构建与最小依赖面。其构建流水线使用 Melange、APK 包锁定和确定性构建脚本，使同一源码输入能在不同时间、不同机器上产生位对位相同的包。结合 Sigstore 签名后，消费者可验证镜像来源与完整性，代表了 SLSA Build L4 的工业实践方向。

---

## 6. 反例 / 反模式

| 反模式 | 风险 | 本 PoC 中的检测方式 |
|--------|------|---------------------|
| **无来源证明** | 无法追溯构建来源，遭受供应链攻击后无法定位 | `verify-provenance.py` 检查 `provenance.json` 存在且字段完整 |
| **单人审查/无审查** | 内部人员可单点注入恶意代码 | `verify-provenance.py` 要求至少两名审批者 |
| **非密封构建** | 构建时拉取未声明依赖，导致输出不可预测 | `build.py` 不访问网络，输入文件显式声明 |
| **不可复现构建** | 同一源码在不同环境产出不同产物，难以审计 | `verify-provenance.py` 比较 `output_hash` 与当前产物哈希 |
| **静态 provenance** | 手动维护的 provenance 易被篡改 | `build.py` 在构建时动态计算并写入哈希 |

### 反例 A：SolarWinds SUNBURST（构建环境入侵）

SolarWinds Orion 的构建环境被入侵后，攻击者在官方构建代理中将 SUNBURST 后门注入 Orion 核心 DLL。由于构建产物仍使用 SolarWinds 合法证书签名，约 18,000 家客户无法通过传统签名发现异常。该事件说明：

1. **构建环境是核心攻击面**：源码未被篡改，但构建代理被污染。
2. **签名不能替代 provenance**：合法签名只证明发布者身份，不证明构建过程可信。
3. **可复现构建的价值**：若构建可复现，第三方审计者可独立重建产物并对比哈希，发现差异。

---

## 7. 控制点映射：SLSA Build Track L4 → PoC 实现

| SLSA 要求 | PoC 文件/逻辑 | 关键字段/校验 |
|----------|--------------|--------------|
| 双人审查（Two-person review） | `REVIEWERS` + `verify-provenance.py` | 审批者数量 ≥ 2，且与 `SLSA_REVIEWERS`  env 可覆盖 |
| 密封构建（Hermetic build） | `build.py` | 显式读取 `src/main.py`；不访问网络；构建脚本哈希写入 provenance |
| 可复现构建（Reproducible build） | `build.py` + `verify-provenance.py` | 同 commit、同脚本下多次构建输出 `output_hash` 一致 |
| 非伪造 provenance | `provenance.json` | 包含 `git_commit`、`builder_id`、`build_script_hash`、`source_hash`、`output_hash` |
| 源码来自版本控制 | `build.py` 调用 `git rev-parse HEAD` | `git_commit` 字段绑定源码版本 |

> **说明**：本 PoC 为教学用途，使用本地文件和 env 变量模拟 CI 控制。生产环境应替换为 GitHub branch protection、GitHub Artifact Attestations 或 Sigstore/cosign 签名，以满足真正的 L4 非伪造性。

---

## 8. 在 CI 中使用

仓库 `.github/workflows/slsa-l4-poc.yml` 提供了一个 GitHub Actions 示例：

- 检出代码（保留完整 Git 历史，以便获取 commit）。
- 运行 `build.py` 生成产物与 provenance。
- 运行 `verify-provenance.py` 校验。
- 上传产物与 provenance 为构建产物（artifact）。

在真实生产场景中，应进一步使用 [SLSA GitHub Generator](https://github.com/slsa-framework/slsa-github-generator) 或 Sigstore/cosign 对 provenance 进行签名。

---

## 9. 扩展建议

1. **签名 provenance**：使用 `cosign sign-blob` 或 Sigstore Python SDK 对 `provenance.json` 签名。
2. **真实双人审查**：通过 GitHub "Require approvals" 分支保护规则实现，而非本地文件。
3. **可复现构建矩阵**：在多个 runner / 容器环境中运行 `build.py`，比较输出哈希是否一致。
4. **SBOM 联动**：在构建后调用 `syft` 或 `cyclonedx-py` 生成 SBOM，并与 provenance 一起发布。

---

## 10. 权威来源

| 来源 | URL | 说明 | 核查日期 |
|------|-----|------|----------|
| SLSA Specification v1.2 | <https://slsa.dev/spec/v1.2/> | Multi-Track 架构与 Build Track L1-L3 | 2026-07-08 |
| SLSA Build Track | <https://slsa.dev/spec/v1.2/levels#build-track> | L4 草案要求（双人审查、可复现、密封） | 2026-07-08 |
| Sigstore / cosign | <https://docs.sigstore.dev/cosign/overview/> | 无密钥签名 | 2026-07-08 |
| SLSA GitHub Generator | <https://github.com/slsa-framework/slsa-github-generator> | 自动生成 SLSA provenance | 2026-07-08 |
| slsa-verifier | <https://github.com/slsa-framework/slsa-verifier> | Provenance 验证 CLI | 2026-07-08 |
| GitHub Branch Protection | <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches> | 双人审查与状态检查配置 | 2026-07-08 |
| Chainguard / Wolfi | <https://www.chainguard.dev/solutions/reproducible-builds> | 可复现构建工业实践 | 2026-07-08 |
| CISA AA20-352A | <https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-352a> | SolarWinds 供应链攻击技术分析 | 2026-07-08 |

---

## 11. 交叉引用

- 供应链安全主题入口：[`struct/10-supply-chain-security/README.md`](../README.md)
- SLSA 框架与复用边界：[`struct/10-supply-chain-security/01-slsa-framework/slsa-reuse-boundaries.md`](../01-slsa-framework/slsa-reuse-boundaries.md)
- SBOM 标准与复用安全：[`struct/10-supply-chain-security/02-sbom-standards/sbom-reuse-security.md`](../02-sbom-standards/sbom-reuse-security.md)
- 供应链攻击向量：[`struct/10-supply-chain-security/03-attack-vectors/README.md`](../03-attack-vectors/README.md)
- 来源证明示例：[`struct/10-supply-chain-security/04-provenance-examples/README.md`](../04-provenance-examples/README.md)
- 零信任供应链原则：[`struct/10-supply-chain-security/05-zero-trust-supply-chain/zero-trust-principles.md`](../05-zero-trust-supply-chain/zero-trust-principles.md)
- 形式化验证环境：[`struct/99-reference/tools/formal-verification-env/`](../../99-reference/tools/formal-verification-env/)

---

## 12. 分析

SLSA Build L4 的核心价值不在于单一技术，而在于通过**过程控制 + 密码学证明**将构建可信度从“相信构建者”提升为“验证构建证据”。本 PoC 以最小代码量展示了四个控制点的可运行形态：双人审查降低人为篡改风险、密封构建消除未声明依赖、可复现构建保证审计一致性、来源证明提供跨团队验证基础。在真实落地时，应将其嵌入 CI/CD 流水线，并结合 Sigstore/cosign 实现 provenance 的不可伪造签名。
