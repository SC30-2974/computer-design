<template>
  <div class="rounded-3xl border border-cyan-500/30 bg-slate-950/78 p-6">
    <div class="mb-4 flex items-center justify-between">
      <h3 class="text-xl font-semibold text-cyan-50">分析报告</h3>
      <select v-model="selected" class="rounded-xl border border-cyan-500/45 bg-cyan-950/70 px-3 py-2 text-sm text-cyan-200">
        <option v-for="item in companies" :key="item.company_name" :value="item.company_name">
          {{ item.company_name }}
        </option>
      </select>
    </div>

    <button class="rounded-2xl bg-cyan-600 px-5 py-3 font-medium text-white hover:bg-cyan-500" @click="loadReport">生成报告</button>

    <div v-if="errorMessage" class="mt-3 rounded-xl border border-amber-400/30 bg-amber-500/10 px-3 py-2 text-xs text-amber-200">
      {{ errorMessage }}
    </div>

    <div class="mt-4 min-h-[220px] whitespace-pre-wrap rounded-2xl bg-cyan-950/70 p-4 text-sm text-cyan-200">{{ report }}</div>
  </div>
</template>

<script setup lang="ts">
// AI辅助生成：DeepSeek-V3, 2026-04-19
import { onMounted, ref } from 'vue'
import { generateReport, getCompanies } from '../api/finance'

const companies = ref<any[]>([])
const selected = ref('')
const report = ref('请选择企业并生成报告。')
const errorMessage = ref('')

const loadReport = async () => {
  if (!selected.value) return
  try {
    errorMessage.value = ''
    const { data } = await generateReport(selected.value)
    report.value = data?.report || '报告生成失败。'
  } catch {
    errorMessage.value = '报告接口请求失败，已使用回退模式。'
  }
}

onMounted(async () => {
  try {
    const { data } = await getCompanies()
    companies.value = Array.isArray(data?.items) ? data.items : []
    selected.value = companies.value[0]?.company_name || ''
  } catch {
    errorMessage.value = '企业列表加载失败，请刷新页面。'
  }
})
</script>




