function Get-CleanProjectTree {
    param (
        [string]$rootPath = "."
    )

    $mainFolders = @(
        "frontend/src/components/dashboard",
        "frontend/src/components/charts",
        "frontend/src/components/panels",
        "frontend/src/components/ui",
        "backend/src/data",
        "backend/src/models",
        "backend/src/risk",
        "backend/src/execution",
        "backend/src/monitoring",
        "backend/src/analysis",
        "backend/config",
        "docker"
    )

    $extensions = @(".tsx", ".ts", ".py", ".yml", ".json")

    foreach ($folder in $mainFolders) {
        $fullPath = Join-Path $rootPath $folder
        if (Test-Path $fullPath) {
            Write-Output "`n$folder/"
            Get-ChildItem -Path $fullPath -File | 
                Where-Object { $extensions -contains $_.Extension } |
                ForEach-Object {
                    Write-Output "    - $($_.Name)"
                }
        }
    }
}

# Run the function
Set-Location "C:\Users\space\Desktop\blessed\trading-system"
Get-CleanProjectTree