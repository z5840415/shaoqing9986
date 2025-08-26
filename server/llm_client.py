"""Simple LLM client for OpenAI or Gemini."""
from __future__ import annotations

import os
from typing import Any

import requests


def _call_openai(prompt: str, api_key: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def _call_gemini(prompt: str, api_key: str) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-pro:generateContent?key=" + api_key
    )
    payload: dict[str, Any] = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def ask(provider: str, prompt: str) -> str:
    """Return a text completion from the given provider.

    If the required API key is missing or a request fails, a mock response is
    returned instead. Supported providers: ``openai``, ``gemini``, ``mock``.
    """
    provider = provider.lower()
    try:
        if provider == "openai":
            key = os.getenv("OPENAI_API_KEY")
            if key:
                return _call_openai(prompt, key)
            return f"Mock response to: {prompt}"
        if provider == "gemini":
            key = os.getenv("GEMINI_API_KEY")
            if key:
                return _call_gemini(prompt, key)
            return f"Mock response to: {prompt}"
        return f"Mock response to: {prompt}"
    except Exception:
        return f"Mock response to: {prompt}"
