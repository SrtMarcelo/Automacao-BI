from prometheus_client import Counter, Histogram, start_http_server

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


def iniciar_servidor_metricas(porta: int = 8000):
    """Inicia o servidor HTTP do Prometheus para expor as métricas na porta 8000."""
    start_http_server(porta)
    print(f"📊 Servidor de métricas Prometheus rodando na porta {porta}...")