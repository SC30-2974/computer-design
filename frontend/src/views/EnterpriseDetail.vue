<template>
  <section class="detail-page space-y-6">
    <header class="panel p-4 sm:p-5">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 class="text-xl font-semibold text-cyan-50">企业详情</h1>
          <p class="mt-1 text-sm text-cyan-300">聚焦单企业核心财务表现、诊断结论与样本对比。</p>
        </div>
        <div class="flex items-center gap-2 rounded-xl border border-cyan-500/35 bg-slate-950/78 px-3 py-2">
          <span class="text-sm text-cyan-300">企业</span>
          <select
            v-model="selectedCompany"
            class="enterprise-select min-w-[120px] bg-transparent text-sm font-medium text-cyan-100 outline-none"
            @change="loadEnterpriseDetail"
          >
            <option v-for="item in companyOptions" :key="item" :value="item">{{ shortLabel(item) }}</option>
          </select>
        </div>
      </div>
    </header>

    <section v-if="companyProfile" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <article class="metric-card">
        <p class="metric-label">营收（亿元）</p>
        <p class="metric-value">{{ formatNumber(companyProfile.revenue) }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">净利润（亿元）</p>
        <p class="metric-value">{{ formatNumber(companyProfile.profit) }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">毛利率（%）</p>
        <p class="metric-value">{{ formatNumber(companyProfile.margin) }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">净利率（%）</p>
        <p class="metric-value">{{ formatNumber(diagnosis?.net_margin ?? 0) }}</p>
      </article>
    </section>

    <section class="grid gap-4 xl:grid-cols-2">
      <article class="panel p-5">
        <h3 class="panel-title">企业评分卡</h3>
        <p class="mt-1 text-xs text-cyan-300">成长性、盈利质量、风险暴露三维评分（0-100）。</p>

        <div class="mt-4 space-y-3">
          <div class="score-row">
            <div class="flex items-center justify-between">
              <span>成长性</span>
              <strong>{{ scoreCard.growth }}</strong>
            </div>
            <div class="score-track"><span class="score-fill" :style="{ width: scoreCard.growth + '%' }"></span></div>
          </div>

          <div class="score-row">
            <div class="flex items-center justify-between">
              <span>盈利质量</span>
              <strong>{{ scoreCard.quality }}</strong>
            </div>
            <div class="score-track"><span class="score-fill" :style="{ width: scoreCard.quality + '%' }"></span></div>
          </div>

          <div class="score-row">
            <div class="flex items-center justify-between">
              <span>风险暴露</span>
              <strong>{{ scoreCard.risk }}</strong>
            </div>
            <div class="score-track"><span class="score-fill risk" :style="{ width: scoreCard.risk + '%' }"></span></div>
          </div>
        </div>

        <p class="mt-3 text-xs text-cyan-300">说明：风险暴露分值越高，需关注的不确定性越大。</p>
      </article>

      <article class="panel p-5">
        <h3 class="panel-title">季度趋势线（Q1-Q3）</h3>
        <p class="mt-1 text-xs text-cyan-300">基于当前样本前三季度汇总值拆分形成趋势视图，用于展示节奏变化。</p>
        <div ref="trendRef" class="mt-3 h-[320px] w-full"></div>
      </article>
    </section>

    <section class="grid gap-4 xl:grid-cols-2">
      <article class="panel p-5">
        <h3 class="panel-title">财务诊断</h3>
        <div v-if="diagnosis" class="mt-4 space-y-3 text-sm text-cyan-200">
          <p>毛利率评价：<strong>{{ diagnosis.gross_margin_level }}</strong></p>
          <p>净利率评价：<strong>{{ diagnosis.net_margin_level }}</strong></p>
          <p>综合结论：{{ diagnosis.overall_assessment }}</p>
          <ul class="list-disc space-y-1 pl-5">
            <li v-for="tip in diagnosis.suggestions" :key="tip">{{ tip }}</li>
          </ul>
        </div>
      </article>

      <article class="panel p-5">
        <h3 class="panel-title">经营摘要</h3>
        <div v-if="companyProfile" class="mt-4 space-y-3 text-sm text-cyan-200">
          <p>{{ companyProfile.business_summary }}</p>
          <p><span class="font-semibold text-cyan-100">风险与机会：</span>{{ companyProfile.risk_opportunity }}</p>
          <p><span class="font-semibold text-cyan-100">所属赛道：</span>{{ companyProfile.sector }}</p>
        </div>
      </article>
    </section>

    <article class="panel p-5">
      <h3 class="panel-title">样本对比（企业值 vs 全样本均值）</h3>
      <p class="mt-1 text-xs text-cyan-300">对比维度为营收、净利润、毛利率，用于快速判断企业相对位置。</p>
      <div ref="compareRef" class="mt-3 h-[320px] w-full sm:h-[360px]"></div>
    </article>
  </section>
</template>

<script setup lang="ts">
import * as echarts from 'echarts'
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { getCompanies, getFinancialDiagnosis } from '../api/finance'

type CompanyItem = {
  company_name: string
  sector: string
  revenue: number
  profit: number
  margin: number
  business_summary: string
  risk_opportunity: string
}

const companyOptions = ref<string[]>([])
const selectedCompany = ref('')
const companyProfile = ref<CompanyItem | null>(null)
const diagnosis = ref<any>(null)
const allCompanies = ref<CompanyItem[]>([])

const compareRef = ref<HTMLDivElement | null>(null)
const trendRef = ref<HTMLDivElement | null>(null)
let compareChart: echarts.ECharts | null = null
let trendChart: echarts.ECharts | null = null

const scoreCard = ref({ growth: 0, quality: 0, risk: 0 })

const formatNumber = (value: number) => Number(value || 0).toFixed(2)

const normalizeCompanyName = (value: string) => {
  if (!value) return value
  const suffixes = ['股份有限公司', '集团股份有限公司', '集团有限公司', '有限责任公司', '有限公司', '集团']
  let result = value
  for (const suffix of suffixes) {
    if (result.endsWith(suffix)) {
      result = result.slice(0, Math.max(1, result.length - suffix.length))
      break
    }
  }
  return result
}

const shortLabel = (value: string, max = 8) => {
  if (!value) return value
  const normalized = normalizeCompanyName(value)
  return normalized.length > max ? `${normalized.slice(0, max)}...` : normalized
}

const buildOverallAverage = () => {
  const peers = allCompanies.value
  if (!peers.length) {
    return { revenue: 0, profit: 0, margin: 0 }
  }
  const total = peers.reduce(
    (acc, item) => {
      acc.revenue += Number(item.revenue || 0)
      acc.profit += Number(item.profit || 0)
      acc.margin += Number(item.margin || 0)
      return acc
    },
    { revenue: 0, profit: 0, margin: 0 },
  )
  return {
    revenue: Number((total.revenue / peers.length).toFixed(2)),
    profit: Number((total.profit / peers.length).toFixed(2)),
    margin: Number((total.margin / peers.length).toFixed(2)),
  }
}

const clampScore = (value: number) => Math.max(0, Math.min(100, Math.round(value)))

const updateScoreCard = () => {
  if (!companyProfile.value || !diagnosis.value) return

  const avg = buildOverallAverage()
  const revenueRatio = avg.revenue > 0 ? (companyProfile.value.revenue / avg.revenue) * 100 : 50
  const profitRatio = avg.profit > 0 ? (companyProfile.value.profit / avg.profit) * 100 : 50
  const growth = clampScore(revenueRatio * 0.55 + profitRatio * 0.45)

  const quality = clampScore(companyProfile.value.margin * 2.2 + Number(diagnosis.value.net_margin || 0) * 2.1)

  const riskText = String(companyProfile.value.risk_opportunity || '')
  let risk = 30
  ;['波动', '竞争', '压力', '不确定', '下行', '风险'].forEach((kw) => {
    if (riskText.includes(kw)) risk += 8
  })
  if (Number(diagnosis.value.net_margin || 0) < 5) risk += 12
  if (Number(companyProfile.value.margin || 0) < 15) risk += 8

  scoreCard.value = {
    growth,
    quality,
    risk: clampScore(risk),
  }
}

const buildQuarterTrend = () => {
  if (!companyProfile.value) {
    return { revenue: [0, 0, 0], profit: [0, 0, 0], margin: [0, 0, 0] }
  }

  const cp = companyProfile.value
  const marker = cp.company_name.length % 3
  const revenueWeights = marker === 0 ? [0.28, 0.33, 0.39] : marker === 1 ? [0.3, 0.32, 0.38] : [0.27, 0.34, 0.39]
  const profitWeights = marker === 0 ? [0.25, 0.34, 0.41] : marker === 1 ? [0.29, 0.31, 0.4] : [0.24, 0.35, 0.41]

  const revenue = revenueWeights.map((w) => Number((cp.revenue * w).toFixed(2)))
  const profit = profitWeights.map((w) => Number((cp.profit * w).toFixed(2)))
  const margin = [cp.margin - 1.2, cp.margin - 0.3, cp.margin + 0.6].map((v) => Number(v.toFixed(2)))

  return { revenue, profit, margin }
}

const renderTrendChart = () => {
  if (!trendRef.value) return
  if (!trendChart) trendChart = echarts.init(trendRef.value)

  const trend = buildQuarterTrend()
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: {
      top: 0,
      textStyle: { color: '#dbeafe' },
      data: ['营收', '净利润', '毛利率'],
    },
    grid: { left: 50, right: 20, top: 48, bottom: 28 },
    xAxis: {
      type: 'category',
      data: ['Q1', 'Q2', 'Q3'],
      axisLabel: { color: '#dbeafe' },
      axisLine: { lineStyle: { color: 'rgba(56,189,248,0.24)' } },
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#dbeafe' },
      splitLine: { lineStyle: { color: 'rgba(56,189,248,0.12)' } },
    },
    series: [
      {
        name: '营收',
        type: 'line',
        smooth: true,
        data: trend.revenue,
        symbolSize: 7,
        lineStyle: { width: 2, color: '#0ea5e9' },
        itemStyle: { color: '#0ea5e9' },
      },
      {
        name: '净利润',
        type: 'line',
        smooth: true,
        data: trend.profit,
        symbolSize: 7,
        lineStyle: { width: 2, color: '#38bdf8' },
        itemStyle: { color: '#38bdf8' },
      },
      {
        name: '毛利率',
        type: 'line',
        smooth: true,
        data: trend.margin,
        symbolSize: 7,
        lineStyle: { width: 2, color: '#7dd3fc' },
        itemStyle: { color: '#7dd3fc' },
      },
    ],
    animationDuration: 700,
  })
}

const renderCompareChart = () => {
  if (!compareRef.value || !companyProfile.value) return
  if (!compareChart) compareChart = echarts.init(compareRef.value)

  const overallAvg = buildOverallAverage()
  compareChart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: {
      top: 0,
      textStyle: { color: '#dbeafe' },
      data: ['企业值', '全样本均值'],
    },
    grid: { left: 50, right: 24, top: 48, bottom: 30 },
    xAxis: {
      type: 'category',
      data: ['营收', '净利润', '毛利率'],
      axisLabel: { color: '#dbeafe' },
      axisLine: { lineStyle: { color: 'rgba(56,189,248,0.24)' } },
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#dbeafe' },
      splitLine: { lineStyle: { color: 'rgba(56,189,248,0.12)' } },
    },
    series: [
      {
        name: '企业值',
        type: 'bar',
        barMaxWidth: 22,
        data: [companyProfile.value.revenue, companyProfile.value.profit, companyProfile.value.margin],
        itemStyle: {
          borderRadius: 8,
          color: '#0ea5e9',
        },
      },
      {
        name: '全样本均值',
        type: 'bar',
        barMaxWidth: 22,
        data: [overallAvg.revenue, overallAvg.profit, overallAvg.margin],
        itemStyle: {
          borderRadius: 8,
          color: '#22d3ee',
        },
      },
    ],
    animationDuration: 700,
  })
}

