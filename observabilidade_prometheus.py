from __future__ import annotations

import logging
from prometheus_client import Counter, Histogram, start_http_server

# Configuração de logging estruturado
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Definindo as métricas industriais
TOTAL_PESAGENS = Counter(
    "bi_pesagens_processadas_total",
    "Total de pesagens processadas pelo pipeline de BI",
    ["status"],
)

TEMPO_PROCESSAMENTO = Histogram(
    "bi_processamento_segundos",
    "Tempo gasto para processar as pesagens/relatórios",
)

ERROS_CRITICOS = Counter(
    "bi_erros_criticos_total", "Total de divergências ou falhas críticas de envio"
)


def iniciar_servidor_metricas(porta: int = 8000) -> bool:
    """Inicia o servidor HTTP do Prometheus para expor as métricas de forma segura."""
    try:
        start_http_server(porta)
        logger.info(f"📊 Servidor de métricas Prometheus rodando na porta {porta}...")
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor de métricas na porta {porta}: {e}")
        return False
