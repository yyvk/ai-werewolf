import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import GameRoom from '../views/GameRoom.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/game/:id',
      name: 'game',
      component: GameRoom,
      props: true
    }
  ]
})

export default router



