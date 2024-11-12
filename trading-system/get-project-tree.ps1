function Get-ProjectTree {
    param (
        [string]$rootPath = ".",
        [string[]]$excludeDirs = @("node_modules", ".git", "build", "dist", "__pycache__", "venv", "env", ".pytest_cache", ".vscode", "coverage"),
        [string[]]$includeExtensions = @(".tsx", ".ts", ".py", ".yml", ".yaml", "Dockerfile", ".json"),
        [int]$indent = 0
    )

    $items = Get-ChildItem -Path $rootPath | Where-Object {
        $_.Name -notin $excludeDirs -and 
        ($_.PSIsContainer -or $_.Extension -in $includeExtensions)
    } | Sort-Object { $_.PSIsContainer }, Name

    foreach ($item in $items) {
        $indentation = "  " * $indent
        if ($item.PSIsContainer) {
            Write-Output "$indentation$($item.Name)/"
            Get-ProjectTree -rootPath $item.FullName -excludeDirs $excludeDirs -includeExtensions $includeExtensions -indent ($indent + 1)
        }
        else {
            Write-Output "$indentation$($item.Name)"
        }
    }
}

# Save current location
$currentLocation = Get-Location

# Navigate to project root (adjust this path as needed)
Set-Location "C:\Users\space\Desktop\blessed\trading-system"

Write-Output "Project Structure:"
Write-Output "=================="
Get-ProjectTree

# Restore original location
Set-Location $currentLocation