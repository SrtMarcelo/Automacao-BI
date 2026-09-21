from __future__ import annotations

from unittest.mock import MagicMock, patch

import app


def test_app_factory_e_rotas() -> None:
    """Testa a criação da aplicação e todas as rotas para garantir 100% de cobertura do app.py."""
    flask_app = app.create_app({"RATELIMIT_ENABLED": False, "TESTING": True})
    client = flask_app.test_client()

    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
    assert client.get("/gerar-slides-turno").status_code == 200

    # Mock usando lista no side_effect:
    # 1º chamada: lança a exceção para cair no bloco except
    # 2º chamada: retorna um objeto mockado com sucesso para o jsonify do except montar o status 500
    mock_response_erro = MagicMock()

    with patch(
        "app.jsonify",
        side_effect=[Exception("Erro simulado no jsonify"), mock_response_erro],
    ):
        response = client.get("/")
        assert response.status_code == 500

    with patch(
        "app.jsonify",
        side_effect=[Exception("Erro simulado no health"), mock_response_erro],
    ):
        response = client.get("/health")
        assert response.status_code == 500

    with patch(
        "app.jsonify",
        side_effect=[Exception("Erro simulado nos slides"), mock_response_erro],
    ):
        response = client.get("/gerar-slides-turno")
        assert response.status_code == 500
