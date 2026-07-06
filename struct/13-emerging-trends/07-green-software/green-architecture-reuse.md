# 可持续软件架构（GreenArch）初探

> 本交付物探索软件架构复用与碳排放管理的交叉领域，为架构决策引入可持续维度提供初步框架。

---

## 1. Green Software Foundation 框架

### 1.1 SCI：软件碳强度标准

Green Software Foundation（GSF）发布的 **SCI（Software Carbon Intensity）v1.1** 已被采纳为 **ISO/IEC 21031:2024** 国际标准，是衡量软件碳排放的核心计量框架。

**SCI 公式**：

```
SCI = ((E × I) + M) per R
```

| 变量 | 含义 |
|------|------|
| **E** | 软件消耗的电能（kWh） |
| **I** | 电网碳强度（gCO₂e/kWh），location-based |
| **M** | 运行软件的硬件隐含碳排放（embodied carbon）分摊 |
| **R** | 功能单位（functional unit），如"每千次 API 调用"、"每用户会话" |

SCI 的关键设计原则是**将碳排放归一化到功能单位**，使不同架构方案之间具备可比性，从而为架构决策提供量化依据。

### 1.2 三大原则

| 原则 | 核心要义 | 架构含义 |
|------|---------|---------|
| **能源效率** | 减少软件运行所需电能 | 算法优化、资源调度、减少空闲计算 |
| **硬件效率** | 延长硬件生命周期，提高利用率 | 虚拟化、容器密度、多租户共享 |
| **碳感知** | 在碳强度较低的时空运行计算 | 时空转移负载、需求塑形、特征降级 |

---

## 2. GreenArch 2026 首届 Workshop

**GreenArch 2026 —— Software Architecture for Green Sustainable Carbon-aware Software Systems** 是首届聚焦绿色可持续碳感知软件架构的学术 Workshop，将于 **2026 年 6 月** 在荷兰 **阿姆斯特丹** 召开，作为 **IEEE ICSA 2026**（第 23 届国际软件架构会议）的配套 Workshop。

### 关键议题

- **架构拓扑对微服务能效的影响**：研究微服务拆分粒度、通信模式（同步 vs 异步）、服务编排策略与整体能耗之间的关联。初步研究表明，过度细粒度的微服务拆分可能导致显著的通信开销与能耗放大。
- **特征降级（Feature Degradation）**：作为碳感知架构的新兴策略，指在高碳强度时段或高负载场景下，主动降级非核心功能以换取整体能耗降低。Gazeau & Ledoux 在 GreenArch 2026 接收的论文中以 Overleaf 应用为案例，验证了特征降级在保持核心可用性的同时显著降低能耗的可行性。
- **AI 系统的架构级可持续性**：从模型绑定的能耗关注，转向 LLM Agent 系统的架构驱动开销分析，强调"Shift Left"在 AI 可持续设计中的必要性。

---

## 3. 架构复用的碳影响

### 3.1 复用 vs 重写：生命周期碳排放视角

传统 ROI/COCOMO 模型未纳入碳排放维度。从全生命周期视角审视：

| 维度 | 复用既有资产 | 重新开发 |
|------|------------|---------|
| 开发阶段 | 低（避免重复编码/测试） | 高（新开发、CI/CD、开发环境） |
| 运行阶段 | 取决于既有资产能效；老旧组件可能较差 | 可采用最新能效技术 |
| 硬件隐含碳 | 减少新硬件采购 | 可能驱动新硬件部署 |
| 维护阶段 | 与既有维护负担叠加 | 独立维护碳足迹 |

**关键洞察**：复用的碳优势并非绝对。高能耗遗留组件的长期运行碳排放可能远超重写后的现代能效架构，复用决策需引入"碳盈亏平衡分析"。

### 3.2 共享服务/组件的碳分摊模型

在多租户架构中，单一组件的碳排放按使用量分摊至各消费方：

```
CarbonAllocated_i = SCI_component × Usage_i / TotalUsage
```

`Usage_i` 可采用标准化指标（API 调用数、计算分钟数、数据吞吐量），使各团队对复用选择的碳后果承担明确责任。

### 3.3 数据中心碳强度对架构决策的影响

电网碳强度（I）因地域和时段差异巨大（例如，挪威水电区可低至 20 gCO₂e/kWh，而煤电密集区可超过 800 gCO₂e/kWh）。location-based 碳强度应成为部署架构设计的关键输入：

