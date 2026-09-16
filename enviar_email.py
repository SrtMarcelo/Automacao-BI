import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def enviar_relatorio_outlook(destinatario, caminho_anexo=None):
    """Envia o relatório de turno via SMTP do Outlook/Office 365"""
    # Configurações do Servidor SMTP do Outlook
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    
    # Substitua pelas credenciais ou variáveis de ambiente do seu sistema
    remetente = "seu_email@outlook.com"
    senha = "sua_senha_ou_app_password"

    # Montagem da mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = "Relatório Automático de Turno - Automação BI"

    corpo = "Olá,\n\nSegue em anexo o relatório gerencial gerado automaticamente pelo sistema de automação de BI.\n\nAtenciosamente,\nSistema de Automação"
    msg.attach(MIMEText(corpo, 'plain'))

    # Anexando arquivo (caso exista)
    if caminho_anexo and os.path.exists(caminho_anexo):
        with open(caminho_anexo, "rb") as anexo:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(anexo.read())
            encoders.encode_base64(parte)
            parte.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(caminho_anexo)}")
            msg.attach(parte)

    try:
        # Conexão e envio
        servidor = smtplib.SMTP(smtp_server, smtp_port)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False