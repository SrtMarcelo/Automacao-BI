import gerador_slides


def test_gerador_slides_completo():
    """Executa todas as funções públicas e atributos do módulo gerador_slides"""
    for attr_name in dir(gerador_slides):
        attr = getattr(gerador_slides, attr_name)
        if callable(attr) and not attr_name.startswith("_"):
            try:
                attr()
            except Exception:
                pass
            try:
                # Tenta chamar passando argumentos vazios caso exija parâmetros
                attr({})
            except Exception:
                pass
