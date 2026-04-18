<template>
  <div class="app-shell relative min-h-screen overflow-x-hidden bg-cyber-grid text-cyan-50">
    <div class="app-glow app-glow-left"></div>
    <div class="app-glow app-glow-right"></div>

    <aside
      class="fixed inset-y-0 left-0 z-50 hidden w-[292px] border-r border-cyan-500/30 bg-slate-950/72 p-4 shadow-[0_24px_46px_rgba(56,189,248,0.16)] backdrop-blur-2xl transition-transform duration-300 lg:block"
      :class="desktopMenuOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <button
        type="button"
        class="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-500/45 bg-slate-950 text-cyan-100 shadow-[0_8px_18px_rgba(56,189,248,0.18)] transition hover:bg-cyan-950/70"
        title="收起侧栏"
        @click="desktopMenuOpen = false"
      >
        <span class="inline-flex flex-col gap-1">
          <span class="h-[2px] w-4 rounded-full bg-cyan-300"></span>
          <span class="h-[2px] w-4 rounded-full bg-cyan-300"></span>
          <span class="h-[2px] w-4 rounded-full bg-cyan-300"></span>
        </span>
      </button>

      <nav class="space-y-2">
        <button
          v-for="item in menus"
          :key="item.path"
          type="button"
          class="group flex w-full items-center gap-3 rounded-xl border px-3 py-2.5 text-left text-sm transition"
          :class="
            isActive(item.path)
              ? 'border-cyan-500/45 bg-cyan-950/70 text-cyan-100 shadow-[0_0_0_1px_rgba(56,189,248,0.25)]'
              : 'border-transparent text-cyan-200 hover:border-cyan-500/30 hover:bg-slate-950/85'
          "
          :disabled="isTransitioning"
          @click="handleNavigate(item.path)"
        >
          <span
            class="inline-flex h-8 w-8 items-center justify-center rounded-lg"
            :class="isActive(item.path) ? 'bg-cyan-800/55 text-cyan-100' : 'bg-cyan-900/60 text-cyan-300 group-hover:bg-cyan-800/55'"
          >
            <svg class="h-4.5 w-4.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path v-for="(pathDef, index) in iconPathMap[item.icon]" :key="`${item.path}-${index}`" :d="pathDef" />
            </svg>
          </span>
          <span class="truncate font-semibold">{{ item.label }}</span>
        </button>
      </nav>
    </aside>

    <div v-if="mobileMenuOpen" class="fixed inset-0 z-40 bg-sky-950/30 backdrop-blur-[2px] lg:hidden" @click="mobileMenuOpen = false"></div>

    <aside
      class="fixed inset-y-0 left-0 z-50 w-[84%] max-w-[320px] border-r border-cyan-500/30 bg-slate-950/82 p-5 shadow-[0_24px_46px_rgba(56,189,248,0.16)] backdrop-blur-2xl transition-transform duration-300 lg:hidden"
      :class="mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <button
        type="button"
        class="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-500/45 bg-slate-950 text-cyan-100 shadow-[0_8px_18px_rgba(56,189,248,0.18)] transition hover:bg-cyan-950/70"
        title="收起侧栏"
        @click="mobileMenuOpen = false"
      >
        <span class="inline-flex flex-col gap-1">
          <span class="h-[2px] w-4 rounded-full bg-cyan-300"></span>
          <span class="h-[2px] w-4 rounded-full bg-cyan-300"></span>
          <span class="h-[2px] w-4 rounded-full bg-cyan-300"></span>
        </span>
      </button>

      <nav class="space-y-2">
        <button
          v-for="item in menus"
          :key="`mobile-${item.path}`"
          type="button"
          class="group flex w-full items-center gap-3 rounded-xl border px-3 py-3 text-left text-sm transition"
          :class="
            isActive(item.path)
              ? 'border-cyan-500/45 bg-cyan-950/70 text-cyan-100 shadow-[0_0_0_1px_rgba(56,189,248,0.25)]'
              : 'border-transparent text-cyan-200 hover:border-cyan-500/30 hover:bg-slate-950/85'
          "
          :disabled="isTransitioning"
          @click="handleNavigate(item.path)"
        >
          <span
            class="inline-flex h-8 w-8 items-center justify-center rounded-lg"
            :class="isActive(item.path) ? 'bg-cyan-800/55 text-cyan-100' : 'bg-cyan-900/60 text-cyan-300 group-hover:bg-cyan-800/55'"
          >
            <svg class="h-4.5 w-4.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path v-for="(pathDef, index) in iconPathMap[item.icon]" :key="`${item.path}-mobile-${index}`" :d="pathDef" />
            </svg>
          </span>
          <span class="truncate font-semibold">{{ item.label }}</span>
        </button>
      </nav>
    </aside>

    <button
      type="button"
      class="fixed z-30 inline-flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-500/45 bg-slate-950/85 text-cyan-100 shadow-[0_10px_20px_rgba(56,189,248,0.22)] backdrop-blur transition hover:bg-cyan-950/70"
      :class="desktopMenuOpen ? 'left-4 top-4 lg:hidden' : 'left-4 top-4 lg:left-3 lg:top-4'"
      :title="desktopMenuOpen ? '收起侧栏' : '展开侧栏'"
      @click="toggleGlobalMenu"
    >
      <span class="inline-flex flex-col gap-1">
        <span class="h-[2px] w-4 rounded-full bg-cyan-300"></span>
        <span class="h-[2px] w-4 rounded-full bg-cyan-300"></span>
        <span class="h-[2px] w-4 rounded-full bg-cyan-300"></span>
      </span>
    </button>

    <div class="relative flex min-h-screen w-full flex-col transition-[padding] duration-300" :class="desktopMenuOpen ? 'lg:pl-[292px]' : 'lg:pl-0'">
      <div class="stage-shell flex-1 px-0 pb-0 pt-0" ref="stageRef">
        <div ref="energyBurstRef" class="energy-burst"></div>

        <main ref="contentFrameRef" class="content-frame rounded-[28px] border border-cyan-500/30 bg-slate-950/52 p-3 shadow-[0_30px_56px_rgba(56,189,248,0.16)] backdrop-blur-2xl" :class="mainContentClass">
          <div v-if="showPageTitle" class="mb-4 pl-14">
            <h1 class="text-2xl font-black tracking-tight text-cyan-100 sm:text-[2rem]">{{ currentPageTitle }}</h1>
          </div>
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { gsap } from 'gsap'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const iconPathMap = {
  home: ['M3 10.5 12 3l9 7.5', 'M5 9.8V20h14V9.8', 'M10 20v-6h4v6'],
  dashboard: ['M4 4h16v16H4z', 'M8 15v3', 'M12 11v7', 'M16 7v11'],
  enterprise: ['M5 20V6h14v14', 'M9 10h2', 'M13 10h2', 'M9 14h2', 'M13 14h2', 'M11 20v-3h2'],
  agent: ['M12 3v2', 'M9 5h6', 'M6 9h12v9H6z', 'M4 11h2', 'M18 11h2', 'M9 13h.01', 'M15 13h.01', 'M9 17h6'],
  analysis: ['M4 19h16', 'M6 15l4-4 3 3 5-6', 'M18 8h-4', 'M14 8v4'],
  upload: ['M12 4v11', 'M8 8l4-4 4 4', 'M5 20h14'],
} as const

