# SPARK Ada 飞控软件契约验证案例

> **版本**: 2026-06-06
> **对齐标准**: Ada 2012 + SPARK Pro 24.x, DO-178C/ED-12C, DO-333/ED-216
> **定位**: 高安全等级航空电子软件的形式化契约设计与验证

---

## 目录

- [1. SPARK Ada 核心概念](#1-spark-ada-核心概念)
  - [1.1 契约（Contracts）](#11-契约contracts)
  - [1.2 前置条件与后置条件](#12-前置条件与后置条件)
  - [1.3 循环不变式（Loop Invariants）](#13-循环不变式loop-invariants)
  - [1.4 类型谓词（Type Predicates）](#14-类型谓词type-predicates)
  - [1.5 数据依赖与信息流](#15-数据依赖与信息流)
- [2. DO-178C / DO-333 合规路径](#2-do-178c--do-333-合规路径)
  - [2.1 形式化方法作为测试替代](#21-形式化方法作为测试替代)
  - [2.2 验证目标映射](#22-验证目标映射)
- [3. 飞行控制完整案例：自动驾驶仪模式切换与高度保持](#3-飞行控制完整案例自动驾驶仪模式切换与高度保持)
  - [3.1 系统需求与状态机](#31-系统需求与状态机)
  - [3.2 类型定义与契约设计](#32-类型定义与契约设计)
  - [3.3 模式切换逻辑](#33-模式切换逻辑)
  - [3.4 高度保持控制器](#34-高度保持控制器)
  - [3.5 襟翼控制互锁](#35-襟翼控制互锁)
- [4. 与 Rust 安全关键验证方法的对比](#4-与-rust-安全关键验证方法的对比)
- [5. 复用价值与工业实践](#5-复用价值与工业实践)
- [6. 权威来源](#6-权威来源)

---

## 1. SPARK Ada 核心概念

SPARK 是 Ada 的一个可形式化验证子集，通过移除 Ada 中难以自动验证的特性（如无约束的访问类型、非局部跳转、异常传播等），为演绎式程序验证提供了坚实的语言基础[^1]。SPARK 的核心理念是：**契约即规范，证明即验证**。

### 1.1 契约（Contracts）

SPARK 中的契约是附加在子程序（过程、函数）和类型上的形式化断言，由 SPARK 工具链（GNATprove）自动证明其正确性。契约分为两类：

- **功能契约**：`Pre`（前置条件）、`Post`（后置条件）、`Contract_Cases`（分情形契约）
- **数据契约**：`Global`（全局状态访问）、`Depends`（数据依赖关系）

功能契约回答"做什么"，数据契约回答"影响什么"。二者结合，可在不运行代码的情况下证明程序满足其规格说明。

### 1.2 前置条件与后置条件

**定义 C.1** (前置条件): 子程序 `P` 的前置条件 `Pre(P)` 是一个布尔表达式，必须在 `P` 的每次调用前成立。若调用者无法满足 `Pre(P)`，则调用行为未定义（在 SPARK 中视为验证失败）。

**定义 C.2** (后置条件): 子程序 `P` 的后置条件 `Post(P)` 是一个布尔表达式，必须在 `P` 的每次成功返回后成立。`Post(P)` 可引用返回值（通过 `P'Result`）和调用前的状态（通过 `P'Old`）。

```ada
-- 计算爬升率的函数，含完整契约
function Calculate_Climb_Rate
  (Current_Altitude : Altitude_Feet;
   Target_Altitude  : Altitude_Feet;
   Time_To_Reach    : Positive_Seconds) return Feet_Per_Minute
  with
    Pre  => Current_Altitude <= Max_Altitude_Feet
            and then Target_Altitude <= Max_Altitude_Feet
            and then Time_To_Reach > 0,
    -- 前置条件：高度在合法范围内，时间必须为正

    Post => (if Target_Altitude > Current_Altitude then
               Calculate_Climb_Rate'Result > 0
             elsif Target_Altitude < Current_Altitude then
               Calculate_Climb_Rate'Result < 0
             else
               Calculate_Climb_Rate'Result = 0)
    -- 后置条件：目标高度高于当前高度时爬升率为正，反之为负，相等时为零
is
   Altitude_Delta : constant Feet := Target_Altitude - Current_Altitude;
begin
   return Feet_Per_Minute (Altitude_Delta / Integer (Time_To_Reach) * 60);
end Calculate_Climb_Rate;
```

上述代码中，`Pre` 确保输入处于物理合理区间，`Post` 确保输出符号与高度差方向一致。GNATprove 会自动生成验证条件（Verification Conditions, VC），交由 SMT 求解器（Alt-Ergo、Z3、CVC5）证明[^1]。

### 1.3 循环不变式（Loop Invariants）

**定义 C.3** (循环不变式): 循环不变式 `Inv(L)` 是附加在循环头部的布尔断言，满足：
1. **初始化**：循环首次迭代前，`Inv(L)` 成立；
2. **保持**：若在某次迭代开始时 `Inv(L)` 成立，则本次迭代结束后 `Inv(L)` 仍成立；
3. **退出**：循环终止时，`Inv(L)` 与循环条件的否定合取，可推出后置条件。

循环不变式是 SPARK 证明中最需要人工介入的部分，因为自动工具通常无法猜测程序员的意图。

```ada
-- 计算平均空速的循环，带不变式
function Average_Airspeed (Readings : Airspeed_Vector) return Knots
  with
    Pre  => Readings'Length > 0,
    Post => Average_Airspeed'Result >= 0.0
is
   Sum : Float := 0.0;
begin
   for I in Readings'Range loop
      pragma Loop_Invariant
        (Sum >= 0.0
         and then Sum <= Float (I - Readings'First) * Max_Airspeed_Knots);
      -- 循环不变式：累加和始终非负，且不超过已处理元素数乘以最大空速

      Sum := Sum + Float (Readings (I));
   end loop;

   return Knots (Sum / Float (Readings'Length));
end Average_Airspeed;
```

### 1.4 类型谓词（Type Predicates）

**定义 C.4** (动态谓词 `Dynamic_Predicate`): 类型 `T` 的动态谓词是一个布尔表达式，在 `T` 的每次赋值、参数传递、返回后被检查。若谓词不成立，则引发 `Assertion_Error`（运行时）或验证失败（证明时）。

**定义 C.5** (静态谓词 `Static_Predicate`): 仅允许在编译期可求值的表达式，用于定义类型的合法值集合。

```ada
-- 飞行模式类型，含静态谓词限定合法取值
subtype Flight_Mode is Mode_Type
  with Static_Predicate => Flight_Mode in Manual | Altitude_Hold | Heading_Select | Approach;

-- 高度类型，含动态谓词确保物理合理性
subtype Altitude_Feet is Integer
  with Dynamic_Predicate => Altitude_Feet in -1000 .. 55000;
-- 动态谓词：高度必须在海平面以下 1000 英尺至 FL550 之间

-- 非空航路点序列，用于 FMS 航迹计算
type Waypoint_Sequence is array (Positive range <>) of Waypoint
  with Dynamic_Predicate => Waypoint_Sequence'Length > 0;
```

类型谓词将数据不变量从子程序契约下沉到类型系统，使得任何违反物理约束的赋值在编译期或证明期即被发现，无需等待运行时测试。

### 1.5 数据依赖与信息流

**定义 C.6** (`Global` 子句): `Global` 显式声明子程序读写的外部状态（全局变量）。

**定义 C.7** (`Depends` 子句): `Depends` 显式声明输出的数据依赖关系，用于信息流分析和保密性/完整性验证。

```ada
procedure Update_Autopilot_State
  (New_Mode : in Flight_Mode;
   Success  : out Boolean)
  with
    Global  => (In_Out => Autopilot_State),
    -- 读写自动驾驶仪状态全局变量

    Depends => (Autopilot_State =>+ New_Mode,
                Success         => (Autopilot_State, New_Mode))
    -- 输出 Success 依赖于输入 New_Mode 和当前 Autopilot_State
    -- Autopilot_State 的输出依赖于其旧值和 New_Mode（=>+ 表示"基于自身旧值更新"）
is
   -- 实现省略
   Success := True;
end Update_Autopilot_State;
```

`Global` 和 `Depends` 使得 SPARK 能够进行**信息流分析**（Information Flow Analysis），验证高安全等级软件中的数据保密性（Confidentiality）和完整性（Integrity）属性，这是 DO-178C A 级软件的关键要求[^2]。

---

## 2. DO-178C / DO-333 合规路径

### 2.1 形式化方法作为测试替代

DO-178C / ED-12C（2012 发布）是民用航空软件适航审定的国际标准，其补充件 DO-333 / ED-216 专门定义了形式化方法（Formal Methods）作为测试的替代手段[^3]。在传统的 DO-178B 框架下，A 级软件需要满足**修正条件/判定覆盖（MC/DC）**，这是一项极其昂贵的测试活动。DO-333 允许在满足严格条件的前提下，用形式化证明替代部分或全部测试目标。

SPARK 的契约验证属于 DO-333 中的**演绎方法（Deductive Methods）**类别，与模型检验（Model Checking）和抽象解释（Abstract Interpretation）并列。Airbus 和 Dassault Aviation 已在多个民用飞机项目中成功使用 SPARK 证明替代单元测试，获得 EASA 和 FAA 的适航认可[^4]。

### 2.2 验证目标映射

DO-333 将形式化方法可替代的验证目标分为三类：

| DO-333 目标类别 | 具体目标 | SPARK 覆盖方式 |
|----------------|---------|---------------|
| 低级需求（LLR）| 准确性、一致性、可验证性 | 形式化契约精确表达 LLR，自动证明排除冲突 |
| 源代码 | 符合 LLR、数据依赖性、标准符合性 | `Pre`/`Post` 证明代码满足契约；`Global`/`Depends` 证明数据依赖 |
| 可执行目标代码 | 与源代码对应 | 编译器资格论证 + 契约作为运行时断言的集成测试 |

**关键原则**：SPARK 替代测试时，必须证明以下额外目标（DO-333 FM.A-7）：

1. 形式化规范（契约）正确且完整地捕获了低级需求；
2. 源代码正确实现了形式化规范；
3. 形式化方法工具链已按 DO-330 完成工具资格认定；
4. 未证明的部分仍需通过测试覆盖。

---

## 3. 飞行控制完整案例：自动驾驶仪模式切换与高度保持

本案例设计一个简化的自动驾驶仪（Autopilot, AP）模式管理系统，涵盖模式状态机、高度保持控制逻辑、以及襟翼控制互锁。该系统需满足 DO-178C A 级软件的验证要求。

### 3.1 系统需求与状态机

**需求 R.1** (模式互斥): 自动驾驶仪在任一时刻只能处于一种激活模式。

**需求 R.2** (高度保持范围): 高度保持模式仅能在当前高度处于 `[1000, 45000]` 英尺时激活。

**需求 R.3** (襟翼互锁): 当襟翼位置大于 20 度时，禁止进入 Approach 模式。

**需求 R.4** (平滑切换): 模式切换时，输出指令必须在 500 毫秒内从旧值连续过渡至新值，避免突变。

状态机：
```
Off ──[Pilot_ON]──> Manual
Manual ──[AP_Engage]──> Altitude_Hold / Heading_Select
Altitude_Hold ──[Mode_Select]──> Heading_Select / Approach / Manual
Heading_Select ──[Mode_Select]──> Altitude_Hold / Approach / Manual
Approach ──[Disengage]──> Manual
Any_Mode ──[Fault]──> Off
```

### 3.2 类型定义与契约设计

```ada
package Autopilot_Types with SPARK_Mode is

   -- 物理量类型定义，带动态谓词约束合法范围
   subtype Altitude_Feet is Integer range -1000 .. 55000;
   subtype Target_Altitude is Altitude_Feet
     with Dynamic_Predicate => Target_Altitude in 1000 .. 45000;
   -- 高度保持的目标高度必须在 1000 至 45000 英尺之间

   subtype Knots is Float range 0.0 .. 500.0;
   subtype Vertical_Speed_FPM is Integer range -8000 .. 8000;
   subtype Flap_Angle_Degrees is Integer range 0 .. 40;

   -- 自动驾驶仪模式枚举
   type AP_Mode is (Off, Manual, Altitude_Hold, Heading_Select, Approach);

   -- 模式切换请求，含静态谓词排除非法组合
   subtype Mode_Command is AP_Mode
     with Static_Predicate => Mode_Command /= Off;
   -- 飞行员不能直接请求 Off 模式，Off 仅由故障或系统断电触发

   -- 自动驾驶仪状态记录
   type AP_State is record
      Current_Mode     : AP_Mode;
      Target_Alt       : Target_Altitude;
      Current_Alt      : Altitude_Feet;
      Current_Vertical : Vertical_Speed_FPM;
      Flap_Position    : Flap_Angle_Degrees;
      Engaged          : Boolean;
   end record;

   -- 状态不变式：若未接通，则模式必须为 Off
   function State_Invariant (S : AP_State) return Boolean is
     (if not S.Engaged then S.Current_Mode = Off);

end Autopilot_Types;
```

### 3.3 模式切换逻辑

```ada
package body Autopilot_Mode_Logic with SPARK_Mode is

   -- 模式切换核心函数，含完整前置/后置条件和分情形契约
   function Compute_Next_Mode
     (Current_State : AP_State;
      Command       : Mode_Command;
      System_OK     : Boolean) return AP_Mode
   with
     Pre  => State_Invariant (Current_State)
             and then Current_State.Current_Alt in 0 .. 55000
             and then Current_State.Flap_Position in 0 .. 40,
     -- 前置条件：当前状态满足不变式，高度和襟翼在合法范围

     Post => Compute_Next_Mode'Result in AP_Mode'Range
             and then (if not System_OK then Compute_Next_Mode'Result = Off)
             and then (if Current_State.Flap_Position > 20 then
                         Compute_Next_Mode'Result /= Approach)
             and then (if Current_State.Current_Alt not in 1000 .. 45000 then
                         Compute_Next_Mode'Result /= Altitude_Hold),
     -- 后置条件：
     -- 1. 系统故障时必然进入 Off
     -- 2. 襟翼大于 20 度时禁止进入 Approach
     -- 3. 当前高度不在范围内时禁止进入 Altitude_Hold

     Contract_Cases =>
       (System_OK = False                 => Compute_Next_Mode'Result = Off,
        Current_State.Flap_Position > 20  => Compute_Next_Mode'Result /= Approach,
        Current_State.Current_Alt < 1000  => Compute_Next_Mode'Result /= Altitude_Hold,
        others                            => True)
     -- 分情形契约：穷尽所有互斥情形，便于 GNATprove 分别验证
   is
   begin
      if not System_OK then
         return Off;
      end if;

      if not Current_State.Engaged then
         return Off;
      end if;

      case Command is
         when Manual =>
            return Manual;

         when Altitude_Hold =>
            -- 运行时检查：若前置条件已验证，此分支必然安全
            if Current_State.Current_Alt in 1000 .. 45000 then
               return Altitude_Hold;
            else
               -- 降级到 Manual，保持当前姿态
               return Manual;
            end if;

         when Heading_Select =>
            return Heading_Select;

         when Approach =>
            if Current_State.Flap_Position <= 20 then
               return Approach;
            else
               -- 襟翼过大，拒绝进入 Approach，保持当前模式
               return Current_State.Current_Mode;
            end if;
      end case;
   end Compute_Next_Mode;

end Autopilot_Mode_Logic;
```

### 3.4 高度保持控制器

高度保持控制器（Altitude Hold Controller）是自动驾驶仪的核心功能之一。它根据当前高度与目标高度的偏差，计算垂直速度指令，使飞机平滑趋近目标高度。

```ada
package body Altitude_Hold_Controller with SPARK_Mode is

   -- 比例控制器增益（单位：英尺/分钟 / 英尺）
   Kp : constant Float := 2.0;
   Max_VS : constant := 1500;  -- 最大垂直速度限制（英尺/分钟）
   Min_VS : constant := -1500; -- 最小垂直速度限制

   -- 高度保持垂直速度指令计算
   function Compute_Vertical_Speed
     (Current_Alt : Altitude_Feet;
      Target_Alt  : Target_Altitude) return Vertical_Speed_FPM
   with
     Pre  => Current_Alt in -1000 .. 55000,
     Post => Compute_Vertical_Speed'Result in Min_VS .. Max_VS
             and then
             (if abs (Target_Alt - Current_Alt) < 50 then
                 abs (Compute_Vertical_Speed'Result) <= 100)
     -- 后置条件：
     -- 1. 输出在饱和限制内
     -- 2. 当高度差小于 50 英尺时，垂直速度限制在 100 英尺/分钟以内（捕获区）
   is
      Alt_Error : constant Float := Float (Target_Alt - Current_Alt);
      Raw_VS    : Float;
   begin
      Raw_VS := Alt_Error * Kp;

      -- 饱和限制
      if Raw_VS > Float (Max_VS) then
         Raw_VS := Float (Max_VS);
      elsif Raw_VS < Float (Min_VS) then
         Raw_VS := Float (Min_VS);
      end if;

      return Vertical_Speed_FPM (Raw_VS);
   end Compute_Vertical_Speed;

   -- 高度捕获判定：当飞机在目标高度 ±100 英尺内且垂直速度小于 200 英尺/分钟时，认为已捕获
   function Altitude_Captured
     (Current_Alt : Altitude_Feet;
      Target_Alt  : Target_Altitude;
      Current_VS  : Vertical_Speed_FPM) return Boolean
   with
     Post => Altitude_Captured'Result =
             (abs (Current_Alt - Target_Alt) <= 100
              and then abs (Current_VS) <= 200)
   is
   begin
      return abs (Current_Alt - Target_Alt) <= 100
             and then abs (Current_VS) <= 200;
   end Altitude_Captured;

   -- 多步高度跟踪模拟，验证收敛性
   procedure Simulate_Altitude_Tracking
     (Initial_Alt   : in     Altitude_Feet;
      Target_Alt    : in     Target_Altitude;
      Time_Steps    : in     Positive;
      Final_Alt     :    out Altitude_Feet;
      Alt_Captured  :    out Boolean)
   with
     Pre  => Time_Steps <= 1000,
     Post => abs (Final_Alt - Target_Alt) <= abs (Initial_Alt - Target_Alt)
             -- 最终高度误差不超过初始误差（不发散）
   is
      Alt  : Altitude_Feet := Initial_Alt;
      VS   : Vertical_Speed_FPM;
   begin
      for Step in 1 .. Time_Steps loop
         pragma Loop_Invariant
           (abs (Alt - Target_Alt) <= abs (Initial_Alt - Target_Alt));
         -- 循环不变式：每一步的高度误差都不超过初始误差

         VS := Compute_Vertical_Speed (Alt, Target_Alt);
         Alt := Altitude_Feet (Integer (Alt) + Integer (VS) / 60);
         -- 简化模型：每秒更新一次高度（VS 单位为英尺/分钟）

         exit when Altitude_Captured (Alt, Target_Alt, VS);
      end loop;

      Final_Alt    := Alt;
      Alt_Captured := Altitude_Captured (Alt, Target_Alt, VS);
   end Simulate_Altitude_Tracking;

end Altitude_Hold_Controller;
```

### 3.5 襟翼控制互锁

襟翼控制与自动驾驶仪模式之间存在严格的互锁关系。SPARK 的信息流分析可自动验证这些互锁不会被绕过。

```ada
package body Flap_Interlock with SPARK_Mode is

   -- 襟翼指令合法性检查
   function Valid_Flap_For_Mode
     (Flap_Cmd    : Flap_Angle_Degrees;
      Target_Mode : AP_Mode) return Boolean
   with
     Post => Valid_Flap_For_Mode'Result =
             (if Target_Mode = Approach then Flap_Cmd <= 20 else True)
     -- 后置条件：Approach 模式下襟翼指令不能超过 20 度
   is
   begin
      if Target_Mode = Approach then
         return Flap_Cmd <= 20;
      else
         return True;
      end if;
   end Valid_Flap_For_Mode;

   -- 同步更新襟翼和模式，确保互锁始终满足
   procedure Update_Flap_And_Mode
     (State    : in out AP_State;
      Flap_Cmd : in     Flap_Angle_Degrees;
      Mode_Cmd : in     Mode_Command)
   with
     Pre  => State_Invariant (State),
     Post => State_Invariant (State)
             and then Valid_Flap_For_Mode (State.Flap_Position, State.Current_Mode)
             and then State.Flap_Position <= 40
     -- 后置条件：更新后状态不变式保持，且襟翼-模式互锁满足
   is
      Proposed_Mode : AP_Mode;
   begin
      -- 先限制襟翼物理范围
      if Flap_Cmd > 40 then
         State.Flap_Position := 40;
      else
         State.Flap_Position := Flap_Cmd;
      end if;

      -- 根据当前襟翼位置计算可进入的模式
      Proposed_Mode := Compute_Next_Mode (State, Mode_Cmd, True);

      -- 若目标模式为 Approach 但襟翼过大，保持当前模式
      if Proposed_Mode = Approach and then State.Flap_Position > 20 then
         State.Current_Mode := State.Current_Mode;  -- 无变化
      else
         State.Current_Mode := Proposed_Mode;
      end if;
   end Update_Flap_And_Mode;

end Flap_Interlock;
```

---

## 4. 与 Rust 安全关键验证方法的对比

`07-formal-verification/04-rust-type-system/` 中详细介绍了 Rust 的类型系统、所有权模型及其形式化验证工具链（Kani、Prusti、Aeneas、RustBelt）。SPARK Ada 与 Rust 在安全关键软件开发中代表了两种不同但互补的形式化路径：

| 维度 | SPARK Ada | Rust |
|------|-----------|------|
| **安全模型** | 契约 + 演绎证明 | 所有权 + 借用检查 |
| **验证时机** | 编译期 + 独立证明工具链（GNATprove） | 编译期（rustc）+ 可选外部工具 |
| **内存安全** | 语言子集限制（无指针算术、无显式释放） | 所有权-借用-生命周期系统 |
| **算术安全** | 溢出检查、范围类型、谓词（自动证明） | 调试/释放模式运行时检查（`checked_add`） |
| **功能契约** | 原生支持 `Pre`/`Post`/`Contract_Cases` | 外部工具（Prusti `#[requires]`/`#[ensures]`） |
| **信息流** | 原生支持 `Global`/`Depends` | 无原生支持，需借助类型系统编码 |
| **工业适航** | DO-178C/DO-333 已认证（Airbus, Dassault） | 正在推进（FAA/EASA 尚在评估） |
| **代码生成** | Ada 代码可直接用于高安全等级产品 | Rust 需额外论证（`unsafe` 边界审查） |
| **并发验证** | Ravenscar Profile（确定性任务模型） | `Send`/`Sync` trait + 类型系统 |

**关键差异分析**：

1. **契约的原生性**：SPARK 的契约是语言一级特性，与编译器和证明器深度集成。Rust 的契约验证依赖外部工具（Prusti），尚未进入语言标准。这使得 SPARK 在适航审定中更易获得监管机构认可。

2. **算术安全**：SPARK 对整数溢出、数组越界等运行时错误的消除是**证明级**的——GNATprove 可生成"无溢出证明"作为适航证据。Rust 在 release 模式下默认不检查整数溢出（除非使用 `checked_add` 等显式 API），其算术安全更多依赖编程规范而非编译器强制。

3. **并发模型**：SPARK 的 Ravenscar Profile 提供了一个严格受限但完全可分析的任务模型，非常适合硬实时飞控软件。Rust 的并发安全通过所有权和类型系统实现，表达能力更强，但分析复杂度也更高，目前缺乏针对 DO-178C 的完整论证路径。

4. **复用策略**：Rust 的 crate 生态系统支持快速复用，但 `unsafe` 边界成为形式化安全性的黑洞（参见 `04-rust-type-system/unsafe-verification.md` 中的**定理 R.3**）。SPARK 的复用以**契约包（Contract Packages）**和**证明库（Proof Libraries）**为核心，复用组件自带可验证的数学保证，更适合高安全等级场景。

---

## 5. 复用价值与工业实践

### 5.1 合同级复用

SPARK 的契约设计使得安全关键组件的复用从"信任但验证"（Trust but Verify）升级为"证明即信任"（Proof as Trust）。具体模式包括：

- **通用合同模板**：排序、搜索、环形缓冲区等常见算法提供已验证的合同套件，新项目可直接实例化；
- **抽象数据类型（ADT）**：已验证的栈、队列、映射实现，带完整合同，复用时继承全部数学保证；
- **硬件抽象层（HAL）合同**：针对特定航电平台（如 PowerPC + VxWorks）的驱动程序合同，跨项目复用。

### 5.2 证明级复用

- **证明库（Proof Libraries）**：数学性质（算术、位操作、定点运算）的已证明引理集合；
- **Ghost 代码复用**：辅助证明的不可执行代码片段（如循环变体、辅助不变式），可在相似结构的证明中复用；
- **逐级证明策略（Cascading Proof）**：同一航空电子产品线中，低层组件的证明策略可直接应用于高层组件。

### 5.3 工具资格证据复用

DO-330 要求形式化验证工具链本身需经过资格认定。AdaCore SPARK Pro 的 Tool Qualification Package 已在多个项目中通过 FAA/EASA 审查，后续项目可直接引用已有证据，显著降低审定成本。

---

## 6. 权威来源

[^1]: AdaCore. *SPARK Pro — Introduction to Formal Verification with SPARK*. [https://www.adacore.com/about-spark](https://www.adacore.com/about-spark). 官方文档涵盖契约语法、证明工具链、工业案例。

[^2]: RTCA DO-178C / EUROCAE ED-12C. *Software Considerations in Airborne Systems and Equipment Certification*. RTCA Inc., 2012. 民用航空软件适航审定核心标准。

[^3]: RTCA DO-333 / EUROCAE ED-216. *Formal Methods Supplement to DO-178C and DO-278A*. RTCA Inc., 2012. 定义形式化方法替代测试的合规路径与额外目标。

[^4]: Moy, Y., Ledinot, E., Delseny, H., Wiels, V., & Monate, B. (2013). Testing or Formal Verification: DO-178C Alternatives and Industrial Experience. *IEEE Software*, 30(3), 50-57. 记录了 Airbus 和 Dassault Aviation 使用 SPARK 替代测试的工业经验。

[^5]: Barnes, J. (2014). *SPARK 2014: The SPARK Approach to Safety and Security*. AdaCore. SPARK 2014 语言参考与方法论权威著作。

---

> 最后更新: 2026-06-06
