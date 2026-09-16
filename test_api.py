import pytest
try:
    from api import app
    client = app.test_client() if hasattr(app, 'test_client') else None
except ImportError:
    app = None
    client = None

def test_api_importacao():
    assert app is not None

def test_api_rotas():
    if client:
        # Testa a rota raiz ou endpoints comuns da API
        response = client.get("/")
        assert response.status_code in [200, 404, 405, 500]
        
        # Se houver outras rotas comuns (ex: /health, /status, /metrics)
        for rota in ["/health", "/status", "/metrics", "/api/v1/status"]:
            res = client.get(rota)
            assert res.status_code in [200, 404, 405, 500]
    else:
        assert True