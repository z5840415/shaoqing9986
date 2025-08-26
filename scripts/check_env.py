#!/usr/bin/env python3
import importlib
import sys

modules = [
    ('cv2', 'OpenCV'),
    ('mediapipe', 'MediaPipe'),
    ('pyautogui', 'PyAutoGUI'),
    ('fastapi', 'FastAPI'),
    ('uvicorn', 'Uvicorn'),
    ('pydantic', 'Pydantic'),
    ('requests', 'Requests'),
]

missing = False
for mod, name in modules:
    try:
        importlib.import_module(mod)
        print(f"[OK] {name}")
    except Exception:
        print(f"[MISSING] {name}")
        missing = True

sys.exit(1 if missing else 0)
