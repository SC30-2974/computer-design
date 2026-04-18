<template>
  <section class="agent-room flex h-screen min-h-screen p-0">
    <div class="flex flex-1 flex-col overflow-hidden rounded-none bg-transparent">
      <div class="flex-1 overflow-hidden p-0">
        <iframe
          src="https://udify.app/chatbot/v2rkJLTx9Z9hWdS3"
          class="agent-room-frame h-full w-full rounded-none"
          frameborder="0"
          allow="microphone"
        ></iframe>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// 智能研判室页面采用嵌入 Dify 聊天能力。
// 容器改为沉浸式全屏，直接让智能体页面占满可视区。
</script>

<style scoped>
.agent-room {
  background:
    radial-gradient(840px 500px at 16% 12%, rgba(37, 99, 235, 0.4), transparent 60%),
    radial-gradient(740px 460px at 86% 78%, rgba(14, 165, 233, 0.32), transparent 66%),
    linear-gradient(158deg, rgba(2, 8, 23, 0.86), rgba(18, 70, 146, 0.76));
}

.agent-room-frame {
  background: linear-gradient(158deg, rgba(2, 8, 23, 0.78), rgba(18, 70, 146, 0.66));
  filter: none;
}
</style>



