#!/usr/bin/env python3
"""
standard-tracker-dashboard.py
=============================

标准状态可视化看板（Streamlit）。

用法:
    streamlit run struct/99-reference/tools/standard-tracker-dashboard.py

功能:
- 读取 standard-tracker-snapshot.json 与 standard-status-snapshot.json
- 展示各标准链接健康度、状态、预期发布时间
- 按健康状态筛选
- 显示趋势告警（若存在缓存）

"""

import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TRACKER_SNAPSHOT = PROJECT_ROOT / "struct" / "99-reference" / "tools" / "standard-tracker-snapshot.json"
STATUS_SNAPSHOT = PROJECT_ROOT / "reports" / "standard-status-snapshot.json"


def load_json(path: Path) -> dict:
    """加载 JSON 文件，若不存在则返回空字典。"""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        st.error(f"读取 {path} 失败: {e}")
        return {}


def health_badge(reachable: bool) -> str:
    return "🟢 可达" if reachable else "🔴 不可达"


def status_badge(status: str) -> str:
    mapping = {
        "正常": "🟢",
        "重定向": "🟡",
        "失效或受限": "🔴",
        "无法访问": "⚫",
        "网络受限，需人工复核": "🟠",
    }
    return f"{mapping.get(status, '⚪')} {status}"


def main():
    st.set_page_config(page_title="标准状态看板", layout="wide")
    st.title("📡 国际标准与权威来源状态看板")
    st.caption("数据来源: standard-tracker-snapshot.json / standard-status-snapshot.json")

    tracker_snapshot = load_json(TRACKER_SNAPSHOT)
    status_snapshot = load_json(STATUS_SNAPSHOT)

    generated_at = tracker_snapshot.get("generated_at") or status_snapshot.get("generated_at")
    if generated_at:
        st.write(f"**快照时间**: {generated_at}")
    else:
        st.warning("未找到快照文件。请先运行以下脚本生成快照：")
        st.code("python struct/99-reference/tools/standard-tracker.py --snapshot\npython scripts/standard-status-checker.py")
        return

    # Tracker 数据
    tracker_standards = tracker_snapshot.get("standards", [])
    total = len(tracker_standards)
    reachable = sum(1 for s in tracker_standards if s.get("status_url_check", {}).get("reachable"))

    # 摘要指标
    col1, col2, col3 = st.columns(3)
    col1.metric("监控标准总数", total)
    col2.metric("可达", reachable)
    col3.metric("不可达", total - reachable)

    # 筛选器
    st.divider()
    st.subheader("🔍 筛选")
    filter_status = st.multiselect(
        "健康状态",
        options=["全部", "可达", "不可达"],
        default=["全部"],
    )

    # 标准列表
    st.divider()
    st.subheader("📋 标准跟踪列表")

    for std in tracker_standards:
        url_ok = std.get("status_url_check", {}).get("reachable", False)
        if "全部" not in filter_status:
            if "可达" in filter_status and not url_ok:
                continue
            if "不可达" in filter_status and url_ok:
                continue

        with st.expander(f"{std['name']} — {health_badge(url_ok)}"):
            st.write(f"**当前状态**: {std.get('current_status', '—')}")
            st.write(f"**预期发布**: {std.get('expected_release', '—')}")
            st.write(f"**发布后的行动**: {std.get('action_on_release', '—')}")
            st.write(f"**状态页**: [{std.get('status_url', '')}]({std.get('status_url', '')})")
            if std.get("rss_url"):
                st.write(f"**RSS/Atom**: [{std['rss_url']}]({std['rss_url']})")
            if std.get("mailing_list"):
                st.write(f"**讨论列表**: {std['mailing_list']}")

    # 权威来源索引状态（若存在）
    status_items = status_snapshot.get("items", [])
    if status_items:
        st.divider()
        st.subheader("📚 权威来源索引复核状态")
        counts = {}
        for item in status_items:
            counts[item.get("check_status", "未知")] = counts.get(item.get("check_status", "未知"), 0) + 1
        st.write(counts)

        filter_idx = st.multiselect(
            "检测结果",
            options=["全部"] + list(counts.keys()),
            default=["全部"],
        )

        for item in status_items:
            status = item.get("check_status", "未知")
            if "全部" not in filter_idx and status not in filter_idx:
                continue
            with st.expander(f"{item.get('name', '—')} — {status_badge(status)}"):
                st.write(f"**版本**: {item.get('version', '—')}")
                st.write(f"**状态**: {item.get('status', '—')}")
                st.write(f"**URL**: [{item.get('url', '')}]({item.get('url', '')})")
                http_status = item.get("http_status")
                if http_status:
                    st.write(f"**HTTP 状态**: {http_status}")
                if item.get("final_url"):
                    st.write(f"**最终 URL**: {item['final_url']}")
                if item.get("error"):
                    st.write(f"**错误**: {item['error']}")

    st.divider()
    st.caption("由 standard-tracker-dashboard.py 生成 | 最后刷新: " + datetime.now(timezone.utc).isoformat())


if __name__ == "__main__":
    main()
