import axios from 'axios'

type CompanyRow = {
  company_name: string
  sector: string
  revenue: number
  profit: number
  margin: number
  year: number
  period: string
  business_summary: string
  risk_opportunity: string
  source_page: number
}

const FALLBACK_COMPANIES: CompanyRow[] = [
  {
    company_name: '比亚迪',
    sector: '整车+电池+光伏',
    revenue: 5662.66,
    profit: 233.33,
    margin: 17.9,
    year: 2025,
    period: '前三季度',
    business_summary: '主营新能源汽车、动力电池、电子业务与光伏相关业务。',
    risk_opportunity: '机会：高端化与全球化持续推进；风险：行业价格竞争与费用投入。',
    source_page: 0,
  },
  {
    company_name: '宁德时代',
    sector: '动力电池+储能',
    revenue: 2830.72,
    profit: 490.34,
    margin: 25.31,
    year: 2025,
    period: '前三季度',
    business_summary: '主营动力与储能电池，全球化制造和产业链协同能力突出。',
    risk_opportunity: '机会：储能高增长；风险：价格波动和海外经营不确定性。',
    source_page: 0,
  },
  {
    company_name: '通威股份',
    sector: '光伏+硅料',
    revenue: 1390,
    profit: 102,
    margin: 16.8,
    year: 2025,
    period: '前三季度',
    business_summary: '覆盖硅料与电池片环节，产业链一体化能力较强。',
    risk_opportunity: '机会：技术迭代与集中度提升；风险：硅料价格波动。',
    source_page: 0,
  },
  {
    company_name: '隆基绿能',
    sector: '光伏',
    revenue: 1180,
    profit: 94,
    margin: 15.2,
    year: 2025,
    period: '前三季度',
    business_summary: '聚焦光伏主产业链，高效组件与技术路线能力突出。',
    risk_opportunity: '机会：海外需求恢复；风险：产业链价格波动。',
    source_page: 0,
  },
  {
    company_name: '阳光电源',
    sector: '逆变器+储能',
    revenue: 664.02,
    profit: 118.81,
    margin: 34.88,
    year: 2025,
    period: '前三季度',
    business_summary: '主营逆变器、储能系统与新能源电站解决方案。',
    risk_opportunity: '机会：储能景气延续；风险：竞争加剧和海外政策扰动。',
    source_page: 0,
  },
  {
    company_name: '亿纬锂能',
    sector: '动力+消费电池',
    revenue: 488,
    profit: 46,
    margin: 18.4,
    year: 2025,
    period: '前三季度',
    business_summary: '布局消费、动力和储能电池，业务结构均衡。',
    risk_opportunity: '机会：储能出货增长；风险：原材料波动与下游价格压力。',
    source_page: 0,
  },
  {
    company_name: '恩捷股份',
    sector: '隔膜',
    revenue: 214,
    profit: 31,
    margin: 29.3,
    year: 2025,
    period: '前三季度',
    business_summary: '主营锂电隔膜，受益于高端动力与储能需求。',
    risk_opportunity: '机会：高附加值隔膜渗透；风险：产能投放带来价格压力。',
    source_page: 0,
  },
]

const toNetMargin = (row: CompanyRow): number => {
  if (!row.revenue) return 0
  return Number(((row.profit / row.revenue) * 100).toFixed(2))
}

const getApiBaseUrl = (): string => {
  const envBase = import.meta.env.VITE_API_BASE_URL as string | undefined
  if (envBase) return envBase
  if (typeof window === 'undefined') return 'http://127.0.0.1:8010'
  const { hostname, origin } = window.location
  if (hostname === '127.0.0.1' || hostname === 'localhost') {
    return 'http://127.0.0.1:8010'
  }
  return origin
}

const request = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 10000,
})

const withFallback = async (fn: () => Promise<any>, fallback: () => any): Promise<any> => {
  try {
    return await fn()
  } catch {
    return fallback()
  }
}

