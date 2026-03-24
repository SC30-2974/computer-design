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
        "name": "比亚迪",
        "sector": "整车+电池+光伏",
        "revenue": 5662.66,
        "profit": 233.33,
        "margin": 17.9,
        "year": 2025,
        "period": "2025 年前三季度",
        "summary": "主营新能源汽车、手机部件及组装、二次充电电池与光伏业务，汽车电动化与智能化仍是核心增长主线。",
        "opportunity": "新能源汽车、电池和储能协同推进，全球化与智能化布局仍有望继续释放增量。",
        "risk": "前三季度归母净利润同比下降 7.55%，行业价格竞争与海外经营环境变化仍会影响盈利表现。",
        "source": "《各企业2025年财报数据（一季度至三季度）》中比亚迪股份有限公司 2025 年第三季度报告，第 210-218 页。",
    },
    {
        "name": "恩捷股份",
        "sector": "锂电隔膜",
        "revenue": 95.43,
        "profit": -0.86,
        "margin": 15.9,
        "year": 2025,
        "period": "2025 年前三季度",
        "summary": "核心产品覆盖锂电池隔离膜、BOPP 薄膜和包装印刷品，隔膜业务覆盖动力、消费和储能电池客户。",
        "opportunity": "全球新能源与储能需求仍在增长，隔膜龙头地位和海外客户覆盖有助于稳固市场份额。",
        "risk": "隔膜行业竞争加剧、价格下行，前三季度归母净利润转负，盈利修复仍需观察。",
        "source": "《各企业2025年财报数据（一季度至三季度）》中云南恩捷新材料股份有限公司 2025 年第三季度报告，第 381-391 页。",
    },
    {
        "name": "隆基绿能",
        "sector": "光伏组件",
        "revenue": 509.15,
        "profit": -34.03,
        "margin": 1.2,
        "year": 2025,
        "period": "2025 年前三季度",
        "summary": "主营光伏硅片、电池组件及解决方案，处于光伏制造与全球化布局核心环节。",
        "opportunity": "供给侧改革与技术创新若持续推进，海外新兴市场和高效产品有望带来盈利修复空间。",
        "risk": "光伏供需失衡、低价竞争和贸易壁垒仍在，前三季度仍处亏损状态。",
        "source": "《各企业2025年财报数据（一季度至三季度）》中隆基绿能科技股份有限公司 2025 年第三季度报告，第 645-656 页。",
    },
    {
        "name": "宁德时代",
        "sector": "动力电池+储能",
        "revenue": 2830.72,
        "profit": 490.34,
        "margin": 25.3,
        "year": 2025,
        "period": "2025 年前三季度",
        "summary": "主营动力电池与储能电池，具备从材料、电池系统到回收的全链条研发与产业化能力。",
        "opportunity": "动力电池全球市占率和储能电池产量继续领先，动力与储能双轮驱动仍具扩张空间。",
        "risk": "产品价格与汇率波动仍是经营管理重点，全球化扩张下对成本与外部政策的敏感度较高。",
        "source": "《各企业2025年财报数据（一季度至三季度）》中宁德时代新能源科技股份有限公司 2025 年第三季度报告，第 850-858 页。",
    },
    {
        "name": "阳光电源",
        "sector": "逆变器+储能",
        "revenue": 664.02,
        "profit": 118.81,
        "margin": 34.9,
        "year": 2025,
        "period": "2025 年前三季度",
        "summary": "聚焦光伏逆变器、储能系统、风电变流及氢能等清洁能源装备，并提供全生命周期解决方案。",
        "opportunity": "全球光伏与储能装机保持高增，逆变器和储能系统需求仍在扩张。",
        "risk": "市场竞争加剧带来毛利率下滑风险，海外政策和项目交付节奏也会影响业绩兑现。",
        "source": "《各企业2025年财报数据（一季度至三季度）》中阳光电源股份有限公司 2025 年第三季度报告，第 1066-1074 页。",
    },
    {
        "name": "亿纬锂能",
        "sector": "消费+动力+储能电池",
        "revenue": 450.02,
        "profit": 28.16,
        "margin": 16.0,
        "year": 2025,
        "period": "2025 年前三季度",
        "summary": "主营消费电池、动力电池和储能电池，覆盖智慧生活、绿色交通和能源转型等多元场景。",
        "opportunity": "满产满销与市占率提升推动前三季度营收增长 32.17%，储能和动力业务仍有扩张空间。",
        "risk": "前三季度归母净利润同比下降 11.70%，仍需继续消化费用与减值等盈利扰动。",
        "source": "《各企业2025年财报数据（一季度至三季度）》中惠州亿纬锂能股份有限公司 2025 年第三季度报告，第 1286-1295 页。",
    },
    {
        "name": "通威股份",
        "sector": "光伏+硅料",
        "revenue": 646.0,
        "profit": -52.7,
        "margin": 2.7,
        "year": 2025,
        "period": "2025 年前三季度",
        "summary": "以农业与新能源双主业协同发展，光伏产业链覆盖硅料、电池等关键环节。",
        "opportunity": "报告指出产业链价格在本报告期内已有回升，单季盈利指标出现持续改善。",
        "risk": "光伏主产业仍处低景气区间，前三季度归母净利润为负，行业波动对业绩影响明显。",
        "source": "《各企业2025年财报数据（一季度至三季度）》中通威股份有限公司 2025 年第三季度报告，第 1503-1512 页。",
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


def source_text(company: dict[str, Any]) -> str:
    return (
        f"数据来源：{company['source']} "
        "毛利率优先采用报告披露口径，未直接披露时按前三季度营业收入与营业成本测算。"
    )


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
        return f"{matched['name']}{matched['period']}归母净利润约 {matched['profit']} 亿元。\n{source_text(matched)}"
    if matched and "营收" in q:
        return f"{matched['name']}{matched['period']}营业收入约 {matched['revenue']} 亿元。\n{source_text(matched)}"
    if matched and "毛利率" in q:
        return f"{matched['name']}{matched['period']}毛利率约 {matched['margin']}%。\n{source_text(matched)}"
    if matched and ("风险" in q or "机会" in q):
        return (
            f"{matched['name']}的潜在机会：{matched['opportunity']}\n"
            f"{matched['name']}的主要风险：{matched['risk']}\n"
            f"{source_text(matched)}"
        )
    if "毛利率" in q and "比亚迪" in q and "宁德时代" in q:
        return (
            "毛利率对比：宁德时代 25.3%，比亚迪 17.9%，宁德时代更高。\n"
            "数据来源：《各企业2025年财报数据（一季度至三季度）》对应企业三季报。"
        )
    if "趋势" in q or "机会" in q:
        return (
            "从已整理的三季报看，动力电池与储能企业仍保持较强增长韧性，光伏制造环节则继续承受供需失衡与价格竞争压力。\n"
            "数据来源：《各企业2025年财报数据（一季度至三季度）》对应企业三季报。"
        )

    return (
        "当前支持企业前三季度营收、净利润、毛利率、企业机会与风险等问题。\n"
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
        f"1. 核心指标：{company['period']}营业收入约 {company['revenue']} 亿元，归母净利润约 {company['profit']} 亿元，毛利率约 {company['margin']}%。\n"
        f"2. 行业定位：企业位于{company['sector']}方向，毛利率较样本均值{gap_text} {abs(margin_gap)} 个百分点。\n"
        f"3. 经营摘要：{company['summary']}\n"
        f"4. 潜在机会：{company['opportunity']}\n"
        f"5. 主要风险：{company['risk']}\n"
        f"{source_text(company)}"
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
