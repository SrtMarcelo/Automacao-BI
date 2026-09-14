import os
import smtplib
import sys
from email.message import EmailMessage

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def enviar_relatorio_direto():
    try:
        sap_url = os.getenv("SAP_API_URL", "https://seu-ambiente-sap/sap/opu/odata/...")

        # Se a URL contiver o placeholder padrão ou a flag de mock, usamos os dados simulados
        if "seu-ambiente-sap" in sap_url or "mock" in sap_url:
            print(
                "⚠️ URL do SAP não configurada ou modo simulação detectado. Utilizando payload mockado de balança..."
            )
            dados_mock = [
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
            ]
            df = pd.DataFrame(dados_mock)
        else:
            print("📊 Consultando dados via API OData do SAP S/4HANA...")
            response = requests.get(
                sap_url,
                auth=(os.getenv("SAP_USER"), os.getenv("SAP_PASSWORD")),
                timeout=30,
            )
            response.raise_for_status()
            df = pd.DataFrame(response.json()["d"]["results"])

        df.to_excel("relatorio_automatico.xlsx", index=False)

        # Configuração do e-mail
        remetente = os.getenv("EMAIL_USER")
        destinatario = os.getenv("EMAIL_DESTINATARIO")
        senha_app = os.getenv("EMAIL_PASSWORD")

        msg = EmailMessage()
        msg["Subject"] = "📊 Relatório Diário Automático - Indicadores Operacionais"
        msg["From"] = remetente
        msg["To"] = destinatario
        msg.set_content(
            f"Relatório gerado via integração SAP S/4HANA (Modo Resiliente/Mock).\n"
            f"Total de registros processados: {len(df)}"
        )

        with open("relatorio_automatico.xlsx", "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename="relatorio_automatico.xlsx",
            )

        print("🚀 Conectando ao servidor SMTP para disparo...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)

        print("Relatório enviado com sucesso! ✅")

    except Exception as e:  # noqa: BLE001
        print(f"❌ Erro crítico na integração ou envio: {e}")
        sys.exit(1)


if __name__ == "__main__":
    enviar_relatorio_direto()
