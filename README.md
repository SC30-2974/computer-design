# 新能源投资者智能体系统（前后端完整代码）

## 1. 项目结构

```text
computer-design/
├─ backend/
│  └─ app/
│     └─ main.py          # FastAPI 后端（API + 静态页面托管）
├─ frontend/
│  └─ index.html          # 前端页面（HTML/CSS/JS）
├─ requirements.txt       # Python 依赖
├─ run.bat                # Windows 一键启动脚本
└─ README.md
```

## 2. 环境要求

- Windows + VS Code
- Python 3.9 及以上

## 3. 在 VS Code 中启动

1. 打开项目目录：`D:\computer-design`
2. 打开终端（PowerShell）执行：

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

3. 浏览器访问：

```text
http://127.0.0.1:8000
```

## 4. 一键启动方式（可选）

双击项目根目录下的 `run.bat`，会自动创建虚拟环境、安装依赖并启动服务。

## 5. 后端 API 说明

- `GET /api/companies`：获取企业列表及指标
- `GET /api/metrics?metric=revenue|profit|margin`：获取指定指标
- `POST /api/ask`：智能问答
  - 请求体：`{"question":"宁德时代2025年净利润是多少？"}`
- `POST /api/report`：生成企业简报
  - 请求体：`{"company":"宁德时代"}`

## 6. 说明

当前是竞赛演示版（内置示例数据），已经具备“智能问数 + 可视化 + 报告生成”完整闭环。  
后续可将后端问答逻辑替换为 Dify 或大模型 API，实现真实知识库推理。
