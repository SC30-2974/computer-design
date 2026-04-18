<template>
  <section class="agent-room min-h-[calc(100vh-4rem)] p-0 -mx-2 sm:-mx-4 lg:-mx-6 flex">
    <div class="flex flex-1 flex-col overflow-hidden rounded-none bg-transparent">
      <div class="flex-1 overflow-visible p-0">
        <iframe
          src="https://udify.app/chatbot/v2rkJLTx9Z9hWdS3"
          class="agent-room-frame h-[calc(100vh-4rem)] w-full rounded-none"
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

<style scoped>
.agent-room {
  background:
    radial-gradient(900px 520px at 14% 8%, rgba(56, 189, 248, 0.08), transparent 60%),
    radial-gradient(740px 460px at 88% 85%, rgba(14, 165, 233, 0.05), transparent 66%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 252, 255, 0.94));
}

.agent-room-frame {
  background: #ffffff;
  filter: none;
}
</style>



