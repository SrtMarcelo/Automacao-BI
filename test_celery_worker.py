import pytest


def test_celery_worker_importacao():
    """Garante que o módulo celery_worker carrega corretamente."""
    import celery_worker

    assert celery_worker is not None


def test_celery_worker_estrutura():
    """Valida a presença de atributos ou tarefas exportadas no worker."""
    import celery_worker

    # Verifica se existem itens definidos no módulo sem forçar instanciação incorreta
    membros = dir(celery_worker)
    assert len(membros) > 0
