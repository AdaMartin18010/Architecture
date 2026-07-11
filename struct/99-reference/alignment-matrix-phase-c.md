# Phase C 对齐矩阵与 A+B+C 累计汇总

> **版本**: 2026-06-10
> **定位**: Phase C（扩展对齐与纵深）8 项交付物的标准对齐关系总表，及 Phase A+B+C 累计对齐汇总
> **维护**: 每次新增/更新 Phase C 类扩展文档时同步更新

---

## 一、Phase C 文档 × 标准/框架对齐矩阵

| 文档名称 | 对齐标准 | 覆盖领域 | 与已有文档的互补关系 | 引用规范（URL + 日期） |
|---|---|---|---|---|
| **C-01 SysML v2 复用映射** | OMG SysML v2 (2023), ISO/IEC 42010:2022, OMG RAS 2.0, ISO/IEC 26550:2015, IEEE 1471 | 元模型标准层 / 模型驱动系统工程 | 与 C-02 MBSE 整合互补：C-01 聚焦语言级复用语义，C-02 聚焦方法论与工具链；与 01/03 PLE 整合文档形成标准族互补 | OMG SysML v2: <https://www.omg.org/spec/SysML/> (2023-06)<br>ISO 42010:2022: <https://www.iso.org/obp/ui> (2022)<br>OMG RAS: <https://www.omg.org/spec/RAS/> (2024) |
| **C-02 MBSE 与 PLE 整合** | INCOSE SE Vision 2035, ISO/IEC 26550:2015, ISO/IEC 42010:2022, IEC 63278 (AAS), ISO 15288:2023, OMG SysML v2 | 元模型标准层 / 系统工程与产品线工程 | 与 C-01 形成"语言-方法"双轴；与 11/05 AAS-OPC UA 映射形成工业-系统工程桥梁 | INCOSE: <https://www.incose.org/SEVision2035> (2023)<br>ISO 26550: <https://www.iso.org/standard/69529.html> (2023)<br>ISO 15288: <https://www.iso.org/standard/81702.html> (2023) |
| **C-03 数字孪生通用参考架构** | ISO 23247, AEDT, Gartner 数字孪生框架, IEC 63278 (AAS 对比参考) | 工业物联网 / 数字孪生（非工业场景） | 与 11/05 AAS-OPC UA 映射互补：C-03 覆盖通用/商业数字孪生，11/05 聚焦工业自动化；与 C-02 MBSE 形成模型-孪生闭环 | ISO 23247: <https://www.iso.org/standard/77378.html> (2021)<br>AEDT: <https://www.digitaltwinconsortium.org/> (2026-06) |
| **C-04 OWASP SCVS 映射** | OWASP SCVS 1.0, SLSA 1.2, SPDX 2.3, CycloneDX 1.6, NIST SSDF | 供应链安全 / 组件验证 | 与 10/01 SLSA、10/02 SBOM 形成"构建-清单-验证"三角；C-04 填补组件验证控制族空白，与 C-05 GUAC 形成"标准-工具"闭环 | OWASP SCVS: <https://scvs.owasp.org/> (2020)<br>SLSA 1.2: <https://slsa.dev/spec/v1.2/> (2025)<br>NIST SSDF: <https://csrc.nist.gov/projects/ssdf> (2024) |
| **C-05 GUAC 供应链图谱** | GUAC v0.x, SLSA 1.2, OpenSSF Scorecard, SPDX 2.3, CycloneDX 1.6, OSV | 供应链安全 / 风险量化与知识图谱 | 与 C-04 SCVS 互补：C-04 提供验证标准，C-05 提供动态风险分析能力；与 10/03 攻击向量形成"防御-检测"闭环 | GUAC: <https://guac.sh/> (2026)<br>OpenSSF Scorecard: <https://securityscorecards.dev/> (2026)<br>OSV: <https://osv.dev/> (2026) |
| **C-06 TMForum 电信架构复用** | TMForum ODF, eTOM, SID, ODA, CAMARA | 业务架构 / 电信垂直行业 | 与 02/02 FEA BRM、B-04 BIAN 形成"政府-金融-电信"三行业业务能力映射互补；与 03 应用架构微服务形成行业-技术映射 | TMForum: <https://www.tmforum.org/> (2026)<br>CAMARA: <https://camara.project.org/> (2026) |
| **C-07 NAF/MODAF 北约架构复用** | NAF 4.0, MODAF, DoDAF 2.02, UAF 1.3 | 业务架构 / 国防使命工程 | 与 B-01 DoDAF/UAF 互补：B-01 覆盖美国/国际视角，C-07 覆盖北约/英国视角；与 02/07 国防使命工程形成纵深 | NATO NAF: <https://nafdocs.org/> (2018)<br>MODAF: <https://www.mod.uk/> (2012)<br>DoDAF: <https://dodcio.defense.gov/dodaf/> (2010) |
| **C-08 复用决策工具 v2.0** | — (内部工具，对齐 ISO 26565:2026 产品线成熟度框架 / 26566 产品线纹理, NASA RRL) | 工具链 / 复用决策支持 | 与 99-reference/tools/reuse-decision-tool/ (v1.0) 互补：升级为 CLI+Web 双模，新增数据驱动模板与测试覆盖；与 06/03 成熟度模型形成评估-决策闭环 | 项目内部: `./struct/99-reference/tools/reuse-decision-tool-v2/` (2026-06-10)<br>ISO 26565: <https://www.iso.org/standard/81436.html> (2026)<br>ISO 26566: <https://www.iso.org/standard/81437.html> (2026) |

