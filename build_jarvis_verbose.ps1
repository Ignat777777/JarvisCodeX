param(
    [ValidateSet("onefile", "onedir")]
    [string]$BuildMode = "onefile",
    [switch]$NoClean,
    [switch]$RunSelfTest,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Quote-Arg {
    param([string]$Arg)
    if ($Arg -match '[\s;"]') {
        return '"' + ($Arg -replace '"', '\"') + '"'
    }
    return $Arg
}

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $projectRoot
$specOutputDir = Join-Path $projectRoot "build\pyinstaller_specs"
New-Item -ItemType Directory -Force -Path $specOutputDir | Out-Null

$pythonExe = (Get-Command python -ErrorAction Stop).Source
$iconPath = "C:\Users\PC\OneDrive\Desktop\jarvis.ico"
$hasIcon = Test-Path -LiteralPath $iconPath
if (-not $hasIcon) {
    Write-Host "[skip --icon] icon not found: $iconPath"
}

$requiredData = @(
    @{ Source = "jarvis_commands.json"; Dest = "." },
    @{ Source = "jarvis_settings.json"; Dest = "." },
    @{ Source = "jarvis_news_cache.json"; Dest = "." },
    @{ Source = "latest_silero_models.yml"; Dest = "." },
    @{ Source = "arduino_uno_commands.json"; Dest = "." },
    @{ Source = "jarvis_arduino_uno.ino"; Dest = "." },
    @{ Source = "arduino-script.ino"; Dest = "." },
    @{ Source = "models"; Dest = "models" },
    @{ Source = "sketches"; Dest = "sketches" },
    @{ Source = "_style_assets"; Dest = "_style_assets" },
    @{ Source = "Jarvis_Sound_Pack"; Dest = "Jarvis_Sound_Pack" },
    @{ Source = "channel_media"; Dest = "channel_media" },
    @{ Source = "channel_refs"; Dest = "channel_refs" },
    @{ Source = "channel_refs_png"; Dest = "channel_refs_png" }
)

$dataItems = New-Object System.Collections.Generic.List[string]
foreach ($entry in $requiredData) {
    $src = [string]$entry.Source
    $dest = [string]$entry.Dest
    $srcPath = Join-Path $projectRoot $src
    if (Test-Path -LiteralPath $srcPath) {
        $dataItems.Add("$srcPath;$dest")
    } else {
        Write-Host "[skip --add-data] missing: $srcPath"
    }
}

$photos = Get-ChildItem -LiteralPath $projectRoot -File -Filter "photo_*.jpg" -ErrorAction SilentlyContinue | Sort-Object Name
foreach ($photo in $photos) {
    $dataItems.Add("$($photo.FullName);.")
}

$candidateHiddenImports = @(
    "PySide6",
    "vosk",
    "pyaudio",
    "pygame",
    "numpy",
    "torch",
    "openai",
    "pystray",
    "PIL",
    "PIL.Image",
    "sounddevice",
    "edge_tts",
    "soundfile",
    "silero",
    "jarvis_telegram"
)

$probeModules = @'
import importlib.util
import json

mods = [
    "PySide6",
    "vosk",
    "pyaudio",
    "pygame",
    "numpy",
    "torch",
    "openai",
    "pystray",
    "PIL",
    "PIL.Image",
    "sounddevice",
    "edge_tts",
    "soundfile",
    "silero",
    "jarvis_telegram",
]
out = {}
for m in mods:
    try:
        out[m] = importlib.util.find_spec(m) is not None
    except Exception:
        out[m] = False
print(json.dumps(out, ensure_ascii=True))
'@

$probeJson = $probeModules | & $pythonExe -
$moduleAvailability = $probeJson | ConvertFrom-Json

$hiddenImports = New-Object System.Collections.Generic.List[string]
foreach ($moduleName in $candidateHiddenImports) {
    $prop = $moduleAvailability.PSObject.Properties[$moduleName]
    $isInstalled = $false
    if ($null -ne $prop) {
        $isInstalled = [bool]$prop.Value
    }
    if ($isInstalled) {
        $hiddenImports.Add($moduleName)
    } else {
        Write-Host "[skip --hidden-import] missing module: $moduleName"
    }
}

$findPortaudio = @'
import glob
import os
import site

paths = []
try:
    paths.extend(site.getsitepackages())
except Exception:
    pass
try:
    paths.append(site.getusersitepackages())
except Exception:
    pass

seen = set()
for base in paths:
    if not base:
        continue
    for pattern in ("**/*portaudio*.dll", "**/*libportaudio*.dll"):
        for p in glob.glob(os.path.join(base, pattern), recursive=True):
            n = os.path.normpath(p)
            if n not in seen:
                seen.add(n)
                print(n)
'@

$portaudioDlls = @()
$portaudioLines = $findPortaudio | & $pythonExe -
if ($portaudioLines) {
    foreach ($line in $portaudioLines) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if (-not (Test-Path -LiteralPath $line)) { continue }
        if ($portaudioDlls -notcontains $line) {
            $portaudioDlls += $line
        }
    }
}

