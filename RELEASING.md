# 发布指南：doubao-free-credits

本文档给维护者，说明怎么把这个 Skill 上架到 GitHub 和 WorkBuddy 技能市场。
**用户只需阅读 README.md**，本文件是给要发版的人看的。

---

## 一、当前状态

- 版本：1.0.0
- Git 提交：已初始化（`D:\WorkBuddy\tmp\doubao-skill-publish`）
- 远端：**未配置**（需你自行创建仓库后推送）
- 发布包：`D:\WorkBuddy\outputs\doubao-free-credits-1.0.0.zip`（13.3 KB，7 个文件）

---

## 二、发布到 GitHub

### 1. 本地已就绪

```bash
cd /d/WorkBuddy/tmp/doubao-skill-publish
git log --oneline        # 确认提交存在
```

### 2. 创建远端仓库

在 https://github.com/new 建仓，建议：

- 仓库名：`doubao-free-credits`
- 仓库描述：豆包 / 火山方舟 / Seedance / 小云雀 / 即梦 官方免费额度领取清单助手（WorkBuddy Skill）
- 可见性：Public
- 不要勾选 "Add a README"（本地已有）

### 3. 推送

```bash
cd /d/WorkBuddy/tmp/doubao-skill-publish
git remote add origin https://github.com/<你的用户名>/doubao-free-credits.git
git push -u origin master
```

未安装 `gh` CLI 时也可以用网页方式：打开仓库 → Add file → Upload files，把
`doubao-free-credits/` 目录里的文件拖上去。

### 4. 打 Release

仓库页 → Releases → Draft a new release：

- Tag：`v1.0.0`
- 标题：`doubao-free-credits v1.0.0`
- 附件：`D:\WorkBuddy\outputs\doubao-free-credits-1.0.0.zip`

这样别人既能用 git clone，也能直接下 ZIP。

---

## 三、发布到 WorkBuddy 技能市场

### 提交入口

- 开放平台：https://open.workbuddy.cn/docs/skill
- 技能市场：WorkBuddy 客户端 →【专家·技能·连接器】→【技能】
- 创建入口：技能市场右上角【添加技能】→【创建技能】

### 提交材料清单

| 项目 | 要求 | 本Skill 的值 |
|---|---|---|
| 技能名称 | ≤20 字，简洁 | 豆包免费积分助手（9 字）✓ |
| 技能描述 | 100–300 字 | 见 SKILL.md `description_zh` ✓ |
| 图标 | 512×512 PNG | **需另做**，见第五节 |
| 分类标签 | 平台已有分类 | 建议「办公效率」或「开发工具」 |
| 权限声明 | 列出所需权限 | `allowed-tools: Bash`；可选 `ARK_API_KEY` |
| 使用说明 | 可选，推荐 | README.md ✓ |
| 技能包 | ZIP，根目录为`{skill-name}/` | `doubao-free-credits-1.0.0.zip` ✓ |

### 审核要点（官方规范）

- `SKILL.md` 必须存在，YAML frontmatter 必填 `description`、`description_zh`、
  `description_en`、`version`、`author`
- ZIP 内根目录必须是 `{skill-name}/`，且与 frontmatter的 `name` 字段**完全一致**
- 只用规范内字段，不要自造。发布版已移除本地版的 `metadata` / `visibility` /
  `agent_created` / `category` 等非规范字段
- 目录结构仅允许 `SKILL.md`、`references/`、`scripts/`、`templates/`

> 本技能当前目录结构完全符合：SKILL.md + references/（2 个 md）+ scripts/（2 个 py）
> + README.md + .gitignore。

审核周期通常 1–3 个工作日，检查安全性、稳定性、合规性。
解析失败可邮件联系 openworkbuddy@tencent.com。

---

## 四、版本迭代

改完数据或脚本后：

```bash
cd /d/WorkBuddy/tmp/doubao-skill-publish/doubao-free-credits
# 1. 同步改 SKILL.md 里的 version
# 2. 更新 references/claim-channels.md 顶部的「最后核验日期」
cd /d/WorkBuddy/tmp/doubao-skill-publish
# 3. 提交
git add -A && git commit -m "chore: bump to 1.1.0"
# 4. 重打包
cd doubao-free-credits && python -c "
import zipfile,pathlib
files=[p for p in pathlib.Path('.').rglob('*') if p.is_file() and '__pycache__' not in str(p)]
with zipfile.ZipFile('D:/WorkBuddy/outputs/doubao-free-credits-1.1.0.zip','w',zipfile.ZIP_DEFLATED) as z:
    [z.write(p,p.as_posix()) for p in files]
print('ok',len(files))"
```

**唯一需要长期维护的数据源是 `references/claim-channels.md`**，
所有免费额度数值都集中在这一个文件，改它就够了。

---

## 五、待补：512×512 图标

市场提交要求 512×512 PNG 图标。当前尚未制作。生成方式：

用 WorkBuddy 的图像生成能力，prompt 参考：

```
扁平矢量风格图标，暖橙渐变背景，中央一只白色陶瓷豆荚形状的容器，
内部溢出金色光点象征积分/额度，简洁几何线条，无文字，
512x512，居中构图，柔和阴影
```

生成后保存为 `doubao-free-credits/icon.png`，并在 SKILL.md 里补`_icon.png`
（本地安装时客户端会读取该文件作为菜单图标）。

---

## 六、合规自查清单

发布前逐项确认：

- [x] 只使用官方公开活动路径，无协议逆向
- [x] 无多账号批量注册刷额度逻辑
- [x] 无绕过实名/学生认证的实现
- [x] API Key 仅从环境变量或本地文件读取，不硬编码
- [x] 输出中Key 仅脱敏显示前 4 后 4
- [x] 所有网络调用为只读（`GET /api/v3/users/me`）
- [x] 不写用户文件，除可选的本地凭据读取
- [x] 额度数值标注「以官方页面为准」，不承诺固定值

审核最容易卡在两条：**allowed-tools 权限范围**和**外部网络请求声明**。
本技能只申请 `Bash` 且只调一个官方只读接口，属于最小权限。