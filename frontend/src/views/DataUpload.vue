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
        :disabled="uploading || deletingId !== null"
        @click="triggerUpload"
      >
        {{ uploading ? '上传中...' : '上传最新财报 PDF' }}
      </button>

      <p v-if="statusText" class="mt-3 text-sm text-emerald-800">{{ statusText }}</p>
      <div
        v-if="isRefreshingData"
        class="mt-3 inline-flex items-center gap-2 rounded-full border border-emerald-300/40 bg-white/90 px-3 py-1.5 text-xs font-medium text-emerald-800"
      >
        <span class="h-2 w-2 animate-pulse rounded-full bg-emerald-500"></span>
        <span>数据刷新中，完成后会自动同步到其他页面。</span>
      </div>
    </div>

    <div class="rounded-2xl border border-emerald-300/25 bg-white p-5">
      <div class="mb-3 flex items-center justify-between">
        <h4 class="text-sm font-semibold text-emerald-900">上传记录</h4>
        <button
          class="text-xs text-emerald-700 disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="uploading || deletingId !== null || isRefreshingData"
          @click="fetchUploads"
        >
          刷新记录
        </button>
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
                <div class="flex items-center gap-3">
                  <button class="text-emerald-700 hover:underline" @click="openUpload(item.id)">打开 PDF</button>
                  <button
                    class="text-rose-600 hover:underline disabled:cursor-not-allowed disabled:opacity-50"
                    :disabled="uploading || isRefreshingData || deletingId === item.id"
                    @click="handleDelete(item)"
                  >
                    {{ deletingId === item.id ? '删除中...' : '删除' }}
                  </button>
                </div>
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
        <li>删除上传记录后，其他页面会同步刷新相关图表数据。</li>
      </ul>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { deleteUpload, getCompanies, getUploadFileUrl, listUploads, refreshData, uploadFinancePdf } from '../api/finance'

type UploadItem = {
  id: number
  fileName: string
  uploadTime: string
}

const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)
const deletingId = ref<number | null>(null)
const isRefreshingData = ref(false)
const statusText = ref('')
const uploads = ref<UploadItem[]>([])

const triggerUpload = () => {
  if (uploading.value || deletingId.value !== null || isRefreshingData.value) return
  fileInput.value?.click()
}

const emitDataRefreshed = () => {
  const now = Date.now().toString()
  localStorage.setItem('dataRefreshAt', now)
  window.dispatchEvent(new CustomEvent('data-refreshed', { detail: { at: now } }))
}

const buildSignature = (items: any[]) =>
  items
    .map((item) => `${item.company_name}-${item.revenue}-${item.profit}-${item.margin}`)
    .join('|')

const pollRefresh = async (baselineSignature: string) => {
  const maxTries = 60
  for (let i = 0; i < maxTries; i += 1) {
    await new Promise((resolve) => setTimeout(resolve, 3000))
    try {
      const { data } = await getCompanies()
      const items = Array.isArray(data?.items) ? data.items : []
      const signature = buildSignature(items)
      if (signature !== baselineSignature) {
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

const handleDelete = async (item: UploadItem) => {
  if (uploading.value || deletingId.value === item.id) return

  const confirmed = window.confirm(`确认删除《${item.fileName}》吗？删除后其他模块的数据会同步刷新。`)
  if (!confirmed) return

  deletingId.value = item.id
  statusText.value = '正在删除，请稍候...'
  try {
    const before = await getCompanies()
    const beforeItems = Array.isArray(before?.data?.items) ? before.data.items : []
    const baselineSignature = buildSignature(beforeItems)

    await deleteUpload(item.id)
    uploads.value = uploads.value.filter((upload) => upload.id !== item.id)
    isRefreshingData.value = true
    statusText.value = `已删除 ${item.fileName}，当前列表已更新，正在后台刷新数据...`
    const refreshed = await pollRefresh(baselineSignature)
    await fetchUploads()
    if (refreshed) {
      emitDataRefreshed()
      statusText.value = `已删除 ${item.fileName}，其他模块数据已同步刷新。`
    } else {
      emitDataRefreshed()
      statusText.value = `已删除 ${item.fileName}，后台刷新时间较长，请稍后查看其他页面数据。`
    }
  } catch (error: any) {
    const detail = error?.response?.data?.detail || error?.message || '未知错误'
    statusText.value = `删除失败：${detail}`
    console.error('删除失败', error)
  } finally {
    isRefreshingData.value = false
    deletingId.value = null
  }
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

    const uploadRes = await uploadFinancePdf(file)
    const uploadedItem = uploadRes?.data?.item
    if (uploadedItem?.id) {
      uploads.value = [
        {
          id: uploadedItem.id,
          fileName: uploadedItem.fileName,
          uploadTime: uploadedItem.uploadTime,
        },
        ...uploads.value.filter((item) => item.id !== uploadedItem.id),
      ]
    }

    isRefreshingData.value = true
    statusText.value = '上传完成，当前列表已更新，正在解析入库并刷新图表...'
    try {
      await refreshData()
      const refreshed = await pollRefresh(baselineSignature)
      await fetchUploads()
      statusText.value = refreshed
        ? '上传完成，其他页面数据已同步刷新。'
        : '上传完成，后台仍在解析中，请稍后查看其他页面数据。'
      if (refreshed) {
        emitDataRefreshed()
      }
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
    isRefreshingData.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

onMounted(() => {
  fetchUploads()
})
</script>
