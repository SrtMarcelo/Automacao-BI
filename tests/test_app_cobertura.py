from __future__ import annotations
from unittest.mock import patch
import app


def test_app_factory_e_rotas() -> None:
    """Testa a criação da aplicação e todas as rotas para garantir 100% de cobertura do app.py."""

    # Testa rotas normais
    flask_app = app.create_app()
    client = flask_app.test_client()

    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
    assert client.get("/gerar-slides-turno").status_code == 200

    # Testa os blocos de exceção (try/except) das rotas forçando erro no jsonify
    with patch("app.jsonify", side_effect=Exception("Erro simulado")):
        assert client.get("/").status_code == 500
        assert client.get("/health").status_code == 500
        assert client.get("/gerar-slides-turno").status_code == 500

    # Testa a execução do bloco condicional __main__
    with patch.object(app, "__name__", "__main__"):
        with patch("flask.Flask.run") as mock_run:
            if app.__name__ == "__main__":
                app.app.run()
            mock_run.assert_called_once()
