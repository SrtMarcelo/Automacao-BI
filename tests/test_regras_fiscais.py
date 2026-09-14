import pytest
from regras_fiscais import validar_nota_fiscal_produtor, RegraFiscalError

def test_validacao_fiscal_sucesso():
    # Chave válida com 44 dígitos
    chave = "35230500000000000000550010000000011234567890"
    liquido = validar_nota_fiscal_produtor(chave, 50000.0, 15000.0)
    assert liquido == 35000.0

def test_validacao_fiscal_chave_invalida():
    with pytest.raises(RegraFiscalError, match="Chave de acesso"):
        validar_nota_fiscal_produtor("123", 50000.0, 15000.0)

def test_validacao_fiscal_peso_invalido():
    chave = "35230500000000000000550010000000011234567890"
    with pytest.raises(RegraFiscalError, match="Peso bruto"):
        validar_nota_fiscal_produtor(chave, 10000.0, 15000.0)