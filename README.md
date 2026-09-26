[![Pipeline de CI - SAP BI](https://github.com/SrtMarcelo/Automacao-BI/actions/workflows/ci.yml/badge.svg)](https://github.com/SrtMarcelo/Automacao-BI/actions)
[![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen.svg)](https://github.com/SrtMarcelo/Automacao-BI/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# Sistema de BI e Automação de Relatórios

Pipeline de dados em Python para extração, tratamento e automação de relatórios 
de indicadores comerciais e operacionais (KPIs), com simulação de integração 
corporativa (SAP). Projeto pessoal desenvolvido para aplicar práticas de 
engenharia de dados a um contexto industrial real.

## 🏛️ Visão Geral da Arquitetura

- **Extração & Persistência**: conexão estruturada com bancos relacionais via 
  SQLAlchemy, manipulação de dados com Pandas.
- **Automação de Disparos**: envio programado de relatórios executivos por e-mail.
- **Agendamento**: execução automatizada de tarefas via agendador dedicado.
- **Processamento Assíncrono**: filas de tarefas em background com Celery.
- **API REST**: endpoints Flask para integração com outros sistemas.
- **Validação Fiscal**: verificação de chave NFe (dígito verificador módulo 11) 
  e regras de tolerância de peso.
- **Observabilidade**: alertas automáticos e exportação de métricas via 
  Prometheus para monitoramento operacional.
- **Segurança**: credenciais isoladas em variáveis de ambiente, sem exposição 
  no código-fonte; verificação automática de segredos no pipeline de CI.
- **Garantia de Qualidade**: padronização de código (Black, Ruff) e cobertura 
  de testes automatizados (Pytest) validada em pipeline.
- **CI/CD**: GitHub Actions executando linting, testes, cobertura e 
  verificação de segredos expostos a cada alteração.

## 🛠️ Pilha Tecnológica

- **Linguagem**: Python 3.11+
- **Dados**: Pandas, SQLAlchemy, MySQL
- **API & Automação**: Flask, Celery
- **Qualidade**: Pytest, Pytest-Cov, Black, Ruff
- **Segurança**: python-dotenv, detect-secrets
- **CI/CD**: GitHub Actions

## 🚀 Como Executar

```bash
# Clonar o repositório
git clone https://github.com/SrtMarcelo/Automacao-BI.git
cd Automacao-BI

# Criar ambiente virtual e instalar dependências
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# Rodar os testes
pytest -v --cov=. --cov-report=term-missing
```

---
Desenvolvido por Marcelo Ferreira De Jesus.
