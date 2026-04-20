# Markdown Sharer

一个简单的 Markdown 文档分享工具，支持在线编辑和生成分享链接。

## 功能

- 在线编写和预览 Markdown 文档
- 文档管理（创建、编辑、删除）
- 生成分享链接，有效期 7 天
- 访客无需登录即可查看和下载文档

## 本地开发

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

## Docker 部署

```bash
docker-compose up -d --build
```

访问 http://localhost

## 目录结构

```
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── main.py    # 入口文件
│   │   ├── models.py  # 数据模型
│   │   ├── schemas.py # Pydantic 模型
│   │   ├── crud.py    # 数据库操作
│   │   └── database.py
│   └── Dockerfile
├── frontend/          # Vue 3 前端
│   ├── src/
│   │   ├── views/     # 页面组件
│   │   ├── api/       # API 请求
│   │   └── router/    # 路由配置
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```
