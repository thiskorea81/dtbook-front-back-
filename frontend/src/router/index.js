// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Result from '@/views/Result.vue'
import Chat from '@/views/Chat.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/result', name: 'Result', component: Result },
  { path: '/chat', name: 'Chat', component: Chat }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
