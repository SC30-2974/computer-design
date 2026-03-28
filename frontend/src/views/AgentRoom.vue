<template>
  <section class="h-[calc(100vh-9rem)] rounded-3xl border border-emerald-300/30 bg-white/80 p-4 shadow-[0_16px_40px_rgba(16,185,129,0.22)]">
    <div class="flex h-full flex-col overflow-hidden rounded-2xl border border-emerald-300/25 bg-white/90">
      <div class="flex items-center justify-between border-b border-emerald-300/10 px-4 py-3">
        <h3 class="text-sm font-semibold text-emerald-900">Dify 智能研判室</h3>
        <span class="text-xs text-emerald-700">沉浸式问答</span>
      </div>

      <div class="flex-1 overflow-hidden">
        <iframe
          src="https://udify.app/chatbot/v2rkJLTx9Z9hWdS3"
          class="h-full w-full"
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

