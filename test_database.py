import os
import pytest
from database import inicializar_banco, inserir_pesagem, buscar_pesagens_por_tenant


@pytest.fixture(autouse=True)
def gerenciar_banco_teste():
    db_file = "industrial_saas.db"
    # Remove o banco antes do teste para garantir ambiente limpo
    if os.path.exists(db_file):
        os.remove(db_file)
    yield
    # Remove o banco após o teste
    if os.path.exists(db_file):
        os.remove(db_file)


def test_inicializar_banco():
    inicializar_banco()
    assert os.path.exists("industrial_saas.db")


def test_inserir_e_buscar_pesagem():
    inicializar_banco()

    # Insere dados para diferentes tenants
    inserir_pesagem("empresa_a", id_balanca=101, peso=5000.0)
    inserir_pesagem("empresa_b", id_balanca=202, peso=7500.0)

    # Testa a busca estritamente filtrada da Empresa A
    resultados_a = buscar_pesagens_por_tenant("empresa_a")
    assert len(resultados_a) == 1
    assert resultados_a[0][1] == "empresa_a"
    assert resultados_a[0][2] == 101
    assert resultados_a[0][3] == 5000.0

    # Testa a busca da Empresa B
    resultados_b = buscar_pesagens_por_tenant("empresa_b")
    assert len(resultados_b) == 1
    assert resultados_b[0][1] == "empresa_b"
