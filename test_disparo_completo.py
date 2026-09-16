from unittest.mock import patch

from disparo_automatico import enviar_pesagem_sap_async


@patch("disparo_automatico.requests.post")
def test_enviar_pesagem_sap_async_sucesso(mock_post):
    # Simula uma resposta de sucesso da API/SAP
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "sucesso"}

    resultado = enviar_pesagem_sap_async({"id_pesagem": 123, "peso": 50000})
    assert resultado is not None
