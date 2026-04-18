<template>
  <section class="flex min-h-full flex-col gap-6">
    <div class="grid gap-4 md:grid-cols-3">
      <article class="rounded-2xl border border-cyan-500/30 bg-slate-950/75 p-5 shadow-[0_12px_30px_rgba(56,189,248,0.18)]">
        <p class="text-xs uppercase tracking-widest text-cyan-300">收录企业数</p>
        <p class="mt-3 text-3xl font-semibold text-cyan-100">{{ totalCompanies }}</p>
      </article>
      <article class="rounded-2xl border border-cyan-500/30 bg-slate-950/75 p-5 shadow-[0_12px_30px_rgba(56,189,248,0.18)]">
        <p class="text-xs uppercase tracking-widest text-cyan-300">前三季度总营收</p>
        <p class="mt-3 text-3xl font-semibold text-cyan-100">{{ totalRevenue.toLocaleString() }} 亿元</p>
      </article>
      <article class="rounded-2xl border border-cyan-500/30 bg-slate-950/75 p-5 shadow-[0_12px_30px_rgba(56,189,248,0.18)]">
        <p class="text-xs uppercase tracking-widest text-cyan-300">平均毛利率</p>
        <p class="mt-3 text-3xl font-semibold text-cyan-100">{{ avgMargin.toFixed(2) }}%</p>
      </article>
    </div>

    <div class="grid gap-6 lg:grid-cols-3">
      <div class="rounded-3xl border border-cyan-500/30 bg-slate-950/58 p-6 lg:col-span-3">
        <div class="mb-4 flex items-center justify-between gap-4">
          <h3 class="text-xl font-semibold text-cyan-100">新能源各赛道占比</h3>
          <p class="text-sm text-cyan-300">按赛道聚合企业营收 / 净利润（亿元）</p>
        </div>
        <div class="grid gap-5 xl:grid-cols-2">
          <div class="rounded-2xl border border-cyan-500/25 bg-slate-950/58 p-4">
            <div class="mb-2 flex items-center justify-between">
              <p class="text-sm font-semibold text-cyan-100">营收占比</p>
              <p class="text-xs text-cyan-300">按赛道聚合企业营收（亿元）</p>
            </div>
            <div ref="pieRef" class="h-[320px] w-full lg:h-[380px]"></div>
          </div>
          <div class="rounded-2xl border border-cyan-500/25 bg-slate-950/58 p-4">
            <div class="mb-2 flex items-center justify-between">
              <p class="text-sm font-semibold text-cyan-100">净利润占比</p>
              <p class="text-xs text-cyan-300">按赛道聚合净利润（亿元）</p>
            </div>
            <div ref="profitPieRef" class="h-[320px] w-full lg:h-[380px]"></div>
          </div>
        </div>
      </div>

      <div class="rounded-3xl border border-cyan-500/30 bg-slate-950/58 p-6 lg:col-span-3">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-xl font-semibold text-cyan-100">营收-净利润分布</h3>
        </div>
        <div ref="scatterRef" class="h-[520px] w-full lg:h-[680px]"></div>
      </div>
    </div>

    <section class="rounded-3xl border border-cyan-500/30 bg-slate-950/58 p-1">
      <div class="px-5 pt-5">
        <h3 class="text-lg font-semibold text-cyan-100">财务指标对比</h3>
      </div>
      <FinancialAnalysisView />
    </section>
  </section>
</template>

<script setup lang="ts">
import * as echarts from 'echarts'
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { getCompanies } from '../api/finance'
import FinancialAnalysisView from './FinancialAnalysis.vue'

const pieRef = ref<HTMLDivElement | null>(null)
const profitPieRef = ref<HTMLDivElement | null>(null)
const scatterRef = ref<HTMLDivElement | null>(null)
let pieChart: echarts.ECharts | null = null
let profitPieChart: echarts.ECharts | null = null
let scatterChart: echarts.ECharts | null = null

const companies = ref<any[]>([])

// 汇总企业数量。
const totalCompanies = computed(() => companies.value.length)

// 汇总总营收。
const totalRevenue = computed(() => companies.value.reduce((sum, item) => sum + Number(item.revenue || 0), 0))

// 计算平均毛利率。
const avgMargin = computed(() => {
  if (!companies.value.length) return 0
  const sum = companies.value.reduce((acc, item) => acc + Number(item.margin || 0), 0)
  return sum / companies.value.length
})

// 按赛道聚合营收，供饼图展示。
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

const buildSectorSeries = () => {
  const map = new Map<string, number>()
  companies.value.forEach((item) => {
    const sector = String(item.sector || '未分类')
    const key = sector === '新上传' ? shortLabel(String(item.company_name || '新上传')) : sector
    map.set(key, (map.get(key) || 0) + Number(item.revenue || 0))
  })
  return Array.from(map.entries()).map(([name, value]) => ({ name, value: Number(value.toFixed(2)) }))
}

const buildProfitSectorSeries = () => {
  const map = new Map<string, number>()
  companies.value.forEach((item) => {
    const sector = String(item.sector || '未分类')
    const key = sector === '新上传' ? shortLabel(String(item.company_name || '新上传')) : sector
    const profit = Number(item.profit || 0)
    // 饼图不支持负值；占比场景仅统计正向净利润。
    if (profit > 0) {
      map.set(key, (map.get(key) || 0) + profit)
    }
  })
  return Array.from(map.entries()).map(([name, value]) => ({ name, value: Number(value.toFixed(2)) }))
}

