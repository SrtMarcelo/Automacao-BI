from unittest.mock import patch, mock_open
from disparo_automatico import enviar_relatorio_direto


def test_enviar_relatorio_direto_sucesso():
    """Testa a execução completa do relatório no modo mock com sucesso."""
    with patch("pandas.DataFrame.to_excel"), \
         patch("smtplib.SMTP_SSL") as mock_smtp, \
         patch("os.path.exists", return_value=True), \
         patch("os.remove"), \
         patch("builtins.open", mock_open(read_data=b"conteudo_fake_excel")):
        
        # Configura o contexto do servidor SMTP simulado
        smtp_instance = mock_smtp.return_value.__enter__.return_value
        smtp_instance.login.return_value = (235, b"Autenticacao aceita")
        
        resultado = enviar_relatorio_direto()
        assert resultado is True


def test_enviar_relatorio_direto_falha_conexao():
    """Testa o comportamento quando ocorre uma exceção no envio do e-mail."""
    with patch("pandas.DataFrame.to_excel"), \
         patch("smtplib.SMTP_SSL", side_effect=Exception("Erro de conexão SMTP")), \
         patch("os.path.exists", return_value=True), \
         patch("os.remove"), \
         patch("builtins.open", mock_open(read_data=b"conteudo_fake_excel")):
        
        resultado = enviar_relatorio_direto()
        assert resultado is False