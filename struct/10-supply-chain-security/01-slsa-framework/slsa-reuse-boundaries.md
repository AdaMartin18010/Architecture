# SLSA 1.0 四级框架的复用安全边界详解

> **版本**: 2026-06-06
> **权威来源**: SLSA Specification v1.0 (slsa.dev), OpenSSF Best Practices, Sigstore/cosign 2026 Stack
> **定位**: Track D 供应链安全工程深化内容，为 Phase 4（2027-Q2）预热
> **交叉引用**: `struct/04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md`

---

## 1. 引言：为什么复用需要 SLSA 边界

软件架构复用的核心悖论在于：**复用度越高，供应链攻击面越大**。
当一个系统 80–90% 的代码来自外部依赖（参见 Sonatype 2026 报告），任何上游组件的构建过程被篡改，都将直接传导至下游所有消费者。
SLSA（Supply-chain Levels for Software Artifacts）框架通过分级构建证明（Build Provenance）为这一悖论提供了形式化的安全边界。

> **定理 S.RB.1** (SLSA Reuse Boundary Monotonicity): 若组件 C 被复用于系统 S，则 S 在供应链安全维度的有效 SLSA 等级不超过 C 的 SLSA 等级。即 `SLSA(S) ≤ min{SLSA(Cᵢ)}`。

本文件将 SLSA v1.0 Build Track 的四个等级（L0–L4，含 L4 规划）映射到架构复用决策中，明确"达到 Lx 的资产可在什么场景复用"，并提供可执行的升级路径。

---

## 2. SLSA 等级总览与复用安全边界

SLSA v1.0 采用**多轨道（Multi-Track）模型**，当前发布的 Build Track 定义了 L1–L3 三个正式等级，L4 处于社区规划阶段（Build Level 4 Workstream，由 David A. Wheeler 主导）。
为完整覆盖复用安全边界，本文沿用 v0.1 中 L4 的成熟实践（可复现构建、双人审查）并结合 v1.2 草案进行前瞻性分析。

| 等级 | 核心目标 | 复用安全边界含义 | 2026 工具链支持 |
|------|---------|-----------------|----------------|
| **L0** | 无保证 | 不可信资产，禁止复用于生产环境 | — |
| **L1** | 知道软件从何而来 | 可复用于内部原型、POC 阶段 | GitHub Actions, GitLab CI |
| **L2** | 防止构建后被篡改 | 可复用于非关键业务系统、内部工具 | Sigstore/cosign keyless, SLSA GitHub Generator |
| **L3** | 防止构建过程中被篡改 | 可复用于生产系统、金融/医疗等高合规场景 | GitHub Actions (hardened), Google Cloud Build, GitLab native attestation |
| **L4** | 最大化构建可信度 | 可复用于关键基础设施、国防、航空航天 | Nix, Bazel (hermetic), Source Track L3 |

> **引用**: SLSA.dev Spec v1.0 — "Build L3 provides robust protection against tampering and unauthorized access, ensuring a high level of trust and integrity in the software development process." [^1]

---

## 3. 各级别详细解析

### 3.1 Build L1: Provenance Generation — "可追溯复用"

#### 要求清单

| 要求编号 | 要求描述 | 验证方法 |
|---------|---------|---------|
| BL1-R1 | 构建过程完全脚本化/自动化 | 存在 `Makefile` / `build.sh` / CI 配置文件 |
| BL1-R2 | 生成并发布 Provenance（来源证明） | Provenance 文件随制品分发 |
| BL1-R3 | Provenance 包含构建定义和依赖信息 | 符合 SLSA Provenance v1 格式 |

#### 复用决策矩阵

| 复用场景 | 允许性 | 条件与限制 |
|---------|-------|-----------|
| 内部原型 / POC | ✅ 允许 | 需在 SBOM 中标记为 L1，明确无篡改保护 |
| 开发/测试环境 | ⚠️ 有条件 | 需配合依赖扫描（`npm audit`, `cargo audit`）使用 |
| 非关键生产系统 | ❌ 不建议 | 无签名保护，无法检测构建后篡改 |
| 关键生产系统 | ❌ 禁止 | 不满足最小篡改检测要求 |
| 开源组件再分发 | ⚠️ 有条件 | 需明确告知下游消费者无构建保证 |

