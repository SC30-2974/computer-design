# 新能源财报智能分析平台

一个围绕新能源企业财报场景搭建的前后端项目，覆盖行业看板、企业详情、指标对比、报告导出、PDF 上传解析和问答能力。当前仓库采用 `Vue 3 + Vite` 前端、`FastAPI` 后端、`SQLite` 本地数据存储，并保留了可选的在线 RAG 能力。

## 项目亮点

- 宏观行业大屏：按赛道聚合企业营收，展示样本总量、总营收和平均毛利率。
- 财务指标对比：支持营收、净利润、毛利率横向对比，并提供多企业“对战模式”。
- 企业详情页：展示企业评分卡、财务诊断、经营摘要、样本均值对比和季度趋势线。
- 智能研判室：通过嵌入式 Dify 聊天页提供问答入口。
- 财报上传：支持上传 PDF、记录上传历史，并触发解析入库。
- 报告导出：支持导出多企业对比文本报告和打印式 PDF。
- 本地兜底：即使后端不可用，前端也内置一份示例数据，便于演示和联调。

## 技术栈

### 前端

- Vue 3
- Vite
- TypeScript
- Tailwind CSS
- ECharts
- Axios

### 后端

- FastAPI
- Uvicorn
- SQLite
- pdfplumber
- LangChain / Chroma / OpenAI（可选，用于在线 RAG）

## 当前业务范围

项目目前围绕 `2025 年前三季度` 新能源企业财报数据组织界面和默认样本，内置的主要企业包括：

- 比亚迪
- 宁德时代
- 阳光电源
- 隆基绿能
- 通威股份
- 恩捷股份
- 亿纬锂能

如果 PDF 解析未命中规则，系统会自动回退到这批整理好的样例数据，保证前端页面不会空白。

## 运行架构

```text
frontend (Vue + Vite)
  ├─ 本地开发时运行在 5173
  ├─ 生产构建输出到 frontend/dist
  └─ GitHub Pages 仅部署前端静态产物

backend (FastAPI)
  ├─ 提供 /api/* 接口
  ├─ 读取 data/finance_app.db
  ├─ 负责 PDF 上传、解析入库、报告生成、财务诊断
  └─ 可选接入 OpenAI + Chroma 做在线 RAG

data
  ├─ raw/                原始 PDF 与 latest_pdf_path.txt
  ├─ uploads/            已上传 PDF
  ├─ finance_app.db      主业务数据库
  └─ chroma_db/          向量库目录（启用在线 RAG 时使用）
```

## 目录结构

```text
computer-design/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ db.py
│  │  ├─ rag_engine.py
│  │  ├─ schemas.py
│  │  └─ services/
│  └─ scripts/
│     ├─ init_db.py
│     └─ sync_data.py
├─ frontend/
│  ├─ src/
│  │  ├─ api/
│  │  ├─ components/
│  │  ├─ layouts/
│  │  ├─ router/
│  │  └─ views/
│  ├─ dist/
│  ├─ package.json
│  └─ vite.config.ts
├─ data/
├─ .github/workflows/deploy-pages.yml
├─ Dockerfile
├─ requirements.txt
├─ run.bat
└─ README.md
```

## 环境要求

- Python `3.10+` 推荐
- Node.js `18+` 推荐
- npm `9+` 或更高版本

说明：

- GitHub Pages 工作流使用的是 `Node.js 22`
- `Dockerfile` 基于 `python:3.10-slim`

## 本地快速启动

推荐按“后端 8010 + 前端 5173”的方式启动，这和当前前端默认本地 API 配置一致，最省事。

### 1. 安装后端依赖

```powershell
cd D:\computer-design
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. 初始化数据库

```powershell
cd D:\computer-design
.\.venv\Scripts\python.exe backend\scripts\init_db.py
```

这一步会：

- 创建 `data/finance_app.db`
- 创建 `uploads` 等数据表
- 尝试从 `data/raw/各企业2025年财报数据.pdf` 提取数据
- 如果提取失败，则回退为仓库内置样例数据

### 3. 启动后端

```powershell
cd D:\computer-design
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8010
```

启动后可访问健康检查：

```text
http://127.0.0.1:8010/api/health
```

### 4. 启动前端

新开一个终端：

```powershell
cd D:\computer-design\frontend
npm install
npm run dev
```

然后打开：

```text
http://127.0.0.1:5173
```

## Windows 一键脚本

仓库提供了 `run.bat`：

```bat
cd /d D:\computer-design
.\run.bat
```

它会自动：

- 创建 `.venv`
- 安装 Python 依赖
- 启动 FastAPI

注意：

- 当前 `run.bat` 默认把后端启动在 `8000` 端口
- 当前前端本地默认请求的是 `http://127.0.0.1:8010`

如果你想直接使用当前前端零配置联调，建议仍然手动把后端启动在 `8010`。如果坚持使用 `8000`，请为前端配置 `VITE_API_BASE_URL=http://127.0.0.1:8000`。

