<template>
  <section class="space-y-6 p-4 sm:p-5">
    <div class="flex flex-wrap items-center gap-3">
      <select v-model="metric" class="report-select rounded-xl border border-cyan-500/30 px-5 py-2.5 text-base font-semibold text-cyan-100" @change="loadData">
        <option value="revenue">营收（亿元）</option>
        <option value="profit">净利润（亿元）</option>
        <option value="margin">毛利率（%）</option>
      </select>

      <select v-model="sector" class="report-select rounded-xl border border-cyan-500/30 px-5 py-2.5 text-base font-semibold text-cyan-100" @change="loadData">
        <option value="">全部赛道</option>
        <option v-for="item in sectors" :key="item" :value="item">{{ item }}</option>
      </select>
    </div>

    <div ref="barRef" class="h-[320px] w-full sm:h-[380px] lg:h-[420px]"></div>

    <div class="border-t border-cyan-500/20 pt-5">
      <div class="mb-3 flex items-center justify-between gap-3">
        <h3 class="text-xl font-semibold text-cyan-100">多企业对战模式</h3>
        <button class="rounded-xl bg-cyan-600 px-5 py-2.5 text-base font-semibold text-cyan-50 hover:bg-cyan-500" @click="runBattle">
          生成对战结论
        </button>
      </div>

      <p class="mb-3 text-base text-cyan-200/80">最多选择 4 家企业进行横向对比。</p>

      <div class="mb-4 flex flex-wrap gap-2">
        <label
          v-for="item in companyOptions"
          :key="item"
          class="inline-flex cursor-pointer items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold"
          :class="selectedCompanies.includes(item) ? 'border-cyan-500/45 bg-cyan-900/60 text-cyan-100' : 'border-cyan-500/35 bg-slate-950/78 text-cyan-200'"
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
        <div class="rounded-xl bg-cyan-950/70 p-3 text-base font-semibold text-cyan-100">营收冠军：{{ battleResult.winners.revenue }}</div>
        <div class="rounded-xl bg-cyan-950/70 p-3 text-base font-semibold text-cyan-100">净利润冠军：{{ battleResult.winners.profit }}</div>
        <div class="rounded-xl bg-cyan-950/70 p-3 text-base font-semibold text-cyan-100">毛利率冠军：{{ battleResult.winners.margin }}</div>
      </div>

      <div class="mt-5 p-1">
        <p class="mb-2 text-base font-semibold text-cyan-100">企业对比雷达图</p>
        <div ref="radarRef" class="h-[280px] w-full sm:h-[320px]"></div>
      </div>
    </div>

    <div class="border-t border-cyan-500/20 pt-5">
      <div class="mb-3 flex items-center justify-between gap-3">
        <h3 class="text-xl font-semibold text-cyan-100">企业对比报告</h3>
        <div class="flex flex-wrap items-center gap-2">
          <select v-model="reportSector" class="report-select rounded-xl border border-cyan-500/30 px-4 py-2 text-sm font-semibold text-cyan-100">
            <option value="">全部赛道</option>
            <option v-for="item in sectors" :key="`report-${item}`" :value="item">{{ item }}</option>
          </select>
          <button class="rounded-xl border border-cyan-500/45 bg-slate-950/78 px-5 py-2.5 text-base font-semibold text-cyan-200 hover:bg-cyan-950/70" @click="exportComparePdf">
            导出 PDF 报告
          </button>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full text-base">
          <thead class="bg-cyan-950/70 text-cyan-200">
            <tr>
              <th class="px-3 py-2 text-left">企业</th>
              <th class="px-3 py-2 text-left">赛道</th>
              <th class="px-3 py-2 text-left">营收（亿元）</th>
              <th class="px-3 py-2 text-left">净利润（亿元）</th>
              <th class="px-3 py-2 text-left">毛利率（%）</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-cyan-800/30 bg-slate-950/78 text-cyan-100">
            <tr v-for="item in reportRows" :key="item.company_name">
              <td class="px-3 py-2" :title="item.company_name">{{ shortLabel(item.company_name) }}</td>
              <td class="px-3 py-2">{{ item.sector }}</td>
              <td class="px-3 py-2">{{ item.revenue }}</td>
              <td class="px-3 py-2">{{ item.profit }}</td>
              <td class="px-3 py-2">{{ item.margin }}</td>
            </tr>
            <tr v-if="!reportRows.length">
              <td colspan="5" class="px-3 py-5 text-center text-cyan-300/80">当前赛道暂无可导出数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import * as echarts from 'echarts'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  downloadPdfTable,
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
const reportSector = ref('')
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

