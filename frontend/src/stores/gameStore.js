import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { gameAPI } from '@/api/game'

export const useGameStore = defineStore('game', () => {
  // 状态
  const games = ref([])
  const currentGame = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const stats = ref({ total_games: 0, active_games: 0 })

  // 计算属性
  const activeGames = computed(() => 
    games.value.filter(g => g.status === 'running')
  )

  const hasCurrentGame = computed(() => currentGame.value !== null)

  // 操作
  async function fetchGames() {
    try {
      loading.value = true
      error.value = null
      const data = await gameAPI.getGames()
      games.value = data.games || []
    } catch (e) {
      error.value = '获取游戏列表失败'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchStats() {
    try {
      const data = await gameAPI.getStats()
      stats.value = data
    } catch (e) {
      console.error('获取统计失败:', e)
    }
  }

  async function createGame(config) {
    try {
      loading.value = true
      error.value = null
      const data = await gameAPI.createGame(config)
      
      if (data.success) {
        await fetchGames()
        return data.game_id
      }
    } catch (e) {
      error.value = '创建游戏失败'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function loadGame(gameId) {
    try {
      loading.value = true
      error.value = null
      const data = await gameAPI.getGame(gameId)
      currentGame.value = data
      return data
    } catch (e) {
      error.value = '加载游戏失败'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function startGame(gameId) {
    try {
      loading.value = true
      error.value = null
      const data = await gameAPI.startGame(gameId)
      
      if (data.success) {
        await loadGame(gameId)
      }
      return data
    } catch (e) {
      error.value = '开始游戏失败'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteGame(gameId) {
    try {
      await gameAPI.deleteGame(gameId)
      await fetchGames()
    } catch (e) {
      error.value = '删除游戏失败'
      console.error(e)
      throw e
    }
  }

  async function gameAction(gameId, action) {
    try {
      loading.value = true
      error.value = null
      
      // 使用nextRound API
      if (action.type === 'next-round') {
        const data = await gameAPI.nextRound(gameId)
        return data
      } else {
        const data = await gameAPI.gameAction(gameId, action)
        return data
      }
    } catch (e) {
      error.value = '执行操作失败'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  function clearCurrentGame() {
    currentGame.value = null
  }

  return {
    // 状态
    games,
    currentGame,
    loading,
    error,
    stats,
    // 计算属性
    activeGames,
    hasCurrentGame,
    // 操作
    fetchGames,
    fetchStats,
    createGame,
    loadGame,
    startGame,
    deleteGame,
    gameAction,
    clearCurrentGame,
  }
})