#### 升级路径

```text
L0 → L1
├── 步骤 1: 将手动构建迁移至 CI/CD（GitHub Actions / GitLab CI / Jenkins）
├── 步骤 2: 使用 SLSA GitHub Generator 或自研脚本生成 Provenance
├── 步骤 3: 将 Provenance 作为 Release Artifact 附加
└── 验证: 检查 Provenance 中 buildType、externalParameters、resolvedDependencies 完整性
```

> **交叉引用**: `struct/04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md` §5.2 指出，L1 级别的 Provenance 是 SBOM 全生命周期的起点，但缺乏密码学保证的 Provenance 无法防御 Lockfile 注入攻击。

---

### 3.2 Build L2: Hosted Build + Authenticated Provenance — "防篡改复用"

#### 要求清单

| 要求编号 | 要求描述 | 验证方法 |
|---------|---------|---------|
| BL2-R1 | 使用版本控制系统（Git/SVN） | 源码来源可追溯至特定 commit |
| BL2-R2 | 使用托管构建服务 | 构建在 GitHub Actions / Cloud Build / GitLab CI 等托管平台执行 |
| BL2-R3 | Provenance 经过签名和认证 | 使用 Sigstore/cosign keyless signing 或 GPG/X.509 签名 |
| BL2-R4 | Provenance 由构建服务生成 | 非人工手动创建，防止伪造 |

#### 复用决策矩阵

| 复用场景 | 允许性 | 条件与限制 |
|---------|-------|-----------|
| 内部工具/后台管理 | ✅ 允许 | 适合非面向客户的业务支持系统 |
| SaaS 服务（非核心模块） | ✅ 允许 | 需配合运行时监控（Falco/Tetragon） |
| 金融服务（非交易核心） | ⚠️ 有条件 | 需叠加 SAST/SCA 扫描，并满足 Source Track L1 |
| 医疗系统（HIPAA 范围） | ❌ 不建议 | 需达到 L3 才能满足 HIPAA 安全规则 |
| 关键基础设施 | ❌ 禁止 | 不满足构建过程隔离要求 |

#### 升级路径

```text
L1 → L2
├── 步骤 1: 将构建迁移至托管 CI/CD（避免本地/自托管 runner）
├── 步骤 2: 集成 Sigstore/cosign keyless signing（推荐）
│   └── cosign sign --yes --oidc-issuer=https://token.actions.githubusercontent.com <image>
├── 步骤 3: 使用 SLSA GitHub Generator v2.0+ 自动生成签名 Provenance
├── 步骤 4: 在 registry 中存储签名和 Provenance（OCI 1.1 参考类型）
└── 验证: cosign verify --certificate-identity=ci@org.com --certificate-oidc-issuer=<issuer> <image>
```

> **2026 Sigstore/cosign 新特性**:
> Cosign v2.4.1 支持 Rekor v1.2 透明日志，提供非否认性证明。
> keyless signing 通过 OIDC 将短期签名密钥绑定至 CI 身份，彻底消除长期密钥管理风险 [^2]。

---

### 3.3 Build L3: Hardened Build Platform — "可信复用"

#### 要求清单

| 要求编号 | 要求描述 | 验证方法 |
|---------|---------|---------|
| BL3-R1 | 构建定义来源于版本控制中的源码 | `buildType` 指向仓库内文件，非外部配置 |
| BL3-R2 | 构建环境是临时的（Ephemeral） | 每次构建使用全新 VM/容器，构建后销毁 |
| BL3-R3 | 构建环境是隔离的（Isolated） | 构建间无共享状态、无网络访问（除必要依赖下载） |
| BL3-R4 | 构建平台满足安全基线 | 平台通过审计（如 ISO 27001, SOC 2）或公开透明 |
| BL3-R5 | Provenance 非伪造性 | 仅构建平台可访问签名密钥，构建者无法伪造 |

#### 复用决策矩阵

