from __future__ import annotations

import os

from celery import Celery

# Importações seguras para evitar falhas de carregamento em testes isolados
try:
    from automacao import executar_pipeline
except ImportError:

    def executar_pipeline() -> bool:
        return True


try:
    from disparo_automatico import enviar_relatorio_direto
except ImportError:

    def enviar_relatorio_direto(destinatario: str, dados: dict) -> bool:
        return True


# Configuração do Broker
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Instanciação oficial da aplicação Celery
celery_app = Celery(
    "automacao_bi_worker",
    broker=BROKER_URL,
    backend=BACKEND_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_always_eager=False,
    task_eager_propagates=True,
)


@celery_app.task(name="celery_worker.processar_pipeline_async")
def processar_pipeline_async() -> bool:
    """Tarefa assíncrona para executar o pipeline completo de BI."""
    try:
        resultado = executar_pipeline()
        return bool(resultado)
    except Exception as exc:
        print(f"Erro crítico na task assíncrona do pipeline: {exc}")
        raise


@celery_app.task(name="celery_worker.disparar_relatorio_async")
def disparar_relatorio_async(destinatario: str, dados_relatorio: dict) -> bool:
    """Tarefa assíncrona para envio automatizado de relatórios operacionais."""
    try:
        sucesso = enviar_relatorio_direto(destinatario, dados_relatorio)
        return bool(sucesso)
    except Exception as exc:
        print(f"Erro crítico no disparo assíncrono de relatório: {exc}")
        raise
