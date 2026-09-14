import re

class RegraFiscalError(Exception):
    pass

def validar_nota_fiscal_produtor(chave_acesso: str, peso_bruto: float, tara: float) -> float:
    """Valida a chave de acesso da NF e a integridade da pesagem de cana/subprodutos."""
    if not chave_acesso or not re.match(r'^\d{44}$', chave_acesso):
        raise RegraFiscalError("Chave de acesso da Nota Fiscal inválida: deve conter exatamente 44 dígitos.")
    
    if peso_bruto <= tara:
        raise RegraFiscalError("Peso bruto não pode ser menor ou igual à tara do veículo.")
    
    peso_liquido = peso_bruto - tara
    if peso_liquido <= 0:
        raise RegraFiscalError("Peso líquido calculado é inválido para fins fiscais.")
        
    return round(peso_liquido, 2)