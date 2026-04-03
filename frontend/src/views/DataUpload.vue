<template>
  <section class="space-y-6 rounded-3xl border border-emerald-300/25 bg-white/85 p-6">
    <div>
      <h3 class="text-lg font-semibold text-emerald-900">财报数据上传</h3>
      <p class="mt-1 text-sm text-emerald-700/80">
        上传新的企业财报 PDF 后，会自动解析入库并刷新图表数据。
      </p>
    </div>

    <div class="rounded-2xl border border-emerald-300/30 bg-emerald-50/60 p-5">
      <input ref="fileInput" type="file" accept="application/pdf" class="hidden" @change="handleFileChange" />
      <button
        type="button"
        class="inline-flex items-center rounded-xl border border-emerald-300/60 bg-white px-4 py-2 text-sm font-semibold text-emerald-900 hover:bg-emerald-50"
        :disabled="uploading"
        @click="triggerUpload"
      >
        {{ uploading ? '上传中...' : '上传最新财报 PDF' }}
      </button>

      <p v-if="statusText" class="mt-3 text-sm text-emerald-800">{{ statusText }}</p>
    </div>

    <div class="rounded-2xl border border-emerald-300/25 bg-white p-5">
      <div class="mb-3 flex items-center justify-between">
        <h4 class="text-sm font-semibold text-emerald-900">上传记录</h4>
        <button class="text-xs text-emerald-700" @click="fetchUploads">刷新记录</button>
      </div>
      <div class="overflow-x-auto rounded-xl border border-emerald-300/20">
        <table class="min-w-full text-sm">
          <thead class="bg-emerald-50 text-emerald-800">
            <tr>
              <th class="px-3 py-2 text-left">文件名</th>
              <th class="px-3 py-2 text-left">上传时间</th>
              <th class="px-3 py-2 text-left">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-emerald-300/15 bg-white text-emerald-900">
            <tr v-for="item in uploads" :key="item.id">
              <td class="px-3 py-2">{{ item.fileName }}</td>
              <td class="px-3 py-2">{{ item.uploadTime }}</td>
              <td class="px-3 py-2">
                <button class="text-emerald-700 hover:underline" @click="openUpload(item.id)">打开 PDF</button>
              </td>
            </tr>
            <tr v-if="uploads.length === 0">
              <td colspan="3" class="px-3 py-6 text-center text-emerald-600/70">暂无上传记录</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="rounded-2xl border border-emerald-300/25 bg-white p-5 text-sm text-emerald-800/80">
      <p class="font-medium text-emerald-900">上传说明</p>
      <ul class="mt-2 list-disc pl-5">
        <li>仅支持 PDF 文件。</li>
        <li>上传成功后会自动触发解析与入库。</li>
        <li>刷新其他页面即可看到最新图表数据。</li>
      </ul>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getCompanies, getUploadFileUrl, listUploads, refreshData, uploadFinancePdf } from '../api/finance'

const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)
const statusText = ref('')
const uploads = ref<any[]>([])

const triggerUpload = () => {
  if (uploading.value) return
  fileInput.value?.click()
}

const buildSignature = (items: any[]) =>
  items
    .map((item) => `${item.company_name}-${item.revenue}-${item.profit}-${item.margin}`)
    .join('|')

const pollRefresh = async (baselineSignature: string) => {
  const maxTries = 10
  for (let i = 0; i < maxTries; i += 1) {
    await new Promise((resolve) => setTimeout(resolve, 3000))
    try {
      const { data } = await getCompanies()
      const items = Array.isArray(data?.items) ? data.items : []
      const signature = buildSignature(items)
      if (signature !== baselineSignature) {
        const now = Date.now().toString()
        localStorage.setItem('dataRefreshAt', now)
        window.dispatchEvent(new CustomEvent('data-refreshed', { detail: { at: now } }))
        return true
      }
    } catch {
      // ignore and retry
    }
  }
  return false
}

const fetchUploads = async () => {
  try {
    const { data } = await listUploads()
    uploads.value = Array.isArray(data?.items) ? data.items : []
  } catch {
    uploads.value = []
  }
}

const openUpload = (id: number) => {
  const url = getUploadFileUrl(id)
  window.open(url, '_blank')
}

const handleFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  uploading.value = true
  statusText.value = '正在上传，请稍候...'
  try {
    const before = await getCompanies()
    const beforeItems = Array.isArray(before?.data?.items) ? before.data.items : []
    const baselineSignature = buildSignature(beforeItems)

    await uploadFinancePdf(file)
    statusText.value = '上传完成，正在解析入库并刷新图表...'
    try {
      await refreshData()
      const refreshed = await pollRefresh(baselineSignature)
      statusText.value = refreshed
        ? '上传完成，数据已刷新。请返回图表页面查看最新结果。'
        : '上传完成，解析中。请稍后手动刷新图表页面。'
      await fetchUploads()
    } catch (refreshError: any) {
      const detail = refreshError?.response?.data?.detail || refreshError?.message || '未知错误'
      statusText.value = `上传成功，但刷新失败：${detail}`
    }
  } catch (error: any) {
    const detail = error?.response?.data?.detail || error?.message || '未知错误'
    statusText.value = `上传失败：${detail}`
    console.error('上传失败', error)
  } finally {
    uploading.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

onMounted(() => {
  fetchUploads()
})
</script>
