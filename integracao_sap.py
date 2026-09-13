from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import smtplib
import sys
import time
from dotenv import load_dotenv
import pandas as pd
import requests
from sqlalchemy import Column, Float, MetaData, String, Table, create_engine
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

# Carregamento seguro de variáveis de ambiente
load_dotenv()

# Configuração de Observabilidade Corporativa com Rotação (Evita estouro de disco)
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"pipeline_{datetime.now().strftime('%Y%m%d')}.log")

log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

file_handler = RotatingFileHandler(
    log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(log_formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_formatter)

logger = logging.getLogger("SAP_BI_Pipeline")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class SAPDataPipeline:

    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "sqlite:///bi_staging.db")
        self.engine = create_engine(self.db_url)
        self.metadata = MetaData()
        self.odata_url = os.getenv(
            "SAP_API_URL", "https://api.mock-sap-local/odata/v2/Indicadores"
        )
        self._setup_database()

    def _setup_database(self):
        """Define a estrutura relacional de Staging com segurança transacional."""
        self.staging_table = Table(
            "staging_indicadores_sap",
            self.metadata,
            Column("Centro", String(10), primary_key=True),
            Column("Operacao", String(50), primary_key=True),
            Column("PesoLiquido", Float),
            Column("Material", String(100)),
            Column("Status", String(50)),
            Column(
                "DataProcessamento",
                String(30),
                default=datetime.now().isoformat(),
            ),
        )
        self.metadata.create_all(self.engine)

    def extract_sap_data(self, max_tentativas=3, espera_inicial=5) -> pd.DataFrame:
        """Extrai dados do SAP OData com política de Retry e Backoff Exponencial."""
        tentativa = 0
        while tentativa < max_tentativas:
            try:
                logger.info(
                    f"Conectando ao endpoint OData (Tentativa {tentativa + 1}/{max_tentativas}): {self.odata_url}"
                )

                if "mock" in self.odata_url:
                    logger.warning("Modo Simulação Ativado: Utilizando payload OData mockado.")
                    time.sleep(1)
                    return pd.DataFrame([
                        {
                            "Centro": "3010",
                            "Operacao": "Balança 01",
                            "PesoLiquido": 45200.5,
                            "Material": "Cana Picada",
                            "Status": "Processado",
                        },
                        {
                            "Centro": "3010",
                            "Operacao": "Balança 02",
                            "PesoLiquido": 38900.0,
                            "Material": "Cana Picada",
                            "Status": "Processado",
                        },
                    ])

                response = requests.get(
                    self.odata_url,
                    auth=(os.getenv("SAP_USER"), os.getenv("SAP_PASSWORD")),
                    timeout=30,
                )
                response.raise_for_status()
                return pd.DataFrame(response.json()["d"]["results"])

            except Exception as e:
                tentativa += 1
                logger.error(f"Falha na extração (Tentativa {tentativa}): {e}", exc_info=True)
                if tentativa >= max_tentativas:
                    logger.critical("Número máximo de tentativas excedido na extração do SAP.")
                    raise
                tempo_espera = espera_inicial * tentativa
                logger.info(f"Aguardando {tempo_espera} segundos antes da próxima tentativa...")
                time.sleep(tempo_espera)

    def load_to_staging(self, df: pd.DataFrame):
        """Carrega os dados no banco local com transação atômica e idempotência (Upsert)."""
        if df.empty:
            logger.warning("DataFrame vazio. Nenhuma carga realizada no banco.")
            return

        records = df.to_dict(orient="records")
        logger.info(f"Persistindo {len(records)} registros na tabela de Staging local...")

        try:
            # Transação explícita: Commit automático em sucesso, Rollback automático em falha
            with self.engine.begin() as conn:
                for record in records:
                    stmt = sqlite_insert(self.staging_table).values(record)
                    stmt = stmt.on_conflict_do_update(
                        index_elements=["Centro", "Operacao"],
                        set_={
                            "PesoLiquido": stmt.excluded.PesoLiquido,
                            "Material": stmt.excluded.Material,
                            "Status": stmt.excluded.Status,
                            "DataProcessamento": datetime.now().isoformat(),
                        },
                    )
                    conn.execute(stmt)
            logger.info("Persistência em banco concluída com sucesso (Commit efetuado).")
        except Exception as e:
            logger.critical(f"❌ Erro crítico no banco. Transação revertida (Rollback): {e}", exc_info=True)
            raise

    def generate_report_and_dispatch(self, df: pd.DataFrame):
        """Gera o Excel a partir do banco e dispara o relatório via SMTP com tratamento seguro."""
        arquivo_excel = "relatorio_operacional_sap.xlsx"
        try:
            df.to_excel(arquivo_excel, index=False)
            logger.info(f"Planilha gerada com sucesso: {arquivo_excel}")
        except Exception as e:
            logger.error(f"Erro ao gerar arquivo Excel: {e}", exc_info=True)
            return

        remetente = os.getenv("EMAIL_USER")
        destinatario = os.getenv("EMAIL_DESTINATARIO")
        senha_app = os.getenv("EMAIL_PASSWORD")

        msg = EmailMessage()
        msg["Subject"] = "📊 [Senior BI] Relatório Operacional Automatizado - SAP S/4HANA"
        msg["From"] = remetente
        msg["To"] = destinatario
        msg.set_content(
            f"Pipeline executado com sucesso.\nTotal de registros processados: {len(df)}\nBanco Staging atualizado com idempotência e transação atômica."
        )

        try:
            with open(arquivo_excel, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    filename=arquivo_excel,
                )
        except Exception as e:
            logger.error(f"Erro ao anexar planilha no e-mail: {e}", exc_info=True)
            return

        try:
            logger.info("Iniciando disparo SMTP seguro...")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(remetente, senha_app)
                smtp.send_message(msg)
            logger.info("E-mail disparado com sucesso.")
        except Exception as e:
            logger.error(f"Erro durante o envio do e-mail SMTP: {e}", exc_info=True)

    def run(self):
        try:
            logger.info("=== INÍCIO DO PIPELINE DE BI ===")
            df = self.extract_sap_data()
            self.load_to_staging(df)
            self.generate_report_and_dispatch(df)
            logger.info("=== PIPELINE EXECUTADO COM ÊXITO ===\n")
        except Exception as e:
            logger.critical(f"Falha fatal no pipeline: {e}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    pipeline = SAPDataPipeline()
    pipeline.run()