- 跨地域部署优先将弹性负载调度至低碳区域
- 多云策略纳入碳强度作为区域选择权重
- 边缘节点选址评估当地电网碳结构

---

## 4. 碳感知架构模式

### 4.1 时间转移（Temporal Shifting）

将非关键批处理任务（日志分析、ETL、模型重训练）从高碳时段移至低碳时段（夜间可再生能源富余期）。
实施要点：任务具备可延迟性；调度器集成实时碳强度信号（如 Electricity Maps API）；SLA 与碳节约之间的权衡显性化。

### 4.2 地理转移（Geographic Shifting）

跨区域负载均衡时，将请求路由至碳强度最低的数据中心。与延迟优化的冲突通过"碳-延迟帕累托前沿"显式权衡。

### 4.3 需求塑形（Demand Shaping）

根据实时碳信号调整功能级别：碳信号高时限制非核心功能、降低并发度；碳信号低时恢复正常级别并加速积压处理。

### 4.4 特征降级（Feature Degradation）

在高碳时段或高负载时主动降级非核心功能以降低能耗：

| 功能类别 | 正常模式 | 降级模式 |
|---------|---------|---------|
| 推荐系统 | 实时个性化推荐 | 静态热门列表 |
| 数据分析 | 实时仪表盘 | 小时级缓存快照 |
| 图像处理 | 高分辨率生成 | 低分辨率/缩略图 |
| 搜索 | 语义搜索+排序 | 关键词匹配基础搜索 |

架构实现需预先定义功能级别、降级触发条件与恢复策略，通过配置中心或自适应控制器动态编排。

---

## 5. 复用决策的碳维度

### 5.1 在 ROI/COCOMO 模型中加入碳成本

建议在现有复用决策模型中增加碳成本项：

```
TotalCost = DevCost + MaintenanceCost + OpCost + CarbonCost

CarbonCost = LifetimeCarbon × InternalCarbonPrice
```

其中 `InternalCarbonPrice` 可参考企业碳定价或市场碳价（EU ETS、CCX）。将碳成本内部化后，高能耗遗留资产的复用吸引力将显著下降。

### 5.2 Carbon BOM 概念

借鉴软件物料清单（SBOM）理念，提出 **Carbon BOM（碳物料清单）**：对复用资产附加标准化碳足迹元数据，包括：

- 单功能单位运行碳排放（SCI）
- 硬件隐含碳分摊
- 依赖服务的级联碳足迹
- 碳强度假设（地域、时段基准）

Carbon BOM 使架构师在复用选择时能够像评估安全漏洞一样评估碳影响，实现"碳可见性"（carbon visibility）。

---

## 6. 权威来源

| 来源 | 说明 |
|------|------|
| greensoftware.foundation | Green Software Foundation 官方框架与工具 |
| SCI Specification v1.1 / ISO/IEC 21031:2024 | 软件碳强度国际标准 |
| GreenArch 2026 (ICSA Workshop) | 首届绿色可持续碳感知软件架构 Workshop |
| Gazeau & Ledoux (GreenArch 2026) | Feature Degradation for Frugality: Overleaf Case Study |
| GREENS'26 Workshop Program | 第 10 届绿色与可持续软件国际 Workshop |
| Funke & Lago (GREENS'26) | Injecting Sustainability in Software Architecture: A Rapid Review |

---

> **结语**
> 可持续软件架构正从理念倡导走向工程实践。SCI 国际标准的确立、GreenArch 2026 等学术平台的涌现，以及碳感知架构模式的成熟，共同为架构复用决策引入了新的优化维度。
> 未来的架构师不仅需要在功能、性能、成本之间权衡，还必须将碳排放作为一等公民纳入架构设计空间。


---

## 补充说明：可持续软件架构（GreenArch）初探

## 反例

**反例**：为追求微服务“弹性”而将单体拆分为 200 个服务，每个服务常驻空闲实例，整体能耗翻倍。

## 权威来源

> **权威来源**:
>
> - [Green Software Foundation](https://greensoftware.foundation)
> - [SCI Specification](https://sci.greensoftware.foundation)
> - 核查日期：2026-07-07

## 分析

**分析**：绿色复用要求从架构层面减少冗余计算，并将碳排指标纳入资产准入评估。
