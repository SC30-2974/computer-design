<template>
  <section class="detail-page space-y-6">
    <header class="panel p-4 sm:p-5">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 class="text-xl font-semibold text-emerald-950">企业详情</h1>
          <p class="mt-1 text-sm text-emerald-700">聚焦单企业核心财务表现、诊断结论与样本对比。</p>
        </div>
        <div class="flex items-center gap-2 rounded-xl border border-emerald-200 bg-white px-3 py-2">
          <span class="text-sm text-emerald-700">企业</span>
          <select
            v-model="selectedCompany"
            class="min-w-[120px] bg-transparent text-sm font-medium text-emerald-900 outline-none"
            @change="loadEnterpriseDetail"
          >
            <option v-for="item in companyOptions" :key="item" :value="item">{{ item }}</option>
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
        <h3 class="panel-title">财务诊断</h3>
        <div v-if="diagnosis" class="mt-4 space-y-3 text-sm text-emerald-800">
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
        <div v-if="companyProfile" class="mt-4 space-y-3 text-sm text-emerald-800">
          <p>{{ companyProfile.business_summary }}</p>
          <p><span class="font-semibold text-emerald-900">风险与机会：</span>{{ companyProfile.risk_opportunity }}</p>
          <p><span class="font-semibold text-emerald-900">所属赛道：</span>{{ companyProfile.sector }}</p>
        </div>
      </article>
    </section>

    <article class="panel p-5">
      <h3 class="panel-title">样本对比（企业值 vs 全样本均值）</h3>
      <p class="mt-1 text-xs text-emerald-700">对比维度为营收、净利润、毛利率，用于快速判断企业相对位置。</p>
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
let compareChart: echarts.ECharts | null = null

const formatNumber = (value: number) => Number(value || 0).toFixed(2)

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

const renderCompareChart = () => {
  if (!compareRef.value || !companyProfile.value) return
  if (!compareChart) compareChart = echarts.init(compareRef.value)

  const overallAvg = buildOverallAverage()
  compareChart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: {
      top: 0,
      textStyle: { color: '#064e3b' },
      data: ['企业值', '全样本均值'],
    },
    grid: { left: 50, right: 24, top: 48, bottom: 30 },
    xAxis: {
      type: 'category',
      data: ['营收', '净利润', '毛利率'],
      axisLabel: { color: '#065f46' },
      axisLine: { lineStyle: { color: 'rgba(16,185,129,0.24)' } },
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#065f46' },
      splitLine: { lineStyle: { color: 'rgba(16,185,129,0.12)' } },
    },
    series: [
      {
        name: '企业值',
        type: 'bar',
        barMaxWidth: 22,
        data: [companyProfile.value.revenue, companyProfile.value.profit, companyProfile.value.margin],
        itemStyle: {
          borderRadius: 8,
          color: '#0f766e',
        },
      },
      {
        name: '全样本均值',
        type: 'bar',
        barMaxWidth: 22,
        data: [overallAvg.revenue, overallAvg.profit, overallAvg.margin],
        itemStyle: {
          borderRadius: 8,
          color: '#6ee7b7',
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
  await nextTick()
  renderCompareChart()
}

const handleResize = () => compareChart?.resize()

onMounted(async () => {
  const { data } = await getCompanies()
  const items = Array.isArray(data?.items) ? data.items : []
  allCompanies.value = items
  companyOptions.value = items.map((item: CompanyItem) => item.company_name)
  selectedCompany.value = companyOptions.value[0] || ''
  await loadEnterpriseDetail()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  compareChart?.dispose()
  compareChart = null
})
</script>

<style scoped>
.detail-page {
  color: #065f46;
}

.panel {
  border-radius: 1rem;
  border: 1px solid rgba(16, 185, 129, 0.22);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 8px 20px rgba(6, 95, 70, 0.04);
}

.panel-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #064e3b;
}

.metric-card {
  border-radius: 1rem;
  border: 1px solid rgba(16, 185, 129, 0.2);
  background: linear-gradient(180deg, #ffffff 0%, #f4fff9 100%);
  padding: 1rem;
}

.metric-label {
  font-size: 0.78rem;
  color: #0f766e;
}

.metric-value {
  margin-top: 0.4rem;
  font-size: 1.55rem;
  font-weight: 700;
  color: #064e3b;
}
</style>
