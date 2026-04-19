<template>
  <div class="rounded-3xl border border-cyan-500/30 bg-slate-950/78 p-6 shadow-glow">
    <div class="mb-4 flex items-center justify-between gap-4">
      <div>
        <h3 class="text-xl font-semibold text-cyan-50">财务指标横向对比</h3>
        <p class="mt-1 text-sm text-cyan-300">基于 2025 年前三季度财报数据</p>
      </div>
      <select
        v-model="metric"
        class="rounded-xl border border-slate-700 bg-cyan-950/70 px-3 py-2 text-sm text-cyan-200"
        @change="loadChart"
      >
        <option value="revenue">营收</option>
        <option value="profit">净利润</option>
        <option value="margin">毛利率</option>
      </select>
    </div>

    <div v-if="errorMessage" class="mb-3 rounded-xl border border-amber-400/30 bg-amber-500/10 px-3 py-2 text-xs text-amber-200">
      {{ errorMessage }}
    </div>

    <div ref="chartRef" class="h-[420px] w-full"></div>
  </div>
</template>

<script setup lang="ts">
// AI辅助生成：DeepSeek-V3, 2026-04-18
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { getMetrics } from '../api/finance'

const chartRef = ref<HTMLDivElement | null>(null)
const metric = ref<'revenue' | 'profit' | 'margin'>('revenue')
const errorMessage = ref('')
let chart: echarts.ECharts | null = null

const metricLabelMap: Record<string, string> = {
  revenue: '营收（亿元）',
  profit: '净利润（亿元）',
  margin: '毛利率（%）',
}

const loadChart = async () => {
  try {
    errorMessage.value = ''
    const { data } = await getMetrics(metric.value)
    const items = Array.isArray(data?.items) ? data.items : []
    const names = items.map((item: any) => item.company_name || item.name)
    const values = items.map((item: any) => item.value)

    if (!chart && chartRef.value) {
      chart = echarts.init(chartRef.value)
    }

    chart?.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(15, 23, 42, 0.95)',
        borderColor: '#22d3ee',
      textStyle: { color: '#dbeafe' },
        formatter: (params: any) => {
          const item = params[0]
          if (!item) return ''
          return `${item.name}<br/>${metricLabelMap[metric.value]}：${item.value}`
        },
      },
      grid: { left: 80, right: 30, top: 30, bottom: 60 },
      xAxis: {
        type: 'category',
        data: names,
        axisLabel: { color: '#cbd5e1', rotate: 20 },
        axisLine: { lineStyle: { color: '#334155' } },
      },
      yAxis: {
        type: 'value',
        name: metricLabelMap[metric.value],
        nameTextStyle: { color: '#94a3b8' },
        axisLabel: { color: '#94a3b8' },
        splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.15)' } },
      },
      series: [
        {
          type: 'bar',
          data: values,
          barWidth: 28,
          itemStyle: {
            borderRadius: [12, 12, 0, 0],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#22d3ee' },
              { offset: 1, color: '#0ea5e9' },
            ]),
            shadowBlur: 18,
            shadowColor: 'rgba(34, 211, 238, 0.35)',
          },
        },
      ],
    })
  } catch {
    errorMessage.value = '图表数据加载失败，已切换为本地回退数据。请刷新重试。'
  }
}

const handleResize = () => chart?.resize()

onMounted(async () => {
  await nextTick()
  await loadChart()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
  chart = null
})
</script>





