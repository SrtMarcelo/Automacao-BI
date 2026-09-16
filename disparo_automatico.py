from __future__ import annotations

import logging
import os
import smtplib
from email.message import EmailMessage
from typing import Any, Dict, Optional

import pandas as pd
import requests
from celery import Celery
from dotenv import load_dotenv

# Importando as métricas do Prometheus com segurança
try:
    from observabilidade_prometheus import ERROS_CRITICOS, TOTAL_PESAGENS
except ImportError:
    # Fallback caso o módulo de métricas não esteja presente em ambiente isolado de teste
    class DummyMetric:
        def inc(self) -> None:
            pass

        def labels(self, **kwargs: Any) -> DummyMetric:
            return self

    ERROS_CRITICOS = DummyMetric()  # type: ignore
    TOTAL_PESAGENS = DummyMetric()  # type: ignore

load_dotenv()

# Configuração do Celery
celery_app = Celery(
    "automacao_bi", broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=5, default_retry_delay=60)
def enviar_pesagem_sap_async(
    self, dados_pesagem: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Tarefa assíncrona do Celery para envio resiliente ao SAP HANA com tratamento de erros."""
    if dados_pesagem is None:
        dados_pesagem = {}

    sap_url = os.getenv("SAP_API_URL", "https://seu-ambiente-sap/sap/opu/odata/...")
    chave_acesso = dados_pesagem.get("chave_acesso", "N/A")

    try:
        # Modo simulação / mock
        if "seu-ambiente-sap" in sap_url or "mock" in sap_url:
            logger.warning(
                f"⚠️ Modo simulação: Processando pesagem da chave {chave_acesso}..."
            )
            TOTAL_PESAGENS.labels(status="sucesso").inc()
            return {"status": "SUCESSO_MOCK", "chave": chave_acesso}

        logger.info("🔄 Enviando pesagem para API OData do SAP S/4HANA...")
        response = requests.post(
            sap_url,
            json=dados_pesagem,
            auth=(os.getenv("SAP_USER", ""), os.getenv("SAP_PASSWORD", "")),
            timeout=30,
        )

        # Tratamento de erro do cliente (4xx exceto 429)
        if 400 <= response.status_code < 500 and response.status_code != 429:
            logger.error(
                f"❌ Erro cliente irreversível no SAP ({response.status_code})"
            )
            ERROS_CRITICOS.inc()
            TOTAL_PESAGENS.labels(status="erro").inc()
            response.raise_for_status()

        response.raise_for_status()
        TOTAL_PESAGENS.labels(status="sucesso").inc()
        return {"status": "SUCESSO", "resposta": response.json()}

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.HTTPError,
    ) as exc:
        status_code = getattr(getattr(exc, "response", None), "status_code", None)
        if status_code and 400 <= status_code < 500 and status_code != 429:
            raise exc

        logger.warning(
            f"❌ Falha de comunicação/servidor com SAP. Tentativa {self.request.retries + 1}/5. Erro: {exc}"
        )
        raise self.retry(exc=exc)


def _obter_dados_relatorio(sap_url: str) -> pd.DataFrame:
    """Obtém os dados do relatório via API ou dados mockados de balança."""
    if "seu-ambiente-sap" in sap_url or "mock" in sap_url:
        logger.warning("⚠️ Modo simulação de balança ativado para o relatório.")
        dados_mock = [
            {
                "Centro": "3010",
                "Operacao": "Balança 01",
                "PesoLiquido": 45200.5,
                "Material": "Cana Picada",
                "Status": "Processado",
            },
            {
                "Centro": "3010",
                "Operacao": "Balança 02",
                "PesoLiquido": 38900.0,
                "Material": "Cana Picada",
                "Status": "Processado",
            },
        ]
        return pd.DataFrame(dados_mock)

    logger.info("📊 Consultando dados via API OData do SAP S/4HANA...")
    response = requests.get(
        sap_url,
        auth=(os.getenv("SAP_USER", ""), os.getenv("SAP_PASSWORD", "")),
        timeout=30,
    )
    response.raise_for_status()
    return pd.DataFrame(response.json()["d"]["results"])


def enviar_relatorio_direto() -> bool:
    """Gera o relatório operacional e envia por e-mail de forma segura e resiliente."""
    nome_arquivo = "relatorio_automatico.xlsx"
    df: Optional[pd.DataFrame] = None

    try:
        sap_url = os.getenv("SAP_API_URL", "https://seu-ambiente-sap/sap/opu/odata/...")
        df = _obter_dados_relatorio(sap_url)
        df.to_excel(nome_arquivo, index=False)

        remetente = os.getenv("EMAIL_USER", "remetente@empresa.com")
        destinatario = os.getenv("EMAIL_DESTINATARIO", "destinatario@empresa.com")
        senha_app = os.getenv("EMAIL_PASSWORD", "senha_secreta")

        msg = EmailMessage()
        msg["Subject"] = "📊 Relatório Diário Automático - Indicadores Operacionais"
        msg["From"] = remetente
        msg["To"] = destinatario
        msg.set_content(
            f"Relatório gerado via integração SAP S/4HANA (Modo Resiliente/Mock).\n"
            f"Total de registros processados: {len(df)}"
        )

        with open(nome_arquivo, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=nome_arquivo,
            )

        logger.info("🚀 Conectando ao servidor SMTP para disparo...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)

        logger.info("Relatório enviado com sucesso! ✅")
        TOTAL_PESAGENS.labels(status="sucesso").inc()
        return True

    except Exception as e:
        ERROS_CRITICOS.inc()
        TOTAL_PESAGENS.labels(status="erro").inc()
        logger.error(f"❌ Erro crítico na integração ou envio: {e}")
        return False

    finally:
        if os.path.exists(nome_arquivo):
            try:
                os.remove(nome_arquivo)
            except OSError:
                pass


if __name__ == "__main__":
    sucesso = enviar_relatorio_direto()
    sys.exit(0 if sucesso else 1)
