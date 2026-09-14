import smtplib
from email.message import EmailMessage
import bcrypt
import pandas as pd
from sqlalchemy import create_engine, text

# --- 1. CONFIGURAÇÃO DO BANCO ---
url_conexao = "mysql+pymysql://root:JGwsTBYFWtLCVfBsOKJmZLzmTNexZjhF@yamanote.proxy.rlwy.net:12296/railway"
engine = create_engine(url_conexao)


# --- 2. FUNÇÕES DE SEGURANÇA E AUTOMAÇÃO ---
def gerar_senha_hash(senha_plana):
    """Transforma a senha digitada em um código seguro ($2b$12$...)"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha_plana.encode("utf-8"), salt)


def cadastrar_usuario(nome, email, senha_pura, db_engine=engine):
    """Realiza o cadastro no banco já com a senha criptografada"""
    if not nome or not email or not senha_pura:
        raise ValueError("Dados incompletos para cadastro.")

    try:
        senha_protegida = gerar_senha_hash(senha_pura)
        query = text("INSERT INTO usuarios (nome, email, senha) VALUES (:n, :e, :s)")
        with db_engine.connect() as conexao:
            conexao.execute(query, {"n": nome, "e": email, "s": senha_protegida})
            conexao.commit()
        return True
    except Exception as e:
        print(f"❌ Erro ao cadastrar: {e}")
        return False


def processar_bi_e_enviar_email(db_engine=engine):
    """Gera o Excel e envia o e-mail automático"""
    df = pd.read_sql("SELECT * FROM usuarios", db_engine)
    caminho_arquivo = "relatorio_vendas_jotta.xlsx"
    df.to_excel(caminho_arquivo, index=False)

    msg = EmailMessage()
    msg["Subject"] = "📊 Relatório Automático - Jotta Store"
    msg["From"] = "mekanics153@gmail.com"
    msg["To"] = "mekanics153@gmail.com"
    msg.set_content(
        f"Relatório gerado com sucesso.\nTotal de usuários na base: {len(df)}"
    )

    with open(caminho_arquivo, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="xlsx",
            filename="relatorio_vendas_jotta.xlsx",
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("mekanics153@gmail.com", "rfvpmoeolsqelzjo")
        smtp.send_message(msg)

    return True


# --- 3. FUNÇÃO DE LOGIN PURA (Fácil de testar) ---
def autenticar_usuario(email, senha, db_engine=engine):
    """Compara a senha digitada com o Hash do banco de dados de forma testável"""
    query = text("SELECT senha FROM usuarios WHERE email = :e")
    with db_engine.connect() as conexao:
        resultado = conexao.execute(query, {"e": email}).fetchone()

        if not resultado:
            return "usuario_nao_encontrado"

        hash_do_banco = resultado[0]

        # Compatibilidade para string ou bytes vindos do banco
        if isinstance(hash_do_banco, str):
            hash_bytes = hash_do_banco.encode("utf-8")
        else:
            hash_bytes = hash_do_banco

        try:
            if bcrypt.checkpw(senha.encode("utf-8"), hash_bytes):
                processar_bi_e_enviar_email(db_engine)
                return "sucesso"
            else:
                return "senha_incorreta"
        except ValueError:
            return "senha_antiga_insegura"
