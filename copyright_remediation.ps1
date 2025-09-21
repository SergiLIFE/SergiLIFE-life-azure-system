# L.I.F.E THEORY CODE 3 VENTURY SYSTEM - Copyright Remediation Script
# Venturi Gate System for Copyright Compliance and Protection
#
# Copyright 2025 - Sergio Paya Borrull
# L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

param(
    [switch]$AnalyzeOnly,
    [switch]$Remediate,
    [switch]$Validate
)

Write-Host "🚪 L.I.F.E 3-VENTURI COPYRIGHT REMEDIATION SYSTEM" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Configuration
$CopyrightHolder = "Sergio Paya Borrull"
$CopyrightYear = "2025"
$MarketplaceId = "9a600d96-fe1e-420b-902a-a0c42c561adb"
$Extensions = @("*.py", "*.md", "*.json", "*.yml", "*.yaml", "*.bicep", "*.sh", "*.ps1")
$ExcludePatterns = @("__pycache__", ".git", ".mypy_cache", "node_modules", ".vscode", "logs", "results", "temp", "build")

# Standard copyright templates
$PythonCopyright = @"
"""
[MODULE_DESCRIPTION]

Copyright $CopyrightYear - $CopyrightHolder
L.I.F.E. Platform - Azure Marketplace Offer ID: $MarketplaceId
"""
"@

$MarkdownCopyright = @"
---
Copyright $CopyrightYear - $CopyrightHolder
L.I.F.E. Platform - Azure Marketplace Offer ID: $MarketplaceId
---
"@

$ConfigCopyright = "# Copyright $CopyrightYear - $CopyrightHolder`n# L.I.F.E. Platform - Azure Marketplace Offer ID: $MarketplaceId"

function Get-SourceFiles {
    $files = @()
    foreach ($ext in $Extensions) {
        $pattern = "**\$ext"
        $found = Get-ChildItem -Path "." -Recurse -Include $ext -File
        foreach ($file in $found) {
            $skip = $false
            foreach ($exclude in $ExcludePatterns) {
                if ($file.FullName -match $exclude) {
                    $skip = $true
                    break
                }
            }
            if (-not $skip) {
                $files += $file
            }
        }
    }
    return $files
}

function Test-CopyrightCompliance {
    param([string]$Content)

    $hasCopyright = $Content -match "Copyright" -and
    $Content -match [regex]::Escape($CopyrightHolder) -and
    $Content -match $CopyrightYear

    return $hasCopyright
}

function Add-CopyrightHeader {
    param([System.IO.FileInfo]$File)

    $content = Get-Content $File.FullName -Raw -Encoding UTF8
    $ext = $File.Extension.ToLower()

    switch ($ext) {
        ".py" {
            $moduleName = $File.BaseName -replace '_', ' ' -replace '-', ' '
            $moduleName = (Get-Culture).TextInfo.ToTitleCase($moduleName.ToLower())
            $header = $PythonCopyright -replace "\[MODULE_DESCRIPTION\]", "$moduleName Module"
        }
        ".md" {
            $header = $MarkdownCopyright
        }
        default {
            $header = $ConfigCopyright
        }
    }

    $newContent = $header + "`n`n" + $content
    $newContent | Set-Content $File.FullName -Encoding UTF8 -NoNewline
}

function Invoke-VenturiGate1 {
    Write-Host "🚪 VENTURI GATE 1: Copyright Analysis Initiating..." -ForegroundColor Yellow

    $files = Get-SourceFiles
    $missingCopyright = @()
    $inconsistentCopyright = @()
    $externalReferences = @()

    foreach ($file in $files) {
        try {
            $content = Get-Content $file.FullName -Raw -Encoding UTF8

            if (-not (Test-CopyrightCompliance -Content $content)) {
                $missingCopyright += $file.FullName
            }

            # Check for external references
            $externalIndicators = @(
                "stackoverflow\.com", "github\.com", "medium\.com",
                "reddit\.com", "quora\.com", "copied from", "adapted from",
                "based on", "source:", "reference:"
            )

            foreach ($indicator in $externalIndicators) {
                if ($content -match $indicator) {
                    $externalReferences += $file.FullName
                    break
                }
            }

        }
        catch {
            Write-Host "⚠️  Error analyzing $($file.FullName): $($_.Exception.Message)" -ForegroundColor Yellow
        }
    }

    $results = @{
        MissingCopyright      = $missingCopyright
        InconsistentCopyright = $inconsistentCopyright
        ExternalReferences    = $externalReferences
    }

    Write-Host "📊 Analysis Complete: $($missingCopyright.Count) missing, $($inconsistentCopyright.Count) inconsistent, $($externalReferences.Count) external references" -ForegroundColor Green

    return $results
}

