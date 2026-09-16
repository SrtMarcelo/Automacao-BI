from app import app

if __name__ == "__main__":
  from waitress import serve

  print("Servidor profissional rodando na porta 5000...")
  serve(app, host="127.0.0.1", port=5000)