#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成豆包 / 字节系官方免费额度领取清单（只读，无网络请求）。"""

import argparse
import json
import sys

CHANNELS = [
    {
        "id": "doubao_seedance",
        "name": "豆包 App · Seedance 2.0 每日免费次数",
        "value": "约 10 次视频生成/日",
        "entry": "豆包 App（V7.2+）或 doubao.com → 创作 → AI 视频",
        "url": "https://www.doubao.com/",
        "require": "登录个人账号，无需实名",
        "validity": "当日有效，0 点刷新不累计",
        "profiles": ["creator", "student", "developer"],
        "priority": 1,
        "pitfall": "额度仅限 Seedance 2.0；换模型直接扣账户余额。部分场景需在「我的 → 我的权益」手动领取。",
    },
    {
        "id": "dreamina",
        "name": "即梦 Dreamina · 每日免费次数",
        "value": "约 5 次视频生成/日",
        "entry": "dreamina.jianying.com 登录剪映账号 → 视频生成",
        "url": "https://dreamina.jianying.com/",
        "require": "剪映/即梦账号",
        "validity": "每日自动刷新",
        "profiles": ["creator", "student"],
        "priority": 2,
        "pitfall": "与其他渠道额度不冲突，可叠加。",
    },
    {
        "id": "xiaoyunque",
        "name": "小云雀 · 新用户次数 + 每日积分",
        "value": "新用户约 3 次 + 每日约 130 积分（10 积分 ≈ 1 次 Seedance-fast 生成）",
        "entry": "xiaoyunque.volcengine.com 注册 + 实名认证",
        "url": "https://xiaoyunque.volcengine.com/",
        "require": "注册并完成实名认证",
        "validity": "当日有效，过期清零",
        "profiles": ["creator", "developer"],
        "priority": 3,
        "pitfall": "积分当日不用就作废，别攒着。查看路径：个人中心 → 我的权益。",
    },
    {
        "id": "ark_gateway",
        "name": "火山方舟 · 网关密钥免费 tokens",
        "value": "约 200 万 tokens，关联新模型可扩至 500 万 / 1000 万",
        "entry": "console.volcengine.com/vei/aigateway → 创建网关访问密钥 → 关联 doubao-seed-1.6 系列",
        "url": "https://console.volcengine.com/vei/aigateway/overview",
        "require": "火山引擎账号，无需绑卡、无需预充值",
        "validity": "按活动周期，跨周期可能清零",
        "profiles": ["developer"],
        "priority": 1,
        "pitfall": "扩容需在火山配额中心提交 ai-gateway-token-limit 申请，说明密钥 ID 与目标额度。",
    },
    {
        "id": "ark_seedance_fast",
        "name": "火山方舟 · Seedance-fast 新用户赠送",
        "value": "约 50 个生成 tokens",
        "entry": "火山引擎智能创作云 → Seedance 2.0-fast，完成个人实名认证",
        "url": "https://console.volcengine.com/spr/iark/overview",
        "require": "实名认证；部分情况需余额充值满 200 元开通试用",
        "validity": "通常当月",
        "profiles": ["creator", "developer"],
        "priority": 4,
        "pitfall": "用过智能创作云其他试用的老账号不属于新用户，领不到。",
    },
    {
        "id": "doubao_student",
        "name": "豆包电脑版 · 学生认证订阅",
        "value": "约 3 个月电脑版订阅会员",
        "entry": "doubao.com/download/desktop 安装客户端 → 客户端内完成学生认证",
        "url": "https://www.doubao.com/download/desktop",
        "require": "中国大陆高校全日制在读大专 / 本科 / 研究生",
        "validity": "按活动期，通常覆盖学期",
        "profiles": ["student"],
        "priority": 1,
        "pitfall": "认证必须在电脑客户端内发起，移动端网页不支持。认准 3 个月标准订阅。",
    },
]

PROFILE_LABEL = {
    "student": "学生",
    "developer": "开发者（API 优先）",
    "creator": "视频 / 图像创作者",
    "all": "全量",
}


def pick(profile):
    if profile == "all":
        return sorted(CHANNELS, key=lambda c: c["priority"])
    return sorted(
        [c for c in CHANNELS if profile in c["profiles"]],
        key=lambda c: c["priority"],
    )


def render_md(profile, items):
    lines = []
    lines.append(f"# 豆包免费额度领取清单 · {PROFILE_LABEL.get(profile, profile)}")
    lines.append("")
    lines.append("> 数据来自字节官方公开活动与文档（最后核验 2026-10-15）。数值为官方口径，")
    lines.append("> 活动可能随时调整，请以页面实际显示为准。")
    lines.append("")
    for i, c in enumerate(items, 1):
        lines.append(f"## {i}. {c['name']}")
        lines.append(f"- **额度**：{c['value']}")
        lines.append(f"- **入口**：{c['entry']}")
        lines.append(f"- **链接**：{c['url']}")
        lines.append(f"- **前置条件**：{c['require']}")
        lines.append(f"- **有效期**：{c['validity']}")
        lines.append(f"- **注意**：{c['pitfall']}")
        lines.append("")
    lines.append("## 通用规则")
    lines.append("- 同一手机号在豆包 / 火山 / 小云雀的免费额度会合并计算，不叠加。")
    lines.append("- 赠送额度通常只对特定模型生效，且多为当日或当月清零。")
    lines.append("- 豆包 App 与即梦的额度彼此独立，可叠加使用。")
    lines.append("")
    lines.append("---")
    lines.append("查方舟 token 余额：`python scripts/ark_balance.py`（需配置 ARK_API_KEY）")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="生成豆包免费额度领取清单")
    ap.add_argument(
        "--profile",
        default="all",
        choices=["student", "developer", "creator", "all"],
        help="用户身份画像",
    )
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    items = pick(args.profile)
    if args.json:
        print(json.dumps({"profile": args.profile, "channels": items}, ensure_ascii=False, indent=2))
    else:
        print(render_md(args.profile, items))
    return 0


if __name__ == "__main__":
    sys.exit(main())