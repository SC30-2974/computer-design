# AI辅助生成：豆包 2.0 专家模型, 2026-04-16
from __future__ import annotations

from typing import Any


def build_financial_diagnosis(company: dict[str, Any]) -> dict[str, Any]:
    revenue = float(company["revenue"])
    profit = float(company["profit"])
    gross_margin = float(company["margin"])
    net_margin = round((profit / revenue) * 100, 2) if revenue else 0.0

    if gross_margin > 20:
        gross_margin_level = "健康"
    elif gross_margin > 10:
        gross_margin_level = "一般"
    else:
        gross_margin_level = "承压"

    if net_margin > 10:
        net_margin_level = "优秀"
    elif net_margin > 5:
        net_margin_level = "稳健"
    elif net_margin >= 0:
        net_margin_level = "偏弱"
    else:
        net_margin_level = "亏损"

    if gross_margin > 20 and net_margin > 10:
        overall_assessment = "财务结构较优，主营盈利能力较强。"
    elif gross_margin > 10 and net_margin > 5:
        overall_assessment = "主营业务具备一定盈利质量，整体经营相对稳健。"
    elif net_margin < 0:
        overall_assessment = "当前净利润为负，财务表现承压，需要重点关注降本与景气修复。"
    else:
        overall_assessment = "盈利能力处于中性区间，需结合行业周期继续观察。"

    suggestions: list[str] = []
    if gross_margin <= 10:
        suggestions.append("关注主营业务毛利率修复及价格竞争压力。")
    if net_margin < 5:
        suggestions.append("关注费用率、减值损失与利润兑现能力。")
    if profit < 0:
        suggestions.append("建议重点评估行业景气、库存消化与现金流安全边际。")
    if not suggestions:
        suggestions.append("建议继续关注收入增长质量与全球化扩张节奏。")

    return {
        "company_name": company["company_name"],
        "period": company["period"],
        "revenue": revenue,
        "profit": profit,
        "gross_margin": gross_margin,
        "net_margin": net_margin,
        "gross_margin_level": gross_margin_level,
        "net_margin_level": net_margin_level,
        "overall_assessment": overall_assessment,
        "suggestions": suggestions,
        "business_summary": company.get("business_summary", ""),
        "risk_opportunity": company.get("risk_opportunity", ""),
    }
