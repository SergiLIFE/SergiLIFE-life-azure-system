# Simple Repository Cleanup
Write-Host "Starting repository cleanup..." -ForegroundColor Green

# Create directories
New-Item -ItemType Directory -Path "documentation/markdown" -Force | Out-Null
New-Item -ItemType Directory -Path "automation/batch-scripts" -Force | Out-Null  
New-Item -ItemType Directory -Path "automation/powershell-scripts" -Force | Out-Null
New-Item -ItemType Directory -Path "platforms/html-platforms" -Force | Out-Null
New-Item -ItemType Directory -Path "algorithms/python-core" -Force | Out-Null

# Move files
Write-Host "Moving markdown files..." -ForegroundColor Yellow
Get-ChildItem -File "*.md" | Move-Item -Destination "documentation/markdown/" -Force

Write-Host "Moving Python files..." -ForegroundColor Yellow  
Get-ChildItem -File "*.py" | Move-Item -Destination "algorithms/python-core/" -Force

Write-Host "Moving batch files..." -ForegroundColor Yellow
Get-ChildItem -File "*.bat" | Move-Item -Destination "automation/batch-scripts/" -Force

Write-Host "Moving PowerShell files..." -ForegroundColor Yellow
Get-ChildItem -File "*.ps1" | Where-Object { $_.Name -ne "CLEANUP_SIMPLE.ps1" } | Move-Item -Destination "automation/powershell-scripts/" -Force

Write-Host "Moving HTML files..." -ForegroundColor Yellow
Get-ChildItem -File "*.html" | Move-Item -Destination "platforms/html-platforms/" -Force

$rootFiles = (Get-ChildItem -File).Count
Write-Host "Repository cleanup complete! Root files: $rootFiles" -ForegroundColor Green