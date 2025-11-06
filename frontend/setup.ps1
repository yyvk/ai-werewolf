# AI狼人杀前端 - 自动安装脚本
# PowerShell脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI狼人杀前端 - 自动安装" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Node.js
Write-Host "[1/4] 检查Node.js..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "Node.js版本: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "错误: 未找到Node.js，请先安装Node.js 16+" -ForegroundColor Red
    Write-Host "下载地址: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# 检查npm
Write-Host "[2/4] 检查npm..." -ForegroundColor Yellow
if (Get-Command npm -ErrorAction SilentlyContinue) {
    $npmVersion = npm --version
    Write-Host "npm版本: $npmVersion" -ForegroundColor Green
} else {
    Write-Host "错误: 未找到npm" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host "[3/4] 安装依赖包..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟，请耐心等待..." -ForegroundColor Cyan
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "依赖安装成功！" -ForegroundColor Green
} else {
    Write-Host "依赖安装失败，请检查错误信息" -ForegroundColor Red
    exit 1
}

# 完成
Write-Host "[4/4] 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🎉 安装成功！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "1. 启动后端服务:" -ForegroundColor White
Write-Host "   cd .." -ForegroundColor Gray
Write-Host "   python main.py --mode web" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 启动前端服务:" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 打开浏览器访问:" -ForegroundColor White
Write-Host "   http://localhost:3000" -ForegroundColor Gray
Write-Host ""












