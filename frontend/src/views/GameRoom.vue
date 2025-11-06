<template>
  <div class="game-room" :class="getPhaseClass()">
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="sky-gradient"></div>
      <div class="stars" v-if="isNightPhase()"></div>
      <div class="moon" v-if="isNightPhase()">🌙</div>
      <div class="sun" v-else-if="currentGame">☀️</div>
    </div>

    <div class="container">
      <div class="game-header">
        <button @click="$router.push('/')" class="btn btn-back">
          ← 返回首页
        </button>
        <div class="game-title">
          <h1>AI狼人杀</h1>
          <div v-if="currentGame" class="phase-indicator">
            <span class="phase-badge" :class="getPhaseClass()">
              {{ getPhaseText() }}
            </span>
            <span class="round-badge">第 {{ currentGame.round }} 轮</span>
          </div>
        </div>
      </div>

      <div v-if="loading && !isStreaming && !currentGame" class="loading">
        <div class="spinner"></div>
        <p>加载游戏中...</p>
      </div>

      <div v-if="currentGame" class="game-content">
        <!-- 侧边信息面板 -->
        <div class="game-info-panel">
          <div class="info-card">
            <h3>🎮 游戏信息</h3>
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
              :disabled="loading || isStreaming">
              <span v-if="isStreaming">⏳ 进行中...</span>
              <span v-else>▶️ 下一轮</span>
            </button>
            <button 
              @click="refreshGame" 
              class="btn btn-secondary btn-block"
              :disabled="loading">
              🔄 刷新状态
            </button>
          </div>
        </div>

        <!-- 主游戏区域 -->
        <div class="game-main-panel">
          <!-- 狼人杀游戏桌 -->
          <div class="village-view">
            <div class="game-table-container">
              <!-- 左侧玩家 (1-6号位) -->
              <div class="players-side players-left">
                <div 
                  v-for="slotNum in 6" 
                  :key="'left-' + slotNum"
                  class="player-slot"
                  :class="getSlotClass(slotNum)"
                  @mouseenter="hoveredPlayer = getPlayerBySlotNum(slotNum)"
                  @mouseleave="hoveredPlayer = null">
                  <template v-if="getPlayerBySlotNum(slotNum)">
                    <div class="player-card-simple">
                      <div class="player-avatar-large">
                        {{ getPlayerIcon(getPlayerBySlotNum(slotNum)) }}
                      </div>
                      <div class="player-info">
                        <div class="player-nickname">{{ getPlayerBySlotNum(slotNum).name }}</div>
                      </div>
                      <div class="player-number-badge">{{ slotNum }}</div>
                    </div>
                  </template>
                  <template v-else>
                    <div class="empty-slot-simple">
                      <div class="empty-avatar">❓</div>
                      <div class="empty-number">{{ slotNum }}</div>
                    </div>
                  </template>
                </div>
              </div>
              
              <!-- 中央游戏桌 -->
              <div class="table-center">
                <div class="table-surface">
                  <div class="table-info">
                    <!-- 实时对话显示 -->
                    <div v-if="currentSpeaker" class="current-speaker-display">
                      <div class="speech-bubble">
                        <div class="speaker-header">
                          <span class="speaker-avatar">{{ getPlayerIcon({ role: currentSpeaker.role }) }}</span>
                          <span class="speaker-name">{{ currentSpeaker.name }}</span>
                          <span class="speaker-role">({{ currentSpeaker.role }})</span>
                        </div>
                        <div class="speech-text-live">
                          {{ currentSpeaker.text }}<span class="cursor-blink">|</span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 流式状态提示 -->
                    <div v-else-if="isStreaming && streamingEvents.length > 0" class="streaming-status">
                      <div class="status-icon">⚡</div>
                      <div class="status-text">{{ streamingEvents[streamingEvents.length - 1].text }}</div>
                    </div>
                    
                    <!-- 默认状态 -->
                    <div v-else-if="currentGame.status === 'waiting'" class="waiting-message">
                      ⏳ 等待游戏开始
                    </div>
                    <div v-else-if="!isStreaming" class="idle-message">
                      <div class="round-display">第 {{ currentGame.round }} 轮</div>
                      <div class="phase-display">{{ getPhaseText() }}</div>
                      <div class="action-hint">点击 "下一轮" 继续</div>
                    </div>
                    <div v-else class="processing-message">
                      <div class="spinner-icon">⚙️</div>
                      <div class="process-text">游戏进行中...</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 右侧玩家 (7-12号位) -->
              <div class="players-side players-right">
                <div 
                  v-for="slotNum in 6" 
                  :key="'right-' + (slotNum + 6)"
                  class="player-slot"
                  :class="getSlotClass(slotNum + 6)"
                  @mouseenter="hoveredPlayer = getPlayerBySlotNum(slotNum + 6)"
                  @mouseleave="hoveredPlayer = null">
                  <template v-if="getPlayerBySlotNum(slotNum + 6)">
                    <div class="player-card-simple">
                      <div class="player-avatar-large">
                        {{ getPlayerIcon(getPlayerBySlotNum(slotNum + 6)) }}
                      </div>
                      <div class="player-info">
                        <div class="player-nickname">{{ getPlayerBySlotNum(slotNum + 6).name }}</div>
                      </div>
                      <div class="player-number-badge">{{ slotNum + 6 }}</div>
                    </div>
                  </template>
                  <template v-else>
                    <div class="empty-slot-simple">
                      <div class="empty-avatar">❓</div>
                      <div class="empty-number">{{ slotNum + 6 }}</div>
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </div>

          <!-- 游戏事件日志 -->
          <div class="events-section">
            <h3>📜 游戏日志</h3>
            <div class="events-list" ref="eventsListRef">
              <!-- 流式事件 -->
              <div v-if="streamingEvents.length > 0">
                <div v-for="(event, index) in streamingEvents" :key="'stream-' + index" 
                     class="event-item" 
                     :class="'event-' + event.type">
                  {{ event.text }}
                </div>
              </div>
              
              <!-- 当前正在说话的玩家 -->
              <div v-if="currentSpeaker" class="event-item event-streaming">
                <div class="speaker-header">
                  <span class="speaker-avatar-mini">{{ getPlayerIcon({ role: currentSpeaker.role }) }}</span>
                  <span class="speaker-name">{{ currentSpeaker.name }}</span>
                  <span class="speaker-role">({{ currentSpeaker.role }})</span>
                  <span class="typing-indicator">💬</span>
                </div>
                <div class="speech-text">
                  {{ currentSpeaker.text }}<span class="cursor-blink">|</span>
                </div>
              </div>
              
              <!-- 历史事件 -->
              <div v-if="!isStreaming && currentGame.events && currentGame.events.length > 0">
                <div v-for="(event, index) in currentGame.events" :key="index" class="event-item">
                  {{ event }}
                </div>
              </div>
              
              <div v-if="!isStreaming && streamingEvents.length === 0 && (!currentGame.events || currentGame.events.length === 0)" class="empty-events">
                📝 暂无游戏事件
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useGameStore } from '@/stores/gameStore'