| 复用场景 | 允许性 | 条件与限制 |
|---------|-------|-----------|
| 企业级 SaaS 核心服务 | ✅ 允许 | 2026 年企业基线标准 |
| 金融服务（含交易核心） | ✅ 允许 | 满足 PCI-DSS、SOX 合规要求 |
| 医疗系统（HIPAA/CRA） | ✅ 允许 | 满足 EU CRA 网络安全要求 |
| 汽车软件（ISO 26262） | ⚠️ 有条件 | 需叠加 Source Track L2（认证提交历史） |
| 航空航天/国防（DO-178C） | ⚠️ 有条件 | 建议向 L4 演进，需形式化验证配合 |
| 开源组件再分发 | ✅ 允许 | npm provenance（SLSA L3）已成为社区信任标志 |

#### 升级路径

```text
L2 → L3
├── 步骤 1: 启用隔离构建环境
│   ├── GitHub Actions: 使用 hosted runners（非 self-hosted）
│   ├── Google Cloud Build: 使用默认 worker pool
│   └── 私有环境: 确保 VM 每次构建后重建（Ephemeral）
├── 步骤 2: 限制构建网络访问
│   ├── 禁用构建步骤中的任意网络调用（`curl`, `wget`）
│   ├── 依赖预下载至内部代理仓库（ Nexus / Artifactory ）
│   └── 使用 `--network=none` 或等价容器策略
├── 步骤 3: 分离构建者与签名者权限
│   └── 使用 OIDC 联邦身份，让 CI 平台（非用户）获取签名凭证
├── 步骤 4: 实施构建平台安全基线
│   ├── 定期轮换构建镜像
│   ├── 扫描构建环境中的 CVE
│   └── 记录构建平台审计日志
└── 验证: 使用 slsa-verifier 检查 Provenance 的 builder.id 和 buildLevel
```

> **交叉引用**: `struct/04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md` §4.4 指出，
> Rust（Cargo）和 Node.js（npm）生态在 2026 年已原生支持 SLSA L3 provenance（npm provenance via Sigstore，crates.io Trusted Publishing），
> 而 JVM 生态仍需手动配置。

---

### 3.4 Build L4: Reproducible + Hermetic + Two-Person Review — "最高可信复用"

#### 要求清单（基于 v0.1 + v1.2 规划）

| 要求编号 | 要求描述 | 验证方法 |
|---------|---------|---------|
| BL4-R1 | 所有源码变更经过双人审查 | 分支保护规则强制 ≥2 approvers |
| BL4-R2 | 构建是无参数的（Parameterless） | 构建输出仅由源码版本决定，无环境变量/外部输入影响 |
| BL4-R3 | 构建是密闭的（Hermetic） | 所有依赖（含工具链）均来自锁定的、可验证的来源 |
| BL4-R4 | 构建是可复现的（Reproducible） | 不同时间、不同机器构建产生比特级相同的输出 |
| BL4-R5 | Source Track L3 | 源码永久保留，提交历史认证，双人审查 |

#### 复用决策矩阵

| 复用场景 | 允许性 | 条件与限制 |
|---------|-------|-----------|
| 关键基础设施（能源/水利/通信） | ✅ 允许 | 符合 NIST CIP、EU NIS2 指令 |
| 国防/军事系统 | ✅ 允许 | 符合 CMMC Level 3+ |
| 航空航天（DO-178C A级） | ✅ 允许 | 需配合形式化验证（参见 `struct/07-formal-verification/`） |
| 金融核心清算系统 | ✅ 允许 | 满足最高级别监管审计要求 |
| 一般企业应用 | ⚠️ 过度 | 成本收益比不优，L3 通常足够 |
| 快速迭代的互联网产品 | ❌ 不建议 | 双人审查和可复现构建显著增加交付周期 |

#### 升级路径

