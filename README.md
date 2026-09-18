# Sistema de BI e Automação de Relatórios 

[![Pipeline de CI - SAP BI](https://github.com/SrtMarcelo/Automacao-BI/actions/workflows/ci.yml/badge.svg)](https://github.com/SrtMarcelo/Automacao-BI/actions)
[![Coverage Status](https://img.shields.io/badge/coverage-%3E90%25-brightgreen.svg)](https://github.com/SrtMarcelo/Automacao-BI/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Pipeline de dados automatizado em Python voltado para a extração, tratamento, monitoramento em tempo real de indicadores comerciais e operacionais (KPIs) e integração corporativa. O projeto possui arquitetura validada por suítes de testes automatizados e processamento de CI/CD contínuo.

🏛️ Visão Geral da Arquitetura
O ecossistema foi projetado sob padrões rigorosos de engenharia de software para garantir robustez, consistência e rastreabilidade absoluta dos dados:

Camada de Extração & Persistência: Conexão segura e estruturada com bancos de dados relacionais via SQLAlchemy e manipulação de alta performance com Pandas.

Automação de Disparos: Módulo integrado para processamento e envio programado/seguro de relatórios executivos gerenciais.

Garantia de Qualidade: Padronização estrita de código (Black e Ruff) e alta cobertura de testes unitários automatizados (Pytest) com padrão estrito assegurado em pipeline.

CI/CD Integrado: Esteira de integração contínua (GitHub Actions) que executa linting, testes e auditorias de cobertura a cada alteração no repositório.

🛠️ Pilha Tecnológica
Linguagem: Python 3.11+

Engenharia & Bancos de Dados: Pandas, SQLAlchemy, MySQL

Qualidade e Testes: Pytest, Pytest-Cov, Black, Ruff

Infraestrutura CI/CD: GitHub Actions

© Desenvolvido por Marcelo Ferreira De Jesus. Todos os direitos reservados.
