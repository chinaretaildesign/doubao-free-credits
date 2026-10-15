#!/usr/bin/env bash
# 一键推送脚本：在 GitHub 建好空仓库后，把地址填到下面这行再运行
#
# 用法：
#   1. 浏览器打开 https://github.com/new 建仓（名字填 doubao-free-credits，Public，不要勾 README）
#   2. 把仓库 HTTPS 地址填到下方 REPO_URL 变量（不含结尾 .git 也可）
#   3. 双击运行本文件，或在 Git Bash 执行：bash push_to_github.sh

REPO_URL="https://github.com/chinaretaildesign/doubao-free-credits.git"

if [ -z "$REPO_URL" ]; then
  echo "请先把下方 REPO_URL 改成你真实的仓库地址。"
  exit 1
fi

cd "$(dirname "$0")" || exit 1

echo ">> 当前仓库状态"
git log --oneline

if git remote get-url origin >/dev/null 2>&1; then
  echo ">> origin 已存在，更新为：$REPO_URL"
  git remote set-url origin "$REPO_URL"
else
  echo ">> 添加远端：$REPO_URL"
  git remote add origin "$REPO_URL"
fi

echo ">> 推送 master 分支"
git push -u origin master

echo ""
echo "推送完成。接下来："
echo "1. 打开仓库页面确认文件都在"
echo "2. Releases → Draft a new release，tag填 v1.0.0"
echo "3. 上传附件 D:/WorkBuddy/outputs/doubao-free-credits-1.0.0.zip"
echo "4. 发布到WorkBuddy 技能市场：https://open.workbuddy.cn/docs/skill"