# AI狼人杀 - 完整启动脚本
# 同时启动后端和前端

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI狼人杀 - 完整启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 启动后端
Write-Host "[1/2] 启动后端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd ..; python main.py --mode web"
Write-Host "后端服务启动中..." -ForegroundColor Green
Start-Sleep -Seconds 3

# 启动前端
Write-Host "[2/2] 启动前端服务..." -ForegroundColor Yellow
Write-Host "前端服务将在此窗口运行..." -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🎮 服务启动完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "访问地址:" -ForegroundColor Yellow
Write-Host "- 前端: http://localhost:3000" -ForegroundColor Cyan
Write-Host "- 后端: http://localhost:8000" -ForegroundColor Cyan
Write-Host "- API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Gray
Write-Host ""

npm run dev












