import requests

try:
    # O site httpbin.org/delay/3 simula uma resposta que demora 3 segundos,
    # mas o nosso timeout está fixo em 1.0 segundo para forçar o corte.
    response = requests.get("https://httpbin.org/delay/3", timeout=1.0)
    print("Sucesso:", response.status_code)
except requests.exceptions.Timeout:
    print(
        "Sucesso no teste! O timeout rígido bloqueou a requisição lenta com segurança."
    )
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