const route = useRoute()
const gameStore = useGameStore()

const { currentGame, loading } = storeToRefs(gameStore)
const refreshInterval = ref(null)
const streamingEvents = ref([])
const currentSpeaker = ref(null)
const isStreaming = ref(false)
const eventsListRef = ref(null)
const hoveredPlayer = ref(null)

function getStatusText(status) {
  const statusMap = {
    'created': '已创建',
    'waiting': '等待中',
    'running': '进行中',
    'finished': '已结束'
  }
  return statusMap[status] || status
}

// 判断是否为夜晚阶段
function isNightPhase() {
  if (!currentGame.value) return false
  const phase = currentGame.value.phase?.toLowerCase() || ''
  return phase.includes('night') || phase.includes('黑夜')
}

// 获取阶段样式类
function getPhaseClass() {
  if (!currentGame.value) return 'phase-day'
  return isNightPhase() ? 'phase-night' : 'phase-day'
}

// 获取阶段文本
function getPhaseText() {
  if (!currentGame.value) return ''
  const phase = currentGame.value.phase
  if (isNightPhase()) return '🌙 黑夜'
  if (phase?.includes('discussion') || phase?.includes('讨论')) return '☀️ 白天 - 讨论'
  if (phase?.includes('voting') || phase?.includes('投票')) return '☀️ 白天 - 投票'
  return `☀️ ${phase}`
}

