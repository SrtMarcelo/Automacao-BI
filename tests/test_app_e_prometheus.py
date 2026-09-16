from __future__ import annotations

from unittest.mock import patch
import app
import observabilidade_prometheus


def test_app_rotas() -> None:
    """Testa todas as rotas do app Flask (sucesso e falha)."""
    client = app.app.test_client()

    # Sucesso nas rotas
    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
    assert client.get("/gerar-slides-turno").status_code == 200


@patch("observabilidade_prometheus.start_http_server")
def test_iniciar_servidor_metricas(mock_start_server) -> None:
    """Testa a inicialização bem-sucedida e com falha do Prometheus."""
    # Sucesso
    resultado = observabilidade_prometheus.iniciar_servidor_metricas(8000)
    assert resultado is True
    mock_start_server.assert_called_once_with(8000)

    # Simula erro (porta em uso)
    mock_start_server.side_effect = Exception("Porta ocupada")
    resultado_erro = observabilidade_prometheus.iniciar_servidor_metricas(8000)
    assert resultado_erro is False
