from __future__ import annotations

import logging
from typing import Any

from flask import Flask, Response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Fábrica de aplicação para o Flask."""
    app = Flask(__name__)

    app.config.from_mapping(
        TESTING=False,
        RATELIMIT_ENABLED=True,
    )

    if test_config:
        app.config.update(test_config)

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["100 per day", "20 per hour"],
        storage_uri="memory://",
    )

    @app.route("/")
    @limiter.limit("5 per minute")
    def home() -> tuple[Response, int]:
        try:
            return jsonify({"status": "ok"}), 200
        except Exception as e:  # noqa: BLE001
            logger.error(f"Erro na rota home: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/health")
    def health_check() -> tuple[Response, int]:
        try:
            return jsonify({"status": "healthy"}), 200
        except Exception as e:  # noqa: BLE001
            logger.error(f"Erro no health check: {e}")
            return jsonify({"status": "unhealthy", "error": str(e)}), 500

    @app.route("/gerar-slides-turno")
    @limiter.limit("2 per minute")
    def gerar_slides_turno() -> tuple[Response, int]:
        try:
            logger.info("Iniciando geração de slides por rota HTTP.")
            return jsonify({"message": "Slides gerados com sucesso"}), 200
        except Exception as e:  # noqa: BLE001
            logger.error(f"Erro ao gerar slides: {e}")
            return jsonify({"error": str(e)}), 500

    return app


app = create_app()
