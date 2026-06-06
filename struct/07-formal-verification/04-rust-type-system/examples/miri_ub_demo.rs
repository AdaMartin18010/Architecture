// Miri UB 检测示例
// 运行: rustup run nightly cargo miri test --test miri_ub_demo

pub fn buggy_write(x: &mut [u8]) {
    unsafe {
        let p = x.as_mut_ptr();
        // 当 x.len() < 11 时触发越界 UB
        *p.add(10) = 1;
    }
}

pub fn safe_write(x: &mut [u8]) {
    if let Some(v) = x.get_mut(10) {
        *v = 1;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_buggy_may_ub() {
        let mut buf = vec![0u8; 11];
        buggy_write(&mut buf);
        assert_eq!(buf[10], 1);
    }

    #[test]
    fn test_safe_ok() {
        let mut buf = vec![0u8; 5];
        safe_write(&mut buf);
        // 不会 panic，只是无操作
    }
}
