<template>
  <div class="rounded-3xl border border-cyan-500/30 bg-slate-950/72 p-5">
    <div class="mb-2 text-xs uppercase tracking-[0.24em] text-cyan-300">{{ company.sector }}</div>
    <div class="text-2xl font-semibold text-cyan-50">{{ company.company_name }}</div>
    <div class="mt-4 grid grid-cols-3 gap-3 text-sm">
      <div class="rounded-2xl bg-cyan-950/65 p-3">
        <div class="text-cyan-300">钀ユ敹</div>
        <div class="mt-1 text-lg font-semibold text-cyan-50">{{ company.revenue }}</div>
      </div>
      <div class="rounded-2xl bg-cyan-950/65 p-3">
        <div class="text-cyan-300">鍑€鍒╂鼎</div>
        <div class="mt-1 text-lg font-semibold text-cyan-50">{{ company.profit }}</div>
      </div>
      <div class="rounded-2xl bg-cyan-950/65 p-3">
        <div class="text-cyan-300">姣涘埄鐜?/div>
        <div class="mt-1 text-lg font-semibold text-cyan-50">{{ company.margin }}%</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  company: Record<string, any>
}>()
</script>



