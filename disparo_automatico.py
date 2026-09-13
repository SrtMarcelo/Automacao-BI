import os
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()


def enviar_relatorio_direto():
  try:
    print("📊 Consultando dados via API OData do SAP S/4HANA...")

    # Chamada segura utilizando variáveis de ambiente para usuário e senha
    response = requests.get(
        "https://seu-ambiente-sap/sap/opu/odata/...",
        auth=(os.getenv("SAP_USER"), os.getenv("SAP_PASSWORD")),
        timeout=30,
    )
    response.raise_for_status()  # Lança exceção se a API falhar

    df = pd.DataFrame(response.json()["d"]["results"])
    df.to_excel("relatorio_automatico.xlsx", index=False)

    # Configuração do e-mail
    remetente = os.getenv("EMAIL_USER")
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    senha_app = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = (
        "📊 Relatório Diário Automático - Indicadores Operacionais"
    )
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.set_content(
        f"Relatório gerado via integração SAP S/4HANA.\nTotal de registros:"
        f" {len(df)}"
    )

    with open("relatorio_automatico.xlsx", "rb") as f:
      msg.add_attachment(
          f.read(),
          maintype="application",
          subtype="xlsx",
          filename="relatorio_automatico.xlsx",
      )

    print("🚀 Conectando ao servidor SMTP para disparo...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
      smtp.login(remetente, senha_app)
      smtp.send_message(msg)

    print("Relatório enviado com sucesso! ✅")

  except Exception as e:
    print(f"❌ Erro crítico na integração com o SAP ou envio: {e}")
    exit(1)


if __name__ == "__main__":
  enviar_relatorio_direto()