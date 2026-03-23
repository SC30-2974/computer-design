# 新能源投资者智能体系统（前后端完整代码）

## 1. 项目结构

```text
computer-design/
├─ backend/
│  └─ app/
│     └─ main.py          # FastAPI 后端（API + 前端页面托管）
├─ frontend/
│  └─ index.html          # 前端页面（HTML/CSS/JS）
├─ requirements.txt       # Python 依赖
├─ run.bat                # Windows 一键启动脚本（可选）
└─ README.md
```

## 2. 环境要求

- Windows 10/11
- Python 3.9+
- VS Code（推荐）

## 3. 在终端运行（按你指定方案）

请在 **CMD 终端** 执行以下命令：

```bat
cd /d D:\computer-design
.\.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8010
```

启动成功后，浏览器打开：

```text
http://127.0.0.1:8010
```

## 4. 常见问题

### 4.1 端口占用或权限错误（如 WinError 10013）

把端口改成 `8010`（本项目默认示例就是 8010）。

如果你想继续用 8000，可以先查占用并结束进程：

```bat
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### 4.2 虚拟环境未激活

你如果使用的是 `cmd`，请用：

```bat
.\.venv\Scripts\activate.bat
```

不要在 `cmd` 里运行 `Activate.ps1`（那是 PowerShell 用法）。

## 5. API 列表

- `GET /api/companies`：获取企业列表与指标
- `GET /api/metrics?metric=revenue|profit|margin`：获取指定指标
- `POST /api/ask`：智能问答
  - 请求体：`{"question":"宁德时代2025年净利润是多少？"}`
- `POST /api/report`：生成企业报告
  - 请求体：`{"company":"宁德时代"}`

## 6. 公网访问（可选）

本地启动后，可以用 Cloudflare Tunnel 临时发布公网地址：

```bat
cloudflared tunnel --url http://127.0.0.1:8010
```

会得到一个 `https://xxxx.trycloudflare.com`，可直接分享访问。

## 7. 说明

当前为竞赛演示版（内置示例数据），已完整覆盖三大功能：

- 智能问数
- 运营指标可视化
- 定制报告生成

后续可将后端问答逻辑替换为 Dify 或大模型 API，实现真实知识库能力。
