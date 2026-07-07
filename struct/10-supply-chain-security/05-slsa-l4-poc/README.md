# SLSA Build Level 4 概念验证（PoC）

> 位置：`struct/10-supply-chain-security/05-slsa-l4-poc/`

## 1. PoC 目标

本 PoC 用最小可运行代码演示 **SLSA Build Level 4** 的核心控制点：

- **Two-Person Review（双人审查）**：关键源码变更需至少两名审批者，模拟通过 `REVIEWERS` 文件或环境变量校验。
- **Hermetic Builds（密封构建）**：构建脚本声明并固定输入，禁止外部网络/未声明依赖。
- **Reproducible Builds（可复现构建）**：相同输入（源码、构建脚本、环境）应产生相同的输出哈希。
- **可验证的来源证明（Provenance）**：`provenance.json` 记录构建者身份、源码 Git commit、构建脚本哈希、输出哈希等关键字段。

> 注：本 PoC 为教学和本地验证用途，未集成真实的 Sigstore/cosign 签名或 GitHub OIDC，但已通过脚本字段和校验逻辑体现 L4 关键要素。

## 2. SLSA Build L4 要求映射

| SLSA L4 要求 | PoC 中的体现 |
|--------------|--------------|
| **Two-person review** | `verify-provenance.py` 检查 `REVIEWERS` 记录或 `SLSA_REVIEWERS` 环境变量中至少包含两名审批者。 |
| **Hermetic build** | `build.py` 显式声明输入文件（`src/main.py`），不访问外部网络，构建脚本自身哈希也被记录。 |
| **Reproducible build** | 多次运行 `build.py`（同 commit、同脚本）产生的 `dist/app` 字节相同，`verify-provenance.py` 校验 SHA-256。 |
| **Provenance 可验证** | `provenance.json` 包含 `git_commit`、`builder_id`、`build_script_hash`、`source_hash`、`output_hash`。 |

## 3. 文件结构

```text
05-slsa-l4-poc/
├── README.md                 # 本说明
├── build.py                  # 模拟构建脚本，生成 dist/app 与 provenance.json
├── verify-provenance.py      # 验证 provenance 与当前环境一致性
├── REVIEWERS                 # 双人审查记录（示例）
├── src/
│   └── main.py               # 待构建的示例源码
└── dist/
    └── app                   # 构建产物（由 build.py 生成）
```

## 4. 运行步骤

### 4.1 进入目录

```bash
cd struct/10-supply-chain-security/05-slsa-l4-poc/
```

### 4.2 执行构建

```bash
python build.py
```

输出示例：

```text
[build] Source hash:  1a2b3c...
[build] Script hash:  4d5e6f...
[build] Output hash:  7a8b9c...
[build] Provenance written to dist/provenance.json
[build] Build complete: dist/app
```

### 4.3 验证来源证明

```bash
python verify-provenance.py
```

成功时：

```text
[verify] ✔ git commit matches HEAD: <hash>
[verify] ✔ build script hash matches
[verify] ✔ output hash matches provenance
[verify] ✔ two-person review confirmed (reviewers: alice, bob)
[verify] PASS: SLSA L4 checks succeeded
```

失败时（例如源码或构建脚本被篡改）：脚本会明确指出哪一项校验失败。

## 5. 在 CI 中使用

仓库 `.github/workflows/slsa-l4-poc.yml` 提供了一个 GitHub Actions 示例：

- 检出代码（保留完整 Git 历史，以便获取 commit）。
- 运行 `build.py` 生成产物与 provenance。
- 运行 `verify-provenance.py` 校验。
- 上传产物与 provenance 为构建产物（artifact）。

在真实生产场景中，应进一步使用 [SLSA GitHub Generator](https://github.com/slsa-framework/slsa-github-generator) 或 Sigstore/cosign 对 provenance 进行签名。

## 6. 扩展建议

1. **签名 provenance**：使用 `cosign sign-blob` 或 Sigstore Python SDK 对 `provenance.json` 签名。
2. **真实双人审查**：通过 GitHub "Require approvals" 分支保护规则实现，而非本地文件。
3. **可复现构建矩阵**：在多个 runner / 容器环境中运行 `build.py`，比较输出哈希是否一致。
4. **SBOM 联动**：在构建后调用 `syft` 或 `cyclonedx-py` 生成 SBOM，并与 provenance 一起发布。
