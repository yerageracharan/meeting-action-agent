import json
from unittest.mock import patch

import pytest

from meetagent.provider import ModelError, ProviderConfig, chat_completion


class FakeResponse:
    def __init__(self, body: bytes):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self, limit=-1):
        return self.body if limit < 0 else self.body[:limit]


def fake_completion(content="hello"):
    return json.dumps({"choices": [{"message": {"content": content}}]}).encode("utf-8")


def test_provider_config_normalises_base_url():
    config = ProviderConfig(base_url=" http://localhost:1234/v1/ ")
    assert config.base_url == "http://localhost:1234/v1"


@pytest.mark.parametrize("url", ["", "localhost:11434/v1", "ftp://example.com/v1", "https://"])
def test_provider_config_rejects_invalid_base_url(url):
    with pytest.raises(ValueError, match="BASE_URL"):
        ProviderConfig(base_url=url)


@pytest.mark.parametrize("timeout", [0, -1, 601])
def test_provider_config_rejects_out_of_range_timeout(timeout):
    with pytest.raises(ValueError, match="between 1 and 600"):
        ProviderConfig(timeout_seconds=timeout)


def test_provider_config_from_env_reports_invalid_timeout(monkeypatch):
    monkeypatch.setenv("MEETAGENT_TIMEOUT", "fast")
    with pytest.raises(ValueError, match="MEETAGENT_TIMEOUT must be an integer"):
        ProviderConfig.from_env()


def test_chat_completion_returns_content_from_compatible_response():
    with patch("meetagent.provider.urllib.request.urlopen", return_value=FakeResponse(fake_completion("  ready  "))):
        assert chat_completion("system", "user", ProviderConfig()) == "ready"


def test_chat_completion_rejects_non_object_json_response():
    with patch("meetagent.provider.urllib.request.urlopen", return_value=FakeResponse(b"[]")):
        with pytest.raises(ModelError, match="top-level response was not an object"):
            chat_completion("system", "user", ProviderConfig())


def test_chat_completion_rejects_missing_choice_content():
    with patch("meetagent.provider.urllib.request.urlopen", return_value=FakeResponse(b'{"choices": []}')):
        with pytest.raises(ModelError, match="choices"):
            chat_completion("system", "user", ProviderConfig())


def test_chat_completion_rejects_oversized_response():
    oversized = b"x" * (2_000_001)
    with patch("meetagent.provider.urllib.request.urlopen", return_value=FakeResponse(oversized)):
        with pytest.raises(ModelError, match="safety limit"):
            chat_completion("system", "user", ProviderConfig())
