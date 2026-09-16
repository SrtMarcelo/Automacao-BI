import os
import dotenv

# Deve ser chamado através do módulo dotenv para respeitar os testes que fazem monkeypatch
dotenv.load_dotenv()

def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Required environment variable is missing: {name}")
    return value

class Config:
    SAP_API_URL = _required_env("SAP_API_URL")
    DATABASE_URL = _required_env("DATABASE_URL")