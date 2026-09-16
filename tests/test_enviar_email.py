from unittest.mock import MagicMock, patch

from enviar_email import enviar_relatorio_outlook


def test_enviar_relatorio_sucesso():
    """Testa o envio bem-sucedido de e-mail mockando o servidor SMTP"""
    with patch("smtplib.SMTP") as mock_smtp:
        instancia_smtp = MagicMock()
        mock_smtp.return_value = instancia_smtp

        resultado = enviar_relatorio_outlook("teste@empresa.com", None)
        assert resultado is True
        instancia_smtp.sendmail.assert_called_once()


def test_enviar_relatorio_com_anexo(tmp_path):
    """Testa o envio com um arquivo de anexo válido"""
    anexo_falso = tmp_path / "relatorio_teste.pdf"
    anexo_falso.write_text("conteudo do relatorio")

    with patch("smtplib.SMTP") as mock_smtp:
        instancia_smtp = MagicMock()
        mock_smtp.return_value = instancia_smtp

        resultado = enviar_relatorio_outlook("teste@empresa.com", str(anexo_falso))
        assert resultado is True
        instancia_smtp.sendmail.assert_called_once()


def test_enviar_relatorio_erro():
    """Testa o comportamento da função de e-mail quando ocorre uma exceção"""
    with patch("smtplib.SMTP", side_effect=Exception("Erro de conexão")):
        resultado = enviar_relatorio_outlook("teste@empresa.com", None)
        assert resultado is False
