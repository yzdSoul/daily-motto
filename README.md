# 📜 每日格言 · Daily Motto Web

一个精美的中英文格言 Web 应用，支持每日格言推荐、分类浏览、全文搜索和 REST API。

## ✨ 功能特色

- 🎯 **每日格言** — 每天不同，自动更新
- 🎲 **随机格言** — 一键刷新，总有惊喜
- 📂 **分类浏览** — 哲理智慧、励志奋斗、人生态度、读书学习、英文智慧
- 🔍 **全文搜索** — 支持中文、英文、作者、分类搜索
- 📋 **一键复制** — 点击格言即可复制分享
- 📱 **响应式设计** — 手机、平板、桌面都好看
- 🌙 **暗色主题** — 护眼美观
- 🔌 **REST API** — 方便二次开发

## 🚀 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 打开浏览器访问
# http://localhost:5000
```

## 📡 REST API

| 接口 | 说明 |
|------|------|
| `GET /api/random` | 获取随机格言 |
| `GET /api/daily` | 获取每日格言 |
| `GET /api/all` | 获取全部格言 (支持 `?category=哲理智慧`) |
| `GET /api/search?q=关键词` | 搜索格言 |
| `GET /api/categories` | 获取所有分类和数量 |

示例：

```bash
curl http://localhost:5000/api/daily
curl "http://localhost:5000/api/search?q=千里之行"
curl "http://localhost:5000/api/all?category=英文智慧"
```

## 🛠 技术栈

- **后端**: Python Flask
- **前端**: 原生 HTML/CSS/JS
- **设计**: 暗色主题 · 毛玻璃效果 · 响应式布局
- **字体**: Noto Serif SC (中文) + Inter (英文)

## 🗂 项目结构

```
daily-motto-web/
├── app.py              # Flask 主程序 + API
├── quotes.py           # 格言数据 (24条精选)
├── requirements.txt    # 依赖
├── README.md          # 说明文档
├── templates/
│   ├── index.html     # 首页 (每日+随机)
│   ├── all.html       # 全部格言 (分类筛选)
│   └── search.html    # 搜索页面
└── static/
    ├── style.css      # 样式
    └── app.js         # 交互逻辑
```

## 📄 许可

MIT
