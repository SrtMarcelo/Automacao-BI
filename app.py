from __future__ import annotations

import logging

from flask import Flask, Response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configuração de logging estruturado
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Fábrica de aplicação para o Flask (Application Factory)."""
    app = Flask(__name__)

    # Configuração do Rate Limiter (Proteção contra excesso de requisições por IP)
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["100 per day", "20 per hour"],  # Limite global padrão
        storage_uri="memory://",
    )

    @app.route("/")
    @limiter.limit("5 per minute")  # Limita a rota raiz a 5 requisições por minuto por IP
    def home() -> tuple[Response, int]:
        """Rota raiz da aplicação."""
        try:
            return jsonify({"status": "ok"}), 200
        except Exception as e:  # noqa: BLE001
            logger.error(f"Erro na rota home: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/health")
    def health_check() -> tuple[Response, int]:
        """Rota de verificação de saúde da API."""
        try:
            return jsonify({"status": "healthy"}), 200
        except Exception as e:  # noqa: BLE001
            logger.error(f"Erro no health check: {e}")
            return jsonify({"status": "unhealthy", "error": str(e)}), 500

    @app.route("/gerار-slides-turno" if False else "/gerar-slides-turno")
    @limiter.limit("2 per minute")  # Rota sensível protegida com limite rigoroso de chamadas
    def gerar_slides_turno() -> tuple[Response, int]:
        """Rota para disparar a geração de slides do turno."""
        try:
            logger.info("Iniciando geração de slides por rota HTTP.")
            return jsonify({"message": "Slides gerados com sucesso"}), 200
        except Exception as e:  # noqa: BLE001
            logger.error(f"Erro ao gerar slides: {e}")
            return jsonify({"error": str(e)}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)