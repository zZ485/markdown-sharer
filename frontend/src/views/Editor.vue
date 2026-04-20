<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Vditor from 'vditor'
import 'vditor/dist/index.css'
import api from '../api'

const router = useRouter()
const route = useRoute()
const docId = ref(null)
const title = ref('')
const saving = ref(false)
let vditor = null

onMounted(async () => {
  initVditor()

  if (route.params.id) {
    docId.value = route.params.id
    await loadDocument()
  } else {
    title.value = '未命名文档'
  }
})

function initVditor() {
  vditor = new Vditor('vditor', {
    height: 'calc(100vh - 130px)',
    placeholder: '开始编写 Markdown...',
    mode: 'sv',
    theme: 'classic',
    preview: {
      theme: {
        current: 'light'
      }
    },
    cache: {
      enable: false
    },
    toolbar: [
      'headings', 'bold', 'italic', 'strike', '|',
      'line', 'quote', 'list', 'ordered-list', 'check', '|',
      'code', 'inline-code', '|',
      'link', 'table', '|',
      'undo', 'redo', '|',
      'preview', 'fullscreen'
    ]
  })
}

async function loadDocument() {
  try {
    const res = await api.getDocument(docId.value)
    title.value = res.data.title
    vditor.setValue(res.data.content)
  } catch (e) {
    alert('加载文档失败')
    router.push('/documents')
  }
}

async function saveDocument() {
  if (!title.value.trim()) {
    alert('请输入标题')
    return
  }

  saving.value = true
  const content = vditor.getValue()

  try {
    if (docId.value) {
      await api.updateDocument(docId.value, { title: title.value, content })
    } else {
      const res = await api.createDocument({ title: title.value, content })
      docId.value = res.data.id
      router.replace(`/editor/${docId.value}`)
    }
    alert('保存成功')
  } catch (e) {
    alert('保存失败')
  } finally {
    saving.value = false
  }
}

function goBack() {
  if (vditor.getValue() && !confirm('未保存的内容将丢失，确定返回吗？')) {
    return
  }
  router.push('/documents')
}
</script>

<template>
  <div class="editor-page">
    <div class="editor-header">
      <input
        v-model="title"
        type="text"
        placeholder="文档标题"
        class="title-input"
      />
      <div class="actions">
        <button @click="goBack" class="btn">返回</button>
        <button @click="saveDocument" class="btn primary" :disabled="saving">
          {{ saving ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>
    <div id="vditor"></div>
  </div>
</template>

<style scoped>
.editor-page {
  height: calc(100vh - 65px);
  display: flex;
  flex-direction: column;
}
.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
}
.title-input {
  flex: 1;
  font-size: 1.25rem;
  font-weight: 500;
  border: none;
  outline: none;
  padding: 0.5rem;
  margin-right: 1rem;
}
.title-input:focus {
  background: #f9fafb;
  border-radius: 4px;
}
.actions {
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
.btn.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
