# Sistema de BI e Automação de Relatórios 

[![Pipeline de CI - SAP BI](https://github.com/SrtMarcelo/Automacao-BI/actions/workflows/ci.yml/badge.svg)](https://github.com/SrtMarcelo/Automacao-BI/actions)
[![Coverage Status](https://img.shields.io/badge/coverage-%3E90%25-brightgreen.svg)](https://github.com/SrtMarcelo/Automacao-BI/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Pipeline de dados automatizado em Python voltado para a extração, tratamento, monitoramento de indicadores comerciais (KPIs) e integração corporativa. O projeto possui arquitetura validada por suítes de testes automatizados e esteira de CI/CD contínua.

---

## 🏛️ Visão Geral da Arquitetura

O ecossistema foi projetado sob rigorosos padrões de engenharia de software para garantir robustez, consistência e rastreabilidade dos dados:

* **Camada de Extração & Persistência:** Conexão segura e estruturada com bancos de dados relacionais via SQLAlchemy e manipulação de alta performance com Pandas.
* **Automação de Disparos:** Módulo integrado para envio programado e seguro de relatórios executivos gerenciais.
* **Garantia de Qualidade (Quality Gates):** 
  * Padronização estricta de código via **Black** e **Ruff** (PEP 8).
  * Alta cobertura de testes unitários automatizados (**Pytest**) com **padrão estrito de cobertura acima de 90%** assegurado em pipeline.
* **CI/CD Integrado:** Esteira de integração contínua (GitHub Actions) que executa linting, testes e auditoria de cobertura de código a cada alteração no repositório.

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.11 / 3.14
* **Engenharia de Dados:** Pandas, SQLAlchemy, MySQL
* **Qualidade & Testes:** Pytest, Pytest-Cov, Black, Ruff
* **Infraestrutura CI/CD:** GitHub Actions

---
*© Desenvolvido por Marcelo Ferreira De Jesus. Todos os direitos reservados.*
