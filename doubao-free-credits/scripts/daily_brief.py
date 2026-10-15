#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「今日免费额度播报」——供每日定时任务调用。

只读本地数据，不消耗任何额度，不发送网络请求（除可选的方舟余额查询）。
"""

import argparse
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from claim_guide import CHANNELS, PROFILE_LABEL, pick  # noqa: E402


def daily_items():
    """当日有效的免费额度项（这些最需要当天用掉）。"""
    return [c for c in CHANNELS if c.get("expires") == "daily"]


def evergreen_items():
    """长期有效的额度项（方舟 tokens、学生会员等）。"""
    return [c for c in CHANNELS if c.get("expires") in ("cycle", "month", "long")]


def render_text(profile):
    today = daily_items()
    ever = evergreen_items()
    chosen = {c["id"] for c in pick(profile)} if profile != "all" else None

    def keep(items):
        return [c for c in items if chosen is None or c["id"] in chosen]

    today, ever = keep(today), keep(ever)

    L = []
    L.append("【今日免费额度播报】")
    L.append("")
    if today:
        L.append(f"⏰ 今日有效（过期清零，今天不用就浪费）")
        for c in today:
            L.append(f"  · {c['name'].split('·')[0].strip()}：{c['value']}")
            L.append(f"    入口：{c['entry']}")
        L.append("")
    if ever:
        L.append("📌 长期有效（不急，但别忘了额度限制）")
        for c in ever:
            L.append(f"  · {c['name'].split('·')[0].strip()}：{c['value']}")
        L.append("")
    L.append("三个提醒：")
    L.append("  1. 免费额度通常要手动领，豆包在「我的 → 我的权益 → 领取今日免费额度」")
    L.append("  2. 额度只对指定模型生效，选错模型直接扣账户余额")
    L.append("  3. 同手机号跨平台额度合并计算，不叠加")
    return "\n".join(L)


def render_md(profile, balance):
    today, ever = daily_items(), evergreen_items()
    chosen = {c["id"] for c in pick(profile)} if profile != "all" else None
    if chosen:
        today = [c for c in today if c["id"] in chosen]
        ever = [c for c in ever if c["id"] in chosen]

    L = [f"# 今日免费额度播报 · {PROFILE_LABEL.get(profile, profile)}", ""]

    if balance and balance.get("ok"):
        L.append("**方舟账户**：Key 有效，详见控制台资源管理页")
        L.append("")
    elif balance and balance.get("reason") == "missing_api_key":
        L.append("**方舟账户**：未配置 API Key，跳过余额查询")
        L.append("")

    L.append("## ⏰ 今日有效（过期清零）")
    L.append("")
    if today:
        for c in today:
            L.append(f"- **{c['name'].split('·')[0].strip()}** — {c['value']}")
            L.append(f"  - 入口：{c['entry']}")
            L.append(f"  - 注意：{c['pitfall']}")
    else:
        L.append("- 无")
    L.append("")

    L.append("## 📌 长期有效")
    L.append("")
    if ever:
        for c in ever:
            L.append(f"- **{c['name'].split('·')[0].strip()}** — {c['value']}")
            L.append(f"  - 入口：{c['entry']}")
    else:
        L.append("- 无")
    L.append("")

    L.append("---")
    L.append("")
    L.append("通用规则：同手机号跨平台额度合并；赠送额度限特定模型且多为当日/当月清零；选错模型直接扣余额。")
    return "\n".join(L)


def query_balance(timeout):
    """可选：查询方舟账户。未配置 Key 时返回 None，不报错。"""
    try:
        import ark_balance
    except ImportError:
        return None
    if not (os.environ.get("ARK_API_KEY") or os.path.exists(ark_balance.CRED_FILE)):
        return {"ok": False, "reason": "missing_api_key"}
    import io as _io
    import contextlib
    buf = _io.StringIO()
    old_argv = sys.argv
    try:
        sys.argv = ["ark_balance.py", "--json", "--timeout", str(timeout)]
        with contextlib.redirect_stdout(buf):
            ark_balance.main()
    except SystemExit:
        pass
    finally:
        sys.argv = old_argv
    try:
        return json.loads(buf.getvalue())
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description="今日免费额度播报")
    ap.add_argument(
        "--profile",
        default="all",
        choices=["student", "developer", "creator", "all"],
        help="身份画像",
    )
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--balance", action="store_true", help="附带查询方舟余额（只读）")
    ap.add_argument("--timeout", type=int, default=15)
    args = ap.parse_args()

    balance = query_balance(args.timeout) if args.balance else None

    if args.json:
        payload = {
            "profile": args.profile,
            "daily": [c["id"] for c in daily_items()],
            "evergreen": [c["id"] for c in evergreen_items()],
            "balance": balance,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_md(args.profile, balance))
    return 0


if __name__ == "__main__":
    sys.exit(main())