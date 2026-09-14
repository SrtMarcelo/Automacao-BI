import pytest
from staging_balanca import StagingBalancaRepo

@pytest.fixture
def repo_em_memoria():
    # Utiliza SQLite em memória para testes de integração rápidos e isolados
    repo = StagingBalancaRepo(db_path=":memory:")
    return repo

def test_ciclo_vida_staging_integracao(repo_em_memoria):
    dados_pesagem = {
        "chave_acesso": "35230500000000000000550010000000011234567890",
        "fornecedor": "Fazenda São João",
        "frotista": "Frota Express",
        "tipo_produto": "RB966918",
        "peso_bruto": 45000.0,
        "tara": 15000.0,
        "peso_liquido": 30000.0,
        "status": "APROVADO"
    }

    # Testa a inserção
    sucesso = repo_em_memoria.inserir_pesagem(dados_pesagem)
    assert sucesso is True

    # Testa a leitura e persistência
    registros = repo_em_memoria.listar_todas()
    assert len(registros) == 1
    assert registros[0][1] == dados_pesagem["chave_acesso"]
    assert registros[0][7] == 30000.0

def test_bloqueio_duplicidade_chave(repo_em_memoria):
    dados = {
        "chave_acesso": "11112222333344445555666677778888999900001111",
        "fornecedor": "Teste",
        "frotista": "Teste",
        "tipo_produto": "Cana",
        "peso_bruto": 40000.0,
        "tara": 10000.0,
        "peso_liquido": 30000.0
    }

    # Primeira inserção deve passar
    assert repo_em_memoria.inserir_pesagem(dados) is True
    
    # Segunda inserção com a mesma chave deve falhar por integridade (UNIQUE)
    assert repo_em_memoria.inserir_pesagem(dados) is False

def test_context_manager_staging():
    import os
    db_test = "test_temp.db"
    with StagingBalancaRepo(db_path=db_test) as repo:
        assert repo is not None
        sucesso = repo.inserir_pesagem({
            "chave_acesso": "99998888777766665555444433332222111100009999",
            "fornecedor": "Teste Contexto",
            "frotista": "Frota Contexto",
            "tipo_produto": "Produto X",
            "peso_bruto": 10000.0,
            "tara": 2000.0,
            "peso_liquido": 8000.0
        })
        assert sucesso is True
    
    # Remove o arquivo temporário do banco após o teste
    if os.path.exists(db_test):
        os.remove(db_test)