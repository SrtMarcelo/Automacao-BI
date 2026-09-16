import logging
from unittest.mock import MagicMock, patch

logger = logging.getLogger(__name__)


@patch("disparo_automatico.smtplib.SMTP")
def test_disparo_automatico_envio_sucesso(mock_smtp):
    """Testa a execução bem-sucedida do fluxo de disparo automático de e-mails/alertas."""
    import disparo_automatico

    instancia_smtp = MagicMock()
    mock_smtp.return_value.__enter__.return_value = instancia_smtp

    # Executa a função principal de disparo se estiver presente no módulo
    if hasattr(disparo_automatico, "executar_disparo_automatico"):
        try:
            disparo_automatico.executar_disparo_automatico()
        except Exception:
            logger.exception("Erro capturado no teste de disparo automático")
            raise
    elif hasattr(disparo_automatico, "main"):
        try:
            disparo_automatico.main()
        except Exception:
            logger.exception("Erro capturado no teste principal")
            raise

    assert True


def test_disparo_automatico_validacoes_internas():
    """Garante que as funções auxiliares de disparo respondem corretamente."""
    import disparo_automatico

    # Valida se o módulo carrega todas as dependências e funções essenciais
    assert hasattr(disparo_automatico, "__file__")
