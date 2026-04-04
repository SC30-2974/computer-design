<template>
  <section class="min-h-[calc(100vh-4rem)] rounded-3xl border border-emerald-300/30 bg-white/80 p-3 shadow-[0_16px_40px_rgba(16,185,129,0.22)] sm:p-4 -mx-2 sm:-mx-4 lg:-mx-6 flex">
    <div class="flex flex-1 flex-col overflow-hidden rounded-2xl border border-emerald-300/25 bg-white/90">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-emerald-300/10 px-4 py-3">
        <h3 class="text-sm font-semibold text-emerald-900">Dify 智能研判室</h3>
        <span class="text-xs text-emerald-700">沉浸式问答</span>
      </div>

      <div class="flex-1 overflow-visible p-2 pt-6 sm:p-3 sm:pt-7">
        <iframe
          src="https://udify.app/chatbot/v2rkJLTx9Z9hWdS3"
          class="h-[calc(100%-1.75rem)] w-full min-h-[calc(100vh-14rem)] rounded-xl bg-white"
          frameborder="0"
          allow="microphone"
        ></iframe>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// 智能研判室页面采用嵌入 Dify 聊天能力。
// 容器通过固定可用高度 + overflow 控制，避免出现双滚动条。
</script>
