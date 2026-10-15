#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查询火山方舟账户信息 / Key 有效性（只读，不消耗 token）。

凭据优先级：--key > 环境变量 ARK_API_KEY > ~/.workbuddy/doubao-ark-key.json
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://ark.cn-beijing.volces.com/api/v3/users/me"
CRED_FILE = os.path.join(
    os.path.expanduser("~"), ".workbuddy", "doubao-ark-key.json"
)


def mask(key):
    if not key or len(key) < 10:
        return "(未设置)"
    return f"{key[:4]}...{key[-4:]}"


def load_key(explicit):
    if explicit:
        return explicit, "命令行参数"
    env = os.environ.get("ARK_API_KEY")
    if env:
        return env, "环境变量 ARK_API_KEY"
    if os.path.exists(CRED_FILE):
        try:
            with open(CRED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            key = data.get("api_key")
            if key:
                return key, CRED_FILE
        except (OSError, ValueError):
            return None, CRED_FILE
    return None, None


def query(key, timeout):
    req = urllib.request.Request(
        API, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        return e.code, body
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser(description="查询火山方舟账户信息（只读）")
    ap.add_argument("--key", help="方舟 API Key（不推荐，优先用环境变量）")
    ap.add_argument("--timeout", type=int, default=15, help="超时秒数")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    key, source = load_key(args.key)
    if not key:
        msg = (
            "未找到方舟 API Key。任选一种方式配置：\n"
            "  1) 环境变量：export ARK_API_KEY=你的Key"
            "（PowerShell：$env:ARK_API_KEY=\"你的Key\"）\n"
            "  2) 凭据文件：~/.workbuddy/doubao-ark-key.json，内容 {\"api_key\": \"你的Key\"}\n"
            "Key 获取路径：火山方舟控制台 → API Key 管理。\n"
            "未配置时不会返回任何额度数字。"
        )
        if args.json:
            print(json.dumps({"ok": False, "reason": "missing_api_key"}, ensure_ascii=False, indent=2))
        else:
            print(msg)
        return 2

    status, data = query(key, args.timeout)

    if status == 200:
        payload = {
            "ok": True,
            "key_masked": mask(key),
            "key_source": source,
            "account": data,
            "note": "赠送额度剩余量以控制台「资源管理」页面为准，接口不直接返回。",
            "console": "https://console.volcengine.com/vei/aigateway/overview",
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"✓ Key 有效（{mask(key)}，来源：{source}）")
            acc = data if isinstance(data, dict) else {}
            for k in ("id", "name", "email"):
                if k in acc:
                    print(f"  {k}: {acc[k]}")
            print(f"\n提示：{payload['note']}")
            print(f"  查看入口：{payload['console']}")
        return 0

    reason = {401: "API Key 无效或已过期", 403: "权限不足，可能未完成实名认证"}.get(status)
    if reason is None:
        reason = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
    if args.json:
        print(json.dumps({"ok": False, "http": status, "reason": reason}, ensure_ascii=False, indent=2))
    else:
        print(f"✗ 查询失败（HTTP {status}）：{reason}")
    return 1


if __name__ == "__main__":
    sys.exit(main())