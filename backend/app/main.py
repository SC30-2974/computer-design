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
    title="新能源投资者智能体系统",
    description="2026中国大学生计算机设计大赛演示版：前后端一体化示例",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


COMPANY_DATA: list[dict[str, Any]] = [
    {"name": "宁德时代", "revenue": 4100, "profit": 530, "margin": 22.1},
    {"name": "比亚迪", "revenue": 6200, "profit": 420, "margin": 18.7},
    {"name": "隆基绿能", "revenue": 1180, "profit": 94, "margin": 15.2},
    {"name": "阳光电源", "revenue": 980, "profit": 87, "margin": 21.4},
]

SOURCE_MAP: dict[str, str] = {
    "宁德时代": "数据来源：上市公司年度财报（演示数据）",
    "比亚迪": "数据来源：上市公司年度财报（演示数据）",
    "隆基绿能": "数据来源：上市公司年度财报（演示数据）",
    "阳光电源": "数据来源：上市公司年度财报（演示数据）",
}


class AskRequest(BaseModel):
    question: str


class ReportRequest(BaseModel):
    company: str


def find_company(name: str) -> dict[str, Any] | None:
    for item in COMPANY_DATA:
        if item["name"] == name:
            return item
    return None


def answer_question(question: str) -> str:
    q = question.strip()
    if not q:
        return "请输入问题内容。"

    if "净利润" in q and "宁德时代" in q:
        return "宁德时代净利润约 530 亿元。\n" + SOURCE_MAP["宁德时代"]
    if "毛利率" in q and "比亚迪" in q and "宁德时代" in q:
        return (
            "毛利率对比：宁德时代 22.1%，比亚迪 18.7%。宁德时代更高。\n"
            "数据来源：企业财报对比（演示数据）"
        )
    if "机会" in q:
        return (
            "新能源投资机会：储能需求持续增长、海外市场拓展、政策推动新型电力系统建设。\n"
            "数据来源：行业研报摘要（演示数据）"
        )
    return (
        "已收到问题。当前为演示版智能体问答，可扩展接入 Dify / 大模型 API。\n"
        "示例可问：净利润查询、毛利率对比、行业机会。"
    )


def make_report(company_name: str) -> str:
    company = find_company(company_name)
    if company is None:
        raise HTTPException(status_code=404, detail=f"未找到企业：{company_name}")

    return (
        f"{company_name}投资者简报：\n"
        f"核心指标方面，企业营收约 {company['revenue']} 亿元，"
        f"净利润约 {company['profit']} 亿元，毛利率约 {company['margin']}%。\n"
        "行业对比来看，该企业在盈利能力和规模上处于新能源板块前列。\n"
        "潜在机会：储能及海外业务扩张带来新增量。\n"
        "潜在风险：上游原材料价格波动与行业竞争加剧可能压缩利润空间。\n"
        f"{SOURCE_MAP[company_name]}"
    )


@app.get("/api/companies")
def get_companies() -> dict[str, Any]:
    return {"items": COMPANY_DATA}


@app.get("/api/metrics")
def get_metrics(metric: str = "revenue") -> dict[str, Any]:
    if metric not in {"revenue", "profit", "margin"}:
        raise HTTPException(status_code=400, detail="metric 参数仅支持 revenue/profit/margin")

    return {
        "metric": metric,
        "items": [{"name": row["name"], "value": row[metric]} for row in COMPANY_DATA],
    }


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
