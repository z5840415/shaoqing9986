# Air Gesture Control

Prototype using webcam gestures to control the mouse and a minimal FastAPI LLM proxy.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
pip install -r requirements.txt
```

Copy `.env.template` to `.env` and fill in any keys.

## Running

Start the API then the gesture app:

```bash
python server/main.py  # starts FastAPI on http://127.0.0.1:8000
python app/main.py     # opens the webcam preview
```

or use the helper script:

```bash
./scripts/run.sh        # Windows: scripts\run.bat
```

## Controls

- Move your index fingertip to move the cursor.
- Pinch thumb and index to left‑click.
- Hold the pinch for more than `LONG_PINCH_SEC` to drag.
- Press `Q` to quit.

`pyautogui.FAILSAFE` is disabled; if the cursor runs away, press `Q` or terminate
the process (`Ctrl+C`, closing the window, etc.) to regain control.

Environment variables (can be set in `.env`):

- `CAM_INDEX` (default `0`)
- `SMOOTHING_ALPHA` (default `0.35`)
- `PINCH_PX` (default `40`)
- `LONG_PINCH_SEC` (default `0.6`)
- `GEMINI_API_KEY` / `OPENAI_API_KEY` for the server

macOS and Windows may require granting camera and accessibility permissions to
your terminal or Python interpreter for the webcam and PyAutoGUI to function.

## API Usage

```
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"provider":"mock","prompt":"hi"}'
```

If the required API key is missing, a mock response is returned.
