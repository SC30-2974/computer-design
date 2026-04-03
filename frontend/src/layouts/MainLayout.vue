<template>
  <div class="min-h-screen bg-emerald-grid bg-[#f7fff9] text-emerald-900">
    <aside class="fixed inset-y-0 left-0 z-20 hidden w-72 border-r border-emerald-300/25 bg-white/90 backdrop-blur-xl lg:block">
      <div class="flex h-full flex-col px-5 py-6">
        <div class="mb-8">
          <h1 class="text-xl font-semibold text-emerald-900">新能源财报智能分析平台</h1>
        </div>

        <nav class="space-y-2">
          <RouterLink
            v-for="item in menus"
            :key="item.path"
            :to="item.path"
            class="group flex items-center gap-3 rounded-xl border border-transparent px-3 py-3 text-sm transition-all duration-300"
            :class="
              isActive(item.path)
                ? 'border-emerald-300/40 bg-emerald-500/20 text-emerald-900 shadow-[0_0_0_1px_rgba(110,231,183,0.12)]'
                : 'text-emerald-800 hover:border-emerald-300/25 hover:bg-emerald-500/15 hover:text-emerald-900'
            "
          >
            <span
              class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-base"
              :class="
                isActive(item.path)
                  ? 'bg-emerald-300/25 text-emerald-900'
                  : 'bg-emerald-100 text-emerald-900/75 group-hover:bg-emerald-200'
              "
            >
              {{ item.icon }}
            </span>
            <span class="font-medium">{{ item.label }}</span>
          </RouterLink>
        </nav>
      </div>
    </aside>

    <div
      v-if="mobileMenuOpen"
      class="fixed inset-0 z-40 bg-emerald-950/20 backdrop-blur-[1px] lg:hidden"
      @click="mobileMenuOpen = false"
    ></div>

    <aside
      class="fixed inset-y-0 left-0 z-50 w-[84%] max-w-[320px] border-r border-emerald-300/25 bg-white/95 p-5 backdrop-blur-xl transition-transform duration-300 lg:hidden"
      :class="mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="mb-6 flex items-center justify-between">
        <p class="text-sm font-semibold text-emerald-900">菜单导航</p>
        <button
          class="inline-flex h-8 w-8 items-center justify-center rounded-lg border border-emerald-300/40 text-emerald-900"
          @click="mobileMenuOpen = false"
        >
          ×
        </button>
      </div>
      <nav class="space-y-2">
        <RouterLink
          v-for="item in menus"
          :key="item.path"
          :to="item.path"
          class="group flex items-center gap-3 rounded-xl border border-transparent px-3 py-3 text-sm transition-all duration-300"
          :class="
            isActive(item.path)
              ? 'border-emerald-300/40 bg-emerald-500/20 text-emerald-900 shadow-[0_0_0_1px_rgba(110,231,183,0.12)]'
              : 'text-emerald-800 hover:border-emerald-300/25 hover:bg-emerald-500/15 hover:text-emerald-900'
          "
        >
          <span
            class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-base"
            :class="
              isActive(item.path)
                ? 'bg-emerald-300/25 text-emerald-900'
                : 'bg-emerald-100 text-emerald-900/75 group-hover:bg-emerald-200'
            "
          >
            {{ item.icon }}
          </span>
          <span class="font-medium">{{ item.label }}</span>
        </RouterLink>
      </nav>
    </aside>

    <div class="flex min-h-screen w-full flex-col bg-[#f7fff9] lg:ml-72 lg:w-[calc(100%-18rem)]">
      <header class="sticky top-0 z-10 border-b border-emerald-300/20 bg-white/85 backdrop-blur-xl">
        <div class="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
          <div>
            <h2 class="text-base font-semibold text-emerald-900">{{ currentTitle }}</h2>
          </div>
          <div class="flex items-center gap-2">
            <button
              class="inline-flex h-9 items-center rounded-xl border border-emerald-300/40 bg-white px-3 text-sm text-emerald-900 lg:hidden"
              @click="mobileMenuOpen = true"
            >
              菜单
            </button>
          </div>
        </div>
      </header>

      <main class="flex-1 bg-[#f7fff9] p-4 sm:p-6 lg:p-8">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

// 侧边栏菜单定义：与路由一一对应。
const menus = [
  { path: '/home', label: '主界面', icon: '🏠' },
  { path: '/dashboard', label: '宏观行业大屏', icon: '📊' },
  { path: '/enterprise-detail', label: '企业详情', icon: '🏢' },
  { path: '/agent-room', label: '智能研判室', icon: '🤖' },
  { path: '/financial-analysis', label: '财务指标对比', icon: '📈' },
  { path: '/data-upload', label: '财报上传', icon: '⬆️' },
]

const route = useRoute()
const mobileMenuOpen = ref(false)

// 当前菜单高亮判断。
const isActive = (path: string) => route.path === path

// 顶部标题随当前路由切换。
const currentTitle = computed(() => {
  const target = menus.find((item) => item.path === route.path)
  return target?.label || '新能源财报智能分析平台'
})

// 手机端切换页面后自动收起抽屉菜单。
watch(
  () => route.path,
  () => {
    mobileMenuOpen.value = false
  },
)
</script>
