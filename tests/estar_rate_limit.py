from __future__ import annotations

from app import create_app


def test_rate_limit_exceeded() -> None:
    """Valida se o limitador de taxa bloqueia requisições excessivas (código 429)."""
    # Cria a app com o rate limit ativado explicitamente para este teste
    app = create_app({"TESTING": True, "RATELINIT_ENABLED": True})
    client = app.test_client()

    # Como a rota raiz ("/") tem limite de "5 per minute" configurado no app.py,
    # vamos fazer várias requisições seguidas para estourar o limite.
    responses = [client.get("/") for _ in range(7)]

    # Verifica se pelo menos uma das respostas retornou o status 429 (Too Many Requests)
    status_codes = [r.status_code for r in responses]
    assert 429 in status_codes
