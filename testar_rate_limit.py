from app import create_app

# Cria a aplicação usando a sua factory
app = create_app()
client = app.test_client()

print("Iniciando testes de Rate Limiting...")
for i in range(3):
    response = client.get("/gerar-slides-turno")
    print(f"Tentativa {i+1}: Status {response.status_code}")