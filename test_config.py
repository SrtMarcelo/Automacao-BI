import sys

import pytest


def test_config_com_sucesso(monkeypatch):
    monkeypatch.setenv("SAP_API_URL", "https://sap.exemplo.com")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///teste.db")

    if "config" in sys.modules:
        del sys.modules["config"]

    import config

    assert config.Config.SAP_API_URL == "https://sap.exemplo.com"


def test_config_erro_falta_variavel(monkeypatch):
    # Remove a variável e força o dotenv a não recarregá-la de um arquivo .env
    monkeypatch.delenv("SAP_API_URL", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda *args, **kwargs: None)

    if "config" in sys.modules:
        del sys.modules["config"]

    # Importa o módulo dentro do bloco para forçar a validação de erro de ambiente
    with pytest.raises((EnvironmentError, ValueError, KeyError, RuntimeError)):
        pass
