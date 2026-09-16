import sqlite3

# 1. Cria o arquivo dados.db e a tabela
conexao = sqlite3.connect("dados.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS dados_industriais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setor TEXT,
    metrica TEXT
)
""")

# 2. Insere dados de setores diferentes para teste
cursor.execute(
    "INSERT INTO dados_industriais (setor, metrica) VALUES ('Balanca', 'Peso Bruto: 48.5t')"
)
cursor.execute(
    "INSERT INTO dados_industriais (setor, metrica) VALUES ('Moenda', 'Vazão: 540 t/h')"
)
conexao.commit()

# 3. TESTE DE SEGURANÇA: Simulando o login do usuário do setor 'Balanca'
setor_do_usuario = "Balanca"
print(f"--- Consultando apenas para o setor: {setor_do_usuario} ---")

cursor.execute(
    "SELECT * FROM dados_industriais WHERE setor = ?", (setor_do_usuario,)
)
resultados = cursor.fetchall()

for linha in resultados:
  print(linha)

conexao.close()