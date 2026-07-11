# 软件复用成熟度模型：RCMM、RiSE-RM 与行业映射
>
> 版本: 2026-06-06
> 对齐来源: CMMI (ISACA), RCMM (Jasmine & Vasantla), RiSE-RM (Garcia 2010), Automotive SPICE, Koltun & Hudson (1991)

## 1. 复用成熟度模型谱系

| 模型 | 层级数 | 焦点 | 来源 |
|-----|--------|------|------|
| **CMM / CMMI-DEV** | 5 | 通用软件开发过程 | SEI / ISACA |
| **RCMM** | 5 | 复用导向软件开发 | Jasmine & Vasantla |
| **RiSE-RM** | 7 | 系统化复用采用 | RiSE Labs / Garcia (2010) |
| **Koltun & Hudson** | 5 | 组织 mindset 层面复用 | 1991 |
| **Automotive SPICE** | 6 | 汽车行业过程评估 | VDA QMC |
| **Koltun-Hudson 软件复用** | 5 | 代码/组件/应用/系统复用 | 1991 |

## 2. CMMI 与复用

### 2.1 CMMI 核心信息

- **当前管理方**：ISACA（2016 年从 CMU/SEI 接管）
- **定位**：结果导向的性能改进模型，与 Agile、SAFe、DevSecOps 集成
- **量化收益**（ISACA 数据）：
  - 缺陷减少 30%
  - 开发生产率提升 15%
  - 交付时间偏差减少 43%
  - 客户满意度提升 13%
  - 成本偏差减少 47%

### 2.2 CMMI 成熟度等级

| 等级 | 名称 | 复用含义 |
|-----|------|---------|
| 1 | 初始 | 复用偶然发生，依赖个人英雄主义 |
| 2 | 已管理 | 项目级复用跟踪，基本的配置管理 |
| 3 | 已定义 | 组织级复用过程标准化，领域工程启动 |
| 4 | 量化管理 | 复用率、质量、成本度量驱动决策 |
| 5 | 优化 | 持续过程改进，创新复用技术引入 |

## 3. RCMM（Reuse Capability Maturity Model）

### 3.1 五级定义

| 等级 | 名称 | 特征 | 关键实践 |
|-----|------|------|---------|
| **1** | 初始复用 | 个人级、无计划、临时复制粘贴 | 无 |
| **2** | 可重复复用 | 项目内识别可复用组件；基本的版本控制 | 组件目录、编码标准 |
| **3** | 已定义复用 | 组织级复用过程；领域分析；组件库 | 复用计划、领域工程、质量门 |
| **4** | 已管理复用 | 量化复用指标；投资回报跟踪；供应商管理 | 复用度量、成本模型、资产质量管理 |
| **5** | 优化复用 | 持续改进复用过程；创新技术；跨组织复用 | 基准比较、技术雷达、复用文化 |

### 3.2 与 CMMI 的映射

RCMM 直接基于 CMMI 框架，但增加复用特定过程域：

- **复用计划（Reuse Planning）**
- **资产管理（Asset Management）**
- **领域工程（Domain Engineering）**
- **复用度量（Reuse Measurement）**

## 4. RiSE Reference Model（RiSE-RM）

### 4.1 七级定义

由 RiSE Labs（巴西）通过工业实践与专家验证提出：

| 等级 | 名称 | 核心特征 |
|-----|------|---------|
| **1** | Informal Reuse | 非正式复用；复制粘贴；无管理 |
| **2** | Basic Reuse | 基本复用；识别常见功能；简单库 |
| **3** | Planned Reuse | 计划复用；领域分析；可复用组件设计 |
| **4** | Managed Reuse | 管理复用；组件库管理；版本控制；质量评估 |
| **5** | Family-Oriented Products Reuse | 产品线复用；核心资产库；变体管理 |
| **6** | Measured Reuse | 度量复用；量化指标；ROI 跟踪；过程优化 |
| **7** | Proactive Reuse | 主动复用；预测需求；战略资产投资；跨组织生态 |

