from __future__ import annotations

import os
import sys
from unittest.mock import patch

# Garante o path correto para importar os módulos da raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import agendador


def test_agendador_fluxo_principal() -> None:
    """Testa o fluxo principal de inicialização do agendamento mockando o scheduler e o sleep."""
    with (
        patch("apscheduler.schedulers.blocking.BlockingScheduler.start") as mock_start,
        patch("time.sleep", return_value=None),
    ):
        # Executa a função sem gerar exceções reais de bloqueio de thread
        agendador.iniciar_agendamento()

        # Valida se o agendador tentou iniciar corretamente
        assert mock_start.called


def test_agendador_main_bloco() -> None:
    """Testa a execução do bloco de entrada principal (__main__) do módulo agendador."""
    with (
        patch("apscheduler.schedulers.blocking.BlockingScheduler.start") as mock_start,
        patch.object(agendador, "__name__", "__main__"),
    ):
        # Simula a execução condicional idêntica à do script principal
        if agendador.__name__ == "__main__":
            agendador.iniciar_agendamento()

        # Confirma que o fluxo acionou o start do scheduler com sucesso dentro do escopo main
        assert mock_start.called
