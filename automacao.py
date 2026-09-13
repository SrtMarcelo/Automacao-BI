from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import smtplib
from email.message import EmailMessage
import pandas as pd

# 1. Configuração de Logging de Nível Industrial Sênior
# Garante a criação do diretório de logs e o uso de rotação (evita estouro de disco)
os.makedirs("logs", exist_ok=True)
log_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
log_file = "logs/automacao_bi.log"

# Rotação de arquivo: máximo de 5MB por arquivo, mantendo até 3 backups históricos
file_handler = RotatingFileHandler(
    log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(log_formatter)

# Handler para saída padrão (stdout) para capturar no Docker
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

logger = logging.getLogger("AutomacaoBI")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def enviar_relatorio():
    logger.info("📊 Lendo dados do Excel local: relatorio_automatico.xlsx...")

    if not os.path.exists("relatorio_automatico.xlsx"):
        logger.error(
            "❌ Erro: O arquivo 'relatorio_automatico.xlsx' não foi encontrado."
        )
        return

    try:
        df = pd.read_excel("relatorio_automatico.xlsx")
    except Exception as e:
        logger.critical(
            f"❌ Erro crítico ao ler a planilha Excel: {e}", exc_info=True
        )
        return

    nome_arquivo = "relatorio_automatico.xlsx"

    # Configurações de e-mail utilizando as variáveis de ambiente do .env
    remetente = os.getenv("EMAIL_USER", "mekanics153@gmail.com")
    destinatario = os.getenv("EMAIL_DESTINATARIO", "mekanics153@gmail.com")
    senha_app = os.getenv("EMAIL_PASSWORD", "rfvpmoeolsqelzjo")

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

    # Anexando a planilha gerada com dados reais
    try:
        with open(nome_arquivo, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(f.name)
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=file_name,
        )
    except Exception as e:
        logger.error(f"❌ Erro ao anexar o arquivo: {e}", exc_info=True)
        return

    try:
        logger.info("🚀 Conectando ao servidor SMTP do Gmail...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)

            logger.info("Relatório enviado com sucesso!")

    except Exception as e:
        logger.error(
            f"❌ Erro durante o envio do e-mail: {e}", exc_info=True
        )


if __name__ == "__main__":
    enviar_relatorio()