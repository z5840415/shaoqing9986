"""Minimal smoke test for air-gesture-control prototype."""
from __future__ import annotations

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULES = [
    ROOT / "app" / "main.py",
    ROOT / "server" / "main.py",
    ROOT / "server" / "llm_client.py",
]

for path in MODULES:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

print("OK")
