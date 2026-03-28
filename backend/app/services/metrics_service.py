from __future__ import annotations

import sqlite3
from typing import Any


def fetch_companies(db: sqlite3.Connection, keyword: str = '', sector: str = '', period: str = '前三季度') -> list[dict[str, Any]]:
    sql = """
        SELECT
            id,
            company_name,
            sector,
            revenue,
            profit,
            margin,
            year,
            period,
            business_summary,
            risk_opportunity,
            source_page
        FROM company_metrics
        WHERE period = ?
    """
    params: list[Any] = [period]

    if keyword:
        sql += ' AND (company_name LIKE ? OR sector LIKE ?)'
        params.extend([f'%{keyword}%', f'%{keyword}%'])

    if sector:
        sql += ' AND sector = ?'
        params.append(sector)

    sql += ' ORDER BY revenue DESC'
    rows = db.execute(sql, params).fetchall()
    return [dict(row) for row in rows]


def fetch_metrics(db: sqlite3.Connection, metric: str = 'revenue', period: str = '前三季度', sector: str = '') -> dict[str, Any]:
    if metric not in {'revenue', 'profit', 'margin'}:
        raise ValueError('metric 仅支持 revenue/profit/margin')

    sql = f"""
        SELECT company_name, sector, {metric} AS value, year, period, source_page
        FROM company_metrics
        WHERE period = ?
    """
    params: list[Any] = [period]

    if sector:
        sql += ' AND sector = ?'
        params.append(sector)

    sql += ' ORDER BY value DESC'
    rows = db.execute(sql, params).fetchall()
    return {
        'metric': metric,
        'period': period,
        'items': [dict(row) for row in rows],
    }


def fetch_company_by_name(db: sqlite3.Connection, company_name: str) -> dict[str, Any] | None:
    row = db.execute(
        """
        SELECT *
        FROM company_metrics
        WHERE company_name = ?
        LIMIT 1
        """,
        (company_name,),
    ).fetchone()
    return dict(row) if row else None


def fetch_companies_by_names(db: sqlite3.Connection, names: list[str], period: str = '前三季度') -> list[dict[str, Any]]:
    if not names:
        return []
    placeholders = ','.join(['?'] * len(names))
    sql = f"""
        SELECT company_name, sector, revenue, profit, margin, period, source_page, business_summary, risk_opportunity
        FROM company_metrics
        WHERE period = ? AND company_name IN ({placeholders})
    """
    rows = db.execute(sql, [period, *names]).fetchall()
    # 按用户传入顺序返回，便于前端对战展示。
    mapping = {row['company_name']: dict(row) for row in rows}
    return [mapping[name] for name in names if name in mapping]


def fetch_sectors(db: sqlite3.Connection) -> list[str]:
    rows = db.execute('SELECT DISTINCT sector FROM company_metrics ORDER BY sector ASC').fetchall()
    return [row[0] for row in rows]
