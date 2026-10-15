---
name: doubao-free-credits
display_name: 豆包免费积分助手
description: "豆包免费额度/积分领取与查询助手。汇总豆包 App、火山方舟、Seedance 视频、小云雀、即梦等字节系全部官方免费额度领取路径（每日免费次数、新用户 tokens、学生认证权益），一键生成个性化领取清单与操作指引；支持用火山方舟 API Key 查询账户剩余 token 余额与免费额度状态。支持配置每日提醒自动播报「今天还有多少免费次数没领」。触发词：豆包积分、豆包免费额度、豆包额度、免费token、豆包会员、豆包学生认证、免费领豆包会员、Seedance 免费额度、视频生成免费次数、小云雀积分、即梦免费额度、火山方舟余额、方舟 token 余额、我的 token 够用吗、免费额度还有吗、领取豆包福利、字节系免费福利、帮我领豆包积分、豆包怎么免费用。"
description_zh: "豆包免费积分助手：把豆包 App、火山方舟 API、Seedance 视频生成、小云雀、即梦等字节系官方免费额度路径整理成一份可执行的领取清单，按用户身份（学生 / 开发者 / 视频创作者）给出优先级和操作步骤；支持用火山方舟 API Key 实际查询账户 token 余额与免费额度状态；可配置每日提醒播报当日免费次数领取情况。所有信息来自字节官方公开活动与文档，不做任何破解、绕过验证或多账号刷取。"
description_en: "Doubao Free Credit Assistant: consolidates all official ByteDance free-credit paths (Doubao app, Volcano Ark API, Seedance video generation, Xiaoyunque, Dreamina) into an executable claim checklist, prioritized by user profile (student / developer / video creator). Supports querying real Ark token balance and free-quota status with an API key, and can be wired to a daily reminder that reports unclaimed free generations. All data comes from official ByteDance public campaigns and docs — no cracking, no verification bypass, no multi-account abuse."
version: 1.0.0
author: workbuddy
display_name_en: Doubao Free Credit Assistant
allowed-tools: Bash
license: MIT-0
---

# 豆包免费积分助手（免费额度领取 + 余额查询）

把散落在豆包 App、火山方舟、Seedance、小云雀、即梦各处的**官方免费额度**收拢成一张清单，按你的身份排出优先级，并告诉你每一笔钱具体怎么领、什么时候过期、会不会误扣余额。

> **合规边界（硬性）**：本技能只整理并执行**官方公开活动**的领取路径。绝不破解签名/逆向客户端协议、绝不用多手机号批量注册刷新用户额度、绝不用他人身份做学生认证。若某项活动已被官方取消或收回，脚本会如实标注「已核验下线」，不伪造额度。

---

## 一、何时使用（触发条件）

- 「豆包积分 / 豆包免费额度 / 免费 token / 豆包会员免费领 / 豆包学生认证」
- 「我的方舟 token 还剩多少 / 免费额度还有吗 / 够用吗」
- 「Seedance / 视频生成 免费次数 / 小云雀积分 / 即梦免费额度」
- 「字节系有什么免费福利 / 怎么免费用豆包」

---

## 二、三步走

### 步骤 1 · 生成领取清单（默认动作）

```bash
python scripts/claim_guide.py --profile student      # 学生
python scripts/claim_guide.py --profile developer    # 开发者（API 优先）
python scripts/claim_guide.py --profile creator      # 视频/图像创作者
python scripts/claim_guide.py --profile all          # 全量清单 + JSON
```

输出为一份 Markdown 清单：每项含「额度内容 / 领取入口 / 前置条件 / 有效期 / 常见踩坑」。支持 `--json` 输出结构化数据。

### 步骤 2 · 查余额（有 API Key 才可执行）

```bash
export ARK_API_KEY=你的方舟API_KEY        # Windows PowerShell: $env:ARK_API_KEY="..."
python scripts/ark_balance.py             # 查询账户与免费额度状态
python scripts/ark_balance.py --json
```

查询走方舟官方只读接口 `GET https://ark.cn-beijing.volces.com/api/v3/users/me`，**只读**、不消耗 token、不打印 Key 本身（仅显示前 4 后 4 位）。

若未配置 Key，脚本会输出明确的配置指引并以退出码 2 结束，**不伪造任何数字**。

### 步骤 3 · 每日提醒（可选，需用户明确同意）

不要默认开启。当用户说「每天提醒我领豆包免费次数」时，用 `automation_update` 建一个每日任务，prompt 写：

> 读取 doubao-free-credits 技能的 references/claim-channels.md，播报今天仍可领取的官方免费额度项（豆包 Seedance 每日次数、即梦每日次数、小云雀当日积分），并提示这些额度当日有效、过期清零。若已配置 ARK_API_KEY，附带查询到的 token 余额。

---

## 三、免费额度地图（速查）

| 渠道 | 能拿什么 | 大致量级 | 入口 |有效期 |
|---|---|---|---|---|
| 豆包 App · Seedance 2.0 视频 | 每日免费生成次数 | 约 10 次/日 | App「创作」→「AI 视频」 | 当日 |
| 即梦 Dreamina | 每日免费生成次数 | 约 5 次/日 | dreamina.jianying.com | 当日 |
| 小云雀 | 新用户次数 + 每日通用积分 | 约 3 次 + 130 积分/日 | xiaoyunque.volcengine.com | 当日 |
| 火山方舟 · 网关密钥 | 新用户免费 tokens | 200 万起，扩至 500–1000 万 | console.volcengine.com/vei/aigateway | 按活动周期 |
| 豆包电脑版 · 学生 | 订阅会员 | 约 3 个月 | doubao.com/download/desktop 客户端内认证 | 学期内 |
| 火山方舟 Seedance-fast | 新用户赠送 tokens | 约 50 个生成 tokens | 智能创作云 | 当月 |

> 具体数值随官方活动变动，脚本每次运行会提示「以官方页面为准」，不写死为承诺。

---

## 四、必读的三个踩坑

1. **免费额度通常不会自动到账**：豆包 App 需手动点「我的」→「我的权益」→「领取今日免费额度」；方舟需在「资源管理」点「领取新用户免费额度」。跳过这步就直接扣账户余额。
2. **额度有模型/时效限制**：多数赠送额度只对特定模型（如 Seedance-2.0-mini）生效，且**当月或当日清零**。选错模型会直接走付费。
3. **同手机号跨平台额度会合并**：豆包 / 火山 / 小云雀用同一手机号注册时，身份信息视为同一人，免费额度不叠加。想叠加只能换真实身份——不要用他人信息。

---

## 五、文件说明

- `@references/claim-channels.md` — 各渠道完整领取步骤与官方链接（脚本与每日提醒都会读它）
- `@references/api-spec.md` — 方舟余额查询接口说明与错误码
- `@scripts/claim_guide.py` — 生成领取清单
- `@scripts/ark_balance.py` — 查询方舟 token 余额（只读）

---

## 六、维护约定

官方活动规则变动频繁。更新数据时**只改** `references/claim-channels.md` 中的条目，并在该文件顶部记录 `最后核验日期`，让用户一眼看出信息新鲜度。