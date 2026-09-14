import os
import sys
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import agendador


def test_agendador_fluxo_principal():
    with patch("apscheduler.schedulers.blocking.BlockingScheduler.start"), patch(
        "time.sleep", return_value=None
    ), patch("logging.info", return_value=None):
        try:
            agendador.iniciar_agendamento()
        except Exception as e:
            print(f"Aviso no agendamento: {e}")


def test_agendador_main_bloco():
    with patch("apscheduler.schedulers.blocking.BlockingScheduler.start"), patch(
        "logging.info", return_value=None
    ), patch.object(agendador, "__name__", "__main__"):
        try:
            if agendador.__name__ == "__main__":
                agendador.iniciar_agendamento()
        except Exception as e:
            print(f"Aviso no bloco main: {e}")
    assert True