$pyiArgs = @("--noconfirm", "--windowed", "--noupx", "--name", "Jarvis", "--specpath", $specOutputDir, "--collect-all", "silero", "--collect-data", "_sounddevice_data", "--collect-data", "vosk")
if ($hasIcon) {
    $pyiArgs += "--icon"
    $pyiArgs += $iconPath
}
if ($BuildMode -eq "onefile") {
    $pyiArgs += "--onefile"
} else {
    $pyiArgs += "--onedir"
}
$useClean = -not $NoClean.IsPresent
if ($useClean) {
    $pyiArgs += "--clean"
}

foreach ($hidden in $hiddenImports) {
    $pyiArgs += "--hidden-import"
    $pyiArgs += $hidden
}
foreach ($data in $dataItems) {
    $pyiArgs += "--add-data"
    $pyiArgs += $data
}
foreach ($dll in $portaudioDlls) {
    $pyiArgs += "--add-binary"
    $pyiArgs += "$dll;."
}
$pyiArgs += (Join-Path $projectRoot "main.py")

$displayArgs = $pyiArgs | ForEach-Object { Quote-Arg $_ }
$fullCommand = "python -m PyInstaller " + ($displayArgs -join " ")

Write-Host ""
Write-Host "=== PYINSTALLER COMMAND ==="
Write-Host $fullCommand
Write-Host "==========================="
Write-Host ""
Write-Host ("Build mode : {0}" -f $BuildMode)
Write-Host ("Clean      : {0}" -f $useClean)
Write-Host ("Data items : {0}" -f $dataItems.Count)
Write-Host ("Hidden imp.: {0}" -f $hiddenImports.Count)
Write-Host ("Binaries   : {0}" -f $portaudioDlls.Count)
Write-Host ""

if ($DryRun) {
    Write-Host "DryRun enabled. Build was not started."
    exit 0
}

$timer = [System.Diagnostics.Stopwatch]::StartNew()
& $pythonExe -m PyInstaller @pyiArgs
$pyExit = $LASTEXITCODE
$timer.Stop()

if ($pyExit -ne 0) {
    Write-Host ""
    Write-Host ("Build failed. ExitCode={0}" -f $pyExit)
    exit $pyExit
}

if ($RunSelfTest) {
    Write-Host ""
    Write-Host "Running selftest..."
    & $pythonExe "jarvis_selftest.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Host ("Selftest failed. ExitCode={0}" -f $LASTEXITCODE)
        exit $LASTEXITCODE
    }
}

$outputExe = if ($BuildMode -eq "onefile") {
    Join-Path $projectRoot "dist\Jarvis.exe"
} else {
    Join-Path $projectRoot "dist\Jarvis\Jarvis.exe"
}

Write-Host ""
Write-Host ("Build completed in {0:n1} sec" -f $timer.Elapsed.TotalSeconds)
if (Test-Path -LiteralPath $outputExe) {
    $item = Get-Item -LiteralPath $outputExe
    Write-Host ("OUTPUT_EXE: {0}" -f $item.FullName)
    Write-Host ("SIZE_MB   : {0:n2}" -f ($item.Length / 1MB))
} else {
    Write-Host ("Output exe not found at expected path: {0}" -f $outputExe)
}
