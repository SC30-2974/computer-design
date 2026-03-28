from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class ReportRequest(BaseModel):
    company: str


class CompareReportRequest(BaseModel):
    companies: list[str]
    metric: str = 'revenue'
    period: str = '前三季度'


class FinancialDiagnosisResponse(BaseModel):
    company_name: str
    period: str
    revenue: float
    profit: float
    gross_margin: float
    net_margin: float
    gross_margin_level: str
    net_margin_level: str
    overall_assessment: str
    suggestions: list[str]
    business_summary: str
    risk_opportunity: str
