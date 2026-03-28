from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .db import get_db
from .rag_engine import ask_financial_question, build_vector_store
from .schemas import AskRequest, CompareReportRequest, ReportRequest
from .services.diagnosis_service import build_financial_diagnosis
from .services.metrics_service import (
    fetch_companies,
    fetch_companies_by_names,
    fetch_company_by_name,
    fetch_metrics,
    fetch_sectors,
)

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIST_DIR = BASE_DIR / 'frontend' / 'dist'

app = FastAPI(
    title='新能源财报智能体系统 API',
    description='基于 FastAPI + SQLite + LangChain 的新能源财报分析服务',
    version='4.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

DbDep = Annotated[sqlite3.Connection, Depends(get_db)]


@app.get('/api/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.get('/api/sectors')
def get_sectors(db: DbDep) -> dict[str, list[str]]:
    return {'items': fetch_sectors(db)}


@app.get('/api/companies')
def get_companies(
    db: DbDep,
    keyword: str = Query(default=''),
    sector: str = Query(default=''),
    period: str = Query(default='前三季度'),
) -> dict:
    return {'items': fetch_companies(db, keyword=keyword, sector=sector, period=period)}


@app.get('/api/metrics')
def get_metrics(
    db: DbDep,
    metric: str = Query(default='revenue'),
    sector: str = Query(default=''),
    period: str = Query(default='前三季度'),
) -> dict:
    try:
        return fetch_metrics(db, metric=metric, period=period, sector=sector)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get('/api/financial_diagnosis/{company_name}')
def financial_diagnosis(company_name: str, db: DbDep) -> dict:
    company = fetch_company_by_name(db, company_name)
    if not company:
        raise HTTPException(status_code=404, detail=f'未找到企业：{company_name}')
    return build_financial_diagnosis(company)


@app.get('/api/company-battle')
def company_battle(
    db: DbDep,
    companies: str = Query(default=''),
    period: str = Query(default='前三季度'),
) -> dict:
    names = [item.strip() for item in companies.split(',') if item.strip()]
    if len(names) < 2:
        raise HTTPException(status_code=400, detail='请至少传入 2 家企业名称，英文逗号分隔。')

    rows = fetch_companies_by_names(db, names, period=period)
    if len(rows) < 2:
        raise HTTPException(status_code=404, detail='未找到可对战的企业数据。')

    winner_by_revenue = max(rows, key=lambda x: float(x['revenue']))
    winner_by_profit = max(rows, key=lambda x: float(x['profit']))
    winner_by_margin = max(rows, key=lambda x: float(x['margin']))

    return {
        'period': period,
        'companies': rows,
        'winners': {
            'revenue': winner_by_revenue['company_name'],
            'profit': winner_by_profit['company_name'],
            'margin': winner_by_margin['company_name'],
        },
    }


@app.post('/api/rag/ask')
def rag_ask(req: AskRequest) -> dict:
    return ask_financial_question(req.question)


@app.post('/api/rag/rebuild')
def rag_rebuild() -> dict[str, str]:
    build_vector_store()
    return {'message': '向量库重建完成'}


@app.post('/api/report')
def generate_report(req: ReportRequest, db: DbDep) -> dict:
    company = fetch_company_by_name(db, req.company)
    if not company:
        raise HTTPException(status_code=404, detail=f'未找到企业：{req.company}')

    diagnosis = build_financial_diagnosis(company)
    report = (
        f"{company['company_name']}财报分析简报\n"
        f"1. 核心指标：{company['period']}营收 {company['revenue']} 亿元，归母净利润 {company['profit']} 亿元，毛利率 {company['margin']}%。\n"
        f"2. 经营摘要：{company['business_summary']}\n"
        f"3. 风险与机会：{company['risk_opportunity']}\n"
        f"4. 财务诊断：{diagnosis['overall_assessment']}\n"
        f"5. 建议：{'；'.join(diagnosis['suggestions'])}"
    )
    return {
        'report': report,
        'citations': [
            {
                'source': 'finance_app.db/company_metrics',
                'company_name': company['company_name'],
                'page': company.get('source_page') or '结构化数据',
            }
        ],
    }


@app.post('/api/report/compare')
def compare_report(req: CompareReportRequest, db: DbDep) -> dict:
    if len(req.companies) < 2:
        raise HTTPException(status_code=400, detail='请至少选择 2 家企业。')

    rows = fetch_companies_by_names(db, req.companies, period=req.period)
    if len(rows) < 2:
        raise HTTPException(status_code=404, detail='未找到可对比的企业数据。')

    winner_revenue = max(rows, key=lambda x: float(x['revenue']))['company_name']
    winner_profit = max(rows, key=lambda x: float(x['profit']))['company_name']
    winner_margin = max(rows, key=lambda x: float(x['margin']))['company_name']

    lines = [
        f"多企业对比报告（{req.period}）",
        '',
        '一、企业核心指标',
    ]
    for row in rows:
        lines.append(
            f"- {row['company_name']}：营收 {row['revenue']} 亿元，净利润 {row['profit']} 亿元，毛利率 {row['margin']}%"
        )

    lines.extend(
        [
            '',
            '二、对战结论',
            f'- 营收冠军：{winner_revenue}',
            f'- 净利润冠军：{winner_profit}',
            f'- 毛利率冠军：{winner_margin}',
            '',
            '三、主要风险提示',
        ]
    )
    for row in rows:
        lines.append(f"- {row['company_name']}：{row.get('risk_opportunity') or '暂无'}")

    lines.extend(['', '四、引用来源'])
    for row in rows:
        lines.append(
            f"- {row['company_name']}：finance_app.db/company_metrics，source_page={row.get('source_page') or '结构化数据'}"
        )

    return {
        'report_text': '\n'.join(lines),
        'period': req.period,
        'citations': [
            {
                'source': 'finance_app.db/company_metrics',
                'company_name': row['company_name'],
                'page': row.get('source_page') or '结构化数据',
            }
            for row in rows
        ],
    }
