import pytest
import pandas as pd
from relatorio_operacional_sap import FechamentoTurnoService

def test_consolidar_turno_com_dados():
    dados = [
        {"fornecedor": "Fazenda Boa Vista", "frotista": "Transportes Alfa", "tipo_produto": "RB966918", "peso_bruto": 50000.0, "tara": 15000.0},
        {"fornecedor": "Fazenda Boa Vista", "frotista": "Transportes Alfa", "tipo_produto": "RB966918", "peso_bruto": 48000.0, "tara": 14500.0},
        {"fornecedor": "Agropecuária Santa Rita", "frotista": "TransBeta", "tipo_produto": "CTC4", "peso_bruto": 52000.0, "tara": 16000.0}
    ]
    
    service = FechamentoTurnoService(dados)
    resultado = service.consolidar_turno()
    
    assert not resultado["por_fornecedor"].empty
    assert not resultado["por_frotista"].empty
    assert not resultado["por_variedade"].empty
    
    # Valida se o peso líquido foi calculado corretamente para a Fazenda Boa Vista (35000 + 33500 = 68500)
    df_forn = resultado["por_fornecedor"]
    total_boa_vista = df_forn.loc[df_forn["fornecedor"] == "Fazenda Boa Vista", "peso_liquido_total"].values[0]
    assert total_boa_vista == 68500.0

def test_consolidar_turno_vazio():
    service = FechamentoTurnoService([])
    resultado = service.consolidar_turno()
    
    assert resultado["por_fornecedor"].empty
    assert resultado["por_frotista"].empty
    assert resultado["por_variedade"].empty

def test_exportar_para_excel(tmp_path):
    dados = [
        {"fornecedor": "Teste", "frotista": "Teste", "tipo_produto": "Cana", "peso_bruto": 40000.0, "tara": 10000.0}
    ]
    arquivo_excel = tmp_path / "saida_teste.xlsx"
    
    service = FechamentoTurnoService(dados)
    caminho = service.exportar_para_excel(str(arquivo_excel))
    
    assert caminho == str(arquivo_excel)
    # Verifica se o arquivo foi gerado e pode ser lido de volta
    df_lido = pd.read_excel(caminho, sheet_name="por_fornecedor")
    assert not df_lido.empty