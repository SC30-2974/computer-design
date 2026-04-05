# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.scripts.init_db import (
    PDF_PATH,
    build_business_summary,
    build_risk_opportunity,
    extract_seed_rows,
    get_conn,
    get_default_seed_rows,
    init_db,
    seed_company_metrics,
)

MARKER_PATH = PDF_PATH.parent / "latest_pdf_path.txt"


def get_latest_pdf_path() -> str:
    if MARKER_PATH.exists():
        try:
            return MARKER_PATH.read_text(encoding="utf-8").strip() or str(PDF_PATH)
        except Exception:
            return str(PDF_PATH)
    return str(PDF_PATH)


def set_latest_pdf_path(pdf_path: str | None = None) -> str:
    target = (pdf_path or "").strip() or str(PDF_PATH)
    MARKER_PATH.write_text(target, encoding="utf-8")
    return target


def list_upload_records() -> list[dict[str, Any]]:
    try:
        with get_conn() as conn:
            rows = conn.execute(
                """
                SELECT id, file_name, stored_path, raw_path, upload_time
                FROM uploads
                ORDER BY id ASC
                """
            ).fetchall()
        return [dict(row) for row in rows]
    except Exception:
        return []


def select_effective_uploads(upload_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest_by_company: dict[str, dict[str, Any]] = {}
    for upload in upload_rows:
        latest_by_company[derive_upload_company_name(upload)] = upload
    return sorted(latest_by_company.values(), key=lambda item: int(item.get("id") or 0))


def derive_upload_company_name(upload: dict[str, Any]) -> str:
    file_name = str(upload.get("file_name") or "").strip()
    if file_name:
        stem = Path(file_name).stem
        candidate = stem.split("2025")[0].strip("：: _-")
        return candidate or stem or "未识别企业"

    raw_path = str(upload.get("raw_path") or "").strip()
    if raw_path:
        return Path(raw_path).stem
    return "未识别企业"


def resolve_upload_pdf_path(upload: dict[str, Any]) -> Path | None:
    candidates = [
        str(upload.get("raw_path") or "").strip(),
        str(upload.get("stored_path") or "").strip(),
    ]
    for raw in candidates:
        if not raw:
            continue
        path = Path(raw)
        if path.exists():
            return path
    return None


def build_placeholder_row(upload: dict[str, Any]) -> dict[str, Any]:
    company_name = derive_upload_company_name(upload)
    return {
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


def build_rows_for_upload(upload: dict[str, Any]) -> tuple[list[dict[str, Any]], bool]:
    pdf_path = resolve_upload_pdf_path(upload)
    if pdf_path is None:
        return [], False

    rows = extract_seed_rows(pdf_path)
    if rows:
        return rows, False

    return [build_placeholder_row(upload)], True


def resolve_latest_uploaded_pdf(upload_rows: list[dict[str, Any]]) -> str:
    for upload in reversed(upload_rows):
        pdf_path = resolve_upload_pdf_path(upload)
        if pdf_path is not None:
            return set_latest_pdf_path(str(pdf_path))
    return set_latest_pdf_path(str(PDF_PATH))


def sync_data() -> dict[str, Any]:
    """同步财报数据与向量库。

    流程：初始化数据库 -> 基线样例 + 当前上传文件重建 company_metrics。
    """
    init_db()

    baseline_rows = get_default_seed_rows()
    merged = {row["company_name"]: row for row in baseline_rows}

    upload_rows = list_upload_records()
    effective_uploads = select_effective_uploads(upload_rows)
    parsed_rows = 0
    fallback_uploads = 0

    for upload in effective_uploads:
        rows, used_fallback = build_rows_for_upload(upload)
        if used_fallback:
            fallback_uploads += 1
        parsed_rows += len(rows)
        for row in rows:
            merged[row["company_name"]] = row

    latest_pdf = resolve_latest_uploaded_pdf(effective_uploads)
    seed_company_metrics(list(merged.values()))

    rag_status = "skipped"
    rag_message = "未重建向量库（方案 A 仅做解析入库）。"

    return {
        "rows": parsed_rows,
        "total_rows": len(merged),
        "upload_count": len(effective_uploads),
        "raw_upload_count": len(upload_rows),
        "fallback_uploads": fallback_uploads,
        "pdf": latest_pdf,
        "rag_status": rag_status,
        "rag_message": rag_message,
    }


if __name__ == "__main__":
    result = sync_data()
    print(
        "数据同步完成，"
        f"rows={result['rows']} upload_count={result['upload_count']} rag_status={result['rag_status']}"
    )
