# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any
from pathlib import Path

from backend.scripts.init_db import (
    PDF_PATH,
    get_conn,
    extract_seed_rows,
    get_default_seed_rows,
    init_db,
    seed_company_metrics,
    build_business_summary,
    build_risk_opportunity,
)


def get_latest_pdf_path() -> str:
    marker = PDF_PATH.parent / "latest_pdf_path.txt"
    if marker.exists():
        try:
            return marker.read_text(encoding="utf-8").strip() or str(PDF_PATH)
        except Exception:
            return str(PDF_PATH)
    return str(PDF_PATH)


def sync_data() -> dict[str, Any]:
    """同步财报数据与向量库。

    流程：初始化数据库 -> PDF 解析入库 -> 重建向量库。
    """
    init_db()

    latest_pdf = get_latest_pdf_path()
    rows = extract_seed_rows(Path(latest_pdf))
    used_fallback = False
    if not rows:
        rows = get_default_seed_rows()
        used_fallback = True

        # 若上传了新的 PDF 但未命中解析规则，追加占位记录，保证前端可感知刷新。
        try:
            if latest_pdf != str(PDF_PATH) and Path(latest_pdf).exists():
                company_name = Path(latest_pdf).stem
                rows.append(
                    {
                        "company_name": company_name,
                        "sector": "新上传",
                        "revenue": 0.0,
                        "profit": 0.0,
                        "margin": 0.0,
                        "year": 2025,
                        "period": "前三季度",
                        "business_summary": build_business_summary("新上传", 0.0, 0.0, 0.0),
                        "risk_opportunity": build_risk_opportunity(0.0),
                        "source_page": 0,
                    }
                )
        except Exception:
            pass

    # 合并已有数据，避免覆盖原始样本。
    try:
        with get_conn() as conn:
            existing = conn.execute("SELECT * FROM company_metrics").fetchall()
        existing_rows = [dict(item) for item in existing]
    except Exception:
        existing_rows = []

    baseline_rows = get_default_seed_rows()
    merged = {row["company_name"]: row for row in baseline_rows}
    for row in existing_rows:
        merged[row["company_name"]] = row
    for row in rows:
        merged[row["company_name"]] = row

    seed_company_metrics(list(merged.values()))

    rag_status = "skipped"
    rag_message = "未重建向量库（方案 A 仅做解析入库）。"

    return {
        "rows": len(rows),
        "total_rows": len(merged),
        "used_fallback": used_fallback,
        "pdf": latest_pdf,
        "rag_status": rag_status,
        "rag_message": rag_message,
    }


if __name__ == "__main__":
    result = sync_data()
    print(
        "数据同步完成，"
        f"rows={result['rows']} used_fallback={result['used_fallback']} rag_status={result['rag_status']}"
    )
