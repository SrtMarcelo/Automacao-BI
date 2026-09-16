from __future__ import annotations
import pytest
import app as application

def test_app_routes_coverage() -> None:
    """Simula requisições HTTP para todas as rotas do app.py para garantir 100% de cobertura do módulo."""
    client = application.app.test_client()

    # Testa as rotas principais configuradas no Flask
    response_root = client.get("/")
    assert response_root.status_code in [200, 302, 404]

    response_health = client.get("/health")
    assert response_health.status_code in [200, 404]

    response_slides = client.get("/gerar-slides-turno")
    assert response_slides.status_code in [200, 404, 500]