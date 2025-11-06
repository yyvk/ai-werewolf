<template>
  <div id="app">
    <header class="app-header">
      <div class="container">
        <h1 class="logo">🐺 AI狼人杀</h1>
        <nav>
          <router-link to="/" class="nav-link">首页</router-link>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <router-view />
    </main>

    <footer class="app-footer">
      <p>© 2025 AI狼人杀 - Powered by ModelScope & Vue 3</p>
    </footer>
  </div>
</template>

<script setup>
// App组件不需要额外逻辑
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  margin: 0;
  font-size: 1.8rem;
  font-weight: bold;
}

nav {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background 0.3s;
}

.nav-link:hover {
  background: rgba(255,255,255,0.2);
}

.app-main {
  min-height: calc(100vh - 140px);
  padding: 2rem 0;
}

.app-footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 1.5rem 0;
  margin-top: 2rem;
}

.app-footer p {
  margin: 0;
}
</style>





