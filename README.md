# Jarvis Desktop Assistant

Python/PySide6 desktop assistant project.

## Run

```powershell
python main.py
```

Or use:

```powershell
start_jarvis.bat
```

## Verify

```powershell
verify_jarvis.bat
```

## Notes

- Runtime settings are stored in `jarvis_settings.json`; do not commit real API keys, tokens, passwords, or personal IDs.
- Voice recognition models are expected in `models/` or via `VOSK_MODEL_PATH`; large model files are intentionally not included in Git.
- Sound files in `Jarvis_Sound_Pack/` are included because the app references them.

## Speech models

- `models/vosk-model-small-ru-0.22/` is included for offline Russian speech recognition.
- `models/silero_tts/` is included for local Russian text-to-speech.
