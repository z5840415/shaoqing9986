# Air Gesture Control

Prototype using webcam gestures to control the mouse and a minimal FastAPI LLM proxy.

## Setup

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/check_env.py
```

### Windows
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts\check_env.py
```

If any dependency is missing, the check script prints `[MISSING]` and exits with code `1`.

## Running

Start the API then the gesture app:

```bash
python server/main.py  # FastAPI at http://127.0.0.1:8000
python app/main.py     # webcam preview
```

Or use the helper scripts:
```bash
./scripts/run.sh        # Windows: scripts\run.bat
```

Press `Q` in the preview window to quit.

## Environment Variables

Copy `.env.template` to `.env` and edit as needed:

- `GEMINI_API_KEY` – API key for Gemini
- `OPENAI_API_KEY` – API key for OpenAI
- `CAM_INDEX` – camera device index (default `0`)
- `SMOOTHING_ALPHA` – EMA smoothing factor (default `0.35`)
- `PINCH_PX` – pinch distance in pixels for click (default `40`)
- `LONG_PINCH_SEC` – pinch hold duration for drag (default `0.6`)

## Notes

- **Camera permissions**: On macOS, grant terminal/python camera access in *System Settings → Privacy & Security → Camera*. On Windows, ensure the global camera toggle is on in *Settings → Privacy & security → Camera*.
- **Accessibility**: PyAutoGUI needs accessibility/screen control permission. On macOS enable it in *System Settings → Privacy & Security → Accessibility*. On Windows run the terminal as administrator if needed.
- **Multi‑monitor / HiDPI**: Cursor mapping uses the primary display. Adjust OS scaling if movements feel off on HiDPI setups.
- `pyautogui.FAILSAFE` is disabled. If the cursor misbehaves, press `Q` or terminate the process to regain control.

## Controls

- Move your index fingertip to move the cursor.
- Pinch thumb and index to left-click.
- Hold the pinch longer than `LONG_PINCH_SEC` to drag.

## API Usage

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"provider":"mock","prompt":"hi"}'
```

If the required API key is missing, a mock response is returned.
