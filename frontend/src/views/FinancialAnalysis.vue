<template>
  <section class="space-y-5 rounded-3xl border border-emerald-300/25 bg-white/75 p-4 sm:p-6">
    <div class="flex flex-wrap items-center gap-3">
      <select v-model="metric" class="rounded-xl border border-emerald-300/30 bg-white px-4 py-2 text-sm text-emerald-900" @change="loadData">
        <option value="revenue">营收（亿元）</option>
        <option value="profit">净利润（亿元）</option>
        <option value="margin">毛利率（%）</option>
      </select>

      <select v-model="sector" class="rounded-xl border border-emerald-300/30 bg-white px-4 py-2 text-sm text-emerald-900" @change="loadData">
        <option value="">全部赛道</option>
        <option v-for="item in sectors" :key="item" :value="item">{{ item }}</option>
      </select>
    </div>

    <div ref="barRef" class="h-[320px] w-full sm:h-[380px] lg:h-[420px]"></div>

    <div class="rounded-2xl border border-emerald-300/30 bg-white/85 p-5">
      <div class="mb-3 flex items-center justify-between gap-3">
        <h3 class="text-lg font-semibold text-emerald-900">多企业对战模式</h3>
        <button class="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-500" @click="runBattle">
          生成对战结论
        </button>
      </div>

      <p class="mb-3 text-sm text-emerald-800/80">最多选择 4 家企业进行横向对比。</p>

      <div class="mb-4 flex flex-wrap gap-2">
        <label
          v-for="item in companyOptions"
          :key="item"
          class="inline-flex cursor-pointer items-center gap-2 rounded-full border px-3 py-1.5 text-xs"
          :class="selectedCompanies.includes(item) ? 'border-emerald-500 bg-emerald-100 text-emerald-900' : 'border-emerald-300/40 bg-white text-emerald-800'"
        >
          <input
            type="checkbox"
            class="hidden"
            :checked="selectedCompanies.includes(item)"
            @change="toggleCompany(item)"
          />
          <span :title="item">{{ shortLabel(item) }}</span>
        </label>
      </div>

      <div v-if="battleResult" class="grid gap-3 md:grid-cols-3">
        <div class="rounded-xl bg-emerald-50 p-3 text-sm text-emerald-900">营收冠军：{{ battleResult.winners.revenue }}</div>
        <div class="rounded-xl bg-emerald-50 p-3 text-sm text-emerald-900">净利润冠军：{{ battleResult.winners.profit }}</div>
        <div class="rounded-xl bg-emerald-50 p-3 text-sm text-emerald-900">毛利率冠军：{{ battleResult.winners.margin }}</div>
      </div>

      <div class="mt-5 rounded-xl border border-emerald-300/20 bg-white p-3">
        <p class="mb-2 text-sm font-medium text-emerald-900">企业对比雷达图</p>
        <div ref="radarRef" class="h-[280px] w-full sm:h-[320px]"></div>
      </div>
    </div>

    <div class="rounded-2xl border border-emerald-300/30 bg-white/85 p-5">
      <div class="mb-3 flex items-center justify-between gap-3">
        <h3 class="text-lg font-semibold text-emerald-900">可追溯引用链</h3>
        <div class="flex flex-wrap gap-2">
          <button class="rounded-xl border border-emerald-300 bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-800 hover:bg-emerald-100" @click="exportCompareReport">
            导出对比报告
          </button>
          <button class="rounded-xl border border-emerald-300 bg-white px-4 py-2 text-sm font-semibold text-emerald-800 hover:bg-emerald-50" @click="exportComparePdf">
            导出 PDF 报告
          </button>
        </div>
      </div>

      <div class="overflow-x-auto rounded-xl border border-emerald-300/20">
        <table class="min-w-full text-sm">
          <thead class="bg-emerald-50 text-emerald-800">
            <tr>
              <th class="px-3 py-2 text-left">企业</th>
              <th class="px-3 py-2 text-left">赛道</th>
              <th class="px-3 py-2 text-left">当前指标值</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-emerald-300/15 bg-white text-emerald-900">
            <tr v-for="item in citationRows" :key="item.company_name">
              <td class="px-3 py-2" :title="item.company_name">{{ shortLabel(item.company_name) }}</td>
              <td class="px-3 py-2">{{ item.sector }}</td>
              <td class="px-3 py-2">{{ item.value }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import * as echarts from 'echarts'
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  downloadPdfFromText,
  downloadTextFile,
  generateCompareReport,
  getCompanies,
  getCompanyBattle,
  getMetrics,
} from '../api/finance'

