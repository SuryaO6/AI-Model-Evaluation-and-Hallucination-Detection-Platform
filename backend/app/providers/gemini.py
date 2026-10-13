"""Google Gemini provider integration."""

from time import sleep

from google import genai


def generate(prompt: str, context: str | None, api_key: str) -> str:
    client = genai.Client(api_key=api_key)
    contents = f"{context}\n\n{prompt}" if context else prompt
    last_error: Exception | None = None
    response = None
    for model in (
        "gemini-3.1-flash-lite",
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite",
    ):
        response = None
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                )
                break
            except Exception as exc:
                last_error = exc
                if "503" not in str(exc) or attempt == 2:
                    break
                sleep(2**attempt)
        if response is not None:
            break
    if response is None:
        raise last_error or RuntimeError("Gemini request failed")
    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty response")
    return text.strip()
