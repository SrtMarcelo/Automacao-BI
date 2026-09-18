import os
from gerar_relatorio import wb

def test_gerar_relatorio_excel():
    # Garante que o workbook foi criado corretamente e possui o título certo
    ws = wb.active
    assert ws.title == "Relatório Industrial"
    assert ws["A1"].value == "CENTRO DE CONTROLE INDUSTRIAL (CCI) - RELATÓRIO OPERACIONAL"
    
    # Testa salvar o arquivo temporariamente para cobrir as linhas de salvamento
    output_path = "test_output_relatorio.xlsx"
    wb.save(output_path)
    assert os.path.exists(output_path)
    
    # Limpeza do arquivo de teste
    if os.path.exists(output_path):
        os.remove(output_path)