```text
L3 → L4
├── 步骤 1: 实施 Source Track L3
│   ├── 强制分支保护（main 分支禁止直接推送）
│   ├── 强制 Code Review（≥2 审批者，含安全专家）
│   └── 启用提交签名（GPG/SSH commit signing）
├── 步骤 2: 实现密闭构建（Hermetic Build）
│   ├── 使用 Nix / Bazel 锁定整个工具链（编译器、链接器、构建脚本）
│   ├── 内部缓存所有依赖（禁止运行时下载）
│   └── 固定操作系统和基础镜像版本
├── 步骤 3: 实现可复现构建（Reproducible Build）
│   ├── 消除构建中的非确定性来源（时间戳、随机数、路径依赖）
│   ├── 使用 `SOURCE_DATE_EPOCH` 规范化时间戳
│   ├── 验证: 在不同机器上构建两次，比较 SHA-256 哈希
│   └── 工具: reprotest, diffoscope
├── 步骤 4: 消除构建参数依赖
│   └── 所有构建输入编码在源码或锁定文件中，无环境变量影响输出
└── 验证: 定期执行可复现性验证作为 CI 门控
```

> **引用**: "Solutions like Nix have been pioneers in implementing reproducible builds for over 20 years, ensuring that software builds remain consistent and secure." [^3]

---

## 4. SLSA 等级与依赖治理的交叉引用

`struct/04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md` 提出了分层防御策略。
本文件将其与 SLSA 等级映射如下：

| 防御层 | 依赖治理措施 | 对应 SLSA 等级 | 理由 |
|-------|-------------|---------------|------|
| Layer 1: Proxy Registry | 缓存公共 registry，自动漏洞扫描 | L1–L2 | 保证来源可追溯，但无构建保证 |
| Layer 2: 审批工作流 | 新包/新版本需安全团队审批，7天冷却期 | L2–L3 | 结合签名证明和托管构建信任 |
| Layer 3: Lockfile + 哈希 | 精确版本锁定，密码学哈希验证 | L3 | 需要硬化构建平台保证 lockfile 未被篡改 |
| Layer 4: Vendoring | 关键系统完全离线构建，源码级补丁 | L4 | 密闭构建与可复现性的终极形态 |

> **定理 S.RB.2** (Dependency-SLSA Composition): 若系统 S 依赖组件集合 {C₁, C₂, ..., Cₙ}，且各组件 SLSA 等级为 {L₁, L₂, ..., Lₙ}，则 S 的有效 SLSA 等级为 `min(L₁, L₂, ..., Lₙ)`，与 S 自身的构建等级无关。

这意味着：**即使你的构建达到 L4，但只要有一个依赖是 L1，整个系统的复用安全边界就降级为 L1**。
这正是 `struct/04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md` §6.3 强调"分层组合策略"的根本原因。

---

## 5. 2026–2027 实施路线图

| 阶段 | 时间 | 目标等级 | 关键行动 |
|------|------|---------|---------|
| **Phase 1** | 2026 Q3 | L1 全覆盖 | 所有组件生成 Provenance；CI/CD 全自动化 |
| **Phase 2** | 2026 Q4 | L2 核心系统 | 核心组件启用托管构建 + cosign keyless 签名 |
| **Phase 3** | 2027 Q1 | L3 生产基线 | 生产组件全部达到 Build L3；推动关键供应商提供 L3 证明 |
| **Phase 4** | 2027 Q2 | L4 关键系统 | 金融/国防/关键基础设施组件达到 L4 |

---

## 6. 参考索引

[^1]: SLSA.dev, "SLSA Specification v1.0 — Security Levels", <https://slsa.dev/spec/v1.0/levels>
[^2]: Sigstore Project, "Cosign v2.4.1 Release Notes — Rekor v1.2 Support", 2026; HAMS Tech, "Kubernetes Supply Chain Security in 2026", 2026-02
[^3]: Kubesimplify, "Supply Chain Security Using SLSA — Part 2", 2024-06-13

---

> 最后更新: 2026-06-06
> 关联文件: `slsa-1-1-1-2-update.md`, `struct/04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md`


---

## 补充说明：SLSA 1.0 四级框架的复用安全边界详解

## 概念定义

**定义**：SLSA（Supply-chain Levels for Software Artifacts）是 OpenSSF 提出的框架，通过 Source、Build、Provenance、Common 等 Track 定义软件制品的可验证安全等级。

## 示例

**示例**：使用 Sigstore/cosign 对容器镜像进行签名，配合 GitHub Actions 隔离构建与可复现构建证明，达到 SLSA Build L3。

## 反例

**反例**：项目手动从个人仓库下载二进制依赖且无哈希校验，构建环境未隔离，无法达到 SLSA L1。
