"""xAI Grok provider integration."""

import json
from urllib import request


def generate(prompt: str, context: str | None, api_key: str) -> str:
    contents = f"{context}\n\n{prompt}" if context else prompt
    payload = json.dumps(
        {
            "model": "grok-3-mini",
            "messages": [{"role": "user", "content": contents}],
        }
    ).encode()
    req = request.Request(
        "https://api.x.ai/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=60) as response:
        body = json.load(response)
    text = body["choices"][0]["message"]["content"]
    if not text:
        raise RuntimeError("Grok returned an empty response")
    return text.strip()
