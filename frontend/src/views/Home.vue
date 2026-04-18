<template>
  <section class="home-wrap relative flex min-h-screen flex-col">
    <div class="hero-glow"></div>

    <div class="ring-stage" aria-hidden="true">
      <div class="ring-halo"></div>
      <div class="segment-ring ring-main"></div>
      <div class="segment-ring ring-inner"></div>
      <div class="segment-ring ring-outer"></div>
      <div class="ring-particle ring-particle-a"></div>
      <div class="ring-particle ring-particle-b"></div>
      <div class="ring-particle ring-particle-c"></div>
    </div>

    <div class="hero-center relative z-[1] flex flex-1 items-center justify-center px-2 sm:px-6">
      <div class="hero-panel w-full max-w-5xl p-4 text-center sm:p-6">
        <h1 class="art-title text-3xl font-black leading-tight sm:text-5xl md:text-6xl">
          欢迎来到新能源财报智能体系统
        </h1>
      </div>
    </div>

  </section>
</template>

<script setup lang="ts">
// 主界面：中心欢迎语 + 下端四功能导航。
</script>

<style scoped>
.home-wrap {
  overflow: hidden;
  isolation: isolate;
}

.hero-glow {
  position: absolute;
  left: 50%;
  top: 35%;
  width: min(96vw, 1180px);
  height: min(96vw, 1180px);
  transform: translate(-50%, -50%);
  background: radial-gradient(circle at 50% 50%, rgba(56, 189, 248, 0.12) 0%, rgba(56, 189, 248, 0.05) 45%, rgba(56, 189, 248, 0) 72%);
  filter: blur(12px);
  pointer-events: none;
  z-index: 0;
}

.ring-stage {
  position: absolute;
  left: 50%;
  top: 36%;
  width: min(90vw, 1080px);
  height: min(90vw, 1080px);
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 0;
}

.ring-halo {
  position: absolute;
  inset: 12%;
  border-radius: 999px;
  background: radial-gradient(circle at 48% 45%, rgba(56, 189, 248, 0.14) 0%, rgba(56, 189, 248, 0.05) 40%, rgba(56, 189, 248, 0) 75%);
  filter: blur(6px);
  animation: halo-breathe 6.5s ease-in-out infinite;
}

.segment-ring {
  position: absolute;
  inset: 0;
  border-radius: 999px;
  --ring-thickness: 16px;
  background:
    repeating-conic-gradient(
      from 0deg,
      rgba(56, 189, 248, 0.34) 0deg 12deg,
      rgba(56, 189, 248, 0.12) 12deg 17deg,
      rgba(56, 189, 248, 0) 17deg 26deg
    ),
    repeating-conic-gradient(
      from 96deg,
      rgba(56, 189, 248, 0.28) 0deg 8deg,
      rgba(56, 189, 248, 0) 8deg 24deg
    );
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - var(--ring-thickness)), #000 calc(100% - (var(--ring-thickness) - 1px)));
  mask: radial-gradient(farthest-side, transparent calc(100% - var(--ring-thickness)), #000 calc(100% - (var(--ring-thickness) - 1px)));
  box-shadow:
    inset 0 0 20px rgba(56, 189, 248, 0.14),
    0 0 18px rgba(56, 189, 248, 0.08);
}

.segment-ring::before {
  content: '';
  position: absolute;
  inset: 12%;
  border-radius: inherit;
  background: repeating-conic-gradient(
    from 36deg,
    rgba(56, 189, 248, 0.3) 0deg 8deg,
    rgba(56, 189, 248, 0) 8deg 18deg
  );
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 9px), #000 calc(100% - 8px));
  mask: radial-gradient(farthest-side, transparent calc(100% - 9px), #000 calc(100% - 8px));
  animation: spin-inner 10s linear infinite;
  opacity: 0.56;
}

.segment-ring::after {
  content: '';
  position: absolute;
  inset: -18%;
  border-radius: inherit;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, rgba(56, 189, 248, 0) 68%);
  filter: blur(12px);
  z-index: -1;
}

