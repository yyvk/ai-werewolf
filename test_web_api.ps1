# AI狼人杀 Web API 测试脚本
# PowerShell脚本

$baseUrl = "http://127.0.0.1:8000"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  AI狼人杀 Web API 测试" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查服务健康状态
Write-Host "[1] 检查服务健康状态..." -ForegroundColor Yellow
$health = Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
Write-Host "状态: $($health.status)" -ForegroundColor Green
Write-Host ""

# 2. 获取统计信息
Write-Host "[2] 获取统计信息..." -ForegroundColor Yellow
$stats = Invoke-RestMethod -Uri "$baseUrl/api/stats" -Method GET
Write-Host "总游戏数: $($stats.total_games)" -ForegroundColor Green
Write-Host "活跃游戏: $($stats.active_games)" -ForegroundColor Green
Write-Host ""

# 3. 创建新游戏
Write-Host "[3] 创建新游戏..." -ForegroundColor Yellow
$createBody = @{
    num_players = 6
    llm_provider = "openai"
    model_name = "Qwen/Qwen2.5-32B-Instruct"
} | ConvertTo-Json

$newGame = Invoke-RestMethod -Uri "$baseUrl/api/games" -Method POST -Body $createBody -ContentType "application/json"
$gameId = $newGame.game_id
Write-Host "游戏ID: $gameId" -ForegroundColor Green
Write-Host ""

# 4. 获取游戏详情
Write-Host "[4] 获取游戏详情..." -ForegroundColor Yellow
$game = Invoke-RestMethod -Uri "$baseUrl/api/games/$gameId" -Method GET
Write-Host "游戏状态: $($game.status)" -ForegroundColor Green
Write-Host "游戏阶段: $($game.phase)" -ForegroundColor Green
Write-Host "玩家数量: $($game.num_players)" -ForegroundColor Green
Write-Host ""

# 5. 开始游戏
Write-Host "[5] 开始游戏..." -ForegroundColor Yellow
$start = Invoke-RestMethod -Uri "$baseUrl/api/games/$gameId/start" -Method POST
Write-Host "结果: $($start.message)" -ForegroundColor Green
Write-Host ""

# 6. 获取游戏列表
Write-Host "[6] 获取游戏列表..." -ForegroundColor Yellow
$games = Invoke-RestMethod -Uri "$baseUrl/api/games" -Method GET
Write-Host "总共 $($games.total) 个游戏" -ForegroundColor Green
Write-Host ""

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  测试完成！" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "访问 API 文档: $baseUrl/docs" -ForegroundColor Yellow
Write-Host ""





