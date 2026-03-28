<template>
  <div class="flex min-h-screen bg-emerald-grid bg-[#f7fff9] text-emerald-900">
    <aside class="fixed inset-y-0 left-0 z-20 w-72 border-r border-emerald-300/25 bg-white/90 backdrop-blur-xl">
      <div class="flex h-full flex-col px-5 py-6">
        <div class="mb-8">
          <p class="text-xs uppercase tracking-[0.36em] text-emerald-300/80">Energy ESG AI</p>
          <h1 class="mt-3 text-xl font-semibold text-emerald-900">新能源财报智能分析平台</h1>
          <p class="mt-2 text-xs leading-5 text-emerald-700">绿色产业洞察 · 智能研判 · 资产可追溯</p>
        </div>

        <nav class="space-y-2">
          <RouterLink
            v-for="item in menus"
            :key="item.path"
            :to="item.path"
            class="group flex items-center gap-3 rounded-xl border border-transparent px-3 py-3 text-sm transition-all duration-300"
            :class="isActive(item.path)
              ? 'border-emerald-300/40 bg-emerald-500/20 text-emerald-900 shadow-[0_0_0_1px_rgba(110,231,183,0.12)]'
              : 'text-emerald-800 hover:border-emerald-300/25 hover:bg-emerald-500/15 hover:text-emerald-900'"
          >
            <span
              class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-base"
              :class="isActive(item.path) ? 'bg-emerald-300/25 text-emerald-900' : 'bg-emerald-100 text-emerald-900/75 group-hover:bg-emerald-200'"
            >
              {{ item.icon }}
            </span>
            <span class="font-medium">{{ item.label }}</span>
          </RouterLink>
        </nav>

      </div>
    </aside>

    <div class="ml-72 flex min-h-screen w-[calc(100%-18rem)] flex-col bg-[#f7fff9]">
      <header class="sticky top-0 z-10 border-b border-emerald-300/20 bg-white/85 backdrop-blur-xl">
        <div class="flex h-16 items-center justify-between px-8">
          <div>
            <h2 class="text-base font-semibold text-emerald-900">{{ currentTitle }}</h2>
            <p class="text-xs text-emerald-700">新能源环保风格 · 现代 SaaS 管理台</p>
          </div>
          <div class="rounded-full border border-emerald-300/20 bg-emerald-100 px-3 py-1 text-xs text-emerald-900">
            环保智能模式
          </div>
        </div>
      </header>

      <main class="flex-1 bg-[#f7fff9] p-8">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

// 侧边栏菜单定义：与路由一一对应。
const menus = [
  { path: '/home', label: '主界面', icon: '🏠' },
  { path: '/dashboard', label: '宏观行业大屏', icon: '📊' },
  { path: '/agent-room', label: '智能研判室', icon: '🤖' },
  { path: '/financial-analysis', label: '财务指标对比', icon: '📈' },
  { path: '/knowledge-base', label: '知识库资产管理', icon: '📚' },
]

const route = useRoute()

// 当前菜单高亮判断。
const isActive = (path: string) => route.path === path

// 顶部标题随当前路由切换。
const currentTitle = computed(() => {
  const target = menus.find((item) => item.path === route.path)
  return target?.label || '新能源财报智能分析平台'
})
</script>


