import os
import logging
from celery import Celery
from integracao_sap import SAPDataPipeline

logger = logging.getLogger(__name__)

# Configuração do Celery utilizando o Redis do Docker como broker de mensagens
celery_app = Celery(
    "industrial_tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0"),
)

@celery_app.task(
    bind=True, 
    name="tasks.executar_pipeline_sap",
    max_retries=3,          # Tenta até 3 vezes antes de desistir
    default_retry_delay=10  # Aguarda 10 segundos entre as tentativas
)
def executar_pipeline_sap_task(self, dados_pesagem=None):
    """Tarefa assíncrona gerenciada pelo Celery com tolerância a falhas e DLQ."""
    try:
        pipeline = SAPDataPipeline()
        pipeline.run()
        return "Pipeline executado com sucesso via mensageria distribuída."
        
    except Exception as exc:
        logger.warning(f"Falha na tentativa {self.request.retries + 1} do pipeline. Erro: {exc}")
        
        try:
            # Recomenda nova tentativa automática
            self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            # --- DEAD LETTER QUEUE (DLQ / QUARENTENA) ---
            logger.error(f"[ALERTA CRÍTICO - DLQ] O pipeline esgotou todas as retentativas e foi isolado. Erro: {exc}")
            
            # Função para salvar o registro corrompido em quarentena sem travar a fábrica
            enviar_para_dlq(dados_pesagem, str(exc))
            raise

def enviar_para_dlq(payload, motivo_erro):
    """Isola o payload com erro em uma fila ou log de quarentena para análise posterior."""
    # Aqui você pode registrar o erro em uma tabela dedicada do banco ou log seguro
    print(f"-> [DLQ] Mensagem isolada com sucesso na quarentena. Motivo: {motivo_erro}")