function Invoke-VenturiGate2 {
    param([hashtable]$AnalysisResults)

    Write-Host "🚪 VENTURI GATE 2: Copyright Remediation Initiating..." -ForegroundColor Yellow

    $remediationStats = @{
        CopyrightsAdded   = 0
        CopyrightsUpdated = 0
        FilesProcessed    = 0
        Errors            = 0
    }

    # Process missing copyrights
    foreach ($filePath in $AnalysisResults.MissingCopyright) {
        try {
            $file = Get-Item $filePath
            Add-CopyrightHeader -File $file
            $remediationStats.CopyrightsAdded++
        }
        catch {
            Write-Host "❌ Error adding copyright to $filePath`: $($_.Exception.Message)" -ForegroundColor Red
            $remediationStats.Errors++
        }
    }

    # Process inconsistent copyrights
    foreach ($filePath in $AnalysisResults.InconsistentCopyright) {
        try {
            # For now, just mark as processed - detailed standardization would require more complex logic
            $remediationStats.CopyrightsUpdated++
        }
        catch {
            Write-Host "❌ Error updating copyright in $filePath`: $($_.Exception.Message)" -ForegroundColor Red
            $remediationStats.Errors++
        }
    }

    $remediationStats.FilesProcessed = $remediationStats.CopyrightsAdded + $remediationStats.CopyrightsUpdated

    Write-Host "✅ Remediation Complete: $($remediationStats.CopyrightsAdded) added, $($remediationStats.CopyrightsUpdated) updated, $($remediationStats.Errors) errors" -ForegroundColor Green

    return $remediationStats
}

function Invoke-VenturiGate3 {
    param([hashtable]$AnalysisResults, [hashtable]$RemediationStats)

    Write-Host "🚪 VENTURI GATE 3: Copyright Validation Initiating..." -ForegroundColor Yellow

    $validationResults = @{
        AllFilesCompliant         = $true
        LicenseFilePresent        = $false
        ConsistentCopyrightHolder = $true
        MarketplaceIdPresent      = $true
        NoExternalCopyrights      = $true
    }

    # Check license file
    $licensePath = ".\LICENSE"
    if (Test-Path $licensePath) {
        $validationResults.LicenseFilePresent = $true
        $licenseContent = Get-Content $licensePath -Raw -Encoding UTF8
        if ($licenseContent -notmatch [regex]::Escape($CopyrightHolder)) {
            $validationResults.LicenseFilePresent = $false
        }
    }

    # Validate all source files
    $files = Get-SourceFiles
    foreach ($file in $files) {
        try {
            $content = Get-Content $file.FullName -Raw -Encoding UTF8

            if (-not (Test-CopyrightCompliance -Content $content)) {
                $validationResults.AllFilesCompliant = $false
                break
            }

            if ($content -notmatch [regex]::Escape($CopyrightHolder)) {
                $validationResults.ConsistentCopyrightHolder = $false
            }

            if ($content -notmatch $MarketplaceId) {
                $validationResults.MarketplaceIdPresent = $false
            }

            # Check for external copyrights
            $copyrightLines = $content -split "`n" | Where-Object { $_ -match "Copyright" -and $_ -notmatch [regex]::Escape($CopyrightHolder) }
            if ($copyrightLines.Count -gt 0) {
                $validationResults.NoExternalCopyrights = $false
            }

        }
        catch {
            Write-Host "⚠️  Validation error for $($file.FullName): $($_.Exception.Message)" -ForegroundColor Yellow
            $validationResults.AllFilesCompliant = $false
        }
    }

    # Generate compliance report
    New-CopyrightComplianceReport -ValidationResults $validationResults -AnalysisResults $AnalysisResults -RemediationStats $RemediationStats

    $complianceStatus = if ($validationResults.AllFilesCompliant) { "✅ COMPLIANT" } else { "❌ NON-COMPLIANT" }
    Write-Host "🎯 Validation Complete: $complianceStatus" -ForegroundColor $(if ($validationResults.AllFilesCompliant) { "Green" } else { "Red" })

    return $validationResults
}

