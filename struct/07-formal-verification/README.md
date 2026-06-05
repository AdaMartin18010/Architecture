# 07 形式化验证与复用正确性

## 定位

将复用组件的正确性从"测试验证"提升到"数学证明"的最高等级保证。

## 核心内容

- **TLA+**: 分布式复用组件的时序行为规约（Leslie Lamport）
- **Alloy**: 架构约束的约束求解验证（Daniel Jackson）
- **Coq/Isabelle**: 定理证明与程序验证（CompCert, seL4）
- **Rust 类型系统**: 编译期复用安全的形式化基础（所有权、借用、生命周期）
  - RustBelt (Iris), Aeneas (Inria), Kani (AWS), Prusti (ETH Zurich)
- **SPARK/Ada**: 飞行控制软件的契约验证（Airbus A380 案例）
- **B Method**: 铁路信号系统的形式化精化链
- **模型检测**: SPIN, NuSMV, CBMC
- 形式化验证的复用决策矩阵（工具 × 层次 × 成本）

## 权威对齐

- [TLA+ Home Page](https://lamport.azurewebsites.net/tla/tla.html) (Leslie Lamport, Microsoft)
- [Alloy Tools](https://alloytools.org) (MIT)
- [Coq Proof Assistant](https://coq.inria.fr) (Inria)
- [Isabelle/HOL](https://isabelle.in.tum.de) (TU Munich)
- [RustBelt](https://plv.mpi-sws.org/rustbelt/) (MPI-SWS)
- [SPARK Pro](https://www.adacore.com/about-spark) (AdaCore)
- [Atelier B](https://www.atelierb.eu) (Clearsy)

## 关键公理
>
> **公理 F.1** (Formal Verification Trust Transfer): 若组件 C 通过形式化方法验证了性质 P，则任何使用 C 的系统继承 P 的正确性保证，前提是 C 的使用方式不违反 C 的前置条件。

## 当前状态

- [x] 形式化方法谱系梳理
- [x] TLA+/Alloy/Rust 案例示例
- [ ] DO-178C MC/DC 形式化定义（卷六深化）
- [ ] Rust Polonius 借用检查器形式化

## 关联主题

- `04-component-architecture-reuse`（Rust 生态形式化）
- `11-industrial-iot-otit`（功能安全形式化验证）
