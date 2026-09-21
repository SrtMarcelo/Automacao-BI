from __future__ import annotations

import app as flask_app
import pytest


@pytest.fixture(autouse=True)
def disable_limiter(monkeypatch):
    """Desativa o rate limiting globalmente via configuração do app Flask nos testes."""
    if hasattr(flask_app, "app"):
        monkeypatch.setitem(flask_app.app.config, "RATELIMIT_ENABLED", False)
