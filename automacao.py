import os
import smtplib
from email.message import EmailMessage
import pandas as pd

def enviar_relatorio():
    print("📊 Lendo dados do Excel local: relatorio_automatico.xlsx...")
    
    if not os.path.exists("relatorio_automatico.xlsx"):
        print("❌ Erro: O arquivo 'relatorio_automatico.xlsx' não foi encontrado.")
        return

    df = pd.read_excel("relatorio_automatico.xlsx")
    nome_arquivo = "relatorio_automatico.xlsx"
    
    corpo_email = f"""
    Olá,
    
      O relatório de BI foi gerado com sucesso conectando diretamente ao banco de dados online.
       Total de registros processados: {len(df)}

    Atenciosamente,
    Sistema Automático de BI - Jotta Store
    """
    # Configurações de e-mail utilizando as variáveis de ambiente do .env
    remetente = os.getenv("EMAIL_USER", "mekanics153@gmail.com")
    destinatario = os.getenv("EMAIL_DESTINATARIO", "mekanics153@gmail.com")
    senha_app = os.getenv("EMAIL_PASSWORD", "rfvpmoeolsqelzjo")

    msg = EmailMessage()
    msg['Subject'] = '📊 Relatório Automático Da Loja - Jotta Store'
    msg['From'] = remetente
    msg['To'] = destinatario

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
        msg.add_attachment(file_data, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=file_name)
    except Exception as e:
        print(f"❌ Erro ao anexar o arquivo: {e}")
        return

    try:
        print("🚀 Conectando ao servidor SMTP do Gmail...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)
            
            # 👇 A MENSAGEM ENTRA EXATAMENTE AQUI, LOGO APÓS O ENVIO BEM-SUCEDIDO.
            print("Relatório enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro durante o envio do e-mail: {e}")
if __name__ == "__main__":
    enviar_relatorio() 