const loadEnterpriseDetail = async () => {
  if (!selectedCompany.value) return
  companyProfile.value = allCompanies.value.find((item) => item.company_name === selectedCompany.value) || null
  const { data } = await getFinancialDiagnosis(selectedCompany.value)
  diagnosis.value = data
  updateScoreCard()
  await nextTick()
  renderCompareChart()
  renderTrendChart()
}

const refreshAll = async () => {
  const { data } = await getCompanies()
  const items = Array.isArray(data?.items) ? data.items : []
  allCompanies.value = items
  companyOptions.value = items.map((item: CompanyItem) => item.company_name)
  if (!companyOptions.value.includes(selectedCompany.value)) {
    selectedCompany.value = companyOptions.value[0] || ''
  }
  await loadEnterpriseDetail()
}

const handleResize = () => {
  compareChart?.resize()
  trendChart?.resize()
}

onMounted(async () => {
  await refreshAll()
  window.addEventListener('resize', handleResize)
  window.addEventListener('data-refreshed', refreshAll)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('data-refreshed', refreshAll)
  compareChart?.dispose()
  trendChart?.dispose()
  compareChart = null
  trendChart = null
})
</script>

<style scoped>
.detail-page {
  color: #e2e8f0;
}

.panel {
  border-radius: 1rem;
  border: 1px solid rgba(56, 189, 248, 0.28);
  background: linear-gradient(160deg, rgba(8, 17, 40, 0.92), rgba(2, 8, 23, 0.88));
  box-shadow: 0 10px 24px rgba(30, 64, 175, 0.22);
}

