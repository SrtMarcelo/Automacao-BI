import re

def validar_modulo_11_chave_nfe(chave_acesso: str) -> bool:
    """
    Valida a chave de acesso da NF-e (44 dígitos) utilizando o algoritmo Módulo 11.
    O último dígito da chave é o dígito verificador.
    """
    # Remove qualquer caractere que não seja número
    chave = re.sub(r'\D', '', chave_acesso)

    if len(chave) != 44:
        return False

    # Os primeiros 43 dígitos compõem a base
    base = chave[:43]
    digito_informado = int(chave[43])

    # Pesos do Módulo 11 variam de 2 a 9 da direita para a esquerda
    soma = 0
    peso = 2

    for char in reversed(base):
        soma += int(char) * peso
        peso += 1
        if peso > 9:
            peso = 2

    resto = soma % 11
    digito_calculado = 0 if resto == 0 or resto == 1 else 11 - resto

    return digito_calculado == digito_informado


def validar_tolerancia_peso(peso_fiscal: float, peso_balanca: float, tolerancia_percentual: float = 1.0) -> dict:
    """
    Compara o peso líquido declarado na nota fiscal com o peso aferido na balanca física.
    Permite uma tolerância percentual configurável (padrão: 1.0%).
    """
    if peso_fiscal <= 0 or peso_balanca <= 0:
        return {
            "status": "ERRO",
            "diferenca": 0.0,
            "diferenca_percentual": 0.0,
            "mensagem": "Pesos inválidos informados para validação."
        }

    diferenca = peso_balanca - peso_fiscal
    diferenca_percentual = (abs(diferenca) / peso_fiscal) * 100

    if diferenca_percentual <= tolerancia_percentual:
        return {
            "status": "APROVADO",
            "diferenca": round(diferenca, 2),
            "diferenca_percentual": round(diferenca_percentual, 2),
            "mensagem": "Peso dentro da tolerância fiscal permitida."
        }
    else:
        return {
            "status": "DIVERGENCIA_CRITICA",
            "diferenca": round(diferenca, 2),
            "diferenca_percentual": round(diferenca_percentual, 2),
            "mensagem": f"Divergência de peso superior à tolerância de {tolerancia_percentual}%."
        }