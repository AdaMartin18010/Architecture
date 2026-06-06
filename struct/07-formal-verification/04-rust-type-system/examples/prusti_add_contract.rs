// Prusti 演绎验证示例：简单的 requires/ensures 合约
// 运行: prusti-rustc prusti_add_contract.rs
// 需要先安装 Prusti 工具链

#[cfg(feature = "prusti")]
use prusti_contracts::*;

#[cfg(feature = "prusti")]
#[requires(a > 0 && b > 0)]
#[ensures(result == a + b)]
fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(feature = "prusti")]
fn main() {
    assert_eq!(add(2, 3), 5);
}

#[cfg(not(feature = "prusti"))]
fn main() {
    println!("Prusti verification requires feature 'prusti' enabled.");
}