---

## 二、Phase A+B+C 累计对齐矩阵（简化汇总）

| 阶段 | 主题领域 | 新增对齐标准/框架 | 交付物数量 | 与前期内容的互补关系 |
|------|----------|-------------------|------------|----------------------|
| **Phase A** | 元模型 / 治理 / 供应链 / 应用架构 | ISO 12207:2026, ISO 26565/26566, EU CRA, SLSA 1.2 | 7 项 | **修复与更新**：纠正 ArchiMate 4.0 误报、MCP 版本勘误，补全 03 应用架构基础子目录（分层/微服务/Serverless/事件驱动） |
| **Phase B** | 元模型 / 业务架构 / 治理 / 新兴趋势 | DoDAF/UAF, Zachman, SPICE (ISO 33000), BIAN, GreenArch, OMG RAS v2.2, IEEE 1517, FAIR4RS, ISO 25010:2023 AI 质量 | 12 项 | **横向扩展**：引入国防、金融、可持续软件等 5 个外部视角；标准覆盖从 30 扩展至 35+；工具链补充术语查询、COCOMO 计算器、成熟度问卷 |
| **Phase C** | 元模型 / 工业 IoT / 供应链 / 业务架构 / 工具链 | SysML v2, MBSE/PLE, ISO 23247, AEDT, OWASP SCVS, GUAC, TMForum, NAF/MODAF | 8 项 | **纵深扩展**：填补 MBSE/数字孪生通用架构/电信/国防北约视角空白；升级决策工具至 v2.0；与 Phase 1-5 形成"通用+垂直+工具"完整闭环 |
| **累计** | **13 个一级主题全覆盖** | **42+ 国际标准与框架** | **241 文档 + 23 工具** | **从通用四层架构（业务→应用→组件→功能）到垂直行业（国防/金融/电信/工业）、从理论文档到可执行工具链的完整知识闭环** |

---

## 三、关键互补关系图解

```text
Phase A（修复/更新）
  ├── ArchiMate 4.0 勘误 ──→ 与 01/04 元模型标准层互补
  ├── 03 应用架构补全 ──→ 与 Phase 1 核心层次深化互补
  └── SLSA 1.2 更新 ──→ 与 10/01 供应链安全互补

Phase B（横向扩展）
  ├── DoDAF/UAF + Zachman ──→ 与 TOGAF/ArchiMate 形成多框架映射
  ├── BIAN + TMForum(C-06) ──→ 形成"金融-电信"垂直行业双轴
  ├── SPICE + RCMM/RiSE ──→ 与 06/03 成熟度模型互补
  └── GreenArch ──→ 与 13/06 可持续软件互补

Phase C（纵深扩展）
  ├── SysML v2(C-01) + MBSE/PLE(C-02) ──→ 模型驱动复用"语言-方法"双轴
  ├── SCVS(C-04) + GUAC(C-05) + SLSA ──→ 供应链安全"验证-图谱-构建"三角
  ├── NAF/MODAF(C-07) + DoDAF/UAF(B-01) ──→ 国防架构"美国-北约"双视角
  └── 工具 v2.0(C-08) + 成熟度问卷 + COCOMO ──→ 可执行工具链闭环
```

---

## 四、维护说明

1. **更新触发**：每当新增 Phase C 类扩展文档（新垂直行业、新元模型标准、新工具版本）时，更新本章第一节表格。
2. **URL 健康检查**：每季度使用 `99-reference/tools/standard-tracker.py` 检查引用 URL 有效性，失效链接标记为 `[需更新]`。
3. **累计矩阵更新**：Phase A/B/C 累计矩阵仅在阶段里程碑节点更新（如 Phase D 完成后将新增 Phase D 列）。

---

> **最后更新**: 2026-06-10


---

## 补充说明：Phase C 对齐矩阵与 A+B+C 累计汇总

## 概念定义

**定义**：参考层是结构化知识体系的“地图”，汇总权威来源、术语表、标准索引、课程对标与审计报告，为各主题提供可追溯的引用与一致性校验。

## 示例

**示例**：维护 authoritative-sources.md 登记所有 ISO/IEC、IEEE、NIST、CNCF 来源 URL 与核查日期，确保全书引用可验证。

## 反例

**反例**：参考层链接长期不更新，术语表与正文定义冲突，读者无法确认内容准确性与时效性。

## 权威来源

> **权威来源**:
>
> - [ISO](https://www.iso.org)
> - [IEEE Standards](https://standards.ieee.org)
> - [NIST](https://www.nist.gov)
> - [CNCF](https://www.cncf.io)
> - 核查日期：2026-07-07

## 分析

**分析**：参考层的价值不在于内容本身，而在于建立知识之间的信任锚点；必须随标准演进定期审计与更新。
