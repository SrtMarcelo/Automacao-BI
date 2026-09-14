from unittest.mock import patch, mock_open
import pandas as pd
import automacao

def test_enviar_relatorio_arquivo_nao_encontrado():
    with patch("os.path.exists", return_value=False) as mock_exists:
        automacao.enviar_relatorio()
        mock_exists.assert_called_once()

def test_enviar_relatorio_erro_leitura_excel():
    with patch("os.path.exists", return_value=True), \
         patch("pandas.read_excel", side_effect=Exception("Erro Excel")) as mock_read:
        automacao.enviar_relatorio()
        mock_read.assert_called_once()

def test_enviar_relatorio_erro_anexo():
    with patch("os.path.exists", return_value=True), \
         patch("pandas.read_excel", return_value=pd.DataFrame({"col": [1, 2]})), \
         patch("builtins.open", side_effect=Exception("Erro ao abrir arquivo")) as mock_open_file:
        automacao.enviar_relatorio()
        mock_open_file.assert_called_once()

def test_enviar_relatorio_erro_smtp():
    with patch("os.path.exists", return_value=True), \
         patch("pandas.read_excel", return_value=pd.DataFrame({"col": [1, 2]})), \
         patch("builtins.open", mock_open(read_data=b"dados_excel")), \
         patch("smtplib.SMTP_SSL", side_effect=Exception("Erro SMTP")) as mock_smtp:
        automacao.enviar_relatorio()
        mock_smtp.assert_called_once()

def test_enviar_relatorio_sucesso():
    with patch("os.path.exists", return_value=True), \
         patch("pandas.read_excel", return_value=pd.DataFrame({"col": [1, 2]})), \
         patch("builtins.open", mock_open(read_data=b"dados_excel")), \
         patch("smtplib.SMTP_SSL") as mock_smtp_class:
        
        mock_smtp_instance = mock_smtp_class.return_value.__enter__.return_value
        automacao.enviar_relatorio()
        mock_smtp_instance.login.assert_called_once()
        mock_smtp_instance.send_message.assert_called_once()