from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="新能源财报智能体系统",
    description="面向新能源行业的财报问答、指标分析与报告生成系统",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


COMPANY_DATA: list[dict[str, Any]] = [
    {
        "name": "宁德时代",
        "sector": "动力电池",
        "revenue": 4100,
        "profit": 530,
        "margin": 22.1,
        "year": 2025,
        "summary": "动力电池龙头，储能与海外业务协同明显。",
        "opportunity": "储能需求增长和全球化扩张带来增量空间。",
        "risk": "原材料价格波动和行业竞争可能压缩利润率。",
    },
    {
        "name": "比亚迪",
        "sector": "整车+电池",
        "revenue": 6200,
        "profit": 420,
        "margin": 18.7,
        "year": 2025,
        "summary": "整车与电池双轮驱动，产业链一体化优势明显。",
        "opportunity": "出口和高端车型放量增强增长弹性。",
        "risk": "价格竞争加剧可能影响整车盈利能力。",
    },
    {
        "name": "隆基绿能",
        "sector": "光伏",
        "revenue": 1180,
        "profit": 94,
        "margin": 15.2,
        "year": 2025,
        "summary": "聚焦光伏主产业链，组件与技术路线能力突出。",
        "opportunity": "高效组件和海外市场恢复带动收入改善。",
        "risk": "光伏产业价格波动与阶段性供需错配明显。",
    },
    {
        "name": "通威股份",
        "sector": "光伏+硅料",
        "revenue": 1390,
        "profit": 102,
        "margin": 16.8,
        "year": 2025,
        "summary": "硅料与电池片协同布局，具备成本优势。",
        "opportunity": "一体化布局有助于对冲单环节波动。",
        "risk": "硅料价格下行会拖累整体盈利水平。",
    },
    {
        "name": "阳光电源",
        "sector": "储能+逆变器",
        "revenue": 980,
        "profit": 87,
        "margin": 21.4,
        "year": 2025,
        "summary": "储能系统和逆变器业务布局完整，海外客户基础较好。",
        "opportunity": "海外储能建设持续推进，系统集成需求提升。",
        "risk": "海外政策变化与项目交付节奏可能影响业绩确认。",
    },
    {
        "name": "天齐锂业",
        "sector": "锂矿资源",
        "revenue": 560,
        "profit": 63,
        "margin": 27.6,
        "year": 2025,
        "summary": "上游锂资源企业，对锂盐价格变化较为敏感。",
        "opportunity": "行业复苏时资源端盈利弹性较强。",
        "risk": "锂价波动会直接影响收入和利润表现。",
    },
    {
        "name": "恩捷股份",
        "sector": "隔膜",
        "revenue": 214,
        "profit": 31,
        "margin": 29.4,
        "year": 2025,
        "summary": "锂电池隔膜环节代表企业，盈利质量较高。",
        "opportunity": "中高端隔膜需求稳定，有助于维持产品结构优势。",
        "risk": "新增产能释放后，价格压力可能逐步传导。",
    },
    {
        "name": "亿纬锂能",
        "sector": "动力+消费电池",
        "revenue": 488,
        "profit": 46,
        "margin": 19.1,
        "year": 2025,
        "summary": "动力与消费电池并行发展，客户结构较为均衡。",
        "opportunity": "新客户开拓与储能产品扩展值得关注。",
        "risk": "多业务线扩张下，资本开支和执行压力较大。",
    },
]

REFERENCE_DOCS: list[dict[str, Any]] = [
    {
        "title": "企业财报样本",
        "fileName": "H2_AN202510301771926086_1.pdf",
        "summary": "用于提炼营收、净利润、毛利率、主营业务和风险提示等字段结构。",
        "pageCount": 21,
        "usage": ["报告生成", "来源标注", "企业详情展示"],
    },
    {
        "title": "数据下载路径文档",
        "fileName": "赛题相关数据下载路径文档.pdf",
        "summary": "用于整理数据获取入口、下载路径和数据口径说明。",
        "pageCount": 1,
        "usage": ["数据入口说明", "口径说明", "数据处理流程"],
    },
]

DATA_GUIDE: list[dict[str, str]] = [
    {"step": "01 数据获取", "detail": "优先使用公开披露平台和统一下载入口，保持来源一致。"},
    {"step": "02 字段统一", "detail": "统一营收、净利润、毛利率、年份、企业名称等核心字段。"},
    {"step": "03 来源标记", "detail": "关键指标保留来源说明，方便问答与报告回溯。"},
    {"step": "04 内容生成", "detail": "将指标、行业对比、风险和机会整理为统一输出模板。"},
]

MODULES: list[dict[str, str]] = [
    {"title": "智能问答", "detail": "输入自然语言问题，返回指标结论和来源说明。"},
    {"title": "指标分析", "detail": "对比不同企业的营收、净利润和毛利率表现。"},
    {"title": "企业画像", "detail": "查看赛道归属、经营摘要、机会与风险。"},
    {"title": "报告生成", "detail": "按统一模板生成企业分析简报。"},
]


