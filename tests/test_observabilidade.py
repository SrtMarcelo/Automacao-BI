from unittest.mock import patch, MagicMock
from observabilidade import registrar_divergencia_critica, _disparar_alerta_operacional


@patch("observabilidade.os.getenv")
def test_disparar_alerta_sem_credenciais(mock_getenv):
    # Simula que as variáveis de ambiente de e-mail estão vazias
    mock_getenv.return_value = None
    dados = {"chave_acesso": "123456", "peso_nf": 1000, "peso_balanca": 1200}

    # Deve passar direto pelo fluxo sem credenciais
    registrar_divergencia_critica(dados, 20.0)


@patch("observabilidade.smtplib.SMTP_SSL")
@patch("observabilidade.os.getenv")
def test_registrar_divergencia_com_email(mock_getenv, mock_smtp):
    # Simula credenciais de e-mail válidas
    mock_getenv.side_effect = lambda key: "teste@email.com" if "EMAIL" in key else None

    # Simula o envio bem-sucedido via SMTP
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    dados = {"chave_acesso": "999999", "peso_nf": 5000, "peso_balanca": 6000}
    registrar_divergencia_critica(dados, 20.0)

    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()


@patch("observabilidade.smtplib.SMTP_SSL")
@patch("observabilidade.os.getenv")
def test_disparar_alerta_falha_envio(mock_getenv, mock_smtp):
    # Simula exceção no envio de e-mail para cobrir o bloco except
    mock_getenv.side_effect = lambda key: "teste@email.com" if "EMAIL" in key else None
    mock_smtp.side_effect = Exception("Erro de conexão SMTP")

    _disparar_alerta_operacional("Conteúdo de teste de falha")
