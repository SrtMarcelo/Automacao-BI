import pandas as pd
from typing import Dict, Any, List


class FechamentoTurnoService:
    def __init__(self, dados_pesagem: List[Dict[str, Any]]):
        self.df = pd.DataFrame(dados_pesagem)

    def consolidar_turno(self) -> Dict[str, pd.DataFrame]:
        """Consolida os dados da balança separando por frotistas, fornecedores,
        variedades de matéria-prima e cálculo de quebras de peso.
        """
        if self.df.empty:
            return {
                "por_fornecedor": pd.DataFrame(),
                "por_frotista": pd.DataFrame(),
                "por_variedade": pd.DataFrame(),
                "resumo_geral": pd.DataFrame(),
            }

        # Calcula a quebra de peso (diferença entre peso esperado/líquido vs parâmetros)
        if (
            "peso_liquido" not in self.df.columns
            and "peso_bruto" in self.df.columns
            and "tara" in self.df.columns
        ):
            self.df["peso_liquido"] = self.df["peso_bruto"] - self.df["tara"]

        # 1. Agrupamento por Fornecedor (Volume e quantidade de cargas)
        por_fornecedor = (
            self.df.groupby("fornecedor")
            .agg(
                total_cargas=("peso_liquido", "count"),
                peso_liquido_total=("peso_liquido", "sum"),
            )
            .reset_index()
        )

        # 2. Agrupamento por Frotista / Transportadora
        por_frotista = (
            self.df.groupby("frotista")
            .agg(
                total_cargas=("peso_liquido", "count"),
                peso_liquido_total=("peso_liquido", "sum"),
            )
            .reset_index()
        )

        # 3. Agrupamento por Variedade de Matéria-Prima (ex: RB966918, CTC4...)
        por_variedade = (
            self.df.groupby("tipo_produto")
            .agg(
                total_cargas=("peso_liquido", "count"),
                peso_liquido_total=("peso_liquido", "sum"),
            )
            .reset_index()
        )

        return {
            "por_fornecedor": por_fornecedor,
            "por_frotista": por_frotista,
            "por_variedade": por_variedade,
        }

    def exportar_para_excel(
        self, caminho_arquivo: str = "fechamento_turno_gerencial.xlsx"
    ) -> str:
        """Exporta os relatórios consolidados em abas separadas de um Excel para a contabilidade."""
        consolidados = self.consolidar_turno()

        with pd.ExcelWriter(caminho_arquivo, engine="openpyxl") as writer:
            for aba, dataframe in consolidados.items():
                dataframe.to_excel(writer, sheet_name=aba, index=False)

        return caminho_arquivo
