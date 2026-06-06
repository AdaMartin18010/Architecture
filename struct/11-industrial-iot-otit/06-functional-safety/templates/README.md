# 功能安全 GSN 模块化安全案例模板

> **定位**：为安全关键可复用组件（SEooC / COTS / Proven-in-use）提供标准化的安全论证结构。
> **对齐**：ISO 26262:2018、IEC 61508 Ed.3、Hawkins GSN Pattern Catalogue、Ye & Kelly 契约式模块化保证。

---

## 1. 模板结构

```
gsn-modular-safety-case-template.yaml
├── metadata              # 模板版本与对齐标准
├── component             # 组件身份（SEooC / COTS / Proven-in-use）
├── assumptions           # Assumptions of Use (AoU) + Environment (AoE)
├── guarantees            # 组件提供的安全属性
├── top_level_goal        # GSN 顶层目标与论证策略
├── evidence              # 证据清单（测试报告、分析报告）
├── away_goals            # 引用外部组件的安全案例
├── change_management     # 变更日志与复用影响矩阵
├── tool_qualification    # 工具资质（TCL / TIL）
└── reuse_framework_mapping  # 与项目复用体系的映射
```

---

## 2. 核心概念

### 2.1 SEooC (Safety Element out of Context)

按 ISO 26262 开发、**无完整 item 级系统定义**的组件。供应商创建合理假设，集成商验证假设。

### 2.2 Assumption / Guarantee 契约

| 方向 | 内容 | 责任人 |
|------|------|--------|
| **Assumption** | 组件对集成环境的期望 | 集成商验证 |
| **Guarantee** | 组件承诺的安全属性 | 组件供应商证明 |

### 2.3 Away Goals

GSN 的 **Away Goals** 允许子系统安全案例引用组件级论证而不嵌入。实现真正的**模块化安全案例**。

---

## 3. 使用流程

### 3.1 供应商侧（组件开发者）

1. 复制 `gsn-modular-safety-case-template.yaml` 为 `<component>-safety-case.yaml`
2. 填充 `assumptions`：明确声明集成商必须满足的条件
3. 填充 `guarantees`：声明组件提供的安全属性
4. 收集 `evidence`：测试报告、FMEDA、覆盖率报告
5. 管理 `change_management`：任何变更触发影响分析

### 3.2 集成商侧（系统开发者）

1. 获取组件的 safety-case.yaml
2. 对每条 `assumption` 创建系统级验证需求
3. 在 item-level 安全案例中添加目标：SEooC 假设被目标架构满足
4. 追踪 `away_goals` 到外部组件的安全案例

---

## 4. 复用影响矩阵

| 变更类型 | 触发重新验证 |
|----------|-------------|
| 软件逻辑变更 | G-001, G-002, G-003, EV-FI-001, EV-COV-001 |
| 硬件抽象层变更 | G-001, AOE-001 |
| 假设放松 | 所有 Assumptions |
| 仅文档更新 | 无 |

---

## 5. 与项目工具链的集成

| 项目工具 | 安全案例集成 |
|----------|-------------|
| `verify-all.sh` | 形式化验证证据可补充动态测试证据 |
| `slsa-provenance-github-action.yml` | SLSA provenance 作为供应链安全证据 |
| `assessment-tool.py` | 安全成熟度可作为复用成熟度的一个维度 |

---

*文档生成时间：2026-06-06 · 对齐 ISO 26262:2018 / IEC 61508 Ed.3 / GSN*
