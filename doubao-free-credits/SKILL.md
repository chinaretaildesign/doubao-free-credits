---
name: doubao-free-credits
display_name: 豆包免费积分助手
description: "豆包免费额度/积分领取与查询助手。汇总豆包 App、火山方舟、Seedance 视频、小云雀、即梦等字节系全部官方免费额度领取路径（每日免费次数、新用户 tokens、学生认证权益），一键生成个性化领取清单与每日播报；支持用火山方舟 API Key 查询账户 token 余额与免费额度状态。触发词：豆包积分、豆包免费额度、豆包额度、免费token、豆包会员、豆包学生认证、免费领豆包会员、Seedance 免费额度、视频生成免费次数、小云雀积分、即梦免费额度、火山方舟余额、方舟 token 余额、我的 token 够用吗、免费额度还有吗、领取豆包福利、字节系免费福利、帮我领豆包积分、豆包怎么免费用、AI 免费额度、AI 白嫖、字节系福利、今天有什么免费额度、免费额度提醒、每日额度播报。"
description_zh: "豆包免费积分助手：把豆包 App、火山方舟 API、Seedance 视频生成、小云雀、即梦等字节系官方免费额度路径整理成一份可执行的领取清单，按用户身份（学生 / 开发者 / 视频创作者）给出优先级和操作步骤；支持用火山方舟 API Key 实际查询账户 token 余额与免费额度状态；可配置每日提醒播报当日免费次数领取情况。所有信息来自字节官方公开活动与文档，不做任何破解、绕过验证或多账号刷取。"
description_en: "Doubao Free Credit Assistant: consolidates all official ByteDance free-credit paths (Doubao app, Volcano Ark API, Seedance video generation, Xiaoyunque, Dreamina) into an executable claim checklist, prioritized by user profile (student / developer / video creator). Supports querying real Ark token balance and free-quota status with an API key, and can be wired to a daily reminder that reports unclaimed free generations. All data comes from official ByteDance public campaigns and docs — no cracking, no verification bypass, no multi-account abuse."
category: automation
version: 1.1.0
author: workbuddy
agent_created: true
visibility: public
license: MIT-0
metadata:
  openclaw:
    emoji: "🫘"
    requires:
      bins:
        - python3
      env:
        - ARK_API_KEY
allowed-tools: Bash
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

### 步骤 3 · 每日播报（可选，需用户明确同意）

生成当日播报内容：

```bash
python scripts/daily_brief.py --profile creator      # 学生 / 开发者 / 创作者 / 全量
python scripts/daily_brief.py --profile all --balance # 附带查方舟余额（只读）
python scripts/daily_brief.py --json                 # 结构化输出
```

播报按**过期时效**分两组：

- **⏰ 今日有效** —— 当日清零、不累计。豆包 Seedance、即梦、小云雀都属这类，提醒的核心价值是「今天不用就浪费」
- **📌 长期有效** —— 按活动周期或当月清零的额度。方舟 tokens、学生会员属这类

**不要默认开启定时任务。** 仅当用户明确说「每天提醒我领豆包免费次数」时，用 `automation_update` 创建每日任务，prompt 写：

> 运行 doubao-free-credits 技能，执行 `python scripts/daily_brief.py --profile <用户画像>`，把「⏰ 今日有效」分组的内容播报给我，并强调这些额度当日清零。同时提示三个通用规则：免费额度通常需手动领取、只对指定模型生效、同手机号跨平台额度不叠加。

推荐时间：**上午 9 点**。Seedance 和即梦的额度都是 0 点刷新、深夜领了大概率用不上，所以早上提醒最有效。

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

- `@references/claim-channels.md` — 各渠道完整领取步骤与官方链接（维护数据只改这个文件）
- `@references/api-spec.md` — 方舟余额查询接口说明与错误码
- `@scripts/claim_guide.py` — 生成领取清单（渠道数据的唯一来源，其他脚本从此导入）
- `@scripts/ark_balance.py` — 查询方舟 token 余额（只读）
- `@scripts/daily_brief.py` — 每日播报，按 `expires` 字段区分当日清零与长期有效

---

## 六、渠道数据结构

`claim_guide.py` 的 `CHANNELS` 里每个渠道含一个 `expires` 字段，播报逻辑依赖它：

| 值 | 含义 | 归属分组 |
|---|---|---|
| `daily` | 当日清零，不累计 | ⏰ 今日有效 |
| `cycle` | 按活动周期清零 | 📌 长期有效 |
| `month` | 当月清零 | 📌 长期有效 |
| `long` | 按活动期（通常覆盖学期） | 📌 长期有效 |

新增渠道时**必须填 `expires`**，否则播报会漏掉它。

---

## 七、维护约定

官方活动规则变动频繁。更新数据时**只改** `references/claim-channels.md` 与 `claim_guide.py` 的 `CHANNELS` 列表，并在 `claim-channels.md` 顶部记录 `最后核验日期`，让用户一眼看出信息新鲜度。