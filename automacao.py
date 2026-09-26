import logging
import os
import smtplib
import time
import uuid
from email.message import EmailMessage
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()
import pandas as pd

# 1. Configuração de Logging de Nível Industrial Sênior
os.makedirs("logs", exist_ok=True)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
log_file = "logs/automacao_bi.log"

file_handler = RotatingFileHandler(
    log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(log_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

logger = logging.getLogger("AutomacaoBI")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Localiza automaticamente o arquivo independentemente da extensão exata
DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
caminho_1 = os.path.join(DIRETORIO_SCRIPT, "relatorio_automatico.xlsx.xls")
caminho_2 = os.path.join(DIRETORIO_SCRIPT, "relatorio_automatico.xlsx")

CAMINHO_PLANILHA = caminho_1 if os.path.exists(caminho_1) else caminho_2


def enviar_relatorio():
    execucao_id = uuid.uuid4().hex[:8]
    inicio_execucao = time.perf_counter()
    logger.info(f"[{execucao_id}] Iniciando geração de relatório")

    if not os.path.exists(CAMINHO_PLANILHA):
        logger.error(f"[{execucao_id}] ❌ Erro: O arquivo não foi encontrado.")
    # PASSO 3: Medir leitura da planilha
    try:
        inicio_leitura = time.perf_counter()
        df = pd.read_csv(
            CAMINHO_PLANILHA, sep=None, engine="python", encoding="utf-8-sig"
        )
        tempo_leitura = time.perf_counter() - inicio_leitura

        logger.info(
            f"[{execucao_id}] "
            f"Leitura concluída "
            f"Registros={len(df)} "
            f"Tempo={tempo_leitura:.2f}s"
        )
    except Exception:
        logger.exception(f"[{execucao_id}] ❌ Erro crítico ao ler a planilha Excel")
        return

    remetente = (os.getenv("EMAIL_USER") or "mekanics153@gmail.com").strip()
    destinatario = (os.getenv("EMAIL_DESTINATARIO") or "mekanics153@gmail.com").strip()
    senha_app = (os.getenv("EMAIL_PASSWORD") or "").strip()

    if not all([remetente, destinatario, senha_app]):
        logger.error(
            f"[{execucao_id}] Configuracao de e-mail incompleta no ambiente (.env)"
        )
        return

    msg = EmailMessage()
    msg["Subject"] = "📊 Relatório Automático Da Loja - Jotta Store"
    msg["From"] = remetente
    msg["To"] = destinatario

    corpo_email = f"""Olá,

O relatório de BI foi gerado com sucesso conectando diretamente ao banco de dados online.
Total de registros processados: {len(df)}

Atenciosamente,
Sistema Automático de BI - Jotta Store
"""
    msg.set_content(corpo_email)

    try:
        with open(CAMINHO_PLANILHA, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(f.name)
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=file_name,
        )
    except Exception:
        logger.exception(f"[{execucao_id}] ❌ Erro ao anexar o arquivo")
        return

    # PASSO 4: Medir o envio SMTP
    try:
        logger.info(f"[{execucao_id}] 🚀 Conectando ao servidor SMTP do Gmail...")
        inicio_envio = time.perf_counter()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)

        tempo_envio = time.perf_counter() - inicio_envio

        logger.info(f"[{execucao_id}] " f"E-mail enviado " f"Tempo={tempo_envio:.2f}s")

    except Exception:
        logger.exception(f"[{execucao_id}] ❌ Erro durante o envio e-mail")
        return

    # PASSO 5: Log final consolidado de SUCESSO
    tempo_total = time.perf_counter() - inicio_execucao
    logger.info(
        f"[{execucao_id}] "
        f"Execução concluída "
        f"Status=SUCESSO "
        f"Registros={len(df)} "
        f"TempoTotal={tempo_total:.2f}s"
    )


if __name__ == "__main__":
    enviar_relatorio()
