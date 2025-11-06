<template>
  <div class="home">
    <div class="container">
      <div class="welcome-section">
        <h1 class="title">欢迎来到 AI狼人杀</h1>
        <p class="subtitle">观看AI之间的精彩推理对决</p>
        
        <div class="stats-cards">
          <div class="stat-card">
            <div class="stat-value">{{ stats.total_games }}</div>
            <div class="stat-label">总游戏数</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ stats.active_games }}</div>
            <div class="stat-label">进行中</div>
          </div>
        </div>
      </div>

      <div class="actions-section">
        <button @click="showCreateDialog = true" class="btn btn-primary btn-large">
          🎮 创建新游戏
        </button>
      </div>

      <div class="games-section" v-if="games.length > 0">
        <h2>游戏列表</h2>
        <div class="games-grid">
          <div v-for="game in games" :key="game.game_id" class="game-card">
            <div class="game-header">
              <span class="game-status" :class="game.status">
                {{ getStatusText(game.status) }}
              </span>
              <span class="game-phase">{{ game.phase }}</span>
            </div>
            <div class="game-body">
              <p class="game-id">游戏 ID: {{ game.game_id.substring(0, 8) }}...</p>
              <p class="game-info">
                玩家数: {{ game.num_players }} | 
                轮次: {{ game.round }}
              </p>
            </div>
            <div class="game-actions">
              <button @click="viewGame(game.game_id)" class="btn btn-small">
                查看
              </button>
              <button @click="deleteGameConfirm(game.game_id)" class="btn btn-small btn-danger">
                删除
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="!loading" class="empty-state">
        <p>还没有游戏，创建一个开始吧！</p>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
    </div>

    <!-- 创建游戏对话框 -->
    <div v-if="showCreateDialog" class="modal" @click.self="showCreateDialog = false">
      <div class="modal-content">
        <h2>创建新游戏</h2>
        <form @submit.prevent="createGame">
          <div class="form-group">
            <label>玩家数量</label>
            <input v-model.number="gameConfig.num_players" type="number" min="4" max="12" class="form-input">
          </div>
          <div class="form-group">
            <label>LLM提供商</label>
            <select v-model="gameConfig.llm_provider" class="form-input">
              <option value="openai">OpenAI (ModelScope)</option>
              <option value="dashscope">通义千问</option>
            </select>
          </div>
          <div class="form-group">
            <label>模型名称（可选）</label>
            <input v-model="gameConfig.model_name" type="text" class="form-input" 
                   placeholder="Qwen/Qwen2.5-32B-Instruct">
          </div>
          <div class="form-actions">
            <button type="button" @click="showCreateDialog = false" class="btn btn-secondary">
              取消
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? '创建中...' : '创建游戏' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useGameStore } from '@/stores/gameStore'

const router = useRouter()
const gameStore = useGameStore()

const showCreateDialog = ref(false)
const gameConfig = ref({
  num_players: 6,
  llm_provider: 'openai',
  model_name: ''
})

const { games, stats, loading } = storeToRefs(gameStore)

function getStatusText(status) {
  const statusMap = {
    'created': '已创建',
    'running': '进行中',
    'finished': '已结束'
  }
  return statusMap[status] || status
}

async function createGame() {
  try {
    const gameId = await gameStore.createGame(gameConfig.value)
    showCreateDialog.value = false
    router.push(`/game/${gameId}`)
  } catch (e) {
    alert('创建游戏失败')
  }
}

function viewGame(gameId) {
  router.push(`/game/${gameId}`)
}

async function deleteGameConfirm(gameId) {
  if (confirm('确定要删除这个游戏吗？')) {
    await gameStore.deleteGame(gameId)
  }
}

onMounted(() => {
  gameStore.fetchGames()
  gameStore.fetchStats()
})
</script>

<style scoped>
.home {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.welcome-section {
  text-align: center;
  margin-bottom: 3rem;
}

.title {
  font-size: 3rem;
  margin: 0 0 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 2rem;
}

.stats-cards {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  min-width: 150px;
}

.stat-value {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
}

.stat-label {
  color: #666;
  margin-top: 0.5rem;
}

.actions-section {
  text-align: center;
  margin: 3rem 0;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-large {
  padding: 1.2rem 3rem;
  font-size: 1.3rem;
  font-weight: bold;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
}

.games-section {
  margin-top: 3rem;
}

.games-section h2 {
  margin-bottom: 1.5rem;
}

.games-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.game-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.game-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.game-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.game-status {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
}

.game-status.created {
  background: #3498db;
  color: white;
}

.game-status.running {
  background: #2ecc71;
  color: white;
}

.game-status.finished {
  background: #95a5a6;
  color: white;
}

.game-phase {
  color: #666;
  font-size: 0.9rem;
}

.game-body {
  margin-bottom: 1rem;
}

.game-id {
  font-family: monospace;
  color: #666;
  font-size: 0.9rem;
}

.game-info {
  color: #444;
  margin-top: 0.5rem;
}

.game-actions {
  display: flex;
  gap: 0.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.1rem;
}

.loading {
  text-align: center;
  padding: 3rem;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 模态框 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  max-width: 500px;
  width: 90%;
}

.modal-content h2 {
  margin-top: 0;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}
</style>