const reportRows = computed(() => {
  if (!reportSector.value) return citationRows.value
  return citationRows.value.filter((item) => String(item.sector) === reportSector.value)
})

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
  if (reportSector.value && !values.includes(reportSector.value)) {
    reportSector.value = ''
  }
}

const loadData = async () => {
  const { data } = await getMetrics(metric.value, '前三季度', sector.value)
  const items = Array.isArray(data?.items) ? data.items : []

  if (!sector.value) {
    updateSectors(items)
  }

  // 表格改为企业对比报告：固定展示营收/净利润/毛利率三列。
  const orderByMetric = items.map((item: any) => String(item.company_name))
  const companyMap = new Map(allCompanies.value.map((item: any) => [String(item.company_name), item]))
  citationRows.value = orderByMetric
    .map((name) => companyMap.get(name))
    .filter(Boolean)
    .map((item: any) => ({
      company_name: item.company_name,
      sector: item.sector,
      revenue: Number(item.revenue || 0).toFixed(2),
      profit: Number(item.profit || 0).toFixed(2),
      margin: Number(item.margin || 0).toFixed(2),
    }))

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
    grid: { left: 140, right: 56, top: 42, bottom: 42 },
    xAxis: {
      type: 'value',
      name: metricNameMap[metric.value],
      nameTextStyle: { color: '#dbeafe', fontSize: 16, fontWeight: 700 },
      axisLabel: { color: '#dbeafe', fontSize: 15, fontWeight: 600 },
      splitLine: { lineStyle: { color: 'rgba(34,211,238,0.2)' } },
    },
    yAxis: {
      type: 'category',
      data: names,
      axisLabel: {
        color: '#dbeafe',
        fontSize: 15,
        fontWeight: 600,
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
          color: 'rgba(56,189,248,0.12)',
          borderRadius: 10,
        },
        itemStyle: {
          borderRadius: 10,
          color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
            { offset: 0, color: '#38bdf8' },
            { offset: 1, color: '#0284c7' },
          ]),
          shadowBlur: 12,
          shadowColor: 'rgba(14,165,233,0.45)',
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

const exportComparePdf = async () => {
  if (!reportRows.value.length) return

  const columns = ['企业', '赛道', '营收（亿元）', '净利润（亿元）', '毛利率（%）']
  const rows = reportRows.value.map((item) => [item.company_name, item.sector, item.revenue, item.profit, item.margin])
  downloadPdfTable('企业对比报告', columns, rows)
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
      textStyle: { color: '#dbeafe', fontSize: 15, fontWeight: 600 },
    },
    radar: {
      radius: '62%',
      indicator: [
        { name: '营收', max: 100 },
        { name: '净利润', max: 100 },
        { name: '毛利率', max: 100 },
      ],
      splitLine: { lineStyle: { color: 'rgba(56,189,248,0.22)' } },
      splitArea: { areaStyle: { color: ['rgba(56,189,248,0.02)', 'rgba(56,189,248,0.05)'] } },
      axisLine: { lineStyle: { color: 'rgba(56,189,248,0.3)' } },
      name: { color: '#dbeafe', fontSize: 15, fontWeight: 700 },
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
    color: ['#38bdf8', '#14b8a6', '#0284c7', '#0ea5e9'],
  })
}

const handleResize = () => {
  barChart?.resize()
  radarChart?.resize()
}

const handleStorageRefresh = (event: StorageEvent) => {
  if (event.key === 'dataRefreshAt') {
    refreshAll()
  }
}

onMounted(async () => {
  await refreshAll()
  window.addEventListener('resize', handleResize)
  window.addEventListener('data-refreshed', refreshAll)
  window.addEventListener('storage', handleStorageRefresh)
})

watch(selectedCompanies, () => {
  renderRadarChart()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('data-refreshed', refreshAll)
  window.removeEventListener('storage', handleStorageRefresh)
  barChart?.dispose()
  radarChart?.dispose()
  barChart = null
  radarChart = null
})
</script>

<style scoped>
.report-select {
  background-color: rgba(2, 8, 23, 0.95) !important;
  color: #dbeafe !important;
}

.report-select option {
  background-color: #020817;
  color: #dbeafe;
}
</style>








