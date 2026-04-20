<script setup>
import { computed } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
const route = useRoute()
const isSharePage = computed(() => route.name === 'ShareView')
</script>

<template>
  <div class="app">
    <header v-if="!isSharePage" class="header">
      <RouterLink to="/documents" class="logo">Markdown Sharer</RouterLink>
      <nav>
        <RouterLink to="/documents">文档列表</RouterLink>
        <RouterLink to="/editor">新建文档</RouterLink>
      </nav>
    </header>
    <main :class="{ 'share-page': isSharePage }">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
}
.logo {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  text-decoration: none;
}
nav {
  display: flex;
  gap: 1.5rem;
}
nav a {
  color: #6b7280;
  text-decoration: none;
}
nav a:hover,
nav a.router-link-active {
  color: #2563eb;
}
.share-page {
  padding: 0;
}
</style>
