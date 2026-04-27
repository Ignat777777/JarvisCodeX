# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import glob
import os
import site

from PyInstaller.utils.hooks import collect_all, collect_data_files


project_root = Path.cwd()


def add_existing(items, source, dest="."):
    path = project_root / source
    if path.exists():
        items.append((str(path), dest))


datas = []
for source, dest in [
    ("jarvis_commands.json", "."),
    ("jarvis_settings.json", "."),
    ("jarvis_news_cache.json", "."),
    ("latest_silero_models.yml", "."),
    ("arduino_uno_commands.json", "."),
    ("jarvis_arduino_uno.ino", "."),
    ("arduino-script.ino", "."),
    ("models", "models"),
    ("sketches", "sketches"),
    ("_style_assets", "_style_assets"),
    ("Jarvis_Sound_Pack", "Jarvis_Sound_Pack"),
    ("channel_media", "channel_media"),
    ("channel_refs", "channel_refs"),
    ("channel_refs_png", "channel_refs_png"),
]:
    add_existing(datas, source, dest)

for photo in sorted(project_root.glob("photo_*.jpg")):
    datas.append((str(photo), "."))

binaries = []
seen_binaries = set()
site_roots = []
try:
    site_roots.extend(site.getsitepackages())
except Exception:
    pass
try:
    site_roots.append(site.getusersitepackages())
except Exception:
    pass
for root in site_roots:
    if not root:
        continue
    for pattern in ("**/*portaudio*.dll", "**/*libportaudio*.dll"):
        for dll in glob.glob(os.path.join(root, pattern), recursive=True):
            norm = os.path.normpath(dll)
            key = os.path.normcase(norm)
            if os.path.isfile(norm) and key not in seen_binaries:
                seen_binaries.add(key)
                binaries.append((norm, "."))

hiddenimports = [
    "PySide6",
    "vosk",
    "pyaudio",
    "numpy",
    "torch",
    "PIL",
    "PIL.Image",
    "sounddevice",
    "soundfile",
    "silero",
    "jarvis_telegram",
]

datas += collect_data_files("_sounddevice_data")
datas += collect_data_files("vosk")
tmp_ret = collect_all("silero")
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

icon_path = Path.home() / "OneDrive" / "Desktop" / "jarvis.ico"


a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Jarvis",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon_path) if icon_path.exists() else None,
)
