# SPARK Ada vs Rust：安全关键系统验证方法对比矩阵
>
> 版本: 2026-06-06
> 对齐来源: DO-178C/DO-333, AdaCore SPARK Pro 24, Rust 1.85+, RustBelt (Iris), Aeneas (Inria), Prusti (ETH), Kani (AWS)
> 定位: 为安全关键软件架构师提供两种语言的形式化验证能力对比决策支持

## 1. 语言与验证范式概览

| 维度 | SPARK Ada | Rust |
|-----|-----------|------|
| **语言族** | Ada 子集（命令式，Pascal 风格）| 系统编程语言（C++ 替代）|
| **主要验证范式** | 演绎式程序验证（Contracts + SMT）| 类型系统保证 + 可选形式化验证 |
| **核心安全保证** | 无运行时错误 + 功能正确性 | 内存安全 + 数据竞争自由 |
| **工业认证** | DO-178C/DO-333 FAA/EASA 认可 | 尚无航空级 DO-178C 认证路径 |
| **代码可读性** | 显式合同（Pre/Post/Global/Depends）| 隐式类型约束（所有权/生命周期）|

## 2. 安全保证对比矩阵

| 安全属性 | SPARK Ada | Rust | 说明 |
|---------|-----------|------|------|
| **内存安全** | ✅ 编译期 + 证明期 | ✅ 编译期（所有权系统）| 两者均保证无 use-after-free、double-free |
| **数据竞争自由** | ✅ 信息流分析 | ✅ 编译期（&mut T 唯一性）| Rust 通过类型系统；SPARK 通过 Global/Depends |
| **数组越界** | ✅ 证明 + 运行时检查 | ⚠️ 需 `assert!` 或 `unsafe` | Rust 标准库 `get()` 安全，`[]` 运行时检查 |
| **整数溢出** | ✅ 证明期检测 | ⚠️ Debug 模式 panic，Release 模式 wrap | Rust `checked_add` 可安全处理 |
| **除零** | ✅ 证明期检测 | ⚠️ 运行时 panic | Rust 需显式检查 |
| **未初始化变量** | ✅ 证明期检测 | ✅ 编译期（移动语义）| Rust 更严格：未初始化变量无法使用 |
| **空指针/空引用** | ✅ 排除（Ada 无空指针）| ✅ 编译期（`Option<T>` 显式处理）| Rust `&T` 永不为空，`Option` 强制处理 |
| **别名分析** | ✅ 显式 Global/Depends | ✅ 编译期（借用检查器）| Rust 自动推断；SPARK 显式声明 |
| **并发死锁** | ⚠️ 需额外证明 | ⚠️ 编译期不保证 | 两者均需运行时分析或模型检测 |
| **功能正确性** | ✅ 合同证明（Post 条件）| ⚠️ 需外部工具（Prusti/Kani）| SPARK 原生；Rust 需附加形式化工具 |

## 3. 形式化验证工具链对比

| 工具/能力 | SPARK Ada | Rust |
|----------|-----------|------|
| **编译器** | GNAT Pro (AdaCore) | rustc (开源) |
| **证明器** | Alt-Ergo, Z3, CVC5 (SMT) | 无原生；Kani (CBMC), Prusti (Viper), Aeneas |
| **证明语言** | SPARK 合同（Pre/Post/Loop_Invariant）| 外部注解（`#[requires]`, `#[ensures]`, `kani::proof`）|
| **自动化程度** | 高（80%+ 自动证明）| 中（需人工干预和辅助引理）|
| **证明覆盖** | 完整（可达性、无 RTE、合同满足）| 取决于工具：Kani 属性检测；Prusti 合同验证 |
| **工具资格** | DO-330 TQL-1 工具资格包 | 无（Kani/Prusti 未获航空工具资格）|
| **IDE 集成** | GNAT Studio, VS Code (AdaCore) | VS Code, IntelliJ, rust-analyzer |
| **调试体验** | 合同失败定位精确 | Miri 可检测 UB；形式化工具错误报告较晦涩 |

## 4. 工业应用生态对比

| 应用领域 | SPARK Ada | Rust |
|---------|-----------|------|
| **航空电子** | ✅ 成熟（Airbus, Dassault, Lockheed Martin）| ⚠️ 探索阶段（无人系统、地面支持）|
| **铁路信号** | ✅ 使用（Alstom, Siemens）| ⚠️ 早期试点 |
| **汽车 (AUTOSAR)** | ⚠️ 有限（部分 OEM 研究）| ⚠️ 研究项目（AUTOSAR Adaptive 探讨）|
| **航天** | ✅ 传统优势（ESA, NASA）| ⚠️ SpaceX 部分地面软件 |
| **医疗设备** | ✅ IEC 62304 合规 | ⚠️ 尚无 FDA 认证案例 |
| **核工业** | ✅ 传统使用 | ❌ 无已知应用 |
| **操作系统内核** | ✅ 微内核（seL4 用 Haskell 验证）| ✅ 活跃（Rust for Linux, Redleaf, Theseus）|
| **嵌入式实时** | ✅ Ravenscar Profile（确定性并发）| ⚠️ `no_std` + RTIC 框架 |

## 5. 代码示例对比：安全关键函数

### 5.1 数组查找最大值（带边界保证）

**SPARK Ada:**

