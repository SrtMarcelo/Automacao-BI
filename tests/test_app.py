import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_route(client):
    """Testa se a rota de status da API está online e retorna sucesso"""
    response = client.get("/health")
    assert response.status_code == 200


def test_rota_gerar_slides_flask(client):
    """Testa se a rota web do Flask responde corretamente"""
    response = client.get("/gerar-slides-turno")
    assert response.status_code == 200