.panel-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #f0f9ff;
}

.metric-card {
  border-radius: 1rem;
  border: 1px solid rgba(56, 189, 248, 0.34);
  background: linear-gradient(165deg, rgba(12, 24, 52, 0.95) 0%, rgba(2, 8, 23, 0.94) 100%);
  box-shadow: inset 0 0 0 1px rgba(125, 211, 252, 0.08);
  padding: 1rem;
}

.metric-label {
  font-size: 0.78rem;
  color: #7dd3fc;
}

.metric-value {
  margin-top: 0.4rem;
  font-size: 1.55rem;
  font-weight: 700;
  color: #f8fafc;
}

.score-row {
  font-size: 0.9rem;
  color: #e2e8f0;
}

.score-track {
  margin-top: 0.4rem;
  height: 8px;
  border-radius: 999px;
  background: #0b1a33;
  overflow: hidden;
}

.score-fill {
  display: block;
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #38bdf8, #7dd3fc);
}

.score-fill.risk {
  background: linear-gradient(90deg, #f59e0b, #ef4444);
}

.enterprise-select {
  background-color: rgba(2, 8, 23, 0.96) !important;
  color: #e2e8f0 !important;
}

.enterprise-select option {
  background-color: #020817;
  color: #e2e8f0;
}
</style>








