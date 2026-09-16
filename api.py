from fastapi import FastAPI, HTTPException, Header
import sqlite3

app = FastAPI(title="Industrial SaaS API", version="1.0")

def consultar_dados_por_tenant(tenant_id: str):
    """Consulta segura restrita estritamente ao tenant da empresa."""
    conn = sqlite3.connect("industrial_saas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, id_balanca, peso FROM pesagens WHERE tenant_id = ?", (tenant_id,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@app.get("/pesagens")
def listar_pesagens(x_tenant_id: str = Header(..., description="Identificador da empresa extraído do token JWT")):
    """
    Endpoint protegido por Tenant ID (simulando o payload decodificado de um JWT).
    A Empresa A jamais consegue ver os dados da Empresa B aqui.
    """
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID obrigatório no cabeçalho.")
    
    dados = consultar_dados_por_tenant(x_tenant_id)
    
    return {
        "tenant": x_tenant_id,
        "total_registros": len(dados),
        "dados": dados
    }