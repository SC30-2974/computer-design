<template>
  <section class="space-y-6">
    <div class="grid gap-4 md:grid-cols-3">
      <article class="rounded-2xl border border-emerald-300/30 bg-white/85 p-5 shadow-[0_12px_30px_rgba(16,185,129,0.18)]">
        <p class="text-xs uppercase tracking-widest text-emerald-300">收录企业数</p>
        <p class="mt-3 text-3xl font-semibold text-emerald-900">{{ totalCompanies }}</p>
      </article>
      <article class="rounded-2xl border border-emerald-300/30 bg-white/85 p-5 shadow-[0_12px_30px_rgba(16,185,129,0.18)]">
        <p class="text-xs uppercase tracking-widest text-emerald-300">前三季度总营收</p>
        <p class="mt-3 text-3xl font-semibold text-emerald-900">{{ totalRevenue.toLocaleString() }} 亿元</p>
      </article>
      <article class="rounded-2xl border border-emerald-300/30 bg-white/85 p-5 shadow-[0_12px_30px_rgba(16,185,129,0.18)]">
        <p class="text-xs uppercase tracking-widest text-emerald-300">平均毛利率</p>
        <p class="mt-3 text-3xl font-semibold text-emerald-900">{{ avgMargin.toFixed(2) }}%</p>
      </article>
    </div>

    <div class="rounded-3xl border border-emerald-300/25 bg-white/85 p-6">
      <div class="mb-4 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-emerald-900">新能源各赛道营收占比</h3>
        <p class="text-xs text-emerald-700">按赛道聚合企业营收（亿元）</p>
      </div>
      <div ref="pieRef" class="h-[460px] w-full"></div>
    </div>
  </section>
</template>

<script setup lang="ts">
import * as echarts from 'echarts'
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { getCompanies } from '../api/finance'

const pieRef = ref<HTMLDivElement | null>(null)
let pieChart: echarts.ECharts | null = null

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
const buildSectorSeries = () => {
  const map = new Map<string, number>()
  companies.value.forEach((item) => {
    const key = String(item.sector || '未分类')
    map.set(key, (map.get(key) || 0) + Number(item.revenue || 0))
  })
  return Array.from(map.entries()).map(([name, value]) => ({ name, value: Number(value.toFixed(2)) }))
}

const renderPie = () => {
  if (!pieRef.value) return
  if (!pieChart) {
    pieChart = echarts.init(pieRef.value)
  }

  const pieData = buildSectorSeries()

  pieChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: '{b}<br/>营收：{c} 亿元 ({d}%)',
    },
    legend: {
      bottom: 12,
      textStyle: { color: '#065f46' },
    },
    series: [
      {
        name: '赛道营收占比',
        type: 'pie',
        radius: ['38%', '70%'],
        center: ['50%', '45%'],
        itemStyle: {
          borderColor: '#d1fae5',
          borderWidth: 2,
          borderRadius: 8,
        },
        label: {
          color: '#065f46',
          formatter: '{b}\n{d}%',
        },
        labelLine: {
          lineStyle: { color: '#6ee7b7' },
        },
        data: pieData,
        color: ['#10b981', '#34d399', '#6ee7b7', '#2dd4bf', '#4ade80', '#22c55e'],
        animationDuration: 1000,
        animationEasing: 'cubicOut',
      },
    ],
  })
}

const handleResize = () => pieChart?.resize()

onMounted(async () => {
  const { data } = await getCompanies()
  companies.value = Array.isArray(data?.items) ? data.items : []

  await nextTick()
  renderPie()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  pieChart?.dispose()
  pieChart = null
})
</script>

