<template>
  <main class="min-h-screen px-6 py-8 text-slate-100 lg:px-10">
    <section class="mx-auto max-w-7xl space-y-8">
      <header class="flex flex-col gap-3 rounded-[32px] border border-cyan-500/20 bg-slate-950/60 p-8 shadow-glow lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div class="text-xs uppercase tracking-[0.36em] text-cyan-300">新能源财报智能体系统</div>
          <h1 class="mt-3 text-4xl font-semibold text-white">从 MVP 升级为面向国赛的一体化财报智能分析平台</h1>
          <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-400">
            真实 RAG、自动化财报解析流水线、结构化财务诊断、专业可视化大屏。
          </p>
        </div>
      </header>

      <section class="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <FinancialChart />
        <DiagnosisPanel />
      </section>

      <section class="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <RagChatPanel />
        <ReportPanel />
      </section>
    </section>
  </main>
</template>

<script setup lang="ts">
import DiagnosisPanel from '../components/DiagnosisPanel.vue'
import FinancialChart from '../components/FinancialChart.vue'
import RagChatPanel from '../components/RagChatPanel.vue'
import ReportPanel from '../components/ReportPanel.vue'
</script>