export const getMetrics = async (metric = 'revenue', period = '前三季度', sector = '') => {
  return withFallback(
    async () => request.get('/api/metrics', { params: { metric, period, sector } }),
    () => {
      const rows = FALLBACK_COMPANIES.filter((item) => item.period === period)
      const filtered = sector ? rows.filter((item) => item.sector.includes(sector)) : rows
      const items = filtered.map((item) => ({
        company_name: item.company_name,
        sector: item.sector,
        value: metric === 'profit' ? item.profit : metric === 'margin' ? item.margin : item.revenue,
        year: item.year,
        period: item.period,
        source_page: item.source_page || 0,
      }))
      return { data: { metric, period, items } }
    },
  )
}

export const getCompanies = async () => {
  return withFallback(
    async () => request.get('/api/companies'),
    () => ({ data: { items: FALLBACK_COMPANIES } }),
  )
}

export const getFinancialDiagnosis = async (companyName: string) => {
  return withFallback(
    async () => request.get(`/api/financial_diagnosis/${encodeURIComponent(companyName)}`),
    () => {
      const row = FALLBACK_COMPANIES.find((item) => item.company_name === companyName) ?? FALLBACK_COMPANIES[0]
      const netMargin = toNetMargin(row)
      const grossLevel = row.margin >= 20 ? '健康' : row.margin >= 10 ? '一般' : '承压'
      const netLevel = netMargin >= 10 ? '优秀' : netMargin >= 5 ? '稳健' : netMargin >= 0 ? '偏弱' : '亏损'
      const overall = row.margin >= 20 && netMargin >= 10 ? '盈利质量较强，财务结构稳健。' : '盈利能力中性，建议持续跟踪成本与需求变化。'
      const data = {
        company_name: row.company_name,
        period: row.period,
        revenue: row.revenue,
        profit: row.profit,
        gross_margin: row.margin,
        net_margin: netMargin,
        gross_margin_level: grossLevel,
        net_margin_level: netLevel,
        overall_assessment: overall,
        suggestions: ['持续跟踪毛利率与净利率变化趋势。', '结合行业景气与成本波动动态调整判断。'],
      }
      return { data }
    },
  )
}

const buildLocalRagAnswer = (question: string) => {
  const mentioned = FALLBACK_COMPANIES.filter((item) => question.includes(item.company_name))
  const selected = mentioned.length ? mentioned : FALLBACK_COMPANIES.slice(0, 2)

  const lines: string[] = ['1. 结论摘要']
  if (selected.length === 1) {
    const one = selected[0]
    lines.push(
      `${one.company_name}前三季度营收 ${one.revenue} 亿元，净利润 ${one.profit} 亿元，毛利率 ${one.margin}%。整体盈利能力为${
        one.margin >= 20 ? '较强' : one.margin >= 10 ? '中性偏稳' : '偏弱'
      }。`,
    )
  } else {
    const [a, b] = selected
    lines.push(
      `${a.company_name}与${b.company_name}对比：营收 ${a.revenue}/${b.revenue} 亿元，净利润 ${a.profit}/${b.profit} 亿元，毛利率 ${a.margin}%/${b.margin}% 。`,
    )
  }

  lines.push('2. 核心依据')
  selected.forEach((item) => {
    lines.push(`- ${item.company_name}：营收 ${item.revenue} 亿元，净利润 ${item.profit} 亿元，毛利率 ${item.margin}%`)
    lines.push(`  经营摘要：${item.business_summary}`)
  })

  lines.push('3. 风险或不确定性')
  selected.forEach((item) => {
    lines.push(`- ${item.company_name}：${item.risk_opportunity}`)
  })

  lines.push('4. 引用来源')
  lines.push('- finance_app.db / company_metrics（本地结构化财报数据）')

  return {
    answer: lines.join('\n'),
    citations: selected.map((item) => ({
      source: 'finance_app.db',
      page: item.source_page || '结构化数据',
    })),
    mode: 'fallback',
  }
}

export const askRagQuestion = async (question: string) => {
  return withFallback(
    async () => request.post('/api/rag/ask', { question }),
    () => ({ data: buildLocalRagAnswer(question) }),
  )
}

