"""Send one safe smoke-test request to an accessible Gemini model."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def choose_model(client: genai.Client) -> str:
    """Choose a model that advertises generateContent support."""
    preferred = ("gemini-2.5-flash", "gemini-2.0-flash")
    available: list[str] = []

    for model in client.models.list():
        name = model.name.removeprefix("models/")
        supported_methods = model.supported_actions or []
        if "generateContent" in supported_methods:
            available.append(name)

    for model_name in preferred:
        if model_name in available:
            return model_name
    if available:
        return sorted(available)[0]
    raise RuntimeError("The API account returned no generateContent-capable Gemini models.")


def main() -> int:
    load_dotenv(ENV_FILE)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        print(
            "GEMINI_API_KEY is missing. Add it to backend/.env; "
            "the key is never printed."
        )
        return 2

    try:
        client = genai.Client(api_key=api_key)
        model_name = choose_model(client)
        response = client.models.generate_content(
            model=model_name,
            contents="Reply with exactly: Gemini connection works.",
            config=types.GenerateContentConfig(temperature=0),
        )
    except Exception as error:
        message = str(error).lower()
        if "401" in message or "403" in message or "api key" in message:
            print("Gemini authentication failed. Check GEMINI_API_KEY in backend/.env.")
        elif "404" in message or "model" in message:
            print("No accessible Gemini model was found for this API account.")
        elif "429" in message or "quota" in message or "resource exhausted" in message:
            print("Gemini quota or rate limit reached. Check the Google AI quota.")
        elif "timeout" in message or "connection" in message or "network" in message:
            print("Gemini network request failed. Check connectivity or proxy settings.")
        else:
            print(f"Gemini smoke test failed: {type(error).__name__}.")
        return 1

    print(f"Gemini connection works with model: {model_name}")
    print(response.text or "The model returned an empty text response.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
