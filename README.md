#  Sistema de BI e Automação de Relatórios

Pipeline de dados desenvolvido em Python para automação de extração, tratamento e monitoramento de indicadores comerciais (KPIs). O sistema conecta-se a um banco de dados relacional para otimizar a tomada de decisões estratégicas.

---

##  Tecnologias Utilizadas
* **Python** (Linguagem principal)
* **Pandas** (Manipulação e análise de dados)
* **MySQL** / MySQL Workbench (Banco de dados relacional)
* **Smtplib / EmailMessage** (Automação de envio de e-mails)
* **PythonAnywhere** (Hospedagem e execução em nuvem)

---

##  Como Funciona
1. **Extração de Dados:** O script se conecta de forma automatizada à fonte de dados para resgatar informações brutas de vendas e operações.
2. **Processamento e Análise:** Limpa, filtra e estrutura as informações utilizando scripts em Python (`analise_dados.py` e `automacao.py`), gerando planilhas automatizadas em formato Excel.
3. **Disparo Automático:** O sistema dispara o e-mail de forma programada com o anexo pronto para visualização gerencial (`disparo_automatico.py`).

---

##  Como executar o projeto

Se você quiser clonar e testar o código no seu ambiente local, siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SrtMarcelo/Automacao-BI.git](https://github.com/SrtMarcelo/Automacao-BI.git)
Configure o Banco de Dados:

Certifique-se de ter o MySQL instalado e rodando.

Ajuste as credenciais de acesso ao banco dentro dos arquivos de script, se necessário.

Execute os scripts:

Para rodar a rotina de automação:

Bash
python automacao.py
Para processar e analisar os indicadores:

Bash
python analise_dados.py

