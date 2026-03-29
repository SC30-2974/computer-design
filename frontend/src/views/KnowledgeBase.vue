<template>
  <section class="space-y-5 rounded-3xl border border-emerald-300/25 bg-white/80 p-4 sm:p-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h3 class="text-lg font-semibold text-emerald-900">知识库资产管理</h3>
        <p class="mt-1 text-sm text-emerald-700">展示财报文档解析、向量化和切块状态。</p>
      </div>

      <input
        ref="fileInputRef"
        type="file"
        accept=".pdf,application/pdf"
        class="hidden"
        @change="onFileSelected"
      />
      <button
        class="w-full rounded-xl bg-emerald-400 px-4 py-2 text-sm font-semibold text-emerald-950 hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-70 sm:w-auto"
        :disabled="uploading"
        @click="triggerUpload"
      >
        {{ uploading ? '上传中...' : '上传最新财报 PDF' }}
      </button>
    </div>

    <p v-if="uploadMessage" class="text-sm text-emerald-700">{{ uploadMessage }}</p>

    <div class="overflow-x-auto rounded-2xl border border-emerald-300/15">
      <table class="min-w-full divide-y divide-emerald-300/10 text-sm">
        <thead class="bg-emerald-50 text-emerald-800">
          <tr>
            <th class="px-4 py-3 text-left font-medium">文档名称</th>
            <th class="px-4 py-3 text-left font-medium">所属企业</th>
            <th class="px-4 py-3 text-left font-medium">上传时间</th>
            <th class="px-4 py-3 text-left font-medium">解析状态</th>
            <th class="px-4 py-3 text-left font-medium">切块数量</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-emerald-300/10 bg-white text-emerald-900">
          <tr v-for="item in documents" :key="item.id" class="hover:bg-emerald-500/5">
            <td class="px-4 py-3">{{ item.fileName }}</td>
            <td class="px-4 py-3">{{ item.company }}</td>
            <td class="px-4 py-3">{{ item.uploadTime }}</td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-3 py-1 text-xs"
                :class="item.status === '向量化完成' ? 'bg-emerald-400/20 text-emerald-800' : 'bg-amber-400/20 text-amber-800'"
              >
                {{ item.status }}
              </span>
            </td>
            <td class="px-4 py-3">{{ item.chunks }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { uploadFinancePdf } from '../api/finance'

// Mock 文档记录：用于展示知识库资产面板。
const documents = ref([
  {
    id: 1,
    fileName: '宁德时代2025Q3财报.pdf',
    company: '宁德时代',
    uploadTime: '2026-03-28 09:20',
    status: '向量化完成',
    chunks: 418,
  },
  {
    id: 2,
    fileName: '比亚迪2025Q3财报.pdf',
    company: '比亚迪',
    uploadTime: '2026-03-28 09:35',
    status: '向量化完成',
    chunks: 392,
  },
  {
    id: 3,
    fileName: '阳光电源2025Q3财报.pdf',
    company: '阳光电源',
    uploadTime: '2026-03-28 09:42',
    status: '解析中',
    chunks: 127,
  },
])

const fileInputRef = ref<HTMLInputElement | null>(null)
const uploading = ref(false)
const uploadMessage = ref('')

const triggerUpload = () => {
  fileInputRef.value?.click()
}

const onFileSelected = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  if (!file.name.toLowerCase().endsWith('.pdf')) {
    uploadMessage.value = '仅支持上传 PDF 文件。'
    input.value = ''
    return
  }

  uploading.value = true
  uploadMessage.value = ''
  try {
    const { data } = await uploadFinancePdf(file)
    if (data?.item) {
      documents.value = [data.item, ...documents.value]
    }
    uploadMessage.value = data?.message || '上传成功。'
  } catch (error: any) {
    uploadMessage.value = error?.response?.data?.detail || '上传失败，请检查后端服务后重试。'
  } finally {
    uploading.value = false
    input.value = ''
  }
}
</script>
