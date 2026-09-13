# Usa uma imagem oficial leve do Python
FROM python:3.11-slim

# Criação de um usuário dedicado para evitar execução como root (Security Hardening)
RUN useradd -u 1000 appuser && mkdir /app && chown -R appuser /app

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema se necessário
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copia e instala os requisitos do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto para o container
COPY . .

# Ajusta as permissões de todo o diretório para o usuário da aplicação
RUN chown -R appuser:appuser /app

# Alterna para o usuário não-root por segurança industrial
USER appuser

# Comando padrão para iniciar o orquestrador industrial em modo contínuo
CMD ["python", "agendador.py"]