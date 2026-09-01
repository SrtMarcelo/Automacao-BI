import customtkinter as ctk
from tkinter import messagebox
import bcrypt
import pandas as pd
from sqlalchemy import create_engine, text
import smtplib
from email.message import EmailMessage

# --- 1. CONFIGURAÇÃO DO BANCO ---
url_conexao = "mysql+pymysql://root:JGwsTBYFWtLCVfBsOKJmZLzmTNexZjhF@yamanote.proxy.rlwy.net:12296/railway"
engine = create_engine(url_conexao)

# --- 2. FUNÇÕES DE SEGURANÇA E AUTOMAÇÃO ---
def gerar_senha_hash(senha_plana):
    """Transforma a senha digitada em um código seguro ($2b$12$...)"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha_plana.encode('utf-8'), salt)

def cadastrar_usuario(nome, email, senha_pura):
    """Realiza o cadastro no banco já com a senha criptografada"""
    try:
        senha_protegida = gerar_senha_hash(senha_pura)
        query = text("INSERT INTO usuarios (nome, email, senha) VALUES (:n, :e, :s)")
        with engine.connect() as conexao:
            conexao.execute(query, {"n": nome, "e": email, "s": senha_protegida})
            conexao.commit()
        print(f"✅ Usuário {nome} cadastrado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao cadastrar: {e}")

def processar_bi_e_enviar_email():
    """Gera o Excel e envia o e-mail automático"""
    try:
        df = pd.read_sql("SELECT * FROM usuarios", engine)
        df.to_excel("relatorio_vendas_jotta.xlsx", index=False)

        msg = EmailMessage()
        msg['Subject'] = '📊 Relatório Automático - Jotta Store'
        msg['From'] = 'mekanics153@gmail.com'
        msg['To'] = 'mekanics153@gmail.com'
        msg.set_content(f"Relatório gerado com sucesso.\nTotal de usuários na base: {len(df)}")

        with open("relatorio_vendas_jotta.xlsx", 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='xlsx', filename="relatorio_vendas_jotta.xlsx")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('mekanics153@gmail.com', 'rfvpmoeolsqelzjo')
            smtp.send_message(msg)

        messagebox.showinfo("Sucesso", "🚀 Relatório enviado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha no BI: {e}")

# --- 3. FUNÇÃO DE LOGIN COM VERIFICAÇÃO DE HASH ---
def verificar_login():
    """Compara a senha digitada com o Hash do banco de dados"""
    try:
        email = entry_email.get()
        senha = entry_senha.get()

        query = text("SELECT senha FROM usuarios WHERE email = :e")
        with engine.connect() as conexao:
            resultado = conexao.execute(query, {"e": email}).fetchone()

            if resultado:
                hash_do_banco = resultado[0]
                try:
                    # Compara a senha digitada com a criptografia do banco
                    if bcrypt.checkpw(senha.encode('utf-8'), hash_do_banco.encode('utf-8')):
                        messagebox.showinfo("Acesso Autorizado!")
                        processar_bi_e_enviar_email()
                    else:
                        messagebox.showerror("Erro", "Senha incorreta.")
                except ValueError:
                    # Erro disparado se a senha no banco for texto puro (antiga)
                    messagebox.showerror("Segurança", "Esta conta usa uma senha antiga insegura. Crie um novo usuário.")
            else:
                messagebox.showerror("Erro", "Usuário não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro Crítico", f"Erro na conexão: {e}")

# --- 4. INTERFACE GRÁFICA ---
ctk.set_appearance_mode("dark")
janela = ctk.CTk()
janela.title("Jotta Store - Controle de BI")
janela.geometry("400x350")

ctk.CTkLabel(janela, text="SISTEMA DE BI JOTTA", font=("Roboto", 22, "bold")).pack(pady=20)

entry_email = ctk.CTkEntry(janela, placeholder_text="Seu E-mail", width=300)
entry_email.pack(pady=10)

entry_senha = ctk.CTkEntry(janela, placeholder_text="Sua Senha", width=300, show="*")
entry_senha.pack(pady=10)

ctk.CTkButton(janela, text="ENTRAR E DISPARAR RELATÓRIO", command=verificar_login, fg_color="#238636").pack(pady=20)

# --- 5. EXECUÇÃO ---
# PARA CRIAR UM USUÁRIO NOVO: Descomente a linha abaixo (remova o #), rode uma vez e comente de novo.
# cadastrar_usuario("Mekan", "admin@jotta.com", "jotta2024")

janela.mainloop()