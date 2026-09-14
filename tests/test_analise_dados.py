from unittest.mock import MagicMock, patch

import analise_dados
import bcrypt
import pytest


def test_gerar_senha_hash():
    h = analise_dados.gerar_senha_hash("123456")
    assert h is not None


@patch("analise_dados.engine.connect")
def test_cadastrar_usuario_sucesso(mock_connect):
    mock_conexao = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conexao

    res = analise_dados.cadastrar_usuario("Teste", "teste@email.com", "123456")
    assert res is True


def test_cadastrar_usuario_dados_invalidos():
    with pytest.raises(ValueError):
        analise_dados.cadastrar_usuario("", "", "")


@patch("analise_dados.engine.connect")
def test_autenticar_usuario_sucesso(mock_connect):
    hash_valido = bcrypt.hashpw(b"senha123", bcrypt.gensalt()).decode("utf-8")

    mock_conexao = MagicMock()
    mock_conexao.execute.return_value.fetchone.return_value = (hash_valido,)
    mock_connect.return_value.__enter__.return_value = mock_conexao

    with patch("analise_dados.processar_bi_e_enviar_email", return_value=True):
        resultado = analise_dados.autenticar_usuario("teste@email.com", "senha123")
        assert resultado == "sucesso"


@patch("analise_dados.engine.connect")
def test_autenticar_usuario_nao_encontrado(mock_connect):
    mock_conexao = MagicMock()
    mock_conexao.execute.return_value.fetchone.return_value = None
    mock_connect.return_value.__enter__.return_value = mock_conexao

    resultado = analise_dados.autenticar_usuario("naoexiste@email.com", "senha123")
    assert resultado == "usuario_nao_encontrado"


@patch("analise_dados.engine.connect")
def test_autenticar_usuario_senha_incorreta(mock_connect):
    hash_valido = bcrypt.hashpw(b"outrasenha", bcrypt.gensalt()).decode("utf-8")

    mock_conexao = MagicMock()
    mock_conexao.execute.return_value.fetchone.return_value = (hash_valido,)
    mock_connect.return_value.__enter__.return_value = mock_conexao

    resultado = analise_dados.autenticar_usuario("teste@email.com", "senhaerrada")
    assert resultado == "senha_incorreta"


@patch("analise_dados.engine.connect")
def test_autenticar_usuario_senha_antiga(mock_connect):
    mock_conexao = MagicMock()
    mock_conexao.execute.return_value.fetchone.return_value = (
        "hash_invalido_sem_formato_bcrypt",
    )
    mock_connect.return_value.__enter__.return_value = mock_conexao

    resultado = analise_dados.autenticar_usuario("teste@email.com", "senha123")
    assert resultado == "senha_antiga_insegura"


@patch("analise_dados.engine.connect")
def test_cadastrar_usuario_erro_banco(mock_connect):
    mock_conexao = MagicMock()
    mock_conexao.execute.side_effect = Exception("Erro simulado no banco")
    mock_connect.return_value.__enter__.return_value = mock_conexao

    resultado = analise_dados.cadastrar_usuario("Teste", "teste@email.com", "123456")
    assert resultado is False


@patch("analise_dados.engine.connect")
def test_autenticar_usuario_valor_invalido(mock_connect):
    mock_conexao = MagicMock()
    mock_conexao.execute.return_value.fetchone.return_value = (b"hash_bytes_invalidos",)
    mock_connect.return_value.__enter__.return_value = mock_conexao

    resultado = analise_dados.autenticar_usuario("teste@email.com", "senha123")
    assert resultado == "senha_antiga_insegura"