## 前端页面说明

前端主要页面如下：

- `/home`：平台欢迎页和功能入口
- `/dashboard`：宏观行业大屏
- `/agent-room`：智能研判室（Dify iframe）
- `/financial-analysis`：财务指标对比与企业对战
- `/enterprise-detail`：企业详情与财务诊断
- `/data-upload`：财报 PDF 上传与刷新

## 数据导入与刷新

### 默认数据来源

- `data/raw/各企业2025年财报数据.pdf`
- `backend/scripts/init_db.py` 中整理好的兜底样例

### 上传新 PDF

可以通过页面 `数据上传` 使用，也可以调用接口：

- `POST /api/knowledge/upload`
- `POST /api/data/refresh`

当前刷新逻辑会：

- 读取最新上传的 PDF 路径
- 尝试解析企业、营收、净利润、毛利率等字段
- 合并进 `company_metrics`
- 更新前端图表所依赖的数据表

## RAG 能力说明

项目已经包含 `rag_engine.py`，但默认是“本地回退模式”，不开箱即用地依赖在线模型。

### 默认行为

- `ENABLE_ONLINE_RAG` 未设置为 `1` 时，`/api/rag/ask` 会走本地回退逻辑
- 本地回退会基于 `finance_app.db` 中的企业数据组织回答
- 这种模式不需要 OpenAI Key，也适合离线演示

### 开启在线 RAG 需要的环境变量

| 变量名 | 用途 | 是否必需 |
| --- | --- | --- |
| `ENABLE_ONLINE_RAG` | 设为 `1` 后启用在线检索问答 | 是 |
| `OPENAI_API_KEY` | OpenAI API Key | 是 |
| `OPENAI_BASE_URL` | 兼容代理或中转地址 | 否 |
| `EMBEDDING_MODEL` | 向量模型，默认 `text-embedding-3-small` | 否 |
| `LLM_MODEL` | 对话模型，默认 `gpt-4o-mini` | 否 |

### 重建向量库

```powershell
curl -X POST http://127.0.0.1:8010/api/rag/rebuild
```

说明：

- 向量库构建目录为 `data/chroma_db`
- 当前 `/api/data/refresh` 主要负责“解析入库”，不会自动重建在线向量库
- 如果你启用了在线 RAG，建议在更新底层 PDF 后手动调用一次 `/api/rag/rebuild`

## 生产部署

### GitHub Pages

仓库已提供工作流：

- 文件：`.github/workflows/deploy-pages.yml`
- 触发条件：推送到 `main`
- 构建目录：`frontend/dist`

部署 GitHub Pages 时，请在仓库变量里配置：

```text
VITE_API_BASE_URL=https://你的后端服务地址
```

因为 GitHub Pages 只托管前端静态资源，不会运行 FastAPI。

### Docker 部署后端

```powershell
cd D:\computer-design
docker build -t computer-design-api .
docker run -p 8000:8000 computer-design-api
```

容器启动后默认监听：

```text
http://127.0.0.1:8000
```

## 核心接口

### 基础接口

- `GET /api/health`
- `GET /api/sectors`
- `GET /api/companies`
- `GET /api/metrics?metric=revenue|profit|margin&sector=&period=前三季度`
- `GET /api/financial_diagnosis/{company_name}`
- `GET /api/company-battle?companies=比亚迪,宁德时代&period=前三季度`

### 报告与问答

- `POST /api/report`
- `POST /api/report/compare`
- `POST /api/rag/ask`
- `POST /api/rag/rebuild`

示例：

```json
{
  "company": "宁德时代"
}
```

```json
{
  "companies": ["比亚迪", "宁德时代"],
  "metric": "revenue",
  "period": "前三季度"
}
```

```json
{
  "question": "宁德时代前三季度净利润是多少？"
}
```

### 知识库与上传

- `POST /api/knowledge/upload`
- `GET /api/knowledge/list`
- `GET /api/knowledge/file/{upload_id}`
- `POST /api/data/refresh`

## 已知说明

- 当前维护中的前端主入口是 `frontend/src` 下的 Vite 工程。
- 根目录 `index.html` 是历史静态页面，不参与当前 Vite 构建和 GitHub Pages 工作流。
- 后端当前只提供 API，没有把 `frontend/dist` 挂载为静态站点。
- 前端接口层内置了 fallback 数据，因此后端异常时页面仍可能显示示例内容，这属于当前设计，不一定代表后端已经连通。

## 后续建议

如果你准备继续迭代这个项目，优先建议做这几件事：

1. 统一本地默认端口，避免 `8000` / `8010` 混用。
2. 增加 `.env.example`，把 RAG 和前端 API 配置显式化。
3. 让后端在生产模式下可选托管 `frontend/dist`，简化单机部署。
4. 为 PDF 解析链路补充测试样本和失败提示，降低上传后“看起来成功但未命中规则”的困惑。