.ring-main {
  animation: spin-main 15s linear infinite, ring-luminance 8s ease-in-out infinite;
}

.ring-inner {
  inset: 16%;
  --ring-thickness: 10px;
  opacity: 0.72;
  animation: spin-reverse 11s linear infinite;
}

.ring-outer {
  inset: -8%;
  --ring-thickness: 8px;
  opacity: 0.28;
  animation: spin-main 22s linear infinite;
}

.ring-particle {
  position: absolute;
  width: 14px;
  height: 14px;
  border-radius: 4px;
  background: #22d3ee;
  box-shadow: 0 0 8px rgba(56, 189, 248, 0.24);
  transform-origin: center;
}

.ring-particle-a {
  left: 50%;
  top: 4%;
  animation: orbit-a 7.8s linear infinite;
}

.ring-particle-b {
  right: 6%;
  top: 52%;
  width: 11px;
  height: 11px;
  border-radius: 3px;
  animation: orbit-b 9.4s linear infinite;
}

.ring-particle-c {
  left: 8%;
  bottom: 14%;
  width: 9px;
  height: 9px;
  border-radius: 2px;
  animation: orbit-c 8.6s linear infinite;
}

.hero-center {
  animation: fade-up 0.8s ease-out both;
}

.hero-panel {
  animation: fade-up 0.86s ease-out 0.08s both;
}

.art-title {
  font-family: 'STKaiti', 'KaiTi', 'Microsoft YaHei', sans-serif;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: #e2e8ff;
  text-shadow: 0 4px 12px rgba(56, 189, 248, 0.22);
  transform: translateZ(0);
  animation: fade-up 0.86s ease-out 0.2s both;
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

@keyframes spin-main {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes spin-reverse {
  from {
    transform: rotate(360deg);
  }
  to {
    transform: rotate(0deg);
  }
}

@keyframes spin-inner {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(-360deg);
  }
}

@keyframes ring-luminance {
  0%,
  100% {
    opacity: 0.52;
    filter: saturate(0.85);
  }
  50% {
    opacity: 0.72;
    filter: saturate(0.95);
  }
}

@keyframes halo-breathe {
  0%,
  100% {
    opacity: 0.4;
    transform: scale(0.96);
  }
  50% {
    opacity: 0.56;
    transform: scale(1.04);
  }
}

@keyframes orbit-a {
  from {
    transform: rotate(0deg) translateX(310px) rotate(0deg);
  }
  to {
    transform: rotate(360deg) translateX(310px) rotate(-360deg);
  }
}

@keyframes orbit-b {
  from {
    transform: rotate(360deg) translateX(250px) rotate(360deg);
  }
  to {
    transform: rotate(0deg) translateX(250px) rotate(0deg);
  }
}

@keyframes orbit-c {
  from {
    transform: rotate(0deg) translateX(205px) rotate(0deg);
  }
  to {
    transform: rotate(-360deg) translateX(205px) rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .ring-stage {
    width: min(96vw, 860px);
    height: min(96vw, 860px);
  }

  @keyframes orbit-a {
    from {
      transform: rotate(0deg) translateX(220px) rotate(0deg);
    }
    to {
      transform: rotate(360deg) translateX(220px) rotate(-360deg);
    }
  }

  @keyframes orbit-b {
    from {
      transform: rotate(360deg) translateX(180px) rotate(360deg);
    }
    to {
      transform: rotate(0deg) translateX(180px) rotate(0deg);
    }
  }

  @keyframes orbit-c {
    from {
      transform: rotate(0deg) translateX(150px) rotate(0deg);
    }
    to {
      transform: rotate(-360deg) translateX(150px) rotate(360deg);
    }
  }
}

@media (max-width: 768px) {
  .ring-stage {
    top: 33%;
    width: min(108vw, 760px);
    height: min(108vw, 760px);
  }

  .ring-main {
    --ring-thickness: 12px;
  }

  .ring-inner {
    --ring-thickness: 8px;
  }

  .ring-outer {
    --ring-thickness: 6px;
  }
}
</style>
