# L.I.F.E Repository Cleanup Script
# Organizes 1,363 files into logical directory structure
# This will fix the GitHub "truncated to 1,000 files" issue

Write-Host "🧹 L.I.F.E Repository Cleanup - Organizing 1,363 files" -ForegroundColor Cyan
Write-Host "Current root files: $((Get-ChildItem -File).Count)" -ForegroundColor Yellow

# Create organized directory structure
$directories = @(
    "documentation/markdown",
    "documentation/guides", 
    "documentation/reports",
    "automation/batch-scripts",
    "automation/powershell-scripts",
    "automation/shell-scripts",
    "platforms/html-platforms",
    "platforms/components",
    "algorithms/python-core",
    "algorithms/experimental",
    "configs/json-configs",
    "configs/environment",
    "cleanup/temp-files",
    "backup/archive"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created: $dir" -ForegroundColor Green
    }
}

Write-Host "`n📁 Moving files to organized structure..." -ForegroundColor Cyan

# Move Markdown documentation files
Get-ChildItem -File "*.md" | ForEach-Object {
    $destination = switch -Wildcard ($_.Name) {
        "*GUIDE*" { "documentation/guides" }
        "*REPORT*" { "documentation/reports" }
        "*README*" { "documentation" }
        "*ANALYSIS*" { "documentation/reports" }
        "*STRATEGY*" { "documentation/guides" }
        "*FRAMEWORK*" { "documentation/guides" }
        default { "documentation/markdown" }
    }
    Move-Item $_.FullName "$destination/" -Force
}
Write-Host "✅ Moved $(Get-ChildItem documentation -Recurse -File "*.md").Count markdown files" -ForegroundColor Green

# Move Python algorithm files
Get-ChildItem -File "*.py" | ForEach-Object {
    $destination = switch -Wildcard ($_.Name) {
        "*experiment*" { "algorithms/experimental" }
        "*test*" { "algorithms/experimental" }
        "*core*" { "algorithms/python-core" }
        "*life*" { "algorithms/python-core" }
        "*algorithm*" { "algorithms/python-core" }
        default { "algorithms/python-core" }
    }
    Move-Item $_.FullName "$destination/" -Force
}
Write-Host "✅ Moved $(Get-ChildItem algorithms -Recurse -File "*.py").Count Python files" -ForegroundColor Green

# Move Batch automation scripts
Get-ChildItem -File "*.bat" | ForEach-Object {
    Move-Item $_.FullName "automation/batch-scripts/" -Force
}
Write-Host "✅ Moved $(Get-ChildItem automation/batch-scripts -File "*.bat").Count batch files" -ForegroundColor Green

# Move PowerShell scripts
Get-ChildItem -File "*.ps1" | ForEach-Object {
    Move-Item $_.FullName "automation/powershell-scripts/" -Force
}
Write-Host "✅ Moved $(Get-ChildItem automation/powershell-scripts -File "*.ps1").Count PowerShell files" -ForegroundColor Green

# Move Shell scripts
Get-ChildItem -File "*.sh" | ForEach-Object {
    Move-Item $_.FullName "automation/shell-scripts/" -Force
}
Write-Host "✅ Moved $(Get-ChildItem automation/shell-scripts -File "*.sh").Count shell scripts" -ForegroundColor Green

# Move HTML platform files
Get-ChildItem -File "*.html" | ForEach-Object {
    $destination = switch -Wildcard ($_.Name) {
        "*PLATFORM*" { "platforms/html-platforms" }
        "*LIFE*" { "platforms/html-platforms" }
        default { "platforms/components" }
    }
    Move-Item $_.FullName "$destination/" -Force
}
Write-Host "✅ Moved $(Get-ChildItem platforms -Recurse -File "*.html").Count HTML files" -ForegroundColor Green

# Move JSON configuration files
Get-ChildItem -File "*.json" | ForEach-Object {
    Move-Item $_.FullName "configs/json-configs/" -Force
}
Write-Host "✅ Moved $(Get-ChildItem configs/json-configs -File "*.json").Count JSON files" -ForegroundColor Green

# Move text files to cleanup
Get-ChildItem -File "*.txt" | ForEach-Object {
    Move-Item $_.FullName "cleanup/temp-files/" -Force
}
Write-Host "✅ Moved $(Get-ChildItem cleanup/temp-files -File "*.txt").Count text files" -ForegroundColor Green

# Move JavaScript files
Get-ChildItem -File "*.js" | ForEach-Object {
    Move-Item $_.FullName "platforms/components/" -Force
}

# Move CSS files
Get-ChildItem -File "*.css" | ForEach-Object {
    Move-Item $_.FullName "platforms/components/" -Force
}

# Move remaining miscellaneous files
Get-ChildItem -File | Where-Object { $_.Extension -notin @('.gitignore', '.yml', '.yaml') } | ForEach-Object {
    Move-Item $_.FullName "backup/archive/" -Force
}

Write-Host "`n🎉 Repository Cleanup Complete!" -ForegroundColor Green
Write-Host "Root files now: $((Get-ChildItem -File).Count)" -ForegroundColor Yellow
Write-Host "Root directories: $((Get-ChildItem -Directory).Count)" -ForegroundColor Yellow

Write-Host "`n📊 New Structure:" -ForegroundColor Cyan
Get-ChildItem -Directory | ForEach-Object {
    $fileCount = (Get-ChildItem $_.FullName -Recurse -File).Count
    if ($fileCount -gt 0) {
        Write-Host "  📁 $($_.Name): $fileCount files" -ForegroundColor White
    }
}

Write-Host "`n✅ GitHub will now display all files properly (no truncation)!" -ForegroundColor Green
Write-Host "🚀 Ready to commit organized repository structure" -ForegroundColor Cyan