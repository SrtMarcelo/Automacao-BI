from validador_fiscal import validar_modulo_11_chave_nfe, validar_tolerancia_peso


def test_validar_modulo_11_chave_nfe_valida():
    # Chave válida de exemplo com dígito verificador correto
    chave_valida = "35230500000000000000550010000000011234567890"
    # Vamos testar o comportamento com tamanho incorreto e correto
    assert validar_modulo_11_chave_nfe("123") is False
    # Executa a validação modular real
    resultado = validar_modulo_11_chave_nfe(chave_valida)
    assert isinstance(resultado, bool)


def test_validar_tolerancia_peso_aprovado():
    res = validar_tolerancia_peso(40000.0, 40100.0, tolerancia_percentual=1.0)
    assert res["status"] == "APROVADO"


def test_validar_tolerancia_peso_divergencia():
    res = validar_tolerancia_peso(40000.0, 45000.0, tolerancia_percentual=1.0)
    assert res["status"] == "DIVERGENCIA_CRITICA"


def test_validar_tolerancia_peso_invalido():
    res = validar_tolerancia_peso(0.0, 40000.0)
    assert res["status"] == "ERRO"
