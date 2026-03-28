<template>
  <div class="rounded-3xl border border-slate-800 bg-slate-900/60 p-5">
    <div class="mb-2 text-xs uppercase tracking-[0.24em] text-cyan-300">{{ company.sector }}</div>
    <div class="text-2xl font-semibold text-white">{{ company.company_name }}</div>
    <div class="mt-4 grid grid-cols-3 gap-3 text-sm">
      <div class="rounded-2xl bg-slate-950/60 p-3">
        <div class="text-slate-400">营收</div>
        <div class="mt-1 text-lg font-semibold text-white">{{ company.revenue }}</div>
      </div>
      <div class="rounded-2xl bg-slate-950/60 p-3">
        <div class="text-slate-400">净利润</div>
        <div class="mt-1 text-lg font-semibold text-white">{{ company.profit }}</div>
      </div>
      <div class="rounded-2xl bg-slate-950/60 p-3">
        <div class="text-slate-400">毛利率</div>
        <div class="mt-1 text-lg font-semibold text-white">{{ company.margin }}%</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  company: Record<string, any>
}>()
</script>