### 4.2 过程域结构

RiSE-RM 包含以下过程域（Process Areas）：

- 复用战略与规划
- 领域工程
- 应用工程
- 资产管理
- 变型管理
- 组织培训与推广
- 度量与分析
- 过程质量保证

## 5. Koltun & Hudson 复用框架（1991）

### 5.1 组织 Mindset 层面

| 层级 | 名称 | 描述 |
|-----|------|------|
| **0** | No Reusability | 复制粘贴；所有实例手动更新 |
| **1** | Object & Function Reuse | 小规模单一对象或函数复用 |
| **2** | Component Reuse | 子系统到单个对象的组件复用 |
| **3** | Application Reuse | 完整应用复用；应用家族 |
| **4** | System Reuse | 完整系统复用；多应用组合 |

### 5.2 与 RCMM/RiSE 的关系

Koltun-Hudson 框架侧重于**技术复用粒度**，而 RCMM/RiSE 侧重于**组织过程成熟度**。两者互补：

- Koltun-Hudson 回答"复用什么"
- RCMM/RiSE 回答"如何系统化地复用"

## 6. 汽车行业：Automotive SPICE

### 6.1 与复用的关联

- **SUP.1: Quality Assurance** — 复用资产的质量保证
- **SUP.8: Configuration Management** — 复用组件的版本与变体管理
- **SUP.9: Problem Resolution Management** — 复用组件缺陷的跨项目影响分析
- **SYS.3 / SWE.2: Architectural Design** — 软件产品线架构设计
- **REU: Reuse Management** (特定扩展) — 复用工程管理

### 6.2 ASPICE 与 ISO 26262 的交叉

- ASPICE 过程能力等级与 ISO 26262 ASIL 等级共同决定复用证据的充分性
- SEooC 开发需同时满足 ASPICE Level 3+ 和对应 ASIL 的过程要求

## 7. 成熟度评估问卷设计原则

### 7.1 维度设计

| 维度 | 权重 | 评估要点 |
|-----|------|---------|
| **战略与治理** | 15% | 复用战略、预算、治理委员会 |
| **过程与方法** | 20% | 领域工程、应用工程、变体管理 |
| **资产与基础设施** | 20% | 资产库、搜索、质量门、SBOM |
| **度量与激励** | 15% | 复用率、成本节约、开发者激励 |
| **文化与技能** | 15% | 培训、社区、Golden Path 采用率 |
| **工具与自动化** | 15% | CI/CD 集成、SCA、SBOM、平台工程 |

### 7.2 评估方法

- **自评估**：在线问卷，快速定位
- **第三方评估**：类似 CMMI Appraisal，由授权评估师执行
- **持续监控**：平台工程工具自动收集度量数据

## 8. 案例：汽车 OEM 使用 ASPICE + RCMM 评估复用成熟度

**背景**：某汽车 OEM 在开发新一代车载信息娱乐平台时，需要复用多个 ECU 软件组件，但各供应商成熟度参差不齐。

**做法**：

1. 以 **Automotive SPICE** 评估供应商过程能力，要求关键复用组件达到 Level 3（已定义）以上；
2. 以 **RCMM** 评估复用组织能力，识别“资产目录、领域工程、复用度量”三个薄弱环节；
3. 以 **NASA RRL** 对候选可复用资产进行技术就绪度评分，仅推广 RRL 7 以上组件；
4. 建立跨供应商的复用成熟度仪表盘，季度发布改进报告。

**效果**：关键复用组件缺陷率下降 40%，供应商交付一致性提升，通过 ASPICE 审计所需证据减少 30%。

## 9. 反模式：跳过成熟度评估直接推广实验室原型

> **反模式**：将未经验证的实验室原型直接推广为组织级复用资产。

