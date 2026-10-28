"""Small OpenAI-compatible client for local models and hosted API endpoints."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass
class ProviderConfig:
    base_url: str = "http://localhost:11434/v1"
    model: str = "qwen2.5:3b"
    api_key: str = ""
    timeout_seconds: int = 120

    @classmethod
    def from_env(cls) -> "ProviderConfig":
        return cls(
            base_url=os.getenv("MEETAGENT_BASE_URL", "http://localhost:11434/v1").rstrip("/"),
            model=os.getenv("MEETAGENT_MODEL", "qwen2.5:3b"),
            api_key=os.getenv("MEETAGENT_API_KEY", ""),
            timeout_seconds=int(os.getenv("MEETAGENT_TIMEOUT", "120")),
        )


class ModelError(RuntimeError):
    """Raised when the model server cannot return a usable completion."""


def chat_completion(system_prompt: str, user_prompt: str, config: ProviderConfig | None = None) -> str:
    """Call any OpenAI-compatible /chat/completions endpoint, including Ollama and LM Studio."""
    cfg = config or ProviderConfig.from_env()
    url = cfg.base_url.rstrip("/") + "/chat/completions"
    body = {
        "model": cfg.model,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    headers = {"Content-Type": "application/json"}
    if cfg.api_key:
        headers["Authorization"] = f"Bearer {cfg.api_key}"
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=cfg.timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        detail = getattr(exc, "reason", str(exc))
        raise ModelError(
            f"Could not reach the model server at {url}. Start Ollama or LM Studio, confirm its server is running, "
            f"and check MEETAGENT_BASE_URL. Details: {detail}"
        ) from exc
    except TimeoutError as exc:
        raise ModelError(f"The model request timed out after {cfg.timeout_seconds} seconds.") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ModelError("The model server returned a response that was not valid JSON.") from exc

    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ModelError(f"The model response did not contain a chat completion. Response keys: {list(payload)[:10]}") from exc
    if not isinstance(content, str) or not content.strip():
        raise ModelError("The model returned an empty response. Try a different model or a simpler input.")
    return content.strip()
