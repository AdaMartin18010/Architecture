// Verus 功能正确性证明示例
// 此为 Verus 方言，不能直接用 cargo/rustc 编译；
// 需通过 verus 命令验证：
//   verus verus_add_proof.rs --crate-type=lib
//
// 安装：git clone https://github.com/verus-lang/verus.git
//       cd verus/source && ./tools/get-z3.sh && source ../tools/activate && vargo build --release

#[cfg(verus_keep_ghost)]
use vstd::prelude::*;

#[cfg(verus_keep_ghost)]
verus! {

fn add(a: u32, b: u32) -> (c: u32)
    requires
        a <= 0xffff_ffff - b,
    ensures
        c == a + b,
{
    a + b
}

} // verus!
