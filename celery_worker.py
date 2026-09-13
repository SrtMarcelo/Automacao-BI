import os
from celery import Celery
from integracao_sap import SAPDataPipeline

# Configuração do Celery utilizando o Redis do Docker como broker de mensagens
celery_app = Celery(
    "industrial_tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0"),
)


@celery_app.task(name="tasks.executar_pipeline_sap")
def executar_pipeline_sap_task():
    """Tarefa assíncrona gerenciada pelo Celery para processamento em fila."""
    pipeline = SAPDataPipeline()
    pipeline.run()
    return "Pipeline executado com sucesso via mensageria distribuída."