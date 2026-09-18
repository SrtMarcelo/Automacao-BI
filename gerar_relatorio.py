import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

# 1. Criar o arquivo Workbook do Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Relatório Industrial"

# 2. Cabeçalho principal com Verde Corporativo do Excel
ws.append(["CENTRO DE CONTROLE INDUSTRIAL (CCI) - RELATÓRIO OPERACIONAL"])
ws.merge_cells("A1:H1")

title_cell = ws["A1"]
title_cell.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
title_cell.fill = PatternFill(start_color="107C41", end_color="107C41", fill_type="solid")  # Verde Corporativo
title_cell.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 30

# Linha em branco de respiro
ws.append([])

# 3. Cabeçalhos da Tabela de Dados (Tom de verde harmonioso)
headers = ["Data / Hora", "Setor", "Identificação", "Métrica 1", "Métrica 2", "Origem", "Destino", "Status Executivo"]
ws.append(headers)

header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="1F6E3B", end_color="1F6E3B", fill_type="solid")  # Verde escuro elegante
header_alignment = Alignment(horizontal="center", vertical="center")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

for col_idx in range(1, len(headers) + 1):
    cell = ws.cell(row=3, column=col_idx)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_alignment
    cell.border = thin_border
ws.row_dimensions[3].height = 25

# 4. Inserção dos Dados Reais da Fábrica
rows_data = [
    ["15/09/2026 09:15", "Balança", "KAT-882048.500", 15.2, 33.3, "Boa Vista", "Linha Norte", "Concluído"],
    ["15/09/2026 10:40", "Moenda", "OXY-419250.100", 16.0, 34.1, "São Matheus", "Linha Sul", "Em Operação"],
    ["15/09/2026 11:55", "Caldeira", "BRZ-331047.000", 14.8, 32.2, "Boa Vista", "Linha Norte", "Concluído"]
]

for row_idx, row_data in enumerate(rows_data, start=4):
    ws.append(row_data)
    ws.row_dimensions[row_idx].height = 20
    for col_idx in range(1, len(row_data) + 1):
        cell = ws.cell(row=row_idx, column=col_idx)
        cell.font = Font(name="Calibri", size=11)
        cell.border = thin_border
        if col_idx in [4, 5]:  
            cell.number_format = '#,##0.0'
            cell.alignment = Alignment(horizontal="right", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# 5. Ajustar largura automática das colunas
for col in ws.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws.column_dimensions[col_letter].width = max(max_len + 4, 15)

# 6. Criar e posicionar o Gráfico de Colunas 3D
chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "Comparativo de Métricas por Operação (CCI)"
chart.y_axis.title = "Valores (kg)"
chart.x_axis.title = "Setor"
chart.grouping = "clustered"
chart.view3d = True  

data_ref = Reference(ws, min_col=4, min_row=3, max_col=5, max_row=6)
cats_ref = Reference(ws, min_col=2, min_row=4, max_row=6)
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)

chart.width = 16
chart.height = 10

ws.add_chart(chart, "J3")

# 7. Salvando com a extensão correta (.xlsx) para abrir limpo no Excel
wb.save("Bioaroeira_Relatorio_Excel_BALANCA.xlsx")
print("Relatório corporativo gerado com sucesso!")