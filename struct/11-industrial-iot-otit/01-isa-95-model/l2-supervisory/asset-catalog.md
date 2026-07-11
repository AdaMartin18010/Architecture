# L2 监控层复用资产目录

> **版本**: 2026-06-06
> **层级**: ISA-95 Level 2 — 监控 supervisory 层
> **时间尺度**: 分–小时 (min–h)
> **管理域**: 区域监控、人机交互与过程可视化域
> **对齐来源**: ISA-101 / IEC 62443-2-1, ISA-18.2 / IEC 62682, OPC Foundation HDA, OMAC PackML

---

## 1. 层定义与复用范围

L2 监控层承担区域级生产过程可视化、报警管理、历史数据归档与配方执行协调职责。
该层资产的复用核心在于**人机界面 (HMI) 模板化**、**报警规则库化**与**报表模板标准化**。
在棕地升级或新线复制场景中，复用成熟的 L2 资产可将 HMI 开发工作量降低 50%–70%。

> **交叉引用**: L2 监控层是 `struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md` 中价值流"阶段间接口契约"的可视化呈现层——报警规则与趋势图实质上是将物理层信号转换为运营决策信息的适配器。

---

## 2. 资产分类表

| 序号 | 资产名称 | 描述 | 标准/规范 | 复用频率 | 成熟度 |
|-----|---------|------|----------|---------|--------|
| S1 | **HMI 画面模板库** | 按设备类型预定义的 HMI 画面模板：泵/风机/阀门/罐体/反应釜/传送带。包含标准导航、状态指示、操作面板、趋势嵌入、权限控制框架。 | ISA-101 (HMI Design), IEC 62443-2-1 | 极高 (每个 SCADA/HMI 项目) | 成熟 |
| S2 | **报警管理规则模板** | 基于 ISA-18.2 / IEC 62682 的报警分级、抑制、泛滥管理与优先级矩阵模板。包含 10–30–60 报警泛滥监控 KPI、报警合理化检查清单。 | ISA-18.2 / IEC 62682, EEMUA 191 | 高 (流程工业强制合规) | 成熟 |
| S3 | **实时趋势与历史趋势模板** | 预配置的时间序列趋势图模板：单变量趋势、XY 相关趋势、多变量叠加趋势、SPC 控制图 (X-bar, R, p, c)。集成 OPC HDA / OPC UA Historizing。 | OPC Foundation HDA, ISA-5.1 | 高 (运营监控标配) | 成熟 |
| S4 | **生产报表模板 (Shift/Daily/Monthly)** | 班报/日报/月报的标准报表模板，自动聚合 OEE、产量、能耗、质量合格数、停机事件。支持导出 PDF/Excel/CSV。 | ISA-95 Part 4 (Object Model Attributes), MESA | 高 (管理层决策支持) | 成熟 |
| S5 | **OMAC PackML 状态可视化模板** | 实现 PackML Unit Mode / State Model 的标准 HMI 状态机画面，集成 Mode Manager、State Manager、Equipment Modules 状态显示。 | OMAC PackML State Model V4.0+ | 中 (包装、消费品行业) | 成熟 |
| S6 | **批次电子批记录 (EBR) 模板** | 基于 ISA-88 / IEC 61512 的批次执行过程记录模板，自动捕获配方参数、操作员动作、偏差、签名时间戳，满足 FDA 21 CFR Part 11。 | ISA-88 / IEC 61512, FDA 21 CFR Part 11 | 中 (制药、食品合规) | 成熟 |
| S7 | **能源管理仪表盘模板** | 按 ISO 50001 能源管理体系设计的能耗监控仪表盘模板，包含单位产品能耗、峰谷平用电分析、碳排放因子计算。 | ISO 50001:2018, ISO 14064-1 | 中 (双碳政策驱动) | 发展中 |
| S8 | **视频联动报警模板** | SCADA 报警触发时自动弹出关联 CCTV 视频流的画面模板，支持预置位调用、录像回放、事件标记，用于安全与质量追溯。 | ONVIF Profile S/G, IEC 62443 | 低–中 (高价值产线) | 发展中 |

