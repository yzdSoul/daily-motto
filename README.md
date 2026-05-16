---
title: 📜 每日格言
emoji: 📜
colorFrom: yellow
colorTo: amber
sdk: docker
app_port: 7860
---

# 📜 每日格言 · Daily Motto Web

一个精美的中英文格言 Web 应用，支持每日格言推荐、分类浏览、全文搜索和 REST API。

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/F8TZks?referralCode=your-code)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yzdSoul/daily-motto)
[![Deploy to Hugging Face](https://huggingface.co/datasets/huggingface/badges/raw/main/deploy-to-spaces-lg.svg)](https://huggingface.co/spaces)

## ✨ 功能特色

- 🎯 **每日格言** — 每天不同，自动更新
- 🎲 **随机格言** — 一键刷新，总有惊喜
- 📂 **分类浏览** — 哲理智慧、励志奋斗、人生态度、读书学习、英文智慧
- 🔍 **全文搜索** — 支持中文、英文、作者、分类搜索
- 📋 **一键复制** — 点击格言即可复制分享
- 📱 **响应式设计** — 手机、平板、桌面都好看
- 🌙 **暗色主题** — 护眼美观
- 🔌 **REST API** — 方便二次开发

## 🚀 快速启动（本地）

```bash
pip install -r requirements.txt
python app.py
# 访问 http://localhost:5000
```

## 🌐 免费部署指南

### 方案一：Hugging Face Spaces（推荐 · 无绑卡）

> [Hugging Face Spaces](https://huggingface.co/spaces) 完全免费，无需绑卡，国内可访问。

1. 打开 https://huggingface.co 注册账号
2. 点击右上角头像 → **New Space**
3. 填写：
   - **Space Name**: `daily-motto`
   - **License**: MIT
   - **Space SDK**: **Docker**
4. 点击 **Create Space**
5. 在 Space 页面选择 **Add file** → **Import from repo**
6. 输入仓库地址：`https://github.com/yzdSoul/daily-motto`
7. 等待自动构建（约 1-2 分钟）
8. ✅ 完成！你的格言网站就上线了！

### 方案二：Render（免费 · 可能需要验证手机）

1. 打开 https://render.com 注册
2. 点击 **New +** → **Web Service**
3. 连接 GitHub 仓库 `yzdSoul/daily-motto`
4. 填写：
   - **Name**: `daily-motto`
   - **Region**: 选最近的（Singapore 或 Oregon）
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. 选择 **Free** 计划
6. 点击 **Create Web Service**
7. ✅ 几分钟后就上线了！

### 方案三：Railway（免费 $5/月 · 需绑卡验证）

1. 打开 https://railway.app 注册
2. 点击 **New Project** → **Deploy from GitHub repo**
3. 选择 `yzdSoul/daily-motto`
4. 在 **Settings** 中将 Start Command 设为 `gunicorn app:app`
5. Railway 自动检测 Dockerfile 部署
6. ✅ 自动分配免费域名

### 方案四：PythonAnywhere（免费 · 无需绑卡）

1. 打开 https://www.pythonanywhere.com 注册免费账号
2. 打开 **Dashboard** → **Web** → **Add a new web app**
3. 选择 **Manual configuration** → **Python 3.11**
4. 在 **Code** 部分：
   - **Source code**: `/home/你的用户名/daily-motto-web`
   - **Working directory**: 同上
   - **WSGI configuration file**: 点击编辑，参考下方配置
5. 打开 **Bash Console** 克隆项目：
   ```bash
   git clone https://github.com/yzdSoul/daily-motto
   cd daily-motto
   pip install -r requirements.txt
   ```
6. 编辑 WSGI 文件：
   ```python
   import sys
   path = '/home/你的用户名/daily-motto'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```
7. 点击 **Reload** ✅

## 📡 REST API

| 接口 | 说明 |
|------|------|
| `GET /api/random` | 获取随机格言 |
| `GET /api/daily` | 获取每日格言 |
| `GET /api/all` | 获取全部格言 (支持 `?category=哲理智慧`) |
| `GET /api/search?q=关键词` | 搜索格言 |
| `GET /api/categories` | 获取所有分类和数量 |

## 🛠 技术栈

- **后端**: Python Flask + Gunicorn
- **前端**: 原生 HTML/CSS/JS
- **设计**: 暗色主题 · 毛玻璃效果 · 响应式布局
- **部署**: Docker 容器化，支持任意平台

## 🗂 项目结构

```
daily-motto-web/
├── app.py              # Flask 主程序 + API
├── quotes.py           # 格言数据 (24条精选)
├── requirements.txt    # Flask + Gunicorn
├── Dockerfile          # 容器化部署
├── README.md           # 说明文档
├── templates/
│   ├── index.html     # 首页 (每日+随机)
│   ├── all.html       # 全部格言 (分类筛选)
│   └── search.html    # 搜索页面
└── static/
    ├── style.css      # 暗色主题样式
    └── app.js         # 交互逻辑
```

## 📄 许可

MIT
