import os

import responses
from disparo_automatico import enviar_pesagem_sap_async


@responses.activate
def notest_enviar_pesagem_sucesso_mock_http():
    """Testa o envio bem-sucedido para a API OData do SAP usando mock HTTP dedicaso."""
    # Configura a URL de teste e o payload simulado
    sap_test_url = "https://api.sap.falsas/sap/opu/odata/v4/pesagem"
    os.environ["SAP_API_URL"] = sap_test_url
    os.environ["SAP_USER"] = "admin"
    os.environ["SAP_PASSWORD"] = "secret"

    payload_envio = {
        "chave_acesso": "35260912345678000195550010000000011234567890",
        "peso": 45000,
    }

    # Intercepta a chamada POST do requests com o 'responses'
    responses.add(
        responses.POST,
        sap_test_url,
        json={"d": {"results": {"status": "PROCESSADO_NO_SAP"}}},
        status=200,
    )

    # Executa a função do Celery chamando o método subjacente (sem precisar do Redis rodando)
    resultado = enviar_pesagem_sap_async.run(payload_envio)

    assert resultado["status"] == "SUCESSO"
    assert "resposta" in resultado