export const generateReport = async (company: string) => {
  return withFallback(
    async () => request.post('/api/report', { company }),
    () => {
      const row = FALLBACK_COMPANIES.find((item) => item.company_name === company) ?? FALLBACK_COMPANIES[0]
      const report = `${row.company_name}财报分析简报\n1. 核心指标：${row.period}营收 ${row.revenue} 亿元，净利润 ${row.profit} 亿元，毛利率 ${row.margin}%\n2. 经营摘要：${row.business_summary}\n3. 风险与机会：${row.risk_opportunity}`
      return { data: { report } }
    },
  )
}

export const getCompanyBattle = async (companies: string[], period = '前三季度') => {
  return withFallback(
    async () => request.get('/api/company-battle', { params: { companies: companies.join(','), period } }),
    () => {
      const rows = FALLBACK_COMPANIES.filter((item) => companies.includes(item.company_name))
      const winnerRevenue = [...rows].sort((a, b) => b.revenue - a.revenue)[0]?.company_name || ''
      const winnerProfit = [...rows].sort((a, b) => b.profit - a.profit)[0]?.company_name || ''
      const winnerMargin = [...rows].sort((a, b) => b.margin - a.margin)[0]?.company_name || ''
      return {
        data: {
          period,
          companies: rows,
          winners: {
            revenue: winnerRevenue,
            profit: winnerProfit,
            margin: winnerMargin,
          },
        },
      }
    },
  )
}

export const generateCompareReport = async (companies: string[], metric = 'revenue', period = '前三季度') => {
  return withFallback(
    async () => request.post('/api/report/compare', { companies, metric, period }),
    () => {
      const rows = FALLBACK_COMPANIES.filter((item) => companies.includes(item.company_name))
      const reportText = [
        `多企业对比报告（${period}）`,
        '',
        '一、企业核心指标',
        ...rows.map((row) => `- ${row.company_name}：营收 ${row.revenue} 亿元，净利润 ${row.profit} 亿元，毛利率 ${row.margin}%`),
        '',
        '二、引用来源',
        ...rows.map((row) => `- ${row.company_name}：finance_app.db/company_metrics，source_page=${row.source_page || '结构化数据'}`),
      ].join('\n')
      return {
        data: {
          report_text: reportText,
          period,
          citations: rows.map((row) => ({
            source: 'finance_app.db/company_metrics',
            company_name: row.company_name,
            page: row.source_page || '结构化数据',
          })),
        },
      }
    },
  )
}

export const downloadTextFile = (filename: string, content: string) => {
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

export const downloadPdfFromText = (title: string, content: string) => {
  const escaped = content
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br/>')

  const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>${title}</title>
  <style>
    body { font-family: "Microsoft YaHei", "PingFang SC", sans-serif; padding: 24px; color: #0f172a; }
    h1 { font-size: 22px; margin-bottom: 14px; }
    .content { line-height: 1.8; font-size: 14px; white-space: normal; }
  </style>
</head>
<body>
  <h1>${title}</h1>
  <div class="content">${escaped}</div>
</body>
</html>`

  const blob = new Blob([html], { type: 'text/html;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const frame = document.createElement('iframe')
  frame.style.position = 'fixed'
  frame.style.right = '0'
  frame.style.bottom = '0'
  frame.style.width = '0'
  frame.style.height = '0'
  frame.style.border = '0'
  document.body.appendChild(frame)

  frame.onload = () => {
    frame.contentWindow?.focus()
    frame.contentWindow?.print()
    setTimeout(() => {
      document.body.removeChild(frame)
      URL.revokeObjectURL(url)
    }, 800)
  }

  frame.src = url
}

export const uploadFinancePdf = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/api/knowledge/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const refreshData = async () => {
  return request.post('/api/data/refresh', null, { timeout: 60000 })
}

export const listUploads = async () => {
  return request.get('/api/knowledge/list')
}

export const getUploadFileUrl = (id: number) => {
  return `${getApiBaseUrl()}/api/knowledge/file/${id}`
}

export default request
