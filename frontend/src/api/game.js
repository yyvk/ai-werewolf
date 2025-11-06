import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const gameAPI = {
  // 获取服务健康状态
  getHealth() {
    return api.get('/health')
  },

  // 获取统计信息
  getStats() {
    return api.get('/stats')
  },

  // 创建游戏
  createGame(data) {
    return api.post('/games', data)
  },

  // 获取游戏列表
  getGames() {
    return api.get('/games')
  },

  // 获取游戏详情
  getGame(gameId) {
    return api.get(`/games/${gameId}`)
  },

  // 开始游戏
  startGame(gameId) {
    return api.post(`/games/${gameId}/start`)
  },

  // 下一轮
  nextRound(gameId) {
    return api.post(`/games/${gameId}/next-round`)
  },

  // 执行游戏操作
  gameAction(gameId, action) {
    return api.post(`/games/${gameId}/action`, action)
  },

  // 删除游戏
  deleteGame(gameId) {
    return api.delete(`/games/${gameId}`)
  },
}

export default api

