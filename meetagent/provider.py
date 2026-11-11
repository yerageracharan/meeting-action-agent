"""Small OpenAI-compatible client for local models and hosted API endpoints."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from urllib.parse import urlsplit

MAX_RESPONSE_BYTES = 2_000_000


@dataclass
class ProviderConfig:
    base_url: str = "http://localhost:11434/v1"
    model: str = "qwen2.5:3b"
    api_key: str = ""
    timeout_seconds: int = 120

    def __post_init__(self) -> None:
        if not isinstance(self.base_url, str) or not self.base_url.strip():
            raise ValueError("MEETAGENT_BASE_URL must be a non-empty HTTP(S) URL")
        self.base_url = self.base_url.strip().rstrip("/")
        parts = urlsplit(self.base_url)
        if parts.scheme not in {"http", "https"} or not parts.hostname:
            raise ValueError("MEETAGENT_BASE_URL must include an http:// or https:// scheme and a hostname")
        try:
            _ = parts.port
        except ValueError as exc:
            raise ValueError("MEETAGENT_BASE_URL contains an invalid port") from exc
        if not isinstance(self.model, str) or not self.model.strip():
            raise ValueError("MEETAGENT_MODEL must be a non-empty model name")
        if not isinstance(self.api_key, str):
            raise TypeError("MEETAGENT_API_KEY must be text")
        if isinstance(self.timeout_seconds, bool) or not isinstance(self.timeout_seconds, int):
            raise TypeError("MEETAGENT_TIMEOUT must be an integer number of seconds")
        if not 1 <= self.timeout_seconds <= 600:
            raise ValueError("MEETAGENT_TIMEOUT must be between 1 and 600 seconds")

    @classmethod
    def from_env(cls) -> "ProviderConfig":
        raw_timeout = os.getenv("MEETAGENT_TIMEOUT", "120")
        try:
            timeout = int(raw_timeout)
        except (TypeError, ValueError) as exc:
            raise ValueError("MEETAGENT_TIMEOUT must be an integer number of seconds") from exc
        return cls(
            base_url=os.getenv("MEETAGENT_BASE_URL", "http://localhost:11434/v1"),
            model=os.getenv("MEETAGENT_MODEL", "qwen2.5:3b"),
            api_key=os.getenv("MEETAGENT_API_KEY", ""),
            timeout_seconds=timeout,
        )


class ModelError(RuntimeError):
    """Raised when the model server cannot return a usable completion."""


def chat_completion(system_prompt: str, user_prompt: str, config: ProviderConfig | None = None) -> str:
    """Call any OpenAI-compatible /chat/completions endpoint, including Ollama and LM Studio."""
    cfg = config or ProviderConfig.from_env()
    url = cfg.base_url + "/chat/completions"
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
            raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ModelError(f"The model response exceeded the {MAX_RESPONSE_BYTES:,}-byte safety limit.")
        payload = json.loads(raw.decode("utf-8"))
    except ModelError:
        raise
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

    if not isinstance(payload, dict):
        raise ModelError("The model server returned JSON, but the top-level response was not an object.")
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ModelError("The model response did not contain choices[0].message.content.") from exc
    if not isinstance(content, str) or not content.strip():
        raise ModelError("The model returned an empty response. Try a different model or a simpler input.")
    return content.strip()
