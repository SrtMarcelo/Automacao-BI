import os

import pandas as pd
from sqlalchemy import Column, Float, Integer, MetaData, String, Table, create_engine


class SAPDataPipeline:
    def __init__(self):
        database_url = os.getenv("DATABASE_URL", "sqlite:///bi_staging.db")
        self.engine = create_engine(database_url)
        self.metadata = MetaData()

        # Definição da tabela de staging
        self.staging_table = Table(
            "staging_sap_vendas",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("Centro", String(50)),
            Column("Operacao", String(100)),
            Column("PesoLiquido", Float),
            Column("Material", String(100)),
            Column("Status", String(50)),
        )

        # Cria a tabela no banco se não existir
        self.metadata.create_all(self.engine)

    def extract_sap_data(self):
        """Simula a extração de dados do SAP."""
        dados = [
            {
                "Centro": "3010",
                "Operacao": "Balança 01",
                "PesoLiquido": 45000.0,
                "Material": "Cana de Açúcar",
                "Status": "Pendente",
            },
            {
                "Centro": "3010",
                "Operacao": "Balança 02",
                "PesoLiquido": 52000.0,
                "Material": "Cana de Açúcar",
                "Status": "Pendente",
            },
        ]
        return pd.DataFrame(dados)

    def transform_data(self, df):
        """Transforma e valida os dados extraídos."""
        if df is None or df.empty:
            raise ValueError(
                "DataFrame vazio ou inválido fornecido para transformação."
            )

        # Exemplo de transformação simples (garantir tipos ou limpar dados)
        df = df.copy()
        df["PesoLiquido"] = pd.to_numeric(df["PesoLiquido"], errors="coerce")
        return df

    def load_to_staging(self, df):
        """Carrega os dados para a tabela de staging com lógica de persistência."""
        if df is None or df.empty:
            return

        with self.engine.begin() as conn:
            for _, row in df.iterrows():
                # Lógica de idempotência simulada (atualiza ou insere)
                select_stmt = self.staging_table.select().where(
                    (self.staging_table.c.Centro == row["Centro"])
                    & (self.staging_table.c.Operacao == row["Operacao"])
                )
                existing = conn.execute(select_stmt).fetchone()

                if existing:
                    update_stmt = (
                        self.staging_table.update()
                        .where(
                            (self.staging_table.c.Centro == row["Centro"])
                            & (self.staging_table.c.Operacao == row["Operacao"])
                        )
                        .values(
                            PesoLiquido=row["PesoLiquido"],
                            Material=row["Material"],
                            Status=row["Status"],
                        )
                    )
                    conn.execute(update_stmt)
                else:
                    insert_stmt = self.staging_table.insert().values(
                        Centro=row["Centro"],
                        Operacao=row["Operacao"],
                        PesoLiquido=row["PesoLiquido"],
                        Material=row["Material"],
                        Status=row["Status"],
                    )
                    conn.execute(insert_stmt)

    def run(self, invalid_param=False):
        """Executa o pipeline completo (Extract -> Transform -> Load)."""
        if invalid_param:
            raise Exception("Parâmetro inválido fornecido para a execução do pipeline.")

        raw_data = self.extract_sap_data()
        transformed_data = self.transform_data(raw_data)
        self.load_to_staging(transformed_data)
