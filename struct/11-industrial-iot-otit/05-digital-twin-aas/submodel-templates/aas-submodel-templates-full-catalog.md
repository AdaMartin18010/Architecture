# AAS 子模型模板全清单
>
> 版本: 2026-06-06
> 对齐来源: IDTA (Industrial Digital Twin Association) Submodel Registry, IEC 63278-1:2023, IEC 63278-4 (用例)
> 定位: 覆盖 IDTA 已发布和开发中子模型模板的完整目录

## 1. 已发布子模型模板 (IDTA-020xx)

### 1.1 基础标识类

| ID | 名称 | 版本 | 核心内容 | 应用场景 |
|----|------|------|---------|---------|
| IDTA-02002 | **Contact Information** | 1.0 | 组织/人员联系信息（地址、邮箱、电话、角色）| 供应商管理、服务请求 |
| IDTA-02003 | **Technical Data** | 1.1 | 设备技术参数（电气、机械、环境规格）| 设备选型、工程设计 |
| IDTA-02006 | **Nameplate** | 2.0 | 铭牌信息（制造商、型号、序列号、认证标志）| 资产识别、合规检查 |
| IDTA-02007 | **Identification** | 1.0 | 多标识符管理（全局 ID、内部 ID、条形码、RFID）| 追踪追溯、库存管理 |

### 1.2 文档与生命周期类

| ID | 名称 | 版本 | 核心内容 | 应用场景 |
|----|------|------|---------|---------|
| IDTA-02008 | **Handover Documentation** | 1.0 | 移交文档清单（手册、证书、测试报告、培训材料）| FAT/SAT、运维交接 |
| IDTA-02012 | **Service Notifications** | 1.0 | 服务通知记录（故障报告、服务请求、状态更新）| 售后服务、CMMS 集成 |
| IDTA-02014 | **Maintenance** | 1.0 | 维护计划、维护记录、维护工单 | 预测性维护、CMMS |

### 1.3 环境与可持续性类

| ID | 名称 | 版本 | 核心内容 | 应用场景 |
|----|------|------|---------|---------|
| IDTA-02016 | **Carbon Footprint** | 1.0 | 碳足迹数据（Scope 1/2/3、PCF、组织碳足迹）| ESG 报告、产品护照 |
| IDTA-02017 | **Material** | 1.0 | 材料成分、材料声明（IMDS 对接）、可回收性 | 环保合规、DPP |
| IDTA-02018 | **Circuit Breaker** | 1.0 | 断路器技术数据（额定电流、分断能力、脱扣特性）| 电气设计、安全计算 |

### 1.4 数据与接口类

| ID | 名称 | 版本 | 核心内容 | 应用场景 |
|----|------|------|---------|---------|
| IDTA-02022 | **Time Series Data** | 1.0 | 时间序列数据描述（采样率、单位、存储位置）| 传感器数据、历史数据库 |
| IDTA-02026 | **Provision of 3D Models** | 1.0 | 3D 模型引用（格式、LOD、坐标系、可视化工具）| 数字孪生可视化、VR/AR |

### 1.5 安全与合规类

| ID | 名称 | 版本 | 核心内容 | 应用场景 |
|----|------|------|---------|---------|
| IDTA-02025 | **Functional Safety** | 1.0 (草案) | 安全参数（SIL/PL 等级、安全手册、PFH/PFD）| 功能安全评估、TÜV 认证 |
| IDTA-02027 | **Cybersecurity** | 开发中 | 安全状态、漏洞信息、补丁级别、IEC 62443 对齐 | 安全审计、漏洞管理 |

## 2. 行业特定子模型模板

### 2.1 制造业

| ID | 名称 | 状态 | 核心内容 |
|----|------|------|---------|
| IDTA-02004 | **Provided Documentation for Training** | 已发布 | 培训文档、操作员培训记录、资格认证 |
| IDTA-02005 | **Provided Documentation for Operation** | 已发布 | 操作手册、SOP、故障排除指南 |
| IDTA-02009 | **Single Level Bill of Material (BOM)** | 已发布 | 单层物料清单、组件引用 |
| IDTA-02010 | **Multi Level Bill of Material (BOM)** | 已发布 | 多层物料清单、递归展开 |
| IDTA-02011 | **Document** | 已发布 | 通用文档引用（版本、格式、语言、批准状态）|
| IDTA-02013 | **Software** | 已发布 | 软件版本、许可证、依赖项、补丁级别 |

### 2.2 过程工业

| ID | 名称 | 状态 | 核心内容 |
|----|------|------|---------|
| IDTA-02015 | **P&ID** | 已发布 | 管道仪表图引用、设备关联、测量点标识 |
| IDTA-02019 | **Process Equipment** | 开发中 | 过程设备数据（反应器、换热器、泵、阀门）|
| IDTA-02020 | **Process Instrumentation** | 开发中 | 过程仪表数据（变送器、分析仪、定位器）|
| IDTA-02021 | **Process Control** | 开发中 | 控制回路数据（PID 参数、控制策略、联锁逻辑）|

### 2.3 能源与电力

| ID | 名称 | 状态 | 核心内容 |
|----|------|------|---------|
| IDTA-02023 | **Load Capability** | 开发中 | 负载能力曲线、过载能力、热极限 |
| IDTA-02024 | **Energy Efficiency** | 开发中 | 能效等级、能耗数据、节能措施 |

### 2.4 楼宇自动化

| ID | 名称 | 状态 | 核心内容 |
|----|------|------|---------|
| IDTA-02028 | **Building Information** | 开发中 | 楼宇几何、空间分配、暖通空调参数 |
| IDTA-02029 | **Room Information** | 开发中 | 房间功能、 occupants、环境设定点 |

## 3. 子模型模板结构规范

### 3.1 模板定义文件格式

每个子模型模板包含：

- **JSON Schema**: 数据结构定义（符合 IEC 63278-1 / IDTA-01001）
- **Documentation**: 人类可读规范（Markdown/PDF）
- **Example AASX**: 示例文件
- **Validation Rules**: 一致性检查规则

### 3.2 模板元数据

```json
{
  "idShort": "TechnicalData",
  "identification": "https://admin-shell.io/idta/SubmodelTemplate/TechnicalData/1/1",
  "semanticId": {
    "type": "ExternalReference",
    "keys": [{
      "type": "Submodel",
      "value": "https://admin-shell.io/idta/SubmodelTemplate/TechnicalData/1/1"
    }]
  },
  "kind": "Template",
  "submodelElements": [
    {
      "idShort": "GeneralInformation",
      "modelType": "SubmodelElementCollection",
      "semanticId": "0173-1#02-AAZ81#001",
      "value": [...]
    }
  ]
}
```

### 3.3 语义标识（SemanticId）体系

| 前缀 | 来源 | 说明 |
|-----|------|------|
| `0173-1#...` | ECLASS | 工业分类标准属性 |
| `0112/2///61360_4#...` | IEC CDD | IEC 公共数据字典 |
| `https://admin-shell.io/...` | IDTA | AAS 特定语义标识 |

## 4. 子模型模板选择指南

### 4.1 按资产类型选择

| 资产类型 | 推荐子模型组合 |
|---------|---------------|
| **旋转机械** (泵、风机、压缩机) | Nameplate + Technical Data + Time Series + Maintenance + Carbon Footprint |
| **电气设备** (变压器、开关柜) | Nameplate + Technical Data + Circuit Breaker + Maintenance + Cybersecurity |
| **控制阀** | Nameplate + Technical Data + Process Instrumentation + Maintenance |
| **机器人** | Nameplate + Technical Data + Software + Maintenance + Functional Safety |
| **软件组件** | Identification + Software + Document + Cybersecurity |

### 4.2 按生命周期阶段选择

| 阶段 | 推荐子模型 |
|-----|-----------|
| **设计与采购** | Nameplate + Technical Data + Single Level BOM + Carbon Footprint |
| **安装与调试** | Handover Documentation + Contact Information + Functional Safety |
| **运营** | Time Series + Maintenance + Service Notifications |
| **退役** | Material + Carbon Footprint + Handover Documentation |

## 5. 与数字产品护照 (DPP) 的映射

欧盟数字产品护照 (Digital Product Passport, DPP) 要求的 AAS 子模型：

| DPP 数据类别 | 对应 AAS 子模型模板 |
|-------------|-------------------|
| 产品标识 | Identification + Nameplate |
| 合规信息 | Handover Documentation (证书部分) |
| 可持续性 | Carbon Footprint + Material |
| 供应链 | Single/Multi Level BOM + Contact Information |
| 使用说明 | Provided Documentation for Operation |
| 维护历史 | Maintenance + Service Notifications |

## 6. 参考索引

- IDTA Submodel Registry: <https://github.com/admin-shell-io/submodel-templates>
- IDTA-01001-3-0: Details of the Asset Administration Shell Part 1
- IEC 63278-1:2023: Asset Administration Shell structure
- IEC 63278-4: Use cases and modelling examples
- ECLASS: <https://www.eclass.eu>
- IEC CDD: <https://cdd.iec.ch>
- EU Digital Product Passport: ESPR Regulation (EU) 2024/1781
