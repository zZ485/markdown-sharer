<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import MarkdownIt from 'markdown-it'
import api from '../api'

const route = useRoute()
const document = ref(null)
const error = ref(null)
const loading = ref(true)
const renderedContent = ref('')

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})

onMounted(async () => {
  const token = route.params.token
  try {
    const res = await api.getSharedDocument(token)
    document.value = res.data
    renderedContent.value = md.render(document.value.content)
  } catch (e) {
    if (e.response?.status === 410) {
      error.value = '分享链接已过期'
    } else {
      error.value = '文档不存在'
    }
  } finally {
    loading.value = false
  }
})

function downloadDocument() {
  const token = route.params.token
  window.location.href = `/api/share/${token}/download`
}

function formatDate(date) {
  return new Date(date).toLocaleString('zh-CN')
}
</script>

<template>
  <div class="share-view">
    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="error" class="error">
      <h2>{{ error }}</h2>
      <p>请联系文档分享者获取新的链接</p>
    </div>

    <template v-else-if="document">
      <header class="share-header">
        <h1>{{ document.title }}</h1>
        <div class="meta">
          <span>分享时间：{{ formatDate(document.created_at) }}</span>
          <span>有效期至：{{ formatDate(document.expires_at) }}</span>
        </div>
        <button @click="downloadDocument" class="btn primary">下载文档</button>
      </header>
      <article class="markdown-body" v-html="renderedContent"></article>
    </template>
  </div>
</template>

<style scoped>
.share-view {
  min-height: 100vh;
  background: #fff;
}
.loading, .error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
}
.error h2 {
  color: #dc2626;
  margin-bottom: 0.5rem;
}
.error p {
  color: #6b7280;
}
.share-header {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem 1rem;
  border-bottom: 1px solid #e5e7eb;
}
.share-header h1 {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}
.meta {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 1rem;
}
.meta span {
  margin-right: 1.5rem;
}
.btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  font-size: 0.875rem;
}
.btn.primary {
  background: #2563eb;
  border-color: #2563eb;
  color: #fff;
}
.btn.primary:hover {
  background: #1d4ed8;
}
.markdown-body {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
  line-height: 1.8;
}
.markdown-body :deep(h1) {
  font-size: 1.75rem;
  margin: 1.5rem 0 1rem;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid #e5e7eb;
}
.markdown-body :deep(h2) {
  font-size: 1.5rem;
  margin: 1.25rem 0 0.75rem;
}
.markdown-body :deep(h3) {
  font-size: 1.25rem;
  margin: 1rem 0 0.5rem;
}
.markdown-body :deep(p) {
  margin: 0.75rem 0;
}
.markdown-body :deep(ul), .markdown-body :deep(ol) {
  padding-left: 1.5rem;
  margin: 0.75rem 0;
}
.markdown-body :deep(li) {
  margin: 0.25rem 0;
}
.markdown-body :deep(code) {
  background: #f3f4f6;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-size: 0.875rem;
}
.markdown-body :deep(pre) {
  background: #1f2937;
  color: #e5e7eb;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1rem 0;
}
.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}
.markdown-body :deep(blockquote) {
  border-left: 4px solid #e5e7eb;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #6b7280;
}
.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}
.markdown-body :deep(th), .markdown-body :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 0.5rem 0.75rem;
  text-align: left;
}
.markdown-body :deep(th) {
  background: #f9fafb;
}
.markdown-body :deep(a) {
  color: #2563eb;
  text-decoration: none;
}
.markdown-body :deep(a:hover) {
  text-decoration: underline;
}
.markdown-body :deep(img) {
  max-width: 100%;
  border-radius: 4px;
}
.markdown-body :deep(hr) {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 1.5rem 0;
}
</style>
