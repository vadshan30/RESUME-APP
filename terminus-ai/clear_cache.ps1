# Clear Python Cache
# Run this if you make changes to .py files and they don't seem to take effect

Write-Host "🧹 Clearing Python bytecode cache..." -ForegroundColor Cyan

# Remove all __pycache__ directories recursively
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Remove .pyc files
Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" | Remove-Item -Force

Write-Host "✅ Cache cleared successfully!" -ForegroundColor Green
Write-Host "You can now run your commands with the latest code changes." -ForegroundColor Yellow
