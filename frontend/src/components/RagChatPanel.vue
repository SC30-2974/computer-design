<template>
  <div class="rounded-3xl border border-slate-800 bg-slate-950/80 p-6">
    <h3 class="text-xl font-semibold text-white">RAG 智能问答</h3>
    <p class="mt-1 text-sm text-slate-400">已接入 Dify 智能体，直接在下方窗口提问。</p>

    <div class="mt-4 overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/40">
      <iframe
        src="https://udify.app/chatbot/v2rkJLTx9Z9hWdS3"
        style="width: 100%; height: 100%; min-height: 700px"
        frameborder="0"
        allow="microphone"
      ></iframe>
    </div>

    <p class="mt-3 text-xs text-slate-500">如果某些浏览器策略限制内嵌，可能出现空白。</p>
  </div>
</template>
