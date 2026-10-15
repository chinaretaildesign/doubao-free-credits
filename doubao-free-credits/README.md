# 豆包免费积分助手（doubao-free-credits）

把散落在豆包 App、火山方舟、Seedance、小云雀、即梦各处的**官方免费额度**收拢成一张清单，按你的身份排出优先级，并告诉你每一笔钱具体怎么领、什么时候过期、会不会误扣余额。

一个 WorkBuddy Skill，纯 Python 标准库，无第三方依赖。

## 功能

1. **生成领取清单**：按身份画像（学生 / 开发者 / 视频创作者 / 全量）输出 6 个官方渠道的领取步骤，含入口、前置条件、有效期与踩坑提示。
2. **查询方舟账户**：用火山方舟 API Key 调用官方只读接口 `GET /api/v3/users/me` 校验 Key 与账户信息，不消耗任何额度。
3. **每日提醒（可选）**：配合 WorkBuddy 定时任务，每天播报当日仍可领取的免费次数。

## 免费额度地图

| 渠道 | 能拿什么 | 大致量级 | 有效期 |
|---|---|---|---|
| 豆包 App · Seedance 2.0 视频 | 每日免费生成次数 | 约 10 次/日 | 当日 |
| 即梦 Dreamina | 每日免费生成次数 | 约 5 次/日 | 当日 |
| 小云雀 | 新用户次数 + 每日通用积分 | 约 3 次 + 130 积分/日 | 当日 |
| 火山方舟 · 网关密钥 | 新用户免费 tokens | 200 万起，可扩至 1000 万 | 按活动周期 |
| 豆包电脑版 · 学生 | 订阅会员 | 约 3 个月 | 按活动期 |
| 方舟 Seedance-fast | 新用户赠送 tokens | 约 50 个生成 tokens | 通常当月 |

> 数值为官方公开活动口径，可能随时调整，以页面实际显示为准。

## 安装

**方式一：直接放入技能目录**

```bash
git clone <this-repo> doubao-free-credits
# 放入 ~/.workbuddy/skills/ 目录后重启 WorkBuddy
```

Windows 用户目录为 `C:\Users\<用户名>\.workbuddy\skills\`。

**方式二：解压 ZIP**

下载发行包 `doubao-free-credits-1.0.0.zip`，解压后把 `doubao-free-credits/` 整个文件夹放进 `~/.workbuddy/skills/`。

## 使用

在 WorkBuddy 对话中直接说：

- 「豆包免费额度有哪些」
- 「帮我领豆包积分」
- 「我的方舟 token 还剩多少」

也可在终端手动运行：

```bash
# 生成领取清单
python scripts/claim_guide.py --profile student      # student / developer / creator / all
python scripts/claim_guide.py --profile developer --json

# 查询方舟账户（只读）
export ARK_API_KEY=你的Key          # PowerShell: $env:ARK_API_KEY="你的Key"
python scripts/ark_balance.py
```

API Key 也可落盘到 `~/.workbuddy/doubao-ark-key.json`：

```json
{ "api_key": "你的Key" }
```

## 三个必知的坑

1. **免费额度通常不会自动到账**。豆包 App 需手动点「我的」→「我的权益」→「领取今日免费额度」；火山方舟需在「资源管理」点「领取新用户免费额度」。跳过这步会直接扣账户余额。
2. **额度有模型和时效限制**。多数赠送额度只对特定模型生效，且当日或当月清零。选错模型直接走付费。
3. **同手机号跨平台额度会合并**。豆包 / 火山 / 小云雀用同一手机号注册时，身份信息视为同一人，额度不叠加。

## 合规边界

本技能只整理并指引**官方公开活动**的领取路径。不做协议逆向或破解、不用多手机号批量注册刷取新用户额度、不用他人身份做学生认证。未配置 API Key 时脚本明确报错退出，不伪造任何数字。

## 目录结构

```
doubao-free-credits/
├── SKILL.md                          # 技能定义（必须）
├── README.md                         # 说明文档
├── references/
│   ├── claim-channels.md             # 各渠道完整领取步骤与官方链接
│   └── api-spec.md                   # 方舟查询接口说明与错误码
└── scripts/
    ├── claim_guide.py                # 生成领取清单
    └── ark_balance.py                # 查询方舟账户（只读）
```

## 环境要求

- Python 3.8+（仅标准库，无需 pip 安装）
- 可选：火山方舟 API Key（仅余额查询功能需要）

## 安全说明

`ark_balance.py` 仅调用官方只读接口，不调用任何生成接口，不会消耗额度；输出中 API Key 仅显示前 4 位与后 4 位；除读取环境变量与可选的本地凭据文件外，不写任何文件。

## License

MIT-0