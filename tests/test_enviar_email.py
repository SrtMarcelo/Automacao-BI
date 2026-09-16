import smtplib
from unittest.mock import patch, MagicMock
from enviar_email import enviar_relatorio_outlook


def test_enviar_relatorio_sucesso():
    """Testa o envio bem-sucedido de e-mail cobrindo context managers do SMTP"""
    with patch("smtplib.SMTP") as mock_smtp:
        instance = mock_smtp.return_value.__enter__.return_value
        resultado = enviar_relatorio_outlook("teste@empresa.com", None)
        assert resultado is True


def test_enviar_relatorio_erro():
    """Testa se a função retorna False quando ocorre uma exceção SMTP"""
    with patch("smtplib.SMTP", side_effect=smtplib.SMTPException("Erro de conexão")):
        resultado = enviar_relatorio_outlook("teste@empresa.com", None)
        assert resultado is False