```ada
function Find_Max (Arr : Int_Array) return Integer with
   Pre  => Arr'Length > 0,
   Post => (for all I in Arr'Range => Find_Max'Result >= Arr(I))
           and (for some I in Arr'Range => Find_Max'Result = Arr(I))
is
   Max : Integer := Arr(Arr'First);
begin
   for I in Arr'First + 1 .. Arr'Last loop
      pragma Loop_Invariant
         (for all J in Arr'First .. I - 1 => Max >= Arr(J));
      if Arr(I) > Max then
         Max := Arr(I);
      end if;
   end loop;
   return Max;
end Find_Max;
```

**Rust + Prusti:**

```rust
#[requires(a.len() > 0)]
#[ensures(
    forall(|i: usize| (0 <= i && i < a.len()) ==> result >= a[i]),
    exists(|i: usize| (0 <= i && i < a.len()) && result == a[i])
)]
fn find_max(a: &[i32]) -> i32 {
    let mut max = a[0];
    for i in 1..a.len() {
        body_invariant!(forall(|j: usize| (0 <= j && j < i) ==> max >= a[j]));
        if a[i] > max {
            max = a[i];
        }
    }
    max
}
```

### 5.2 环形缓冲区（无竞争保证）

**SPARK Ada (Ravenscar):**

```ada
protected type Ring_Buffer is
   entry Put (Item : in Data_Type);
   entry Get (Item : out Data_Type);
private
   Buffer : Data_Array;
   Head, Tail, Count : Natural := 0;
   -- 不变量：Count = 实际元素数，自动保护
end Ring_Buffer;
```

**Rust (标准库):**

```rust
use std::sync::mpsc::channel; // 或 crossbeam::channel
let (tx, rx) = channel::<DataType>();
// 所有权系统保证：tx 和 rx 不能同时被同一线程持有
// 编译期排除数据竞争
```

## 6. 复用与生态系统

| 维度 | SPARK Ada | Rust |
|-----|-----------|------|
| **标准库复用** | Ada 标准库（严格，航空级）| crates.io（丰富，质量参差）|
| **包管理** | GPRbuild / Alire（较新）| Cargo（成熟，依赖解析强）|
| **开源生态规模** | 小（ niche，高完整性 ）| 大（活跃，但安全关键库少）|
| **第三方库信任** | 高（来源有限，审查严格）| 需额外审查（cargo-audit, cargo-deny）|
| **代码生成** | 受限（避免未验证代码）| 宏系统强大（但宏安全需审查）|
| **FFI（外部函数接口）** | Ada ↔ C 绑定规范 | `unsafe` FFI，需手动保证前置条件 |
| **生成式 AI 支持** | 良好（合同作为规范，AI 生成后验证）| 良好（类型系统约束 AI 输出）|

## 7. 决策矩阵

| 场景 | 推荐 | 理由 |
|-----|------|------|
| **DO-178C DAL A/B 航空软件** | SPARK Ada | 唯一有完整认证路径和工具资格的形式化方法 |
| **需要替代单元测试（DO-333）** | SPARK Ada | 证明替代测试已获 FAA/EASA 认可 |
| **操作系统/内核开发** | Rust | 内存安全 + 活跃生态 + Linux 内核集成 |
| **快速原型 + 安全保证** | Rust | 学习曲线较平缓，生态丰富 |
| **既有 Ada 代码库演进** | SPARK Ada | 逐步增加合同，增量验证 |
| **多团队大规模协作** | Rust | Cargo + crates.io 的依赖管理更成熟 |
| **AI 生成代码 + 自动验证** | 两者皆可 | SPARK 合同验证；Rust 类型检查 |
| **最严格的功能正确性** | SPARK Ada | 原生合同证明覆盖完整功能正确性 |
| **最高性能的并发程序** | Rust | 零成本抽象 + 编译期数据竞争自由 |
| **工具资格预算有限** | Rust + Kani | 开源工具链，但无航空工具资格 |

## 8. 混合策略建议

对于超大型安全关键系统，可考虑**分层验证策略**：

```
System
├── 安全核心 (Safety-Critical Core)
│   ├── 推荐: SPARK Ada
│   └── 验证: DO-178C/DO-333 形式证明
│
├── 平台层 (Platform / Infrastructure)
│   ├── 推荐: Rust (safe Rust)
│   └── 验证: 类型系统 + Kani 属性检测 + Miri UB 检测
│
└── 应用层 (Application / Business Logic)
    ├── 推荐: Rust / 托管语言
    └── 验证: 测试 + 静态分析 + fuzzing
```

## 9. 参考索引

- DO-178C / ED-12C (2012) — Software Considerations in Airborne Systems
- DO-333 / ED-216 (2012) — Formal Methods Supplement
- Moy et al. (2013): "Testing or Formal Verification: DO-178C Alternatives and Industrial Experience"
- AdaCore: SPARK Pro Documentation (2024)
- RustBelt (Jung et al., POPL 2017): <https://iris-project.org>
- Aeneas (Ho & Protzenko, ICFP 2022): <https://github.com/AeneasVerif/aeneas>
- Prusti (ETH Zurich): <https://www.pm.inf.ethz.ch/research/prusti>
- Kani (AWS): <https://github.com/model-checking/kani>
- Ferrocene (Ferrous Systems): Rust 工业认证计划
