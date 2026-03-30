<template>
  <section class="home-wrap relative flex min-h-[calc(100vh-12rem)] flex-col lg:min-h-[calc(100vh-10rem)]">
    <div class="hero-glow"></div>

    <div class="hero-center relative z-[1] flex flex-1 items-center justify-center px-2 sm:px-6">
      <div class="hero-panel w-full max-w-5xl rounded-[28px] border border-emerald-300/35 bg-white/80 p-7 text-center shadow-[0_24px_80px_rgba(16,185,129,0.16)] sm:p-10">
        <p class="hero-pill mx-auto mb-5 inline-flex items-center rounded-full border border-emerald-300/50 bg-emerald-50 px-4 py-1 text-xs tracking-[0.2em] text-emerald-700">
          智能分析平台
        </p>
        <h1 class="art-title text-3xl font-black leading-tight sm:text-5xl md:text-6xl">
          欢迎来到新能源财报智能体系统
        </h1>
        <p class="hero-subtitle mx-auto mt-6 max-w-3xl text-sm text-emerald-800/80 sm:text-base">
          聚合企业核心财报数据，联动智能研判与可视化分析，快速完成从指标到结论的决策辅助。
        </p>
      </div>
    </div>

    <div class="relative z-[1] pb-2 pt-4">
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <RouterLink
          to="/dashboard"
          class="feature-card rounded-2xl border border-emerald-300/30 bg-white/90 p-5 transition hover:-translate-y-1 hover:shadow-[0_16px_30px_rgba(16,185,129,0.2)]"
        >
          <p class="mb-3 text-xs font-medium tracking-[0.16em] text-emerald-600">全局总览</p>
          <h4 class="mt-2 text-lg font-semibold text-emerald-900">宏观行业大屏</h4>
          <p class="mt-2 text-sm text-emerald-800/80">查看企业总量、总营收和赛道占比。</p>
        </RouterLink>

        <RouterLink
          to="/agent-room"
          class="feature-card rounded-2xl border border-emerald-300/30 bg-white/90 p-5 transition hover:-translate-y-1 hover:shadow-[0_16px_30px_rgba(16,185,129,0.2)]"
        >
          <p class="mb-3 text-xs font-medium tracking-[0.16em] text-emerald-600">智能交互</p>
          <h4 class="mt-2 text-lg font-semibold text-emerald-900">智能研判室</h4>
          <p class="mt-2 text-sm text-emerald-800/80">通过 Dify 智能体进行沉浸式问答。</p>
        </RouterLink>

        <RouterLink
          to="/financial-analysis"
          class="feature-card rounded-2xl border border-emerald-300/30 bg-white/90 p-5 transition hover:-translate-y-1 hover:shadow-[0_16px_30px_rgba(16,185,129,0.2)]"
        >
          <p class="mb-3 text-xs font-medium tracking-[0.16em] text-emerald-600">数据洞察</p>
          <h4 class="mt-2 text-lg font-semibold text-emerald-900">财务指标对比</h4>
          <p class="mt-2 text-sm text-emerald-800/80">横向对比营收、净利润和毛利率表现。</p>
        </RouterLink>

        <RouterLink
          to="/enterprise-detail"
          class="feature-card rounded-2xl border border-emerald-300/30 bg-white/90 p-5 transition hover:-translate-y-1 hover:shadow-[0_16px_30px_rgba(16,185,129,0.2)]"
        >
          <p class="mb-3 text-xs font-medium tracking-[0.16em] text-emerald-600">深度研判</p>
          <h4 class="mt-2 text-lg font-semibold text-emerald-900">企业详情</h4>
          <p class="mt-2 text-sm text-emerald-800/80">聚焦单企业指标、诊断结论与样本对比分析。</p>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// 主界面：中心欢迎语 + 下端三功能导航。
</script>

<style scoped>
.home-wrap {
  overflow: hidden;
}

.hero-glow {
  position: absolute;
  left: 50%;
  top: 36%;
  width: min(84vw, 960px);
  height: min(84vw, 960px);
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle at 50% 50%,
    rgba(16, 185, 129, 0.24) 0%,
    rgba(16, 185, 129, 0.08) 36%,
    rgba(16, 185, 129, 0) 68%
  );
  filter: blur(8px);
  pointer-events: none;
  animation: pulse-glow 4.2s ease-in-out infinite;
}

.hero-center {
  animation: fade-up 0.8s ease-out both;
}

.hero-panel {
  backdrop-filter: blur(8px);
  animation: fade-up 0.86s ease-out 0.08s both;
}

.hero-pill {
  animation: fade-up 0.86s ease-out 0.14s both;
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
  animation: fade-up 0.86s ease-out 0.2s both;
}

.hero-subtitle {
  animation: fade-up 0.86s ease-out 0.28s both;
}

.feature-card {
  position: relative;
  overflow: hidden;
  animation: fade-up 0.8s ease-out both;
}

.feature-card::after {
  content: '';
  position: absolute;
  inset: auto -30% -50% auto;
  width: 160px;
  height: 160px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.18) 0%, rgba(16, 185, 129, 0) 72%);
  transition: transform 0.35s ease;
  pointer-events: none;
}

.feature-card:hover::after {
  transform: translate(-10px, -14px) scale(1.04);
}

.feature-card:nth-child(1) {
  animation-delay: 0.38s;
}

.feature-card:nth-child(2) {
  animation-delay: 0.46s;
}

.feature-card:nth-child(3) {
  animation-delay: 0.54s;
}

.feature-card:nth-child(4) {
  animation-delay: 0.62s;
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

@keyframes pulse-glow {
  0%,
  100% {
    opacity: 0.7;
    transform: translate(-50%, -50%) scale(0.98);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.03);
  }
}
</style>
