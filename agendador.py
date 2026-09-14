import logging

from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Logger próprio do módulo para atender ao padrão industrial do Ruff (LOG015)
logger = logging.getLogger(__name__)


def tarefa_agendada():
    """Função executada periodicamente pelo agendador."""
    logger.info("Executando tarefa agendada de integração/BI...")


def iniciar_agendamento():
    """Configura e inicia o agendador de tarefas em background/bloco."""
    scheduler = BlockingScheduler()
    # Exemplo: agenda para rodar a cada 1 hora ou conforme sua regra de negócio
    scheduler.add_job(tarefa_agendada, "interval", hours=1)

    logger.info("Agendador iniciado com sucesso.")
    scheduler.start()


if __name__ == "__main__":
    iniciar_agendamento()