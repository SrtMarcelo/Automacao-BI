import pandas as pd
import smtplib
from email.message import EmailMessage

# --- 1. FUNÇÃO DE AUTOMAÇÃO ---
def processar_bi_e_enviar_email():
    try:
        print("📊 Lendo dados do Excel local: relatorio_automatico.xlsx...")
        # Lendo o arquivo que você subiu com sucesso
        df = pd.read_excel("relatorio_automatico.xlsx")

        msg = EmailMessage()
         msg['Subject'] = '📊 Relatório Automático - Jotta Store'
          msg['From'] = 'mekanics153@gmail.com'
           msg['To'] = 'mekanics153@gmail.com'

           corpo_email = f"""
          Olá,

        O relatório de BI foi gerado com sucesso a partir dos dados locais.
      Total de registros processados: {len(df)}

          Atenciosamente,
           Sistema de Automação
             """
           msg.set_content(corpo_email)

        # Anexando o arquivo que está no servidor
        with open("relatorio_automatico.xlsx", 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='xlsx',
                filename="relatorio_final_jotta.xlsx"
            )

        print("📧 Conectando ao servidor de e-mail...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('mekanics153@gmail.com', 'rfvpmoeolsqelzjo')
            smtp.send_message(msg)

        print("🚀 Relatório enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro durante a automação: {e}")

if __name__ == "__main__":
    processar_bi_e_enviar_email()