<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const documents = ref([])
const loading = ref(true)
const shareUrl = ref('')
const showShareModal = ref(false)

onMounted(async () => {
  await loadDocuments()
})

async function loadDocuments() {
  loading.value = true
  try {
    const res = await api.getDocuments()
    documents.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function editDoc(id) {
  router.push(`/editor/${id}`)
}

async function deleteDoc(id) {
  if (!confirm('确定要删除这篇文档吗？')) return
  try {
    await api.deleteDocument(id)
    await loadDocuments()
  } catch (e) {
    alert('删除失败')
  }
}

async function shareDoc(id) {
  try {
    const res = await api.createShare(id)
    shareUrl.value = `${window.location.origin}/share/${res.data.share_url.split('/')[2]}`
    showShareModal.value = true
  } catch (e) {
    alert('生成分享链接失败')
  }
}

function copyShareUrl() {
  navigator.clipboard.writeText(shareUrl.value)
  alert('链接已复制到剪贴板')
}

function formatDate(date) {
  return new Date(date).toLocaleString('zh-CN')
}
</script>

<template>
  <div class="documents-page">
    <div class="page-header">
      <h1>我的文档</h1>
      <RouterLink to="/editor" class="btn primary">新建文档</RouterLink>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="documents.length === 0" class="empty">
      <p>暂无文档，点击上方按钮创建</p>
    </div>

    <div v-else class="document-list">
      <div v-for="doc in documents" :key="doc.id" class="document-card">
        <div class="doc-info">
          <h3>{{ doc.title }}</h3>
          <p class="doc-meta">
            创建于 {{ formatDate(doc.created_at) }} ·
            更新于 {{ formatDate(doc.updated_at) }}
          </p>
        </div>
        <div class="doc-actions">
          <button @click="editDoc(doc.id)" class="btn">编辑</button>
          <button v-if="!doc.has_share_link" @click="shareDoc(doc.id)" class="btn">分享</button>
          <button v-else @click="shareDoc(doc.id)" class="btn success">更新分享</button>
          <button @click="deleteDoc(doc.id)" class="btn danger">删除</button>
        </div>
      </div>
    </div>

    <div v-if="showShareModal" class="modal" @click.self="showShareModal = false">
      <div class="modal-content">
        <h2>分享链接</h2>
        <p class="share-info">链接有效期 7 天</p>
        <div class="share-url">
          <input type="text" :value="shareUrl" readonly />
          <button @click="copyShareUrl" class="btn primary">复制</button>
        </div>
        <button @click="showShareModal = false" class="btn">关闭</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.documents-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
.page-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
}
.loading, .empty {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}
.document-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.document-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}
.doc-info h3 {
  font-size: 1rem;
  margin-bottom: 0.25rem;
}
.doc-meta {
  font-size: 0.875rem;
  color: #6b7280;
}
.doc-actions {
  display: flex;
  gap: 0.5rem;
}
.btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  font-size: 0.875rem;
  text-decoration: none;
  color: #374151;
}
.btn:hover {
  background: #f3f4f6;
}
.btn.primary {
  background: #2563eb;
  border-color: #2563eb;
  color: #fff;
}
.btn.primary:hover {
  background: #1d4ed8;
}
.btn.success {
  background: #059669;
  border-color: #059669;
  color: #fff;
}
.btn.danger {
  color: #dc2626;
}
.btn.danger:hover {
  background: #fef2f2;
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}
.modal-content h2 {
  margin-bottom: 0.5rem;
}
.share-info {
  color: #6b7280;
  margin-bottom: 1rem;
}
.share-url {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.share-url input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}
</style>
