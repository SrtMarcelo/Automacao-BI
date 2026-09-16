from pptx import Presentation


def gerar_apresentacao_turno(dados_turno: dict) -> str:
    """
    Gera um arquivo PowerPoint com os dados do fechamento de turno.
    Se não houver um template, ele cria uma apresentação nova do zero.
    """
    prs = Presentation()

    # Adiciona um slide em branco ou com layout padrão
    slide_layout = prs.slide_layouts[0]  # 0 geralmente é o slide de título
    slide = prs.slides.add_slide(slide_layout)

    # Preenche o título e subtítulo se existirem no layout
    if len(slide.shapes.placeholders) > 0:
        titulo = slide.shapes.placeholders[0]
        titulo.text = f"Fechamento de Turno - {dados_turno.get('data', 'Hoje')}"

    if len(slide.shapes.placeholders) > 1:
        subtitulo = slide.shapes.placeholders[1]
        subtitulo.text = (
            f"Volume Total: {dados_turno.get('volume_total', '0')}\n"
            f"Eficiência: {dados_turno.get('eficiencia', '0')}%\n"
            f"Turno: {dados_turno.get('turno', 'N/A')}"
        )

    # Salva o arquivo gerado
    caminho_saida = "relatorio_turno.pptx"
    prs.save(caminho_saida)
    return caminho_saida
