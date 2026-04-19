<template>
  <section ref="homeWrapRef" class="home-wrap relative flex min-h-screen flex-col">
    <div ref="heroGlowRef" class="hero-glow"></div>
    <div class="ambient-grid" aria-hidden="true"></div>
    <div class="aurora-veil" aria-hidden="true"></div>
    <div class="light-sweep" aria-hidden="true"></div>

    <div ref="ringStageRef" class="ring-stage" aria-hidden="true">
      <div class="ring-halo"></div>
      <div class="segment-ring ring-main"></div>
      <div class="segment-ring ring-inner"></div>
      <div class="segment-ring ring-outer"></div>
      <div class="ring-particle ring-particle-a"></div>
      <div class="ring-particle ring-particle-b"></div>
      <div class="ring-particle ring-particle-c"></div>
      <div class="ring-orbiters">
        <span
          v-for="orbiter in orbiters"
          :key="orbiter.id"
          class="ring-orbiter"
          :style="orbiter.style"
        ></span>
      </div>
    </div>

    <div class="hero-center relative z-[1] flex flex-1 items-center justify-center px-2 sm:px-6">
      <div ref="heroPanelRef" class="hero-panel w-full max-w-5xl p-4 text-center sm:p-6">
        <h1 ref="artTitleRef" class="art-title text-3xl font-black leading-tight sm:text-5xl md:text-6xl">
          欢迎来到新能源财报智能体系统
        </h1>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// AI閺夊牆鎳庢慨顏堟偨閻旂鐏囬柨娑欘儚eepSeek-V3, 2026-04-18
import { gsap } from 'gsap'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const homeWrapRef = ref<HTMLElement | null>(null)
const ringStageRef = ref<HTMLElement | null>(null)
const heroPanelRef = ref<HTMLElement | null>(null)
const heroGlowRef = ref<HTMLElement | null>(null)
const artTitleRef = ref<HTMLElement | null>(null)
const reducedMotion = ref(false)

const orbiters = computed(() => [
  {
    id: 'o1',
    style: {
      '--size': '12px',
      '--radius': 'clamp(150px, 20vw, 320px)',
      '--duration': '9s',
      '--delay': '0s',
      '--dir': '1',
      '--alpha': '0.92',
    },
  },
  {
    id: 'o2',
    style: {
      '--size': '9px',
      '--radius': 'clamp(120px, 16vw, 250px)',
      '--duration': '7.4s',
      '--delay': '-2.1s',
      '--dir': '-1',
      '--alpha': '0.78',
    },
  },
  {
    id: 'o3',
    style: {
      '--size': '8px',
      '--radius': 'clamp(180px, 23vw, 360px)',
      '--duration': '11.6s',
      '--delay': '-4.2s',
      '--dir': '1',
      '--alpha': '0.68',
    },
  },
  {
    id: 'o4',
    style: {
      '--size': '10px',
      '--radius': 'clamp(138px, 18vw, 280px)',
      '--duration': '8.2s',
      '--delay': '-1.5s',
      '--dir': '-1',
      '--alpha': '0.84',
    },
  },
  {
    id: 'o5',
    style: {
      '--size': '6px',
      '--radius': 'clamp(200px, 25vw, 410px)',
      '--duration': '13.6s',
      '--delay': '-5s',
      '--dir': '1',
      '--alpha': '0.6',
    },
  },
])

let detachPointer: (() => void) | null = null
let detachMediaQuery: (() => void) | null = null

