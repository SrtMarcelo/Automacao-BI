from datetime import datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from integracao_sap import SAPDataPipeline

# Configuração de logs para o orquestrador
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] Orquestrador - %(message)s",
)


def executar_pipeline_job():
  logging.info("=== INICIANDO EXECUÇÃO AGENDADA DO PIPELINE ===")
  try:
    pipeline = SAPDataPipeline()
    pipeline.run()
    logging.info("=== EXECUÇÃO AGENDADA CONCLUÍDA COM SUCESSO ===")
  except Exception as e:
    logging.critical(
        f"CRÍTICO: O pipeline falhou após as políticas de retry. Erro: {e}"
    )


if __name__ == "__main__":
  scheduler = BlockingScheduler()

  # Configurado para disparar automaticamente nos horários de virada de turno da usina
  scheduler.add_job(executar_pipeline_job, "cron", hour="7,15,23", minute=0)

  logging.info(
      "Orquestrador industrial iniciado. Aguardando próximo ciclo de turno..."
  )

  try:
    scheduler.start()
  except (KeyboardInterrupt, SystemExit):
    logging.info("Orquestrador encerrado manualmente.")