type IconKey = keyof typeof iconPathMap
type MenuItem = { path: string; label: string; icon: IconKey }

type HomeNavigateEvent = CustomEvent<{ path: string }>

const menus: MenuItem[] = [
  { path: '/home', label: '主界面', icon: 'home' },
  { path: '/dashboard', label: '行业对比大屏', icon: 'dashboard' },
  { path: '/enterprise-detail', label: '企业详情', icon: 'enterprise' },
  { path: '/agent-room', label: '智能体', icon: 'agent' },
  { path: '/data-upload', label: '财报上传', icon: 'upload' },
]

const route = useRoute()
const router = useRouter()
const mobileMenuOpen = ref(false)
const desktopMenuOpen = ref(false)
const isTransitioning = ref(false)
const stageRef = ref<HTMLElement | null>(null)
const contentFrameRef = ref<HTMLElement | null>(null)
const energyBurstRef = ref<HTMLElement | null>(null)
const SIDEBAR_STORAGE_KEY = 'desktop-menu-open'

const isActive = (path: string) => route.path === path
const isHomePage = computed(() => route.path === '/home')
const isAgentRoomPage = computed(() => route.path === '/agent-room')
const currentPageTitle = computed(() => menus.find((item) => item.path === route.path)?.label || '')
const showPageTitle = computed(() => !isHomePage.value && !isAgentRoomPage.value && currentPageTitle.value !== '')
const mainContentClass = computed(() => {
  if (isHomePage.value || isAgentRoomPage.value) {
    return 'content-frame--immersive border-0 bg-transparent p-0 shadow-none backdrop-blur-0 rounded-none'
  }
  return 'p-4 sm:p-5 lg:p-6'
})

