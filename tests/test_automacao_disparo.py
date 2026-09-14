import os
from unittest.mock import MagicMock, patch
import pandas as pd
import pytest

from automacao import enviar_relatorio
from disparo_automatico import enviar_relatorio_direto


@patch("smtplib.SMTP_SSL")
def test_automacao_enviar_relatorio(mock_smtp):
    df_mock = pd.DataFrame({
        "Centro": ["3010"],
        "Operacao": ["Balança 01"],
        "PesoLiquido": [1000.0],
        "Material": ["Cana"],
        "Status": ["Ok"]
    })
    
    with patch("pandas.read_excel", return_value=df_mock):
        with patch("os.path.exists", return_value=True):
            enviar_relatorio()
            mock_smtp.assert_called_once()


@patch("smtplib.SMTP_SSL")
def test_disparo_automatico_direto(mock_smtp):
    enviar_relatorio_direto()
    mock_smtp.assert_called_once()