某 AI 创业公司将内部实验的推荐算法组件直接发布为公司级复用资产，未经过成熟度评估、文档完善与压力测试。

**后果**：

- 3 个业务团队在峰值流量期间出现性能崩溃；
- 缺乏接口契约文档，集成方反复返工；
- 因缺少安全审查，模型被 prompt 注入攻击，泄露训练数据样本。

**避免方法**：

- 任何组织级复用资产必须经过至少 RCMM L3 / RiSE-RM L4 的过程评估；
- 高影响组件需通过 NASA RRL 或 ASPICE 技术就绪度验证；
- 建立“实验→孵化→生产”生命周期门槛，未达标不得跨团队推广。

## 10. 论证与分析：为何需要多模型融合的成熟度评估

单一成熟度模型难以覆盖“技术—过程—组织”三个维度。CMMI 提供通用过程能力，RCMM/RiSE 聚焦复用特定实践，ASPICE 给出汽车行业证据要求，NASA RRL 提供技术就绪度标尺。多模型融合可以避免“过程能力高但技术不成熟”或“技术先进但治理缺失”的片面结论。

## 11. 国际标准条款映射

| 标准 | 条款/能力 | 本主题映射 | 实践要点 |
|:---|:---|:---|:---|
| **ISO/IEC/IEEE 42030:2019** | Clause 5–7 Evaluation synthesis, value assessment & findings | 复用成熟度评估、资产价值判定 | 定义评估目标、利益相关者关切与成功准则 |
| **CMMI-DEV / ISACA** | Maturity Level 2–5；Process management | RCMM 五级定义与组织过程改进 | 建立量化度量与持续过程改进 |
| **Automotive SPICE v4.0** | SUP.1 / SUP.8 / SYS.3 / SWE.2 / REU | 汽车行业复用证据与过程能力 | 组件质量保证、配置管理与复用工程 |
| **ISO/IEC 26565:2026** | 产品线成熟度框架 | 五级复用成熟度模型 | 战略、过程、资产、度量、文化维度 |
| **NASA RRL** | RRL 1–9 | 可复用资产技术就绪度 | 从概念到多任务验证的分级推广标准 |

## 12. 交叉引用

- 成熟度评估问卷 CLI：[`assessment-questionnaire.md`](./assessment-questionnaire.md)
- ISO 26565/26566 详细对齐：[`iso-26565-26566-final.md`](./iso-26565-26566-final.md)
- SPICE 与 RCMM/RiSE 映射：[`spice-rcmm-rise-mapping.md`](./spice-rcmm-rise-mapping.md)
- 跨层复用治理框架：[`../01-process-governance/cross-layer-governance.md`](../01-process-governance/cross-layer-governance.md)
- 度量指标体系：[`../05-metrics-kpi/metrics-framework.md`](../05-metrics-kpi/metrics-framework.md)

## 13. 参考索引

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| ISACA — CMMI Performance Solutions | <https://www.isaca.org/resources/cmmi> | 2026-07-08 |
| Jasmine & Vasantla — RCMM | <https://doi.org/10.1109/MS.2008.167>（原始论文索引） | 2026-07-08 |
| Garcia (2010) — RiSE Reference Model | <https://rise.com.br/> | 2026-07-08 |
| Koltun & Hudson (1991) — Software Reuse Maturity Framework | <https://dl.acm.org/doi/10.1145/123078.124072> | 2026-07-08 |
| VDA QMC — Automotive SPICE v4.0 | <https://www.automotivespice.com/> | 2026-07-08 |
| ISO/IEC 26565:2026 — 产品线成熟度框架 | <https://www.iso.org/standard/81436.html> | 2026-07-08 |
| ISO/IEC 26566:2026 — 产品线纹理方法 | <https://www.iso.org/standard/81437.html> | 2026-07-08 |
| NASA — Reuse Readiness Levels | <https://www.nasa.gov> | 2026-07-08 |

> 最后更新：2026-07-08