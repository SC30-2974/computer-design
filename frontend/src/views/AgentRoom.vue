<template>
  <section class="min-h-[calc(100vh-4rem)] bg-transparent p-0 -mx-2 sm:-mx-4 lg:-mx-6 flex">
    <div class="flex flex-1 flex-col overflow-hidden rounded-none bg-transparent">
      <div class="flex-1 overflow-visible p-0">
        <iframe
          src="https://udify.app/chatbot/v2rkJLTx9Z9hWdS3"
          class="h-[calc(100vh-4rem)] w-full rounded-none bg-white"
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
