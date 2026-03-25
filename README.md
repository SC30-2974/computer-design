# 新能源财报智能体系统

## 1. 项目说明

这是一个可在本地直接运行的前后端项目，当前包含：

- 智能问答区域
- 企业分析报告生成
- 企业筛选与浏览
- 企业画像展示
- 横向指标对比

当前页面中的企业指标、报告摘要、机会与风险文案，已经按 `2025 年一季度至三季度财报数据` 整理并写入代码。

## 2. 项目结构

```text
computer-design/
├─ backend/
│  ├─ __init__.py
│  └─ app/
│     ├─ __init__.py
│     └─ main.py          # FastAPI 后端，提供 API 并托管前端页面
├─ frontend/
│  └─ index.html          # 前端主页面（唯一维护版本）
├─ index.html             # 与 frontend/index.html 同步，用于 GitHub Pages
├─ requirements.txt       # Python 依赖
├─ run.bat                # Windows 一键启动脚本
└─ README.md
```

说明：

- 本地 FastAPI 读取的是 `frontend/index.html`
- 根目录 `index.html` 用于和 GitHub Pages 保持同一套前端内容
- 两个 `index.html` 需要保持同步，当前已经同步完成

## 3. 运行环境

- Windows 10 / 11
- Python 3.9+
- VS Code（推荐）

## 4. 本地启动

在 `cmd` 或 VS Code 终端中执行：

```bat
cd /d D:\computer-design
.\.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8010
```

启动成功后打开：

```text
http://127.0.0.1:8010
```

停止服务：

```text
Ctrl + C
```

## 5. 一键启动

也可以直接运行：

```bat
cd /d D:\computer-design
.\run.bat
```

## 6. 当前主要接口

- `GET /api/overview`
- `GET /api/sectors`
- `GET /api/companies`
- `GET /api/company/{company_name}`
- `GET /api/metrics?metric=revenue|profit|margin`
- `POST /api/ask`
- `POST /api/report`

示例：

```json
{"company":"宁德时代"}
```

```json
{"question":"宁德时代净利润是多少？"}
```

## 7. 数据说明

当前版本中：

- 企业卡片数据
- 企业画像内容
- 指标对比数据
- 分析报告生成内容

都已经改成基于 `2025 年前三季度` 财报整理后的口径。

目前写入系统的企业包括：

- 比亚迪
- 恩捷股份
- 隆基绿能
- 宁德时代
- 阳光电源
- 亿纬锂能
- 通威股份

其中页面中的“数据来源”说明已经标注到对应企业的报告页码。

## 8. GitHub Pages 说明

如果你要发布到 GitHub Pages：

- 请提交根目录的 `index.html`
- 同时保留 `frontend/index.html` 作为项目维护版本

这样可以保证：

- 本地运行看到的是同一套前端
- GitHub Pages 打开的也是同一套前端

## 9. 常见问题

### 9.1 端口报错

如果 `8010` 被占用，可以换一个端口：

```bat
python -m uvicorn backend.app.main:app --reload --port 8020
```

### 9.2 虚拟环境激活失败

如果你用的是 `cmd`，请执行：

```bat
.\.venv\Scripts\activate.bat
```

不要在 `cmd` 里运行 `Activate.ps1`。

### 9.3 GitHub Pages 和本地显示不一致

通常是因为：

- 你只改了 `frontend/index.html`
- 但没有同步根目录 `index.html`

当前项目建议每次前端改完后，同步一次根目录 `index.html`。

## 10. 当前状态

当前项目已经完成：

- 前后端可本地启动
- GitHub Pages 可使用同一份前端页面
- 前端主要数据已替换为财报整理口径
- 临时提取 PDF/TXT 文件已从项目根目录清理
