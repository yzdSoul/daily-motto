# 📜 每日格言 · 项目档案

## 🌐 项目概况

| 项目 | 信息 |
|------|------|
| **项目名称** | daily-motto · 每日格言 |
| **项目类型** | Flask Web 应用（中英文格言浏览与搜索） |
| **GitHub 仓库** | [github.com/yzdSoul/daily-motto](https://github.com/yzdSoul/daily-motto) |
| **在线地址** | [yzdsoul-daily-motto.hf.space](https://yzdsoul-daily-motto.hf.space) |
| **部署平台** | Hugging Face Spaces（Docker） |
| **费用** | ✅ 完全免费，无需绑卡 |
| **语言** | Python 3 + Flask |
| **本地路径** | `~/projects/daily-motto-web/` |

## ✨ 功能清单

| 功能 | 说明 |
|------|------|
| 🎯 每日格言 | 每天自动更新，不同格言 |
| 🎲 随机格言 | 一键刷新 |
| 📂 分类浏览 | 5 个分类：哲理智慧、励志奋斗、人生态度、读书学习、英文智慧 |
| 🔍 全文搜索 | 支持中英文、作者、分类搜索 |
| 📋 一键复制 | 点击格言即可复制 |
| 🌙 暗色主题 | 毛玻璃效果，响应式布局 |
| 🔌 REST API | 5 个接口 |

## 📦 技术栈

| 层级 | 技术 |
|:----|:------|
| **后端** | Flask + Gunicorn |
| **前端** | 原生 HTML/CSS/JS |
| **字体** | Noto Serif SC（中文）+ Inter（英文） |
| **部署** | Docker 容器化 |

## 🗂 项目结构

```
daily-motto-web/
├── app.py              # Flask 主程序 + 5个API
├── quotes.py           # 24条精选格言 + 数据查询
├── requirements.txt    # Flask + Gunicorn
├── Dockerfile          # 容器化部署
├── README.md           # 说明文档（含部署指南）
├── .gitignore
├── templates/
│   ├── index.html     # 首页
│   ├── all.html       # 分类浏览
│   └── search.html    # 搜索
└── static/
    ├── style.css      # 暗色主题
    └── app.js         # 交互逻辑
```

## 🚀 本地运行

```bash
cd ~/projects/daily-motto-web
pip install -r requirements.txt
python app.py
# 访问 http://localhost:5000
```

## 🔌 REST API 接口

| 方法 | 接口 | 说明 | 参数 |
|:----|:-----|:------|:-----|
| GET | `/api/random` | 随机格言 | - |
| GET | `/api/daily` | 每日格言 | - |
| GET | `/api/all` | 全部格言 | `?category=分类名` |
| GET | `/api/search?q=` | 搜索 | `?q=关键词` |
| GET | `/api/categories` | 分类统计 | - |

## 📌 部署记录

| 平台 | 状态 | 链接 |
|:----|:----|:-----|
| Hugging Face Spaces | ✅ 已部署 | [yzdsoul-daily-motto.hf.space](https://yzdsoul-daily-motto.hf.space) |
| GitHub | ✅ 已推送 | [yzdSoul/daily-motto](https://github.com/yzdSoul/daily-motto) |

## 🛠 备用部署方案

| 平台 | 费用 | 绑卡？ | 说明 |
|:----|:----|:-------|:-----|
| 🤗 Hugging Face | 免费 | ❌ 不用 | ✅ 已部署 |
| 🎨 Render | 免费 | ⚠️ 需验证 | 连接 GitHub 选 Free 计划 |
| 🚂 Railway | $5/月额度 | ⚠️ 需绑卡 | 自动检测 Dockerfile |
| 🐍 PythonAnywhere | 免费 | ❌ 不用 | Bash 克隆 + WSGI 配置 |
