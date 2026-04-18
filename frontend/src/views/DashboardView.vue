<template>
  <main class="min-h-screen px-6 py-8 text-cyan-100 lg:px-10">
    <section class="mx-auto max-w-7xl space-y-8">
      <header class="flex flex-col gap-3 rounded-[32px] border border-cyan-500/20 bg-cyan-950/65 p-8 shadow-glow lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div class="text-xs uppercase tracking-[0.36em] text-cyan-300">鏂拌兘婧愯储鎶ユ櫤鑳戒綋绯荤粺</div>
          <h1 class="mt-3 text-4xl font-semibold text-cyan-50">浠?MVP 鍗囩骇涓洪潰鍚戝浗璧涚殑涓€浣撳寲璐㈡姤鏅鸿兘鍒嗘瀽骞冲彴</h1>
          <p class="mt-3 max-w-3xl text-sm leading-7 text-cyan-300">
            鐪熷疄 RAG銆佽嚜鍔ㄥ寲璐㈡姤瑙ｆ瀽娴佹按绾裤€佺粨鏋勫寲璐㈠姟璇婃柇銆佷笓涓氬彲瑙嗗寲澶у睆銆?
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



