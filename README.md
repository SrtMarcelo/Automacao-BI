
[![Pipeline de CI - SAP BI](https://github.com/SrtMarcelo/Automacao-BI/actions/workflows/ci.yml/badge.svg)](https://github.com/SrtMarcelo/Automacao-BI/actions)
[![Coverage Status](https://img.shields.io/badge/coverage-%3E90%25-brightgreen.svg)](https://github.com/SrtMarcelo/Automacao-BI/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.14-blue.svg)](https://www.python.org/)
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
- **Garantia de Qualidade**: padronização de código (Black, Ruff) e cobertura 
  de testes automatizados (Pytest) validada em pipeline.
- **CI/CD**: GitHub Actions executando linting, testes, cobertura e 
  verificação de segredos expostos a cada alteração.

## 🛠️ Pilha Tecnológica

- **Linguagem**: Python 3.11+
- **Dados**: Pandas, SQLAlchemy, MySQL
- **Qualidade**: Pytest, Pytest-Cov, Black, Ruff
- **CI/CD**: GitHub Actions

---
Desenvolvido por Marcelo Ferreira De Jesus.