const barRef = ref<HTMLDivElement | null>(null)
const radarRef = ref<HTMLDivElement | null>(null)
let barChart: echarts.ECharts | null = null
let radarChart: echarts.ECharts | null = null

const metric = ref<'revenue' | 'profit' | 'margin'>('revenue')
const sector = ref('')
const sectors = ref<string[]>([])

// 对战区状态。
const companyOptions = ref<string[]>([])
const selectedCompanies = ref<string[]>([])
const battleResult = ref<any | null>(null)

// 引用链表格数据。
const citationRows = ref<any[]>([])
const allCompanies = ref<any[]>([])

const metricNameMap: Record<string, string> = {
  revenue: '营收（亿元）',
  profit: '净利润（亿元）',
  margin: '毛利率（%）',
}

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

const shortLabel = (value: string, max = 6) => {
  if (!value) return value
  const normalized = normalizeCompanyName(value)
  return normalized.length > max ? `${normalized.slice(0, max)}...` : normalized
}

const updateSectors = (items: any[]) => {
  const values = Array.from(new Set(items.map((item) => String(item.sector || '')).filter(Boolean)))
  sectors.value = values
}

const loadData = async () => {
  const { data } = await getMetrics(metric.value, '前三季度', sector.value)
  const items = Array.isArray(data?.items) ? data.items : []

  if (!sector.value) {
    updateSectors(items)
  }

  citationRows.value = items

  const names = items.map((item: any) => item.company_name)
  const values = items.map((item: any) => Number(item.value || 0))

  if (!barRef.value) return
  if (!barChart) {
    barChart = echarts.init(barRef.value)
  }

  barChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
    },
    grid: { left: 110, right: 40, top: 35, bottom: 30 },
    xAxis: {
      type: 'value',
      name: metricNameMap[metric.value],
      axisLabel: { color: '#065f46' },
      splitLine: { lineStyle: { color: 'rgba(110,231,183,0.2)' } },
    },
    yAxis: {
      type: 'category',
      data: names,
      axisLabel: {
        color: '#064e3b',
        formatter: (value: string) => shortLabel(value),
      },
      axisTick: { show: false },
    },
    series: [
      {
        type: 'bar',
        data: values,
        barWidth: 18,
        showBackground: true,
        backgroundStyle: {
          color: 'rgba(16,185,129,0.12)',
          borderRadius: 10,
        },
        itemStyle: {
          borderRadius: 10,
          color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
            { offset: 0, color: '#10b981' },
            { offset: 1, color: '#22c55e' },
          ]),
          shadowBlur: 12,
          shadowColor: 'rgba(34,197,94,0.45)',
        },
        animationDuration: 1200,
        animationEasing: 'elasticOut',
      },
    ],
  })
}

const refreshAll = async () => {
  const companyRes = await getCompanies()
  const companies = Array.isArray(companyRes?.data?.items) ? companyRes.data.items : []
  allCompanies.value = companies
  companyOptions.value = companies.map((item: any) => item.company_name)
  selectedCompanies.value = companyOptions.value.slice(0, 2)
  await nextTick()
  await loadData()
  renderRadarChart()
}

