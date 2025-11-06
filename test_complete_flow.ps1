# AI狼人杀 - 完整流程测试脚本

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AI狼人杀完整流程测试" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 1. 创建游戏
Write-Host "[1/6] 创建新游戏..." -ForegroundColor Yellow
$body = @{
    num_players = 6
    llm_provider = "openai"
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri http://localhost:8000/api/games -Method POST -Body $body -ContentType "application/json"
$gameId = $result.game_id
Write-Host "  游戏ID: $gameId" -ForegroundColor Green

# 2. 查看初始状态
Write-Host "`n[2/6] 查看初始状态..." -ForegroundColor Yellow
$game = Invoke-RestMethod -Uri "http://localhost:8000/api/games/$gameId"
Write-Host "  状态: $($game.status)" -ForegroundColor Cyan
Write-Host "  阶段: $($game.phase)" -ForegroundColor Cyan
Write-Host "  轮次: $($game.round)" -ForegroundColor Cyan

# 3. 开始游戏
Write-Host "`n[3/6] 开始游戏..." -ForegroundColor Yellow
$start = Invoke-RestMethod -Uri "http://localhost:8000/api/games/$gameId/start" -Method POST
Write-Host "  $($start.message)" -ForegroundColor Green

# 4. 等待AI思考（第1轮）
Write-Host "`n[4/6] 等待AI完成第1轮（需要30秒）..." -ForegroundColor Yellow
for ($i=1; $i -le 30; $i++) {
    Write-Progress -Activity "AI思考中" -Status "第1轮" -PercentComplete ($i * 3.33)
    Start-Sleep -Seconds 1
}
Write-Progress -Activity "AI思考中" -Completed

# 5. 查看第1轮结果
Write-Host "`n[5/6] 查看第1轮结果..." -ForegroundColor Yellow
$game = Invoke-RestMethod -Uri "http://localhost:8000/api/games/$gameId"

Write-Host "`n  === 游戏信息 ===" -ForegroundColor Cyan
Write-Host "  状态: $($game.status)"
Write-Host "  阶段: $($game.phase)"
Write-Host "  轮次: $($game.round)"

Write-Host "`n  === 玩家状态 ===" -ForegroundColor Cyan
foreach ($player in $game.players) {
    $status = if ($player.is_alive) { "[存活]" } else { "[淘汰]" }
    $color = if ($player.is_alive) { "Green" } else { "Red" }
    Write-Host "  玩家$($player.id): $($player.name) - $($player.role) $status" -ForegroundColor $color
}

Write-Host "`n  === 游戏事件（最后10条）===" -ForegroundColor Cyan
$events = $game.events
$lastEvents = if ($events.Count -gt 10) { $events[($events.Count - 10)..($events.Count - 1)] } else { $events }
foreach ($event in $lastEvents) {
    Write-Host "  • $event" -ForegroundColor White
}

# 6. Web界面链接
Write-Host "`n[6/6] 在浏览器中查看" -ForegroundColor Yellow
Write-Host "  访问: http://localhost:3000/game/$gameId" -ForegroundColor Cyan
Write-Host "  点击 [刷新状态] 按钮查看最新数据`n" -ForegroundColor Yellow

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  测试完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

# 输出摘要
Write-Host "`n【快速命令】" -ForegroundColor Yellow
Write-Host "查看游戏: http://localhost:3000/game/$gameId"
Write-Host "下一轮: Invoke-RestMethod -Uri 'http://localhost:8000/api/games/$gameId/next-round' -Method POST"
Write-Host ""