const setupPointerParallax = () => {
  const wrapEl = homeWrapRef.value
  const ringEl = ringStageRef.value
  const panelEl = heroPanelRef.value
  const glowEl = heroGlowRef.value
  if (!wrapEl || !ringEl || !panelEl || !glowEl || reducedMotion.value) return

  const handlePointerMove = (event: PointerEvent) => {
    const rect = wrapEl.getBoundingClientRect()
    const x = (event.clientX - rect.left) / rect.width - 0.5
    const y = (event.clientY - rect.top) / rect.height - 0.5

    gsap.to(ringEl, {
      x: x * 28,
      y: y * 18,
      rotateY: x * 10,
      rotateX: -y * 10,
      duration: 0.8,
      ease: 'power3.out',
      overwrite: true,
    })

    gsap.to(panelEl, {
      x: x * 14,
      y: y * 10,
      rotateY: x * 6,
      rotateX: -y * 6,
      duration: 0.75,
      ease: 'power3.out',
      overwrite: true,
    })

    gsap.to(glowEl, {
      x: x * 36,
      y: y * 24,
      duration: 1.1,
      ease: 'power2.out',
      overwrite: true,
    })
  }

  const handlePointerLeave = () => {
    gsap.to([ringEl, panelEl, glowEl], {
      x: 0,
      y: 0,
      rotateX: 0,
      rotateY: 0,
      duration: 0.9,
      ease: 'power2.out',
      overwrite: true,
    })
  }

  wrapEl.addEventListener('pointermove', handlePointerMove)
  wrapEl.addEventListener('pointerleave', handlePointerLeave)

  detachPointer = () => {
    wrapEl.removeEventListener('pointermove', handlePointerMove)
    wrapEl.removeEventListener('pointerleave', handlePointerLeave)
  }
}

const runEntranceAnimation = () => {
  const ringEl = ringStageRef.value
  const panelEl = heroPanelRef.value
  const titleEl = artTitleRef.value
  const glowEl = heroGlowRef.value
  if (!ringEl || !panelEl || !titleEl || !glowEl) return

  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })

  tl.set([ringEl, panelEl, titleEl], { opacity: 0, force3D: true })
  tl.fromTo(glowEl, { scale: 0.92, opacity: 0.06 }, { scale: 1.03, opacity: 0.34, duration: 1.3 }, 0)
  tl.fromTo(ringEl, { scale: 0.78, rotateX: 18, rotateY: -16, y: 34 }, { scale: 1, rotateX: 0, rotateY: 0, y: 0, opacity: 1, duration: 1.15 }, 0.04)
  tl.fromTo(panelEl, { y: 36, rotateX: -12, scale: 0.96 }, { y: 0, rotateX: 0, scale: 1, opacity: 1, duration: 0.92 }, 0.2)
  tl.fromTo(titleEl, { y: 18, filter: 'blur(8px)' }, { y: 0, filter: 'blur(0px)', opacity: 1, duration: 0.86 }, 0.34)
}

const setupMotionPreference = () => {
  const mq = window.matchMedia('(prefers-reduced-motion: reduce)')
  const update = () => {
    reducedMotion.value = mq.matches
  }

  update()
  mq.addEventListener('change', update)
  detachMediaQuery = () => mq.removeEventListener('change', update)
}

onMounted(() => {
  setupMotionPreference()
  runEntranceAnimation()

  if (!reducedMotion.value) {
    setupPointerParallax()

    if (ringStageRef.value) {
      gsap.to(ringStageRef.value, {
        scale: 1.018,
        duration: 3.8,
        ease: 'sine.inOut',
        repeat: -1,
        yoyo: true,
      })
    }
  }
})

onBeforeUnmount(() => {
  detachPointer?.()
  detachMediaQuery?.()
})
</script>

<style scoped>
.home-wrap {
  overflow: hidden;
  isolation: isolate;
  perspective: 1800px;
}

.ambient-grid {
  position: absolute;
  inset: -20% -10%;
  pointer-events: none;
  opacity: 0.35;
  background-image:
    linear-gradient(rgba(125, 211, 252, 0.13) 1px, transparent 1px),
    linear-gradient(90deg, rgba(125, 211, 252, 0.12) 1px, transparent 1px);
  background-size: 46px 46px;
  mask-image: radial-gradient(circle at 52% 35%, rgba(0, 0, 0, 0.85), transparent 72%);
  animation: grid-drift 28s linear infinite;
}

.aurora-veil {
  position: absolute;
  inset: -30% -20%;
  pointer-events: none;
  background:
    radial-gradient(72% 42% at 24% 18%, rgba(59, 130, 246, 0.3), transparent 74%),
    radial-gradient(66% 44% at 82% 42%, rgba(6, 182, 212, 0.24), transparent 75%),
    radial-gradient(52% 34% at 50% 90%, rgba(14, 165, 233, 0.22), transparent 82%);
  filter: blur(20px);
  animation: aurora-shift 14s ease-in-out infinite;
}

.light-sweep {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(120deg, rgba(125, 211, 252, 0) 35%, rgba(125, 211, 252, 0.12) 48%, rgba(125, 211, 252, 0) 62%);
  mix-blend-mode: screen;
  transform: translateX(-120%);
  animation: sweep 8.8s ease-in-out infinite;
}

.hero-glow {
  position: absolute;
  left: 50%;
  top: 35%;
  width: min(96vw, 1180px);
  height: min(96vw, 1180px);
  transform: translate(-50%, -50%);
  background: radial-gradient(circle at 50% 50%, rgba(56, 189, 248, 0.2) 0%, rgba(56, 189, 248, 0.08) 45%, rgba(56, 189, 248, 0) 72%);
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
  transform: translate3d(-50%, -50%, 0);
  pointer-events: none;
  z-index: 0;
  transform-style: preserve-3d;
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

.ring-orbiters {
  position: absolute;
  inset: 50%;
}

.ring-orbiter {
  position: absolute;
  left: 0;
  top: 0;
  width: var(--size);
  height: var(--size);
  opacity: var(--alpha);
  border-radius: 999px;
  background: radial-gradient(circle at 35% 30%, rgba(240, 249, 255, 1), rgba(56, 189, 248, 0.88) 58%, rgba(14, 116, 144, 0.22));
  box-shadow:
    0 0 10px rgba(56, 189, 248, 0.46),
    0 0 26px rgba(14, 165, 233, 0.24);
  animation: orbital var(--duration) linear infinite;
  animation-delay: var(--delay);
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
  color: transparent;
  background: linear-gradient(96deg, #f8fdff 10%, #d9f6ff 40%, #7dd3fc 76%, #22d3ee 100%);
  -webkit-background-clip: text;
  background-clip: text;
  text-shadow:
    0 3px 14px rgba(56, 189, 248, 0.28),
    0 0 28px rgba(14, 165, 233, 0.2);
  transform: translateZ(0);
  animation: fade-up 0.86s ease-out 0.2s both;
  position: relative;
}

.art-title::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(110deg, rgba(255, 255, 255, 0) 34%, rgba(255, 255, 255, 0.72) 48%, rgba(255, 255, 255, 0) 62%);
  mix-blend-mode: screen;
  filter: blur(1px);
  transform: translateX(-130%);
  animation: title-sheen 5.8s ease-in-out infinite 1.2s;
  pointer-events: none;
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

@keyframes orbital {
  from {
    transform: rotate(0deg) translateX(var(--radius)) rotate(0deg);
  }
  to {
    transform: rotate(calc(360deg * var(--dir))) translateX(var(--radius)) rotate(calc(-360deg * var(--dir)));
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

@keyframes grid-drift {
  from {
    transform: translate3d(0, 0, 0);
  }
  to {
    transform: translate3d(42px, 38px, 0);
  }
}

@keyframes aurora-shift {
  0%,
  100% {
    transform: scale(1) translate3d(0, 0, 0);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.06) translate3d(-1.2%, 1.6%, 0);
    opacity: 0.88;
  }
}

@keyframes sweep {
  0%,
  100% {
    transform: translateX(-120%);
    opacity: 0;
  }
  22% {
    opacity: 0.42;
  }
  50% {
    transform: translateX(130%);
    opacity: 0;
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

@keyframes title-sheen {
  0%,
  100% {
    transform: translateX(-130%);
    opacity: 0;
  }
  24% {
    opacity: 0.8;
  }
  52% {
    transform: translateX(130%);
    opacity: 0;
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

@media (prefers-reduced-motion: reduce) {
  .ambient-grid,
  .aurora-veil,
  .light-sweep,
  .ring-halo,
  .segment-ring,
  .segment-ring::before,
  .ring-particle,
  .ring-orbiter,
  .art-title::after {
    animation: none !important;
  }
}
</style>