const toggleCompany = (name: string) => {
  if (selectedCompanies.value.includes(name)) {
    selectedCompanies.value = selectedCompanies.value.filter((item) => item !== name)
    return
  }
  if (selectedCompanies.value.length >= 4) return
  selectedCompanies.value = [...selectedCompanies.value, name]
}

const runBattle = async () => {
  if (selectedCompanies.value.length < 2) {
    return
  }
  const { data } = await getCompanyBattle(selectedCompanies.value)
  battleResult.value = data
}

const exportCompareReport = async () => {
  if (selectedCompanies.value.length < 2) {
    return
  }
  const { data } = await generateCompareReport(selectedCompanies.value, metric.value, '前三季度')
  const content = `${data.report_text}\n\n引用链:\n${(data.citations || [])
    .map((item: any) => `- ${item.company_name}: ${item.source}`)
    .join('\n')}`
  downloadTextFile('多企业对比报告.txt', content)
}

const exportComparePdf = async () => {
  if (selectedCompanies.value.length < 2) return
  const { data } = await generateCompareReport(selectedCompanies.value, metric.value, '前三季度')
  const content = `${data.report_text}\n\n引用链:\n${(data.citations || [])
    .map((item: any) => `- ${item.company_name}: ${item.source}`)
    .join('\n')}`
  downloadPdfFromText('多企业对比报告', content)
}

const renderRadarChart = () => {
  if (!radarRef.value) return
  if (!radarChart) {
    radarChart = echarts.init(radarRef.value)
  }

  const rows = allCompanies.value.filter((item) => selectedCompanies.value.includes(item.company_name))
  if (rows.length < 2) {
    radarChart.clear()
    return
  }

  const maxRevenue = Math.max(...rows.map((x) => Number(x.revenue || 0)), 1)
  const maxProfit = Math.max(...rows.map((x) => Number(x.profit || 0)), 1)
  const maxMargin = Math.max(...rows.map((x) => Number(x.margin || 0)), 1)

  const seriesData = rows.map((row) => ({
    name: row.company_name,
    value: [
      Number(((Number(row.revenue || 0) / maxRevenue) * 100).toFixed(2)),
      Number(((Number(row.profit || 0) / maxProfit) * 100).toFixed(2)),
      Number(((Number(row.margin || 0) / maxMargin) * 100).toFixed(2)),
    ],
    raw: row,
  }))

  radarChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const raw = params.data.raw
        return `${params.name}<br/>营收：${raw.revenue} 亿元<br/>净利润：${raw.profit} 亿元<br/>毛利率：${raw.margin}%`
      },
    },
    legend: {
      bottom: 0,
      textStyle: { color: '#065f46' },
    },
    radar: {
      radius: '62%',
      indicator: [
        { name: '营收', max: 100 },
        { name: '净利润', max: 100 },
        { name: '毛利率', max: 100 },
      ],
      splitLine: { lineStyle: { color: 'rgba(16,185,129,0.22)' } },
      splitArea: { areaStyle: { color: ['rgba(16,185,129,0.02)', 'rgba(16,185,129,0.05)'] } },
      axisLine: { lineStyle: { color: 'rgba(16,185,129,0.3)' } },
      name: { color: '#065f46' },
    },
    series: [
      {
        type: 'radar',
        data: seriesData,
        areaStyle: { opacity: 0.16 },
        lineStyle: { width: 2 },
        symbolSize: 5,
      },
    ],
    color: ['#10b981', '#14b8a6', '#22c55e', '#0ea5e9'],
  })
}

const handleResize = () => {
  barChart?.resize()
  radarChart?.resize()
}

onMounted(async () => {
  await refreshAll()
  window.addEventListener('resize', handleResize)
  window.addEventListener('data-refreshed', refreshAll)
})

watch(selectedCompanies, () => {
  renderRadarChart()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('data-refreshed', refreshAll)
  barChart?.dispose()
  radarChart?.dispose()
  barChart = null
  radarChart = null
})
</script>