// 获取所有玩家（包括等待中的）
function getAllPlayers() {
  if (!currentGame.value) return []
  if (currentGame.value.players && currentGame.value.players.length > 0) {
    return currentGame.value.players
  }
  // 游戏未开始时显示占位符
  if (currentGame.value.num_players) {
    return Array.from({ length: currentGame.value.num_players }, (_, i) => ({
      id: i + 1,
      name: `玩家${i + 1}`,
      is_alive: true,
      role: null
    }))
  }
  return []
}

// 计算玩家在圆形布局中的位置
function getPlayerPosition(index, total) {
  const angle = (index * 360 / total) - 90 // 从顶部开始
  const radius = 180 // 圆的半径
  const radian = (angle * Math.PI) / 180
  const x = Math.cos(radian) * radius
  const y = Math.sin(radian) * radius
  
  return {
    left: `calc(50% + ${x}px)`,
    top: `calc(50% + ${y}px)`,
    transform: 'translate(-50%, -50%)'
  }
}

// 根据玩家状态获取图标
function getPlayerIcon(player) {
  if (!player) return '🤖'
  if (player.is_alive === false) return '💀'
  if (!player.role) return '🤖'
  
  return getRoleIcon(player.role)
}

// 根据角色获取图标
function getRoleIcon(role) {
  const roleIcons = {
    '狼人': '🐺',
    '村民': '👨',
    '预言家': '🔮',
    '女巫': '🧙',
    '猎人': '🏹',
    '守卫': '🛡️'
  }
  return roleIcons[role] || '🤖'
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
    // 清空之前的流式事件
    streamingEvents.value = []
    currentSpeaker.value = null
    
    // 手动调用后端API开始游戏（不使用store的方法，避免loading状态影响）
    const response = await fetch(`/api/games/${route.params.id}/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error('启动游戏失败')
    }
    
    const result = await response.json()
    
    if (result.success) {
      // 更新当前游戏的状态（静默加载，不显示loading）
      await gameStore.loadGame(route.params.id, true)
      
      // 等待100ms让后端准备好，然后立即开始流式显示第一轮
      await new Promise(resolve => setTimeout(resolve, 100))
      
      // 立即开始流式显示第一轮
      await nextRound()
    }
  } catch (e) {
    alert('开始游戏失败: ' + (e.message || e))
  }
}

async function nextRound() {
  if (isStreaming.value) {
    alert('当前正在进行中，请稍候...')
    return
  }
  
  try {
    isStreaming.value = true
    streamingEvents.value = []
    currentSpeaker.value = null
    
    console.log('🔌 开始连接EventSource...', route.params.id)
    console.log('📍 URL:', `/api/games/${route.params.id}/stream-round`)
    
    // 使用 EventSource 接收流式数据
    const eventSource = new EventSource(`/api/games/${route.params.id}/stream-round`)
    
    let connectionEstablished = false
    
    eventSource.onopen = () => {
      console.log('✅ EventSource 连接已建立')
      connectionEstablished = true
    }
    
    eventSource.onmessage = (event) => {
      try {
        console.log('📨 收到消息:', event.data)
        const data = JSON.parse(event.data)
        handleStreamEvent(data)
      } catch (e) {
        console.error('❌ 解析事件失败:', e, event.data)
      }
    }
    
    eventSource.onerror = (error) => {
      console.error('❌ EventSource 错误:', error)
      console.log('📊 EventSource readyState:', eventSource.readyState)
      console.log('🔗 连接是否建立:', connectionEstablished)
      console.log('📝 已收到的事件数:', streamingEvents.value.length)
      
      eventSource.close()
      isStreaming.value = false
      currentSpeaker.value = null
      
      // 如果是连接失败，显示错误提示
      if (streamingEvents.value.length === 0 && !connectionEstablished) {
        addStreamingEvent('❌ 连接失败，请检查后端服务是否正常运行', 'error')
        console.error('💡 提示: 请确保后端服务在 http://127.0.0.1:8000 上运行')
      } else {
        console.log('🔄 流式传输中断，重新加载游戏数据')
        loadGameData()
      }
    }
    
    eventSource.addEventListener('complete', (event) => {
      console.log('✅ 流式传输完成', event)
      try {
        const data = JSON.parse(event.data)
        handleStreamEvent(data)
      } catch (e) {
        console.error('解析完成事件失败:', e)
      }
      eventSource.close()
      isStreaming.value = false
      currentSpeaker.value = null
      loadGameData()
    })
    
  } catch (e) {
    console.error('❌ nextRound异常:', e)
    alert('进行下一轮失败: ' + (e.message || e))
    isStreaming.value = false
    currentSpeaker.value = null
  }
}

function handleStreamEvent(data) {
  switch (data.type) {
    case 'round_start':
      if (currentGame.value) {
        currentGame.value.round = data.round
      }
      addStreamingEvent(`🎮 第 ${data.round} 轮开始`, 'system')
      break
      
    case 'phase_change':
      if (currentGame.value) {
        currentGame.value.phase = data.phase
      }
      const phaseText = data.phase === 'discussion' ? '讨论阶段' : '投票阶段'
      addStreamingEvent(`📢 ${phaseText}`, 'system')
      break
      
    case 'speech_start':
      currentSpeaker.value = {
        id: data.player_id,
        name: data.player_name,
        role: data.role,
        text: ''
      }
      break
      
    case 'speech_chunk':
      if (currentSpeaker.value && currentSpeaker.value.id === data.player_id) {
        currentSpeaker.value.text += data.chunk
      }
      break
      
    case 'speech_end':
      if (currentSpeaker.value) {
        addStreamingEvent(`[${currentSpeaker.value.name}] ${data.speech}`, 'speech')
        if (!currentGame.value.events) {
          currentGame.value.events = []
        }
        currentGame.value.events.push(`[${currentSpeaker.value.name}] ${data.speech}`)
      }
      currentSpeaker.value = null
      break
      
    case 'vote':
      addStreamingEvent(`[${data.player_name}] 投票给 玩家${data.vote_to}`, 'vote')
      if (!currentGame.value.events) {
        currentGame.value.events = []
      }
      currentGame.value.events.push(`[${data.player_name}] 投票给 玩家${data.vote_to}`)
      break
      
    case 'elimination':
      addStreamingEvent(`💀 玩家${data.player_id}(${data.player_name}-${data.role}) 被投票淘汰`, 'elimination')
      if (!currentGame.value.events) {
        currentGame.value.events = []
      }
      currentGame.value.events.push(`玩家${data.player_id}(${data.player_name}-${data.role}) 被投票淘汰`)
      break
      
    case 'game_end':
      addStreamingEvent(`🎉 游戏结束！${data.winner}胜利！`, 'game-end')
      if (currentGame.value) {
        currentGame.value.status = 'finished'
      }
      break
      
    case 'complete':
      // 更新完整的游戏数据
      if (data.game_data && currentGame.value) {
        Object.assign(currentGame.value, data.game_data)
      }
      isStreaming.value = false
      break
      
    case 'error':
      console.error('流式事件错误:', data.message)
      addStreamingEvent(`❌ 错误: ${data.message}`, 'error')
      isStreaming.value = false
      break
  }
  
  // 自动滚动到底部
  nextTick(() => {
    if (eventsListRef.value) {
      eventsListRef.value.scrollTop = eventsListRef.value.scrollHeight
    }
  })
}

function addStreamingEvent(text, type) {
  streamingEvents.value.push({
    text,
    type,
    timestamp: Date.now()
  })
}

function getPlayerBySlot(slotNumber) {
  if (!currentGame.value || !currentGame.value.players) {
    return null
  }
  return currentGame.value.players.find(p => p.id === slotNumber)
}

function getPlayerSlotClass(slotNumber) {
  const player = getPlayerBySlot(slotNumber)
  if (!player) return 'slot-empty'
  return player.is_alive ? 'slot-alive' : 'slot-dead'
}

function getPlayerAvatar(player) {
  if (!player) return '👤'
  if (!player.is_alive) return '💀'
  
  // 根据角色返回不同的头像
  const roleAvatars = {
    '狼人': '🐺',
    '村民': '👨',
    '预言家': '🔮',
    '女巫': '🧙',
    '猎人': '🏹'
  }
  
  return roleAvatars[player.role] || '🤖'
}

function getPlayerBySlotNum(slotNum) {
  if (!currentGame.value || !currentGame.value.players) {
    return null
  }
  return currentGame.value.players.find(p => p.id === slotNum)
}

function getSlotClass(slotNum) {
  const player = getPlayerBySlotNum(slotNum)
  if (!player) return 'slot-empty'
  if (player.is_alive === false) return 'slot-dead'
  if (currentSpeaker.value && currentSpeaker.value.id === slotNum) return 'slot-speaking'
  return 'slot-alive'
}

async function refreshGame() {
  await loadGameData()
}

// 自动刷新 - 已禁用，使用流式更新代替
function startAutoRefresh() {
  // 不再使用轮询刷新，改用流式更新
  // 只在游戏未开始或已结束时才自动刷新
  refreshInterval.value = setInterval(() => {
    if (currentGame.value && 
        (currentGame.value.status === 'created' || currentGame.value.status === 'finished') &&
        !isStreaming.value) {
      loadGameData()
    }
  }, 10000) // 减少到每10秒刷新一次，且仅在非进行状态
}

onMounted(() => {
  loadGameData()
  // 注释掉自动刷新，避免闪烁
  // startAutoRefresh()
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
  min-height: 100vh;
  position: relative;
  padding: 2rem 0;
  transition: background 0.8s ease-in-out;
}

/* 白天背景 */
.game-room.phase-day {
  background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 50%, #90EE90 100%);
}

/* 黑夜背景 */
.game-room.phase-night {
  background: linear-gradient(to bottom, #0B1026 0%, #1a1a3e 50%, #2d2d5f 100%);
}

.game-room.phase-night .container {
  color: #e0e0e0;
}

.game-room.phase-night h1,
.game-room.phase-night h3 {
  color: #fff;
}

/* 背景装饰 */
.background-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.sky-gradient {
  position: absolute;
  width: 100%;
  height: 100%;
}

/* 星星效果 */
.stars {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20% 30%, white, transparent),
    radial-gradient(2px 2px at 60% 70%, white, transparent),
    radial-gradient(1px 1px at 50% 50%, white, transparent),
    radial-gradient(1px 1px at 80% 10%, white, transparent),
    radial-gradient(2px 2px at 90% 60%, white, transparent),
    radial-gradient(1px 1px at 33% 80%, white, transparent);
  background-size: 200% 200%;
  animation: twinkle 4s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

/* 月亮 */
.moon {
  position: absolute;
  top: 10%;
  right: 10%;
  font-size: 5rem;
  animation: moonGlow 3s ease-in-out infinite;
}

@keyframes moonGlow {
  0%, 100% { 
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
    transform: translateY(0);
  }
  50% { 
    text-shadow: 0 0 40px rgba(255, 255, 255, 0.8);
    transform: translateY(-10px);
  }
}

/* 太阳 */
.sun {
  position: absolute;
  top: 10%;
  right: 10%;
  font-size: 5rem;
  animation: sunShine 4s ease-in-out infinite;
}

@keyframes sunShine {
  0%, 100% { 
    text-shadow: 0 0 30px rgba(255, 223, 0, 0.8);
    transform: rotate(0deg);
  }
  50% { 
    text-shadow: 0 0 50px rgba(255, 223, 0, 1);
    transform: rotate(180deg);
  }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

.game-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.game-title {
  flex: 1;
  text-align: center;
}

.game-title h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.phase-indicator {
  display: flex;
  justify-content: center;
  gap: 1rem;
  align-items: center;
}

.phase-badge, .round-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.phase-badge.phase-day {
  background: linear-gradient(135deg, #FDB813 0%, #FF8C00 100%);
  color: white;
}

.phase-badge.phase-night {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: #fff;
}

.round-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-back {
  padding: 0.75rem 1.5rem;
  background: rgba(149, 165, 166, 0.9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
}

.btn-back:hover {
  background: rgba(127, 140, 141, 0.9);
  transform: translateY(-2px);
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
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  backdrop-filter: blur(10px);
}

.phase-night .info-card,
.phase-night .action-card {
  background: rgba(44, 62, 80, 0.9);
  color: #e0e0e0;
}

.info-card h3, .action-card h3 {
  margin-top: 0;
  color: #667eea;
}

.phase-night .info-card h3,
.phase-night .action-card h3 {
  color: #a0b8ff;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(238, 238, 238, 0.3);
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  color: #666;
  font-weight: bold;
}

.phase-night .label {
  color: #b0b0b0;
}

.value {
  color: #333;
}

.phase-night .value {
  color: #e0e0e0;
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

/* 村庄视图 - 两侧对坐布局 */
.village-view {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  position: relative;
  backdrop-filter: blur(10px);
}

.phase-night .village-view {
  background: rgba(44, 62, 80, 0.9);
}

.game-table-container {
  display: flex;
  gap: 2rem;
  align-items: center;
  justify-content: center;
  min-height: 600px;
}

/* 左右两侧玩家区域 */
.players-side {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  flex: 0 0 160px;
}

.players-left {
  align-items: flex-end;
}

.players-right {
  align-items: flex-start;
}

/* 玩家槽位 */
.player-slot {
  position: relative;
  width: 140px;
  min-height: 140px;
  transition: all 0.3s ease;
}

.player-slot:hover {
  transform: translateX(0) scale(1.02);
}

.players-left .player-slot:hover {
  transform: translateX(-5px) scale(1.02);
}

.players-right .player-slot:hover {
  transform: translateX(5px) scale(1.02);
}

/* 简化的玩家卡片 */
.player-card-simple {
  background: rgba(255, 255, 255, 0.95);
  border: 3px solid transparent;
  border-radius: 15px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.slot-alive .player-card-simple {
  border-color: #4caf50;
  animation: aliveGlow 3s ease-in-out infinite;
}

.slot-dead .player-card-simple {
  border-color: #9e9e9e;
  opacity: 0.5;
  filter: grayscale(0.5);
}

.slot-speaking .player-card-simple {
  border-color: #667eea;
  animation: speaking 1s ease-in-out infinite;
  box-shadow: 0 0 30px rgba(102, 126, 234, 0.8);
  transform: scale(1.05);
}

.phase-night .player-card-simple {
  background: rgba(44, 62, 80, 0.9);
}

.player-avatar-large {
  font-size: 3.5rem;
  line-height: 1;
  transition: all 0.3s ease;
}

.slot-speaking .player-avatar-large {
  animation: iconBounce 0.6s ease-in-out infinite;
}

@keyframes iconBounce {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-8px) scale(1.1);
  }
}

.player-info {
  text-align: center;
  width: 100%;
}

.player-nickname {
  font-weight: bold;
  color: #333;
  font-size: 1rem;
  line-height: 1.3;
  word-break: break-word;
  max-width: 100%;
}

.phase-night .player-nickname {
  color: #e0e0e0;
}

.player-number-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: bold;
  box-shadow: 0 3px 10px rgba(0,0,0,0.3);
  border: 2px solid white;
}

.slot-dead .player-number-badge {
  background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
}

/* 简化的空槽位 */
.empty-slot-simple {
  background: rgba(250, 250, 250, 0.5);
  border: 3px dashed #bdbdbd;
  border-radius: 15px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  opacity: 0.3;
  transition: all 0.3s ease;
  position: relative;
}

.empty-slot-simple:hover {
  opacity: 0.5;
  border-color: #9e9e9e;
}

.phase-night .empty-slot-simple {
  background: rgba(44, 62, 80, 0.3);
  border-color: #546e7a;
}

.empty-avatar {
  font-size: 3rem;
  opacity: 0.5;
  filter: grayscale(1);
}

.empty-number {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 32px;
  height: 32px;
  background: #bdbdbd;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: bold;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

@keyframes aliveGlow {
  0%, 100% {
    box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
  }
  50% {
    box-shadow: 0 3px 20px rgba(76, 175, 80, 0.6);
  }
}

@keyframes speaking {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 15px rgba(102, 126, 234, 0.5);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(102, 126, 234, 0.9);
  }
}

/* 中央游戏桌 */
.table-center {
  flex: 0 0 350px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.table-surface {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
  position: relative;
  /* 移除旋转动画以减少性能消耗和闪烁 */
}

.table-surface::before {
  content: '';
  position: absolute;
  inset: 15px;
  border-radius: 50%;
  border: 3px dashed rgba(255, 255, 255, 0.3);
  /* 移除旋转动画 */
}

/* 保留关键帧定义，以防其他地方使用 */
@keyframes tableRotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes borderRotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.phase-night .table-surface {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  box-shadow: 0 10px 40px rgba(52, 73, 94, 0.6);
}

.table-info {
  text-align: center;
  color: white;
  z-index: 1;
  animation: none;
}

.current-speaker-display {
  animation: none;
  max-width: 90%;
  margin: 0 auto;
}

.speech-bubble {
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.speaker-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.speaker-avatar {
  font-size: 2rem;
}

.speaker-name {
  font-size: 1.1rem;
  font-weight: bold;
  color: #667eea;
}

.speaker-role {
  font-size: 0.9rem;
  color: #666;
}

.speech-text-live {
  font-size: 1rem;
  line-height: 1.6;
  text-align: left;
  min-height: 2rem;
  word-wrap: break-word;
}

.cursor-blink {
  animation: blink 1s step-end infinite;
  font-weight: bold;
  color: #667eea;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.streaming-status {
  animation: pulse 1.5s ease-in-out infinite;
}

.status-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.status-text {
  font-size: 1rem;
  opacity: 0.9;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.typing-indicator {
  font-size: 0.85rem;
  opacity: 0.9;
  animation: fadeInOut 1.5s ease-in-out infinite;
}

.waiting-message,
.idle-message,
.processing-message {
  animation: none;
}

.round-display {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.phase-display {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  opacity: 0.9;
}

.action-hint {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-top: 0.3rem;
}

.spinner-icon {
  font-size: 2rem;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.process-text {
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

/* 玩家信息提示卡 */
.player-tooltip {
  position: absolute;
  top: -80px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  animation: tooltipFadeIn 0.3s ease;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.tooltip-content {
  background: rgba(44, 62, 80, 0.98);
  color: white;
  padding: 0.8rem 1.2rem;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.3);
  white-space: nowrap;
  backdrop-filter: blur(10px);
}

.tooltip-name {
  font-weight: bold;
  font-size: 1rem;
  margin-bottom: 0.3rem;
}

.tooltip-role {
  color: #a0b8ff;
  font-size: 0.9rem;
  margin-bottom: 0.2rem;
}

.tooltip-status {
  font-size: 0.85rem;
  color: #e74c3c;
}

.tooltip-status.status-alive {
  color: #2ecc71;
}

/* 中央舞台 */
.center-stage {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 5;
}

.current-speaker-display {
  background: rgba(102, 126, 234, 0.95);
  padding: 1.5rem 2rem;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: fadeIn 0.5s ease;
}

.speaker-avatar {
  font-size: 3rem;
  animation: bounce 1s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.speaker-info-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.speaker-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
}

.typing-indicator {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  animation: fadeInOut 1.5s ease-in-out infinite;
}

.waiting-message,
.idle-message {
  font-size: 1.2rem;
  color: #95a5a6;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.phase-night .waiting-message,
.phase-night .idle-message {
  background: rgba(44, 62, 80, 0.8);
  color: #b0b0b0;
}

/* 游戏事件日志 */
.events-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  backdrop-filter: blur(10px);
}

.phase-night .events-section {
  background: rgba(44, 62, 80, 0.9);
}

.events-section h3 {
  margin-top: 0;
  color: #667eea;
}

.phase-night .events-section h3 {
  color: #a0b8ff;
}

.events-list {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.events-list::-webkit-scrollbar {
  width: 6px;
}

.events-list::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.05);
  border-radius: 3px;
}

.events-list::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.5);
  border-radius: 3px;
}

.events-list::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.7);
}

.event-item {
  padding: 1rem;
  margin-bottom: 0.5rem;
  background: rgba(248, 249, 250, 0.8);
  border-left: 4px solid #667eea;
  border-radius: 8px;
  animation: slideIn 0.3s ease-out;
}

.phase-night .event-item {
  background: rgba(52, 73, 94, 0.6);
  color: #e0e0e0;
}

.event-item.event-system {
  background: rgba(227, 242, 253, 0.9);
  border-left-color: #2196f3;
  font-weight: bold;
}

.phase-night .event-item.event-system {
  background: rgba(33, 150, 243, 0.2);
}

.event-item.event-speech {
  background: rgba(243, 229, 245, 0.9);
  border-left-color: #9c27b0;
}

.phase-night .event-item.event-speech {
  background: rgba(156, 39, 176, 0.2);
}

.event-item.event-vote {
  background: rgba(255, 243, 224, 0.9);
  border-left-color: #ff9800;
}

.phase-night .event-item.event-vote {
  background: rgba(255, 152, 0, 0.2);
}

.event-item.event-elimination {
  background: rgba(255, 235, 238, 0.9);
  border-left-color: #f44336;
  font-weight: bold;
}

.phase-night .event-item.event-elimination {
  background: rgba(244, 67, 54, 0.2);
}

.event-item.event-game-end {
  background: rgba(232, 245, 233, 0.9);
  border-left-color: #4caf50;
  font-weight: bold;
  font-size: 1.1rem;
}

.phase-night .event-item.event-game-end {
  background: rgba(76, 175, 80, 0.2);
}

.event-item.event-error {
  background: rgba(255, 235, 238, 0.9);
  border-left-color: #f44336;
  color: #c62828;
}

.event-item.event-streaming {
  background: linear-gradient(90deg, rgba(248, 249, 250, 0.9) 0%, rgba(232, 234, 246, 0.9) 100%);
  border-left-color: #667eea;
  animation: pulse 2s ease-in-out infinite;
}

.phase-night .event-item.event-streaming {
  background: linear-gradient(90deg, rgba(52, 73, 94, 0.6) 0%, rgba(102, 126, 234, 0.3) 100%);
}

.speaker-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.speaker-avatar-mini {
  font-size: 1.5rem;
}

.speaker-name {
  font-weight: bold;
  color: #667eea;
}

.phase-night .speaker-name {
  color: #a0b8ff;
}

.speaker-role {
  color: #999;
  font-size: 0.9rem;
}

.phase-night .speaker-role {
  color: #b0b0b0;
}

.speech-text {
  color: #333;
  line-height: 1.6;
  font-size: 0.95rem;
  padding-left: 2rem;
}

.phase-night .speech-text {
  color: #e0e0e0;
}

.cursor-blink {
  animation: blink 1s step-end infinite;
  color: #667eea;
  font-weight: bold;
}

.phase-night .cursor-blink {
  color: #a0b8ff;
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

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(102, 126, 234, 0);
  }
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}

@keyframes fadeInOut {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.empty-events {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.phase-night .empty-events {
  color: #b0b0b0;
}

.loading {
  text-align: center;
  padding: 3rem;
}

.spinner {
  border: 4px solid rgba(243, 243, 243, 0.3);
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
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.phase-night .error-state {
  background: rgba(44, 62, 80, 0.9);
}

.error-state p {
  font-size: 1.2rem;
  color: #e74c3c;
  margin-bottom: 1.5rem;
}

.phase-night .error-state p {
  color: #ff6b6b;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .game-table-container {
    gap: 1rem;
  }
  
  .players-side {
    flex: 0 0 140px;
  }
  
  .player-slot {
    width: 130px;
    min-height: 130px;
  }
  
  .player-avatar-large {
    font-size: 3rem;
  }
  
  .table-center {
    flex: 0 0 280px;
  }
  
  .table-surface {
    width: 250px;
    height: 250px;
  }
}

@media (max-width: 1200px) {
  .game-table-container {
    flex-direction: column;
    min-height: auto;
    gap: 1.5rem;
  }
  
  .players-side {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    max-width: 100%;
    gap: 0.75rem;
  }
  
  .players-left,
  .players-right {
    align-items: center;
  }
  
  .player-slot {
    width: 160px;
  }
  
  .table-center {
    order: 0;
  }
}

@media (max-width: 992px) {
  .game-content {
    grid-template-columns: 1fr;
  }
  
  .game-info-panel {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .game-header {
    flex-direction: column;
  }
  
  .game-title h1 {
    font-size: 2rem;
  }
  
  .game-info-panel {
    grid-template-columns: 1fr;
  }
  
  .player-slot {
    width: 110px;
    min-height: 110px;
  }
  
  .player-avatar-large {
    font-size: 2.5rem;
  }
  
  .player-nickname {
    font-size: 0.85rem;
  }
  
  .table-surface {
    width: 200px;
    height: 200px;
  }
  
  .player-number {
    width: 24px;
    height: 24px;
    font-size: 0.75rem;
  }
  
  .current-speaker-display {
    padding: 1rem 1.5rem;
  }
  
  .speaker-avatar {
    font-size: 2rem;
  }
  
  .speaker-name {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 10px;
  }
  
  .game-title h1 {
    font-size: 1.5rem;
  }
  
  .phase-badge, .round-badge {
    padding: 0.3rem 0.8rem;
    font-size: 0.85rem;
  }
  
  .players-circle {
    height: 300px;
  }
  
  .player-avatar-circle {
    width: 50px;
    height: 50px;
  }
  
  .player-icon {
    font-size: 1.5rem;
  }
  
  .player-nameplate {
    font-size: 0.75rem;
  }
  
  .village-view {
    padding: 1rem;
  }
  
  .events-section {
    padding: 1rem;
  }
}
</style>

