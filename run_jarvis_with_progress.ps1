param(
    [ValidateSet("onefile", "onedir")]
    [string]$Mode = "onedir",
    [int]$TimeoutSec = 180
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $root

$exePath = if ($Mode -eq "onefile") {
    Join-Path $root "dist\Jarvis.exe"
} else {
    Join-Path $root "dist\Jarvis\Jarvis.exe"
}

if (-not (Test-Path -LiteralPath $exePath)) {
    throw "EXE not found: $exePath"
}

Write-Host ""
Write-Host ("[Jarvis] Mode      : {0}" -f $Mode)
Write-Host ("[Jarvis] Executable: {0}" -f $exePath)
Write-Host ("[Jarvis] Timeout   : {0} sec" -f $TimeoutSec)
Write-Host ""

$before = @(
    Get-Process -Name Jarvis -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty Id
)

$proc = Start-Process -FilePath $exePath -PassThru
$sw = [System.Diagnostics.Stopwatch]::StartNew()

$windowShown = $false
$lastLoggedSec = -1

while ($sw.Elapsed.TotalSeconds -lt $TimeoutSec) {
    Start-Sleep -Milliseconds 500

    $current = @(
        Get-Process -Name Jarvis -ErrorAction SilentlyContinue |
            Where-Object { $before -notcontains $_.Id }
    )

    $hasWindow = $false
    foreach ($p in $current) {
        if ([int]$p.MainWindowHandle -ne 0) {
            $hasWindow = $true
            break
        }
    }

    if ($hasWindow) {
        $windowShown = $true
        Write-Host ("[Jarvis] Window shown in {0:n1} sec." -f $sw.Elapsed.TotalSeconds)
        break
    }

    $elapsedSec = [int][math]::Floor($sw.Elapsed.TotalSeconds)
    if ($elapsedSec -ne $lastLoggedSec -and ($elapsedSec % 5 -eq 0)) {
        $lastLoggedSec = $elapsedSec
        Write-Host ("[Jarvis] Loading... {0} sec (processes: {1})" -f $elapsedSec, $current.Count)
    }

    if ($proc.HasExited) {
        Write-Host ("[Jarvis] Process exited early. ExitCode={0}" -f $proc.ExitCode)
        exit 1
    }
}

if (-not $windowShown) {
    Write-Host ("[Jarvis] Timeout reached ({0} sec). Process may still be starting in background." -f $TimeoutSec)
}