class AskRequest(BaseModel):
    question: str


class ReportRequest(BaseModel):
    company: str


def source_text(company_name: str) -> str:
    return f"数据来源：{company_name}年度财报与已整理知识库（演示数据）"


def find_company(name: str) -> dict[str, Any] | None:
    return next((item for item in COMPANY_DATA if item["name"] == name), None)


def filtered_companies(keyword: str = "", sector: str = "") -> list[dict[str, Any]]:
    items = COMPANY_DATA
    if sector:
        items = [item for item in items if item["sector"] == sector]
    if keyword:
        items = [item for item in items if keyword in item["name"] or keyword in item["sector"]]
    return items


def answer_question(question: str) -> str:
    q = question.strip()
    if not q:
        return "请输入问题内容。"

    matched = next((item for item in COMPANY_DATA if item["name"] in q), None)

    if matched and "净利润" in q:
        return f"{matched['name']}净利润约 {matched['profit']} 亿元。\n{source_text(matched['name'])}"
    if matched and "营收" in q:
        return f"{matched['name']}营收约 {matched['revenue']} 亿元。\n{source_text(matched['name'])}"
    if matched and "毛利率" in q:
        return f"{matched['name']}毛利率约 {matched['margin']}%。\n{source_text(matched['name'])}"
    if matched and ("风险" in q or "机会" in q):
        return (
            f"{matched['name']}的潜在机会：{matched['opportunity']}\n"
            f"{matched['name']}的主要风险：{matched['risk']}\n"
            f"{source_text(matched['name'])}"
        )
    if "毛利率" in q and "比亚迪" in q and "宁德时代" in q:
        return (
            "毛利率对比：宁德时代 22.1%，比亚迪 18.7%，宁德时代更高。\n"
            "数据来源：新能源企业财报对比（演示数据）"
        )
    if "趋势" in q or "机会" in q:
        return (
            "新能源行业当前关注点包括储能建设、海外市场扩张、光伏与锂电产业链协同，以及原材料价格变化带来的利润弹性。\n"
            "数据来源：行业研报摘要与已整理知识库（演示数据）"
        )

    return (
        "当前支持企业营收、净利润、毛利率、企业机会与风险等问题。\n"
        "你可以直接提问：宁德时代净利润是多少？ 阳光电源有哪些风险？"
    )


def make_report(company_name: str) -> str:
    company = find_company(company_name)
    if company is None:
        raise HTTPException(status_code=404, detail=f"未找到企业：{company_name}")

    industry_avg_margin = round(sum(item["margin"] for item in COMPANY_DATA) / len(COMPANY_DATA), 1)
    margin_gap = round(company["margin"] - industry_avg_margin, 1)
    gap_text = "高于" if margin_gap >= 0 else "低于"

    return (
        f"{company_name}分析简报\n"
        f"1. 核心指标：营收约 {company['revenue']} 亿元，净利润约 {company['profit']} 亿元，毛利率约 {company['margin']}%。\n"
        f"2. 行业定位：企业位于{company['sector']}方向，毛利率较样本均值{gap_text} {abs(margin_gap)} 个百分点。\n"
        f"3. 经营摘要：{company['summary']}\n"
        f"4. 潜在机会：{company['opportunity']}\n"
        f"5. 主要风险：{company['risk']}\n"
        f"{source_text(company_name)}"
    )


@app.get("/api/overview")
def get_overview() -> dict[str, Any]:
    return {
        "companyCount": len(COMPANY_DATA),
        "sectorCount": len({item["sector"] for item in COMPANY_DATA}),
        "moduleCount": len(MODULES),
        "modules": MODULES,
    }


@app.get("/api/sectors")
def get_sectors() -> dict[str, Any]:
    return {"items": sorted({item["sector"] for item in COMPANY_DATA})}


@app.get("/api/companies")
def get_companies(
    keyword: str = Query(default=""),
    sector: str = Query(default=""),
) -> dict[str, Any]:
    return {"items": filtered_companies(keyword=keyword, sector=sector)}


@app.get("/api/company/{company_name}")
def get_company(company_name: str) -> dict[str, Any]:
    company = find_company(company_name)
    if company is None:
        raise HTTPException(status_code=404, detail=f"未找到企业：{company_name}")
    return {"item": company}


@app.get("/api/metrics")
def get_metrics(
    metric: str = "revenue",
    sector: str = Query(default=""),
) -> dict[str, Any]:
    if metric not in {"revenue", "profit", "margin"}:
        raise HTTPException(status_code=400, detail="metric 参数仅支持 revenue/profit/margin")

    items = filtered_companies(sector=sector)
    return {
        "metric": metric,
        "items": [
            {"name": row["name"], "sector": row["sector"], "value": row[metric]}
            for row in items
        ],
    }


@app.get("/api/system-board")
def get_system_board() -> dict[str, Any]:
    return {"modules": MODULES, "documents": REFERENCE_DOCS, "guide": DATA_GUIDE}


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
