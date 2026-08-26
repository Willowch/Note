# move_images.ps1
# 将脚本所在目录（Obsidian 仓库根目录）下所有以 "Pasted image" 开头的图片，移动到 resources 目录

$ErrorActionPreference = 'Stop'

$projectDir   = $PSScriptRoot
$resourcesDir = Join-Path $projectDir 'resources'

# 1. 创建 resources 目录（如果不存在）
if (-not (Test-Path -LiteralPath $resourcesDir -PathType Container)) {
    New-Item -ItemType Directory -Path $resourcesDir -Force | Out-Null
    Write-Host "已创建目录: $resourcesDir"
}

# 2. 递归查找所有 Pasted image* 文件（排除 resources 目录本身）
$images = Get-ChildItem -LiteralPath $projectDir -Recurse -File -Filter 'Pasted image*' |
    Where-Object { $_.FullName -notlike "$resourcesDir\*" }

if ($images.Count -eq 0) {
    Write-Host '未找到以 "Pasted image" 开头的图片。'
    exit 0
}

# 3. 逐个移动到 resources（遇到重名自动加序号）
$moved = 0
foreach ($img in $images) {
    $destPath = Join-Path $resourcesDir $img.Name

    if (Test-Path -LiteralPath $destPath) {
        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($img.Name)
        $ext      = $img.Extension
        $n = 1
        do {
            $destPath = Join-Path $resourcesDir ("{0} ({1}){2}" -f $baseName, $n, $ext)
            $n++
        } while (Test-Path -LiteralPath $destPath)
    }

    Move-Item -LiteralPath $img.FullName -Destination $destPath
    $moved++
    Write-Host "已移动: $($img.Name) -> $destPath"
}

Write-Host "完成：共移动 $moved 个文件。"
