import os
import smtplib
from email.message import EmailMessage
import pandas as pd

def enviar_relatorio():
    print("📊 Lendo dados do Excel local: relatorio_automatico.xlsx...")
    
    if not os.path.exists("relatorio_automatico.xlsx"):
        print("❌ Erro: O arquivo 'relatorio_automatico.xlsx' não foi encontrado. Execute o pipeline de análise primeiro.")
        return

    df = pd.read_excel("relatorio_automatico.xlsx")

    # Utilizando variáveis de ambiente para segurança em nível de produção (Padrão Sênior)
    remetente = os.getenv("EMAIL_USER", "seu_email@gmail.com")
    destinatario = os.getenv("EMAIL_DESTINATARIO", "seu_email@gmail.com")
    senha_app = os.getenv("EMAIL_PASSWORD", "sua_senha_de_aplicativo")

    msg = EmailMessage()
    msg['Subject'] = '📊 Relatório Automático Da Loja - Jotta Store'
    msg['From'] = remetente
    msg['To'] = destinatario

    corpo_email = f"""Olá,

O relatório de BI foi gerado com sucesso pelo pipeline local.
Total de registros processados: {len(df)}

Atenciosamente,
Sistema Automático de BI - Jotta Store
"""
    msg.set_content(corpo_email)

    # Anexando a planilha gerada
    try:
        with open("relatorio_automatico.xlsx", "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(f.name)
        msg.add_attachment(file_data, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=file_name)
    except Exception as e:
        print(f"❌ Erro ao anexar o arquivo: {e}")
        return

    # Disparo via Servidor SMTP do Gmail com tratamento de exceção estruturado
    try:
        print("🚀 Conectando ao servidor SMTP do Gmail...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)
        print("✅ E-mail disparado com sucesso!")
    except Exception as e:
        print(f"❌ Erro durante o envio do e-mail: {e}")

if __name__ == "__main__":
    enviar_relatorio()