const buildScatterData = () =>
  companies.value.map((item) => {
    const revenue = Number(item.revenue || 0)
    const profit = Number(item.profit || 0)
    const margin = Number(item.margin || 0)
    return {
      name: shortLabel(String(item.company_name || '未命名企业')),
      value: [revenue, profit, Math.max(12, margin * 2.2 + 12), margin],
    }
  })

const renderSectorPie = (
  chart: echarts.ECharts,
  pieData: Array<{ name: string; value: number }>,
  labelPrefix: string,
  emptyLabel: string,
) => {
  const hasData = pieData.length > 0
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: `{b}<br/>${labelPrefix}：{c} 亿元 ({d}%)`,
    },
    legend: {
      show: false,
    },
    graphic: hasData
      ? []
      : [
          {
            type: 'text',
            left: 'center',
            top: 'middle',
            style: {
              text: emptyLabel,
              fill: '#9bdcff',
              font: '600 14px sans-serif',
            },
          },
        ],
    series: [
      {
        name: `${labelPrefix}占比`,
        type: 'pie',
        radius: ['60%', '90%'],
        center: ['50%', '53%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderColor: '#082f49',
          borderWidth: 2,
          borderRadius: 8,
        },
        label: {
          color: '#dbeafe',
          fontSize: 15,
          fontWeight: 600,
          formatter: '{b}\n{d}%',
        },
        labelLine: {
          lineStyle: { color: '#22d3ee' },
          length: 18,
          length2: 14,
        },
        data: hasData ? pieData : [],
        color: ['#38bdf8', '#7dd3fc', '#22d3ee', '#0ea5e9', '#60a5fa', '#0284c7'],
        animationDuration: 1000,
        animationEasing: 'cubicOut',
      },
    ],
  })
}

const renderPie = () => {
  if (!pieRef.value) return
  if (!pieChart) {
    pieChart = echarts.init(pieRef.value)
  }
  renderSectorPie(pieChart, buildSectorSeries(), '营收', '暂无营收占比数据')
}

const renderProfitPie = () => {
  if (!profitPieRef.value) return
  if (!profitPieChart) {
    profitPieChart = echarts.init(profitPieRef.value)
  }
  renderSectorPie(profitPieChart, buildProfitSectorSeries(), '净利润', '暂无正向净利润占比数据')
}

const renderScatter = () => {
  if (!scatterRef.value) return
  if (!scatterChart) {
    scatterChart = echarts.init(scatterRef.value)
  }
  // 关键修正：卡片尺寸变化后强制同步到实例，避免图表挤在左上角。
  scatterChart.resize({
    width: scatterRef.value.clientWidth,
    height: scatterRef.value.clientHeight,
  })

  const rows = buildScatterData()

  scatterChart.setOption({
    backgroundColor: 'transparent',
    grid: { top: 76, right: 36, bottom: 96, left: 100 },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const [revenue, profit, _size, margin] = params.value
        return `${params.name}<br/>营收：${revenue} 亿元<br/>净利润：${profit} 亿元<br/>毛利率：${Number(margin).toFixed(2)}%`
      },
    },
    xAxis: {
      name: '营收（亿元）',
      nameLocation: 'middle',
      nameGap: 52,
      nameTextStyle: { color: '#a5f3fc', fontSize: 18, fontWeight: 700 },
      axisLabel: { color: '#a5f3fc', fontSize: 15, fontWeight: 600 },
      axisLine: { lineStyle: { color: 'rgba(59,130,246,0.36)' } },
      splitLine: { lineStyle: { color: 'rgba(59,130,246,0.16)' } },
    },
    yAxis: {
      name: '净利润（亿元）',
      nameLocation: 'middle',
      nameGap: 64,
      nameRotate: 90,
      nameTextStyle: { color: '#a5f3fc', fontSize: 18, fontWeight: 700 },
      axisLabel: { color: '#a5f3fc', fontSize: 15, fontWeight: 600 },
      axisLine: { lineStyle: { color: 'rgba(59,130,246,0.36)' } },
      splitLine: { lineStyle: { color: 'rgba(59,130,246,0.16)' } },
    },
    series: [
      {
        type: 'scatter',
        data: rows,
        symbolSize: (value: number[]) => value[2],
        itemStyle: {
          color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [
            { offset: 0, color: '#67e8f9' },
            { offset: 1, color: '#0284c7' },
          ]),
          shadowBlur: 20,
          shadowColor: 'rgba(59,130,246,0.35)',
        },
      },
    ],
    animationDuration: 900,
  })
  scatterChart.resize({
    width: scatterRef.value.clientWidth,
    height: scatterRef.value.clientHeight,
  })
}

const renderAllCharts = () => {
  renderPie()
  renderProfitPie()
  renderScatter()
}

const handleResize = () => {
  pieChart?.resize()
  profitPieChart?.resize()
  scatterChart?.resize()
}

const loadCompanies = async () => {
  const { data } = await getCompanies()
  companies.value = Array.isArray(data?.items) ? data.items : []
  await nextTick()
  renderAllCharts()
}

const handleDataRefresh = () => {
  loadCompanies()
}

const handleStorageRefresh = (event: StorageEvent) => {
  if (event.key === 'dataRefreshAt') {
    loadCompanies()
  }
}

onMounted(async () => {
  await loadCompanies()
  window.addEventListener('resize', handleResize)
  window.addEventListener('data-refreshed', handleDataRefresh)
  window.addEventListener('storage', handleStorageRefresh)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('data-refreshed', handleDataRefresh)
  window.removeEventListener('storage', handleStorageRefresh)
  pieChart?.dispose()
  profitPieChart?.dispose()
  scatterChart?.dispose()
  pieChart = null
  profitPieChart = null
  scatterChart = null
})
</script>







