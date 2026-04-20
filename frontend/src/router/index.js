import { createRouter, createWebHistory } from 'vue-router'
import Editor from '../views/Editor.vue'
import Documents from '../views/Documents.vue'
import ShareView from '../views/ShareView.vue'

const routes = [
  { path: '/', redirect: '/documents' },
  { path: '/documents', name: 'Documents', component: Documents },
  { path: '/editor', name: 'Editor', component: Editor },
  { path: '/editor/:id', name: 'EditorEdit', component: Editor },
  { path: '/share/:token', name: 'ShareView', component: ShareView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
