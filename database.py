import sqlite3


def inicializar_banco():
    # O SQLite cria este arquivo automaticamente na sua pasta, sem instalar nada!
    conn = sqlite3.connect("industrial_saas.db")
    cursor = conn.cursor()

    # Cria a tabela transacional já exigindo o tenant_id na raiz
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pesagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT NOT NULL,
            id_balanca INTEGER NOT NULL,
            peso REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def inserir_pesagem(tenant_id, id_balanca, peso):
    conn = sqlite3.connect("industrial_saas.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pesagens (tenant_id, id_balanca, peso) VALUES (?, ?, ?)",
        (tenant_id, id_balanca, peso),
    )
    conn.commit()
    conn.close()


def buscar_pesagens_por_tenant(tenant_id):
    """Busca estritamente filtrada: a Empresa A nunca vê os dados da Empresa B."""
    conn = sqlite3.connect("industrial_saas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pesagens WHERE tenant_id = ?", (tenant_id,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados


if __name__ == "__main__":
    # 1. Inicializa o banco de dados leve
    inicializar_banco()

    # 2. Simula dados de duas empresas diferentes usando o mesmo sistema
    inserir_pesagem("empresa_a", id_balanca=101, peso=5000.0)
    inserir_pesagem("empresa_b", id_balanca=202, peso=7500.0)

    # 3. Testa o isolamento: Pedindo os dados da Empresa A
    print("Dados da Empresa A:", buscar_pesagens_por_tenant("empresa_a"))
