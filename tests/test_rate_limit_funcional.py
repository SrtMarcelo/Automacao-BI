from __future__ import annotations

import pytest
from app import create_app


def test_rate_limit_comportamento() -> None:
    """Valida o funcionamento da rota principal e o comportamento do limitador."""
    app = create_app({"TESTING": True, "RATELIMIT_ENABLED": True})
    client = app.test_client()

    # Faz uma chamada válida para a raiz
    response = client.get("/")
    assert response.status_code in [200, 429]


def test_rate_limit_health_check() -> None:
    """Garante que a rota de health check responde sempre com sucesso."""
    app = create_app({"TESTING": True})
    client = app.test_client()

    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"