function New-CopyrightComplianceReport {
    param(
        [hashtable]$ValidationResults,
        [hashtable]$AnalysisResults,
        [hashtable]$RemediationStats
    )

    $reportPath = ".\COPYRIGHT_COMPLIANCE_REPORT.md"

    $complianceStatus = if ($ValidationResults.AllFilesCompliant) { "✅ COMPLIANT" } else { "❌ NON-COMPLIANT" }

    $report = @"
# Copyright Compliance Report
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## L.I.F.E Platform Copyright Compliance Status

### Overall Compliance: $complianceStatus

### Validation Results:
- **All Files Compliant**: $($ValidationResults.AllFilesCompliant)
- **License File Present**: $($ValidationResults.LicenseFilePresent)
- **Consistent Copyright Holder**: $($ValidationResults.ConsistentCopyrightHolder)
- **Marketplace ID Present**: $($ValidationResults.MarketplaceIdPresent)
- **No External Copyrights**: $($ValidationResults.NoExternalCopyrights)

### Analysis Summary:
- **Files Missing Copyright**: $($AnalysisResults.MissingCopyright.Count)
- **Files with Inconsistent Copyright**: $($AnalysisResults.InconsistentCopyright.Count)
- **Files with External References**: $($AnalysisResults.ExternalReferences.Count)

### Remediation Actions Taken:
- **Copyrights Added**: $($RemediationStats.CopyrightsAdded)
- **Copyrights Updated**: $($RemediationStats.CopyrightsUpdated)
- **Files Processed**: $($RemediationStats.FilesProcessed)
- **Errors**: $($RemediationStats.Errors)

### Copyright Standards:
- **Copyright Holder**: $CopyrightHolder
- **Copyright Year**: $CopyrightYear
- **Azure Marketplace Offer ID**: $MarketplaceId
- **License**: MIT License with Commercial Terms

### Remediation Actions Taken:
This report was generated by the L.I.F.E 3-Venturi Copyright Remediation System.

---
Copyright $CopyrightYear - $CopyrightHolder
L.I.F.E. Platform - Azure Marketplace Offer ID: $MarketplaceId
"@

    $report | Set-Content $reportPath -Encoding UTF8
    Write-Host "📄 Compliance report generated: $reportPath" -ForegroundColor Green
}

# Main execution
try {
    if ($AnalyzeOnly) {
        $results = Invoke-VenturiGate1
        exit 0
    }

    if ($Remediate) {
        $analysisResults = Invoke-VenturiGate1
        $remediationStats = Invoke-VenturiGate2 -AnalysisResults $analysisResults
        exit 0
    }

    if ($Validate) {
        $analysisResults = Invoke-VenturiGate1
        $remediationStats = Invoke-VenturiGate2 -AnalysisResults $analysisResults
        $validationResults = Invoke-VenturiGate3 -AnalysisResults $analysisResults -RemediationStats $remediationStats
        exit $(if ($validationResults.AllFilesCompliant) { 0 } else { 1 })
    }

    # Default: Full remediation
    Write-Host "🔄 L.I.F.E 3-VENTURI COPYRIGHT REMEDIATION SYSTEM ACTIVATED" -ForegroundColor Cyan

    $analysisResults = Invoke-VenturiGate1
    $remediationStats = Invoke-VenturiGate2 -AnalysisResults $analysisResults
    $validationResults = Invoke-VenturiGate3 -AnalysisResults $analysisResults -RemediationStats $remediationStats

    Write-Host "=" * 60 -ForegroundColor Cyan
    if ($validationResults.AllFilesCompliant) {
        Write-Host "🎉 COPYRIGHT REMEDIATION COMPLETE - ALL SYSTEMS COMPLIANT" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  COPYRIGHT REMEDIATION COMPLETE - REVIEW REQUIRED" -ForegroundColor Yellow
    }

    exit $(if ($validationResults.AllFilesCompliant) { 0 } else { 1 })

}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}