const runRouteTransition = async (path: string) => {
  if (path === route.path) {
    mobileMenuOpen.value = false
    return
  }

  if (isTransitioning.value) return

  const frame = contentFrameRef.value
  const burst = energyBurstRef.value
  if (!frame || !burst) {
    await router.push(path)
    mobileMenuOpen.value = false
    return
  }

  isTransitioning.value = true
  await new Promise<void>((resolve) => {
    const timeline = gsap.timeline({ onComplete: resolve })

    timeline.set(burst, { opacity: 0, scale: 0.3 })
    timeline.to(frame, {
      duration: 0.42,
      scale: 0.87,
      rotateY: -14,
      rotateX: 7,
      z: -40,
      filter: 'blur(2px)',
      transformOrigin: '50% 44%',
      ease: 'power3.inOut',
    })
    timeline.to(
      burst,
      {
        opacity: 1,
        scale: 1.25,
        duration: 0.28,
        ease: 'power2.out',
      },
      0.05,
    )
    timeline.to(
      burst,
      {
        opacity: 0,
        scale: 2.4,
        duration: 0.32,
        ease: 'power2.in',
      },
      0.27,
    )
    timeline.call(() => {
      void router.push(path)
    }, [], 0.24)
    timeline.fromTo(
      frame,
      {
        scale: 0.9,
        rotateY: 14,
        rotateX: -6,
        opacity: 0.78,
        filter: 'blur(3px)',
      },
      {
        duration: 0.56,
        scale: 1,
        rotateY: 0,
        rotateX: 0,
        opacity: 1,
        filter: 'blur(0px)',
        ease: 'power3.out',
      },
      0.32,
    )
  })

  await nextTick()
  isTransitioning.value = false
  mobileMenuOpen.value = false
}

const handleNavigate = (path: string) => {
  void runRouteTransition(path)
}

const toggleGlobalMenu = () => {
  if (window.innerWidth < 1024) {
    mobileMenuOpen.value = !mobileMenuOpen.value
    return
  }
  desktopMenuOpen.value = !desktopMenuOpen.value
}

const handleHomeNavigate = (event: Event) => {
  const navigateEvent = event as HomeNavigateEvent
  if (navigateEvent.detail?.path) {
    void runRouteTransition(navigateEvent.detail.path)
  }
}

onMounted(() => {
  const cachedValue = window.localStorage.getItem(SIDEBAR_STORAGE_KEY)
  desktopMenuOpen.value = cachedValue === '1'
  window.addEventListener('home:navigate', handleHomeNavigate as EventListener)
})

onBeforeUnmount(() => {
  window.removeEventListener('home:navigate', handleHomeNavigate as EventListener)
})

watch(
  () => route.path,
  () => {
    mobileMenuOpen.value = false
  },
)

watch(desktopMenuOpen, (value) => {
  window.localStorage.setItem(SIDEBAR_STORAGE_KEY, value ? '1' : '0')
})
</script>

<style scoped>
.app-shell {
  isolation: isolate;
}

.app-glow {
  position: fixed;
  border-radius: 999px;
  filter: blur(36px);
  pointer-events: none;
  z-index: 0;
}

.app-glow-left {
  left: -12vw;
  top: -18vh;
  width: 36vw;
  height: 36vw;
  min-width: 280px;
  min-height: 280px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.34), rgba(37, 99, 235, 0));
}

.app-glow-right {
  right: -8vw;
  top: 34vh;
  width: 30vw;
  height: 30vw;
  min-width: 240px;
  min-height: 240px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.32), rgba(56, 189, 248, 0));
}

.stage-shell {
  perspective: 1600px;
  position: relative;
  z-index: 1;
}

.content-frame {
  transform-style: preserve-3d;
  min-height: calc(100vh - 6.5rem);
  background:
    radial-gradient(680px 340px at 86% 16%, rgba(56, 189, 248, 0.28) 0%, rgba(56, 189, 248, 0) 72%),
    linear-gradient(162deg, rgba(2, 8, 23, 0.76), rgba(18, 70, 146, 0.62));
  box-shadow:
    0 22px 40px rgba(2, 132, 199, 0.2),
    inset 0 0 0 1px rgba(56, 189, 248, 0.22);
}

.content-frame--immersive {
  min-height: 100vh;
}

.energy-burst {
  position: fixed;
  left: 50%;
  top: 50%;
  width: 18px;
  height: 18px;
  pointer-events: none;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.95), rgba(14, 165, 233, 0.92));
  box-shadow:
    0 0 16px rgba(56, 189, 248, 0.52),
    0 0 36px rgba(14, 165, 233, 0.3),
    0 0 70px rgba(29, 78, 216, 0.24);
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.3);
  z-index: 70;
}
</style>


