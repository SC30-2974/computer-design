<template>
  <div class="rounded-3xl border border-cyan-500/30 bg-slate-950/78 p-6">
    <div class="mb-4 flex items-center justify-between">
      <h3 class="text-xl font-semibold text-cyan-50">财务诊断</h3>
      <select
        v-model="selected"
        class="rounded-xl border border-slate-700 bg-cyan-950/70 px-3 py-2 text-sm text-cyan-200"
        @change="loadDiagnosis"
      >
        <option v-for="item in companies" :key="item.company_name" :value="item.company_name">
          {{ item.company_name }}
        </option>
      </select>
    </div>

    <div v-if="errorMessage" class="mb-3 rounded-xl border border-amber-400/30 bg-amber-500/10 px-3 py-2 text-xs text-amber-200">
      {{ errorMessage }}
    </div>

    <div v-if="diagnosis" class="space-y-4 text-sm text-slate-300">
      <div class="grid grid-cols-2 gap-4">
        <div class="rounded-2xl bg-cyan-950/70 p-4">
          <div class="text-cyan-300">毛利率 / 评价</div>
          <div class="mt-2 text-xl font-semibold text-cyan-50">{{ diagnosis.gross_margin }}% · {{ diagnosis.gross_margin_level }}</div>
        </div>
        <div class="rounded-2xl bg-cyan-950/70 p-4">
          <div class="text-cyan-300">净利率 / 评价</div>
          <div class="mt-2 text-xl font-semibold text-cyan-50">{{ diagnosis.net_margin }}% · {{ diagnosis.net_margin_level }}</div>
        </div>
      </div>

      <div class="rounded-2xl bg-cyan-950/70 p-4">
        <div class="text-cyan-300">综合判断</div>
        <div class="mt-2 text-base text-cyan-50">{{ diagnosis.overall_assessment }}</div>
      </div>

      <div class="rounded-2xl bg-cyan-950/70 p-4">
        <div class="text-cyan-300">建议</div>
        <ul class="mt-2 list-disc space-y-1 pl-5">
          <li v-for="item in diagnosis.suggestions" :key="item">{{ item }}</li>
        </ul>
      </div>
    </div>

    <div v-else class="rounded-2xl bg-cyan-950/70 p-4 text-sm text-slate-300">暂无诊断数据。</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getCompanies, getFinancialDiagnosis } from '../api/finance'

const companies = ref<any[]>([])
const selected = ref('')
const diagnosis = ref<any | null>(null)
const errorMessage = ref('')

const loadDiagnosis = async () => {
  if (!selected.value) return
  try {
    errorMessage.value = ''
    const { data } = await getFinancialDiagnosis(selected.value)
    diagnosis.value = data
  } catch {
    errorMessage.value = '诊断数据获取失败，请稍后重试。'
  }
}

onMounted(async () => {
  try {
    const { data } = await getCompanies()
    companies.value = Array.isArray(data?.items) ? data.items : []
    selected.value = companies.value[0]?.company_name || ''
    await loadDiagnosis()
  } catch {
    errorMessage.value = '企业列表加载失败，请刷新页面。'
  }
})
</script>



