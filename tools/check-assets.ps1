param(
  [string]$Root = (Split-Path -Parent $PSScriptRoot),
  [int]$MaxPrecacheImageBytes = 4200000
)

$ErrorActionPreference = "Stop"
$manifestPath = Join-Path $Root "assets-manifest.js"
$swPath = Join-Path $Root "sw.js"

if (!(Test-Path $manifestPath)) {
  throw "Missing assets-manifest.js"
}

if (!(Test-Path $swPath)) {
  throw "Missing sw.js"
}

$manifestText = Get-Content -Raw -LiteralPath $manifestPath
$swText = Get-Content -Raw -LiteralPath $swPath
$assetMatches = [regex]::Matches($manifestText, '"(assets/[^"]+)"')
$missing = New-Object System.Collections.Generic.List[string]
$oversizedPrecache = New-Object System.Collections.Generic.List[string]

foreach ($match in $assetMatches) {
  if ($match.Groups[1].Value.Contains("<")) {
    continue
  }
  if ($match.Groups[1].Value.EndsWith("/")) {
    continue
  }
  $relative = $match.Groups[1].Value.Replace("/", [IO.Path]::DirectorySeparatorChar)
  $path = Join-Path $Root $relative
  if (!(Test-Path $path)) {
    $missing.Add($match.Groups[1].Value)
    continue
  }

  if ($swText.Contains($match.Groups[1].Value)) {
    $length = (Get-Item -LiteralPath $path).Length
    if ($length -gt $MaxPrecacheImageBytes) {
      $oversizedPrecache.Add("$($match.Groups[1].Value) ($length bytes)")
    }
  }
}

if ($missing.Count -or $oversizedPrecache.Count) {
  if ($missing.Count) {
    Write-Host "Missing assets:"
    $missing | ForEach-Object { Write-Host " - $_" }
  }
  if ($oversizedPrecache.Count) {
    Write-Host "Oversized precached assets:"
    $oversizedPrecache | ForEach-Object { Write-Host " - $_" }
  }
  exit 1
}

Write-Host "Asset manifest OK. $($assetMatches.Count) references checked."
