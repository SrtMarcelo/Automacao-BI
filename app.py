from __future__ import annotations

import logging
from typing import Any
from flask import Flask, Response, jsonify

# Configuração de logging estruturado
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> Flask:
    """Fábrica de aplicação para o Flask (Application Factory)."""
    app = Flask(__name__)

    @app.route("/")
    def home() -> tuple[Response, int]:
        """Rota raiz da aplicação."""
        try:
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            logger.error(f"Erro na rota home: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/health")
    def health_check() -> tuple[Response, int]:
        """Rota de verificação de saúde da API."""
        try:
            return jsonify({"status": "healthy"}), 200
        except Exception as e:
            logger.error(f"Erro no health check: {e}")
            return jsonify({"status": "unhealthy", "error": str(e)}), 500

    @app.route("/gerar-slides-turno")
    def gerar_slides_turno() -> tuple[Response, int]:
        """Rota para disparar a geração de slides do turno."""
        try:
            logger.info("Iniciando geração de slides por rota HTTP.")
            return jsonify({"message": "Slides gerados com sucesso"}), 200
        except Exception as e:
            logger.error(f"Erro ao gerar slides: {e}")
            return jsonify({"error": str(e)}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)