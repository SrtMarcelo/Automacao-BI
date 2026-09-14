import logging
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# Configuração do Logging Estruturado para Auditoria Industrial
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "auditoria_balanca.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def registrar_divergencia_critica(dados_pesagem: dict, diferenca_percentual: float):
    """
    Registra uma divergência crítica no log de auditoria e dispara alerta operacional.
    """
    mensagem_alerta = (
        f"🚨 DIVERGÊNCIA CRÍTICA DETECTADA!\n"
        f"Chave de Acesso: {dados_pesagem.get('chave_acesso', 'N/A')}\n"
        f"Peso Nota Fiscal: {dados_pesagem.get('peso_nf', 0)} kg\n"
        f"Peso Balança: {dados_pesagem.get('peso_balanca', 0)} kg\n"
        f"Diferença Encontrada: {diferenca_percentual:.2f}%\n"
        f"Status: Requer intervenção imediata do operador de pátio."
    )

    # 1. Grava no log estruturado de auditoria
    logging.error(
        f"DIVERGENCIA_CRITICA | {dados_pesagem} | Diferenca: {diferenca_percentual:.2f}%"
    )
    print(f"📝 Log de auditoria gerado: {mensagem_alerta}")

    # 2. Dispara o alerta operacional (E-mail / Webhook)
    _disparar_alerta_operacional(mensagem_alerta)


def _disparar_alerta_operacional(conteudo_alerta: str):
    """
    Envia o alerta por e-mail para o operador de pátio / analista de BI.
    """
    remetente = os.getenv("EMAIL_USER")
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    senha_app = os.getenv("EMAIL_PASSWORD")

    if not remetente or not destinatario or not senha_app:
        print(
            "⚠️ Credenciais de e-mail não configuradas no .env. Alerta registrado apenas em log."
        )
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = "🚨 ALERTA CRÍTICO: Divergência de Peso na Balança"
        msg["From"] = remetente
        msg["To"] = destinatario
        msg.set_content(conteudo_alerta)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)
        print("📧 Alerta operacional disparado por e-mail com sucesso!")
    except Exception as e:
        print(f"❌ Falha ao enviar alerta por e-mail: {e}")
