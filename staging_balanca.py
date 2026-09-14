import sqlite3
from typing import Dict, Any, List

class StagingBalancaRepo:
    def __init__(self, db_path: str = "staging_balanca.db"):
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._criar_tabela()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar()

    def _criar_tabela(self):
        """Cria a tabela de staging para armazenar as pesagens validadas."""
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS pesagens_staging (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chave_acesso TEXT UNIQUE,
                fornecedor TEXT,
                frotista TEXT,
                tipo_produto TEXT,
                peso_bruto REAL,
                tara REAL,
                peso_liquido REAL,
                status TEXT
            )
        """)
        self._conn.commit()

    def inserir_pesagem(self, dados: Dict[str, Any]) -> bool:
        """Insere uma pesagem validada na base de staging."""
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                INSERT INTO pesagens_staging 
                (chave_acesso, fornecedor, frotista, tipo_produto, peso_bruto, tara, peso_liquido, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dados.get("chave_acesso"),
                dados.get("fornecedor"),
                dados.get("frotista"),
                dados.get("tipo_produto"),
                dados.get("peso_bruto"),
                dados.get("tara"),
                dados.get("peso_liquido"),
                dados.get("status", "APROVADO")
            ))
            self._conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def listar_todas(self) -> List[tuple]:
        """Retorna todos os registros salvos no staging."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM pesagens_staging")
        return cursor.fetchall()

    def fechar(self):
        """Fecha a conexão com o banco de dados de forma segura."""
        if self._conn:
            self._conn.close()