<template>
  <section class="relative flex min-h-[calc(100vh-12rem)] flex-col lg:min-h-[calc(100vh-10rem)]">
    <!-- 中心欢迎区 -->
    <div class="hero-center flex flex-1 items-center justify-center px-6">
      <div class="text-center">
        <p class="welcome-tag text-xs uppercase tracking-[0.4em] text-emerald-500">Welcome</p>
        <h1 class="art-title mt-5 text-3xl font-black leading-tight sm:text-5xl md:text-6xl">
          欢迎来到新能源财报智能体系统
        </h1>
      </div>
    </div>

    <!-- 下端功能区 -->
    <div class="pb-2 pt-4">
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <RouterLink
          to="/dashboard"
          class="feature-card rounded-2xl border border-emerald-300/30 bg-white/85 p-5 transition hover:-translate-y-1 hover:shadow-[0_16px_30px_rgba(16,185,129,0.2)]"
        >
          <p class="text-xs text-emerald-600">Overview</p>
          <h4 class="mt-2 text-lg font-semibold text-emerald-900">宏观行业大屏</h4>
          <p class="mt-2 text-sm text-emerald-800/80">查看企业总量、总营收和赛道占比。</p>
        </RouterLink>

        <RouterLink
          to="/agent-room"
          class="feature-card rounded-2xl border border-emerald-300/30 bg-white/85 p-5 transition hover:-translate-y-1 hover:shadow-[0_16px_30px_rgba(16,185,129,0.2)]"
        >
          <p class="text-xs text-emerald-600">AI Room</p>
          <h4 class="mt-2 text-lg font-semibold text-emerald-900">智能研判室</h4>
          <p class="mt-2 text-sm text-emerald-800/80">通过 Dify 智能体进行沉浸式问答。</p>
        </RouterLink>

        <RouterLink
          to="/financial-analysis"
          class="feature-card rounded-2xl border border-emerald-300/30 bg-white/85 p-5 transition hover:-translate-y-1 hover:shadow-[0_16px_30px_rgba(16,185,129,0.2)]"
        >
          <p class="text-xs text-emerald-600">Finance</p>
          <h4 class="mt-2 text-lg font-semibold text-emerald-900">财务指标对比</h4>
          <p class="mt-2 text-sm text-emerald-800/80">横向对比营收、净利润和毛利率表现。</p>
        </RouterLink>

        <RouterLink
          to="/knowledge-base"
          class="feature-card rounded-2xl border border-emerald-300/30 bg-white/85 p-5 transition hover:-translate-y-1 hover:shadow-[0_16px_30px_rgba(16,185,129,0.2)]"
        >
          <p class="text-xs text-emerald-600">Data Assets</p>
          <h4 class="mt-2 text-lg font-semibold text-emerald-900">知识库资产管理</h4>
          <p class="mt-2 text-sm text-emerald-800/80">管理文档上传、解析状态与切块数量。</p>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// 主界面：中心欢迎语 + 下端四功能导航。
</script>

<style scoped>
.hero-center {
  animation: fade-up 0.8s ease-out both;
}

.welcome-tag {
  animation: fade-up 0.8s ease-out 0.08s both;
}

.art-title {
  font-family: 'STKaiti', 'KaiTi', 'Microsoft YaHei', sans-serif;
  letter-spacing: 0.02em;
  color: #065f46;
  background: linear-gradient(120deg, #065f46 0%, #0f766e 45%, #10b981 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 8px 20px rgba(16, 185, 129, 0.25);
  animation: fade-up 0.86s ease-out 0.18s both;
}

.feature-card {
  animation: fade-up 0.8s ease-out both;
}

.feature-card:nth-child(1) {
  animation-delay: 0.34s;
}

.feature-card:nth-child(2) {
  animation-delay: 0.42s;
}

.feature-card:nth-child(3) {
  animation-delay: 0.5s;
}

.feature-card:nth-child(4) {
  animation-delay: 0.58s;
}

@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