---

## 3. 复用建议

### 3.1 HMI 模板的跨项目复用

1. **响应式分辨率适配**: HMI 模板应基于矢量图形与相对坐标设计，确保从 10" 触摸屏到 4K 操作站的无损复用。推荐采用 HTML5/WebGL 技术栈（Ignition Perspective, WinCC Unified）。
2. **主题与品牌分离**: 将颜色主题、企业 Logo、字体规范抽离为 CSS/主题文件，基础模板保持中性，实现"换肤不换骨"。
3. **权限矩阵复用**: 基于 RBAC (Role-Based Access Control) 的权限矩阵模板（操作员/班长/工程师/管理员）跨项目复用，仅需调整区域与设备实例映射。

### 3.2 报警管理的合规复用

- **报警合理化库**: 建立企业级报警清单数据库，每个报警条目包含：位号、描述、根本原因、标准响应动作、优先级、抑制条件。新项目从库中勾选复用，避免重复创建。
- **ISA-18.2 生命周期文档模板**: 复用报警识别→合理化→详细设计→实施→运行监控→审计的全生命周期文档模板，确保合规审计一次通过。

### 3.3 跨层复用接口

- **L2 ← L1**: 通过 OPC UA / MQTT 订阅 L1 PLC 的 UDT 实例与报警事件，直接复用 L1 控制层定义的语义结构。详见 [L1 控制层复用资产目录](../l1-control/asset-catalog.md)。
- **L2 → L3**: 通过 B2MML / REST API 上报生产绩效、报警 KPI、批次事件，复用 ISA-95 标准数据对象。
- **L2 ↔ L4**: 能源管理仪表盘可将聚合后的能耗数据推送至企业碳管理平台（L4），实现 OT 数据直接驱动 ESG 报告。

### 3.4 形式化验证提示

> **交叉引用**: 报警泛滥管理规则 (S2) 与 PackML 状态机可视化 (S5) 涉及状态转移的正确性。可借鉴 `struct/07-formal-verification/06-b-method/event-b-railway-refinement.md` 中 **Event-B 精化** 的方法论：将 PackML 状态机规约为抽象 Machine，通过守卫事件验证状态转移的完备性与互斥性；将报警抑制规则建模为上下文公理，确保障碍条件下不会出现死锁报警。

---

## 4. 权威来源

1. ISA-101-2015 — Human Machine Interface Design
2. ISA-18.2 / IEC 62682:2022 — Management of Alarm Systems for the Process Industries
3. EEMUA Publication 191 — Alarm Systems: A Guide to Design, Management and Procurement (Edition 3)
4. OMAC PackML — State Model and Tag Naming Guideline V4.0
5. ISA-88 / IEC 61512-1:2013 — Batch Control Part 1: Models and Terminology
6. IEC 62443-2-1:2010 — Industrial communication networks: Security for industrial automation and control systems
7. ISO 50001:2018 — Energy management systems
8. OPC Foundation — OPC Unified Architecture Historical Data Access (HDA)

---

> 最后更新: 2026-06-06


---

## 补充章节

## 示例

**示例**：汽车工厂将 ISA-95 L0-L4 资产目录映射到 IEC 63278 资产管理壳（AAS），通过 OPC UA FX 实现现场设备与 MES/ERP 的即插即用复用。

## 反例

**反例**：将 IT 系统直接补丁策略套用到 PLC 产线，未考虑实时性约束与功能安全认证，导致停机与安全事故。

## 权威来源

> **权威来源**:
>
> - [ISA-95 / IEC 62264](https://www.isa.org/standards-and-publications/isa-standards/isa-95)
> - [OPC Foundation](https://opcfoundation.org)
> - [IEC 61508-1:2010](https://webstore.iec.ch/en/publication/5515)
> - [IEC 63278 AAS](https://iec.ch/dyn/www/f?p=103:38:0::::FSP_ORG_ID:1363)
> - 核查日期：2026-07-07
