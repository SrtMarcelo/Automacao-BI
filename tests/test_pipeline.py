from datetime import datetime
import os
import sys
import pandas as pd
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from integracao_sap import SAPDataPipeline


@pytest.fixture
def pipeline_instance():
  os.environ["DATABASE_URL"] = "sqlite:///test_bi_staging.db"
  pipeline = SAPDataPipeline()
  yield pipeline

  # Fecha todas as conexões abertas da engine antes de remover o arquivo
  if hasattr(pipeline, "engine") and pipeline.engine:
    pipeline.engine.dispose()

  # Remove o banco de testes com segurança
  if os.path.exists("test_bi_staging.db"):
    try:
      os.remove("test_bi_staging.db")
    except PermissionError:
      pass

def test_extract_sap_mock_data(pipeline_instance):
  df = pipeline_instance.extract_sap_data()
  assert isinstance(df, pd.DataFrame)
  assert not df.empty
  assert "Centro" in df.columns
  assert "Operacao" in df.columns
  assert "PesoLiquido" in df.columns
  assert len(df) == 2


def test_load_to_staging_idempotency(pipeline_instance):
  df_mock = pd.DataFrame([{
      "Centro": "3010",
      "Operacao": "Balança 01",
      "PesoLiquido": 50000.0,
      "Material": "Cana Teste",
      "Status": "Processado",
  }])
  pipeline_instance.load_to_staging(df_mock)

  df_mock_atualizado = pd.DataFrame([{
      "Centro": "3010",
      "Operacao": "Balança 01",
      "PesoLiquido": 50500.0,
      "Material": "Cana Teste",
      "Status": "Atualizado",
  }])
  pipeline_instance.load_to_staging(df_mock_atualizado)

  with pipeline_instance.engine.connect() as conn:
    resultado = conn.execute(
        pipeline_instance.staging_table.select()
    ).fetchall()
    assert len(resultado) == 1
    assert resultado[0].PesoLiquido == 50500.0
    assert resultado[0].Status == "Atualizado"
