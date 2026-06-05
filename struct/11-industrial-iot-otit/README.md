# 11 工业 IoT / OT-IT 融合复用

## 定位

将通用软件复用框架扩展到工业自动化与 OT-IT 融合垂直领域。

## 核心内容

- **ISA-95 / IEC 62264 五层模型**: L0 现场层 → L4 企业层的复用谱系
- **OPC UA FX (2026)**: 现场级确定性通信的复用革命
  - C2C (Controller-to-Controller)
  - C2D (Controller-to-Device)
  - D2D (Device-to-Device)
- **TSN (Time-Sensitive Networking)**: 802.1AS / 802.1Qbv / 802.1CB
- **PLCopen 运动控制**: 跨厂商功能块复用（MC_Power, MC_MoveAbsolute 等）
- **数字孪生与 AAS (Asset Administration Shell)**
  - IEC 63278 元模型
  - AAS 子模型模板复用
  - OPC UA 信息模型映射
- **功能安全**: IEC 61508 / ISO 26262 的软件复用
  - Proven-in-Use (PIU) 统计验证
  - SEooC (Safety Element out of Context)
- **工业边缘计算与 AI 复用**

## 权威对齐

- [OPC Foundation](https://opcfoundation.org) (OPC UA FX 1.0)
- [PLCopen](https://plcopen.org) (Motion Control V2.0)
- [IDTA](https://industrialdigitaltwin.org) (Asset Administration Shell)
- [IEC 61508](https://www.iec.ch) (Functional Safety)
- [NAMUR NOA](https://www.namur.net) (Open Architecture)

## 关键公理
>
> **公理 I.1** (OT Determinism Non-Negotiable): 工业 OT 组件的复用必须以**确定性**为首要约束。任何牺牲确定性以换取灵活性或成本的复用策略在 OT 场景中不可接受。

## 当前状态

- [x] ISA-95 五层复用资产模型
- [x] OPC UA FX 协议层次分析
- [x] PLCopen 功能块接口定义
- [ ] AAS 到 OPC UA NodeSet 的完整映射规范
- [ ] PIU 贝叶斯方法扩展工具

## 关联主题

- `07-formal-verification`（PLC 状态机 TLA+ 验证）
- `12-ai-native-reuse`（工业边缘 AI 模型复用）
