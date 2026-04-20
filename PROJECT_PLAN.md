# Markdown Sharer - 项目开发计划

## 项目背景

产品经理兼职工作中，因无法加入对方公司飞书，每次 MD 文档需通过微信手动传输，效率低且不便。本项目旨在搭建一个可私有部署的 Markdown 文档分享平台。

---

## 核心功能

| 功能模块 | 描述 |
|---------|------|
| **文档编辑** | 在线编写 + 实时预览 Markdown |
| **文档管理** | 保存、查看、修改、删除文档 |
| **链接分享** | 生成唯一链接分享给指定用户 |
| **访客查看** | 无需登录，通过链接查看文档 |
| **文档下载** | 访客可下载 MD 文件 |

---

## 技术方案（已确认）

### 前端
- **框架**: Vue 3 + Vite
- **Markdown 编辑器**: Vditor（功能全面，支持实时预览）
- **Markdown 渲染**: markdown-it
- **样式**: TailwindCSS
- **HTTP 客户端**: Axios

### 后端
- **框架**: FastAPI（Python）
- **数据库**: SQLite（轻量，单文件，易于备份）
- **ORM**: SQLAlchemy
- **存储**: 本地文件系统

### 部署
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **服务器**: 腾讯云轻量服务器 (CentOS)

---

## 数据模型设计

### 文档表 (documents)
| 字段 | 类型 | 描述 |
|------|------|------|
| id | String (UUID) | 主键 |
| title | String | 文档标题 |
| content | Text | Markdown 内容 |
| share_token | String | 分享令牌（唯一，用于生成链接） |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| expires_at | DateTime | 分享过期时间（创建后 7 天） |

---

## API 设计

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/documents | 创建文档 |
| GET | /api/documents | 获取文档列表 |
| GET | /api/documents/:id | 获取文档详情 |
| PUT | /api/documents/:id | 更新文档 |
| DELETE | /api/documents/:id | 删除文档 |
| POST | /api/documents/:id/share | 生成分享链接 |
| GET | /share/:token | 访客查看文档（检查过期） |
| GET | /share/:token/download | 访客下载文档（检查过期） |

> 分享链接有效期：7 天，过期后访问返回 410 Gone

---

## 开发任务清单

### 阶段一：项目初始化
- [ ] 创建项目目录结构
- [ ] 初始化前端项目（Vue 3 + Vite）
- [ ] 初始化后端项目（FastAPI）
- [ ] 配置数据库连接（SQLite + SQLAlchemy）

### 阶段二：后端 API 开发
- [ ] 定义数据模型（Document）
- [ ] 实现文档 CRUD 接口
  - [ ] POST /api/documents - 创建文档
  - [ ] GET /api/documents - 获取文档列表
  - [ ] GET /api/documents/:id - 获取文档详情
  - [ ] PUT /api/documents/:id - 更新文档
  - [ ] DELETE /api/documents/:id - 删除文档
- [ ] 实现分享功能接口
  - [ ] POST /api/documents/:id/share - 生成分享链接
  - [ ] GET /share/:token - 访客查看（含过期检查）
  - [ ] GET /share/:token/download - 访客下载（含过期检查）

### 阶段三：前端页面开发
- [ ] 编辑器页面
  - [ ] 集成 Vditor 编辑器
  - [ ] 实时预览功能
  - [ ] 保存/更新文档
- [ ] 文档列表页面
  - [ ] 展示所有文档
  - [ ] 编辑/删除操作
  - [ ] 生成分享链接
- [ ] 访客查看页面
  - [ ] Markdown 渲染展示
  - [ ] 过期提示
  - [ ] 下载按钮

### 阶段四：部署配置
- [ ] 编写前端 Dockerfile
- [ ] 编写后端 Dockerfile
- [ ] 编写 docker-compose.yml
- [ ] 配置 Nginx 反向代理
- [ ] 样式美化与响应式适配

---

## 项目结构

```
markdown-sharer/
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── views/          # 页面
│   │   ├── api/            # API 请求
│   │   └── ...
│   ├── Dockerfile
│   └── ...
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── main.py         # 入口
│   │   ├── models.py       # 数据模型
│   │   ├── schemas.py      # Pydantic 模型
│   │   ├── crud.py         # 数据库操作
│   │   └── database.py     # 数据库连接
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── nginx.conf
└── README.md
```

---

## 后续可扩展功能

- [ ] 文档分类/标签
- [ ] 文档版本历史
- [ ] 分享链接访问统计
- [ ] 批量导出
- [ ] 暗色主题
