from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="新能源财报智能体系统",
    description="面向新能源财报分析场景的问答、可视化与报告生成演示系统",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


COMPANY_DATA: list[dict[str, Any]] = [
    {"name": "宁德时代", "sector": "动力电池", "revenue": 4100, "profit": 530, "margin": 22.1},
    {"name": "比亚迪", "sector": "整车+电池", "revenue": 6200, "profit": 420, "margin": 18.7},
    {"name": "隆基绿能", "sector": "光伏", "revenue": 1180, "profit": 94, "margin": 15.2},
    {"name": "通威股份", "sector": "光伏+硅料", "revenue": 1390, "profit": 102, "margin": 16.8},
    {"name": "阳光电源", "sector": "储能+逆变器", "revenue": 980, "profit": 87, "margin": 21.4},
    {"name": "天齐锂业", "sector": "锂矿资源", "revenue": 560, "profit": 63, "margin": 27.6},
    {"name": "恩捷股份", "sector": "隔膜", "revenue": 214, "profit": 31, "margin": 29.4},
    {"name": "亿纬锂能", "sector": "动力+消费电池", "revenue": 488, "profit": 46, "margin": 19.1},
]

PROJECT_PHASES: list[dict[str, Any]] = [
    {
        "title": "阶段一：核心功能开发",
        "duration": "4-5天",
        "focus": "完成 Dify 智能体、数据清洗、前端联调三条主线",
        "items": ["智能体搭建组 3 人", "数据清洗组 2 人", "前端开发组 1 人"],
    },
    {
        "title": "阶段二：交付包装",
        "duration": "2-3天",
        "focus": "整理代码、录制视频、完成回归测试与验收",
        "items": ["代码打包+文档整理", "视频剪辑与脚本", "最终测试+环境准备"],
    },
]

TEAM_BOARD: list[dict[str, str]] = [
    {"group": "Dify智能体组", "owner": "成员1-3", "output": "提示词、知识库检索、API 文档、报告模板"},
    {"group": "数据清洗组", "owner": "成员4-5", "output": "企业财报 Excel、来源标注、校验表"},
    {"group": "前端开发组", "owner": "成员6", "output": "问数界面、图表展示、报告交互、样式优化"},
]

DELIVERABLES: list[str] = [
    "Dify 智能体配置 DSL 文件",
    "清洗后财报 Excel",
    "前端代码压缩包",
    "项目总文档",
    "演示视频 MP4",
    "代码说明文档",
    "用户使用手册",
]

SOURCE_MAP: dict[str, str] = {
    item["name"]: f"数据来源：{item['name']} 年度财报与知识库标注（演示数据）"
    for item in COMPANY_DATA
}


class AskRequest(BaseModel):
    question: str


class ReportRequest(BaseModel):
    company: str


def find_company(name: str) -> dict[str, Any] | None:
    return next((item for item in COMPANY_DATA if item["name"] == name), None)


def build_company_summary(company: dict[str, Any]) -> str:
    return (
        f"{company['name']}属于{company['sector']}赛道，"
        f"营收约{company['revenue']}亿元，净利润约{company['profit']}亿元，"
        f"毛利率约{company['margin']}%。"
    )


def answer_question(question: str) -> str:
    q = question.strip()
    if not q:
        return "请输入问题内容。"

    matched = next((item for item in COMPANY_DATA if item["name"] in q), None)

    if matched and "净利润" in q:
        return f"{matched['name']}净利润约 {matched['profit']} 亿元。\n{SOURCE_MAP[matched['name']]}"

    if matched and "营收" in q:
        return f"{matched['name']}营收约 {matched['revenue']} 亿元。\n{SOURCE_MAP[matched['name']]}"

    if matched and "毛利率" in q:
        return f"{matched['name']}毛利率约 {matched['margin']}%。\n{SOURCE_MAP[matched['name']]}"

    if "毛利率" in q and "比亚迪" in q and "宁德时代" in q:
        return (
            "毛利率对比：宁德时代 22.1%，比亚迪 18.7%，宁德时代更高。\n"
            "数据来源：新能源企业财报对比（演示数据）"
        )

    if "机会" in q or "趋势" in q:
        return (
            "新能源赛道的关注点主要包括储能需求增长、海外市场扩张、光伏和锂电产业链协同，以及政策推动的新型电力系统建设。\n"
            "数据来源：行业研报摘要与项目知识库（演示数据）"
        )

    if "报告" in q and matched:
        return build_company_summary(matched) + "\n可在右侧“定制报告生成”模块中生成完整简报。"

    return (
        "当前是项目演示版问答，可回答企业营收、净利润、毛利率、行业机会等问题。\n"
        "建议提问示例：宁德时代净利润是多少？ 比亚迪和宁德时代毛利率谁更高？"
    )


def make_report(company_name: str) -> str:
    company = find_company(company_name)
    if company is None:
        raise HTTPException(status_code=404, detail=f"未找到企业：{company_name}")

    industry_avg_margin = round(sum(item["margin"] for item in COMPANY_DATA) / len(COMPANY_DATA), 1)
    margin_gap = round(company["margin"] - industry_avg_margin, 1)
    gap_text = "高于" if margin_gap >= 0 else "低于"

    return (
        f"{company_name}投资者分析简报\n"
        f"1. 核心指标：营收约 {company['revenue']} 亿元，净利润约 {company['profit']} 亿元，"
        f"毛利率约 {company['margin']}%。\n"
        f"2. 行业对比：该企业位于{company['sector']}赛道，毛利率较样本均值 {gap_text} {abs(margin_gap)} 个百分点。\n"
        "3. 潜在机会：储能、海外业务和产业链一体化有望带来新增量。\n"
        "4. 潜在风险：原材料价格波动、产能竞争和政策节奏变化可能压缩利润空间。\n"
        f"{SOURCE_MAP[company_name]}"
    )


@app.get("/api/overview")
def get_overview() -> dict[str, Any]:
    return {
        "companyCount": len(COMPANY_DATA),
        "coreFunctions": ["财报问答", "指标可视化", "报告生成"],
        "projectTag": "6人团队协作项目",
        "focus": "Dify + 数据清洗 + 前端联调",
    }


@app.get("/api/companies")
def get_companies() -> dict[str, Any]:
    return {"items": COMPANY_DATA}


@app.get("/api/metrics")
def get_metrics(metric: str = "revenue") -> dict[str, Any]:
    if metric not in {"revenue", "profit", "margin"}:
        raise HTTPException(status_code=400, detail="metric 参数仅支持 revenue/profit/margin")

    return {
        "metric": metric,
        "items": [
            {"name": row["name"], "sector": row["sector"], "value": row[metric]}
            for row in COMPANY_DATA
        ],
    }


@app.get("/api/project-board")
def get_project_board() -> dict[str, Any]:
    return {"phases": PROJECT_PHASES, "teams": TEAM_BOARD, "deliverables": DELIVERABLES}


@app.post("/api/ask")
def ask(req: AskRequest) -> dict[str, str]:
    return {"answer": answer_question(req.question)}


@app.post("/api/report")
def report(req: ReportRequest) -> dict[str, str]:
    return {"report": make_report(req.company)}


if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR)), name="assets")


@app.get("/")
def serve_index() -> FileResponse:
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="frontend/index.html 不存在")
    return FileResponse(index_path)
