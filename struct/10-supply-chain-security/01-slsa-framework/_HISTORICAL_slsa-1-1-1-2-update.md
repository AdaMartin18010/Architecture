# SLSA 1.1 / 1.2 更新与多轨道模型

> **版本**: 2026-06-06
> **权威来源**: SLSA Specification v1.1 / v1.2 (slsa.dev)
> **定位**: 对齐 SLSA 最新版本，从单一等级演进为多轨道模型

---

## 1. SLSA 版本演进

| 版本 | 发布时间 | 核心特征 |
|------|---------|---------|
| SLSA v0.1 | 2022 | 单一等级 L1-L4，覆盖源码和构建 |
| SLSA v1.0 | 2023-04 | 引入 **Build Track**，Source 要求分离 |
| SLSA v1.1 | 2024 | 完善 Build Track，增强验证指南 |
| SLSA v1.2 | 2025+ | 引入 **Source Track**、**Attested Build Environments Track** |

> **关键变化**: SLSA 从单一等级体系演进为**多轨道（Multi-Track）模型**。每个轨道专注于供应链的一个特定环节。

---

## 2. SLSA 1.2 轨道体系

```text
SLSA v1.2 Tracks
├── Build Track（构建轨道）
│   ├── L1: 生成 Provenance
│   ├── L2: 使用版本控制和托管构建服务
│   ├── L3: 强化构建平台，来源可审计
│   └── L4: planned（双人审查、可复现构建）
│
├── Source Track（源码轨道）- NEW in v1.2
│   ├── L1: 版本控制
│   ├── L2: 认证历史
│   └── L3: 双人审查、retained indefinitely
│
├── Attested Build Environments Track（认证构建环境轨道）- NEW in v1.2
│   └── 关注构建环境本身的可信性
│
└── Cross-Track（跨轨道）
    ├── Threats & Mitigations
    ├── Verified Properties
    └── Attestation Formats
```

---

## 3. Build Track 详细要求

### Build L1: Provenance Generation

**目标**: 知道软件从何而来。

**要求**:

- 构建过程完全脚本化/自动化
- 生成并发布 Provenance（来源证明）

**对应威胁**: 上传被篡改的包（Threat F）

### Build L2: Hosted Build + Authenticated Provenance

**目标**: 防止构建后被篡改。

**要求**:

- 使用版本控制
- 使用托管构建服务
- Provenance 经过签名和认证

### Build L3: Hardened Build Platform

**目标**: 防止构建过程中被篡改。

**要求**:

- 构建定义来源于源代码
- 构建环境是临时的（Ephemeral）
- 构建环境是隔离的（Isolated）
- 强化构建平台的安全基线

### Build L4: Reproducible Build + Two-Person Review

**目标**: 最大化构建可信度。

**要求**（planned）:

- 所有变更经过双人审查
- 构建是无参数的（Parameterless）
- 构建是密闭的（Hermetic）
- 构建是可复现的（Reproducible）

---

## 4. Source Track 详细要求（v1.2 新增）

### Source L1: Version Controlled

- 源代码存储在版本控制系统中
- 变更可被追踪

### Source L2: Authenticated History

- 提交历史经过认证
- 无法伪造提交者身份

### Source L3: Retained Indefinitely + Two-Person Reviewed

- 源代码永久保留
- 所有变更经过双人审查
- 分支保护规则强制执行

---

## 5. Attested Build Environments Track（v1.2 新增）

该轨道关注**构建环境本身**的可信性：

- 构建环境是否经过认证？
- 构建环境的配置是否可验证？
- 构建环境的生命周期是否受控？

**应用场景**:

- 云构建平台（GitHub Actions, Google Cloud Build）
- 私有构建农场
- 边缘/本地构建环境

---

## 6. Attestation 格式

SLSA 推荐使用以下证明格式：

| 格式 | 用途 | 状态 |
|------|------|------|
| **Build Provenance** | 记录构建过程 | 推荐 |
| **Source Provenance** | 记录源码来源 | v1.2 新增 |
| **Verification Summary Attestation (VSA)** | 汇总验证结果 | 推荐 |
| **General Attestation Model** | 通用证明模型 | 基础 |

### Build Provenance 核心字段

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{"name": "...", "digest": {"sha256": "..."}}],
  "predicateType": "https://slsa.dev/provenance/v1",
  "predicate": {
    "buildDefinition": {
      "buildType": "...",
      "externalParameters": {},
      "internalParameters": {},
      "resolvedDependencies": []
    },
    "runDetails": {
      "builder": {"id": "..."},
      "metadata": {"invocationId": "...", "startedOn": "...", "finishedOn": "..."}
    }
  }
}
```

---

## 7. SLSA 与 NIST SSDF 的映射

| SLSA 要求 | NIST SSDF 实践 | 说明 |
|-----------|---------------|------|
| Build L1 Provenance | PO.1 Secure Software | 保护软件 |
| Build L2 Source-aware | PW.4 Reusable Code | 安全复用代码 |
| Build L3 Hardened | PW.6 Configure Compiler | 配置编译器 |
| Build L4 Reproducible | PW.8 Test Executable | 测试可执行文件 |
| Source L1 Version Control | PO.3.1 Store Code | 存储代码 |
| Source L3 Two-Person Review | PO.3.2 Review Code | 审查代码 |

---

## 8. 对架构复用的影响

> **定理 S.T1 (更新版)** (SLSA Track Monotonicity): 若组件 A 依赖组件 B，则 A 在某一轨道上的 SLSA 等级小于等于 B 在该轨道上的等级。若 B 的等级不足，提升 A 的等级是徒劳的。

> **定理 S.T3** (Multi-Track Coverage): 单一轨道的高等级不能替代其他轨道的低等级。完整的供应链安全需要所有相关轨道都达到足够等级。

**复用策略调整**:

1. **评估依赖的 SLSA 等级时，必须按轨道分别评估**（Build/Source/Environment）
2. **SBOM 应包含每个依赖的 SLSA 声明**
3. **复用资产的准入标准应明确要求最低 SLSA 轨道等级**

---

## 9. 2026 实施建议

| 优先级 | 行动 | 预期效果 |
|--------|------|---------|
| P0 | 为所有关键组件生成 Build Provenance | 达到 Build L1 |
| P1 | 使用托管 CI/CD 并签名 Provenance | 达到 Build L2 |
| P2 | 强化构建平台（隔离、临时环境） | 达到 Build L3 |
| P3 | 实施 Source Track 控制（分支保护、双人审查） | Source L2-L3 |
| P4 | 推动关键依赖供应商提供 SLSA 证明 | 降低上游风险 |

---

> 最后更新: 2026-06-06
> 权威来源: <https://slsa.dev/spec/v1.2/>


---

## 补充章节

## 概念定义

**定义**：SLSA（Supply-chain Levels for Software Artifacts）是 OpenSSF 提出的框架，通过 Source、Build、Provenance、Common 等 Track 定义软件制品的可验证安全等级。

## 示例

**示例**：使用 Sigstore/cosign 对容器镜像进行签名，配合 GitHub Actions 隔离构建与可复现构建证明，达到 SLSA Build L3。

## 反例

**反例**：项目手动从个人仓库下载二进制依赖且无哈希校验，构建环境未隔离，无法达到 SLSA L1。
