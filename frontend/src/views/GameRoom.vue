<template>
  <div class="game-room">
    <div class="container">
      <div class="game-header">
        <button @click="$router.push('/')" class="btn btn-back">
          ← 返回首页
        </button>
        <h1>游戏房间</h1>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载游戏中...</p>
      </div>

      <div v-else-if="currentGame" class="game-content">
        <div class="game-info-panel">
          <div class="info-card">
            <h3>游戏信息</h3>
            <div class="info-item">
              <span class="label">游戏ID:</span>
              <span class="value">{{ currentGame.game_id.substring(0, 12) }}...</span>
            </div>
            <div class="info-item">
              <span class="label">状态:</span>
              <span class="value status" :class="currentGame.status">
                {{ getStatusText(currentGame.status) }}
              </span>
            </div>
            <div class="info-item">
              <span class="label">阶段:</span>
              <span class="value">{{ currentGame.phase }}</span>
            </div>
            <div class="info-item">
              <span class="label">轮次:</span>
              <span class="value">第 {{ currentGame.round }} 轮</span>
            </div>
            <div class="info-item">
              <span class="label">玩家数:</span>
              <span class="value">{{ currentGame.num_players }}</span>
            </div>
          </div>

          <div class="action-card">
            <button 
              v-if="currentGame.status === 'created'" 
              @click="startGame" 
              class="btn btn-primary btn-block"
              :disabled="loading">
              🎮 开始游戏
            </button>
            <button 
              v-if="currentGame.status === 'running'" 
              @click="nextRound" 
              class="btn btn-success btn-block"
              :disabled="loading">
              ▶️ 下一轮
            </button>
            <button 
              @click="refreshGame" 
              class="btn btn-secondary btn-block"
              :disabled="loading">
              🔄 刷新状态
            </button>
          </div>
        </div>

        <div class="game-main-panel">
          <div class="players-section">
            <h3>玩家列表</h3>
            <p class="tip" v-if="!currentGame.players || currentGame.players.length === 0">
              游戏开始后将显示玩家信息
            </p>
            <div class="players-grid" v-if="currentGame.players && currentGame.players.length > 0">
              <div v-for="player in currentGame.players" :key="player.id" 
                   class="player-card" 
                   :class="{ 'player-dead': !player.is_alive }">
                <div class="player-avatar">{{ player.is_alive ? '🤖' : '💀' }}</div>
                <div class="player-name">{{ player.name }}</div>
                <div class="player-role">{{ player.role }}</div>
                <div class="player-status">{{ player.is_alive ? '存活' : '已淘汰' }}</div>
              </div>
            </div>
            <div class="players-grid" v-else-if="currentGame.num_players">
              <div v-for="i in currentGame.num_players" :key="i" class="player-card">
                <div class="player-avatar">🤖</div>
                <div class="player-name">玩家 {{ i }}</div>
                <div class="player-status">等待中</div>
              </div>
            </div>
          </div>

          <div class="events-section">
            <h3>游戏事件</h3>
            <div class="events-list">
              <div v-if="currentGame.events && currentGame.events.length > 0">
                <div v-for="(event, index) in currentGame.events" :key="index" class="event-item">
                  {{ event }}
                </div>
              </div>
              <div v-else class="empty-events">
                暂无游戏事件
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="error-state">
        <p>游戏不存在或加载失败</p>
        <button @click="$router.push('/')" class="btn btn-primary">
          返回首页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useGameStore } from '@/stores/gameStore'

const route = useRoute()
const gameStore = useGameStore()

const { currentGame, loading } = storeToRefs(gameStore)
const refreshInterval = ref(null)

function getStatusText(status) {
  const statusMap = {
    'created': '已创建',
    'waiting': '等待中',
    'running': '进行中',
    'finished': '已结束'
  }
  return statusMap[status] || status
}

async function loadGameData() {
  try {
    await gameStore.loadGame(route.params.id)
  } catch (e) {
    console.error('加载游戏失败:', e)
  }
}

async function startGame() {
  try {
    await gameStore.startGame(route.params.id)
    alert('游戏已开始！AI正在思考中...')
    // 等待几秒后自动刷新
    setTimeout(() => {
      loadGameData()
    }, 3000)
  } catch (e) {
    alert('开始游戏失败: ' + (e.message || e))
  }
}

async function nextRound() {
  try {
    const response = await gameStore.gameAction(route.params.id, { type: 'next-round' })
    alert('下一轮开始，AI正在思考中...')
    // 等待几秒后自动刷新
    setTimeout(() => {
      loadGameData()
    }, 5000)
  } catch (e) {
    alert('进行下一轮失败: ' + (e.message || e))
  }
}

async function refreshGame() {
  await loadGameData()
}

// 自动刷新
function startAutoRefresh() {
  refreshInterval.value = setInterval(() => {
    if (currentGame.value && currentGame.value.status === 'running') {
      loadGameData()
    }
  }, 5000) // 每5秒刷新一次
}

onMounted(() => {
  loadGameData()
  startAutoRefresh()
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  gameStore.clearCurrentGame()
})
</script>

<style scoped>
.game-room {
  padding: 2rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.game-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.game-header h1 {
  margin: 0;
}

.btn-back {
  padding: 0.75rem 1.5rem;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-back:hover {
  background: #7f8c8d;
}

.game-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

.game-info-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-card, .action-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.info-card h3, .action-card h3 {
  margin-top: 0;
  color: #667eea;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  color: #666;
  font-weight: bold;
}

.value {
  color: #333;
}

.value.status {
  padding: 0.2rem 0.8rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: bold;
}

.value.status.created {
  background: #3498db;
  color: white;
}

.value.status.running {
  background: #2ecc71;
  color: white;
}

.value.status.waiting {
  background: #f39c12;
  color: white;
}

.btn-block {
  width: 100%;
  margin-bottom: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-secondary:hover:not(:disabled) {
  background: #7f8c8d;
}

.btn-success {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-success:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(46, 204, 113, 0.4);
}

.game-main-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.players-section, .events-section {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.players-section h3, .events-section h3 {
  margin-top: 0;
  color: #667eea;
}

.tip {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.player-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
  transition: transform 0.3s;
}

.player-card:hover {
  transform: translateY(-3px);
}

.player-card.player-dead {
  background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
  opacity: 0.6;
}

.player-avatar {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.player-name {
  font-weight: bold;
  color: #333;
  margin-bottom: 0.3rem;
}

.player-role {
  color: #667eea;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

.player-status {
  color: #666;
  font-size: 0.85rem;
}

.events-list {
  max-height: 400px;
  overflow-y: auto;
}

.event-item {
  padding: 1rem;
  margin-bottom: 0.5rem;
  background: #f8f9fa;
  border-left: 4px solid #667eea;
  border-radius: 4px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.empty-events {
  text-align: center;
  padding: 2rem;
  color: #999;
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

.error-state {
  text-align: center;
  padding: 3rem;
}

.error-state p {
  font-size: 1.2rem;
  color: #e74c3c;
  margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
  .game-content {
    grid-template-columns: 1fr;
  }
  
  .players-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>

