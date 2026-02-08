from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from fastapi.responses import FileResponse
import os
from finance_engine.modules.payroll import PayrollManager
from finance_engine.modules.calculator import FinancialCalculator
from finance_engine.modules.business import BusinessAnalytics
from finance_engine.database.session import SessionLocal, init_db
from finance_engine.database.models import SimulacaoFinanceira
from generate_report import generate_full_report

app = FastAPI(title="Jubarte Finance API")

# Configuração de CORS para permitir que o dashboard (port 8080) acesse o backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o banco de dados
init_db()

# Modelos Pydantic para validação de entrada
class PayrollInput(BaseModel):
    salario_bruto: float
    dependentes: int = 0
    beneficios: float = 0
    outros_descontos: float = 0

class AmortizationInput(BaseModel):
    valor: float
    taxa_anual: float
    meses: int

# Endpoints
@app.post("/calculate/payroll")
def calculate_payroll(data: PayrollInput):
    try:
        resultado = PayrollManager.calcular_folha_detalhada(
            data.salario_bruto, 
            dependentes=data.dependentes,
            beneficios=data.beneficios,
            outros_descontos=data.outros_descontos
        )
        # Salva no banco de dados automaticamente
        db = SessionLocal()
        simulacao = SimulacaoFinanceira(
            tipo="PAYROLL_2026",
            parametros_entrada=data.model_dump(),
            resultados={k: str(v) for k, v in resultado.items()},
            usuario_ref="DASHBOARD_USER"
        )
        db.add(simulacao)
        db.commit()
        db.refresh(simulacao)
        db.close()
        
        return {**resultado, "id": simulacao.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/calculate/business")
def get_business_indicators(data: PayrollInput):
    # Calcula custo empresa e break-even básico baseado no salário
    custo = PayrollManager.custo_total_empresa(data.salario_bruto)
    # Exemplo: Break-even fixo para demonstração
    be = BusinessAnalytics.ponto_equilibrio(25000, 40)
    
    return {
        "custo_empresa": custo,
        "break_even": be,
        "margem": 40
    }

@app.post("/calculate/investment_10years")
def calculate_investment_10years(data: PayrollInput):
    try:
        # Primeiro calculamos o salário líquido real para 2026
        folha = PayrollManager.calcular_folha_detalhada(
            data.salario_bruto, 
            dependentes=data.dependentes
        )
        salario_liquido = float(folha['salario_liquido'])
        
        # Premissas corrigidas: 20% do LÍQUIDO, taxa de 0.8% a.m.
        aporte_mensal = salario_liquido * 0.20
        taxa_mensal = 0.008 
        
        evolucao_anual = []
        patrimonio_total = 0
        total_investido_acumulado = 0
        
        for ano in range(1, 11):
            for mes in range(12):
                total_investido_acumulado += aporte_mensal
                patrimonio_total = (patrimonio_total + aporte_mensal) * (1 + taxa_mensal)
            
            juros_gerados_acumulados = patrimonio_total - total_investido_acumulado
            evolucao_anual.append({
                "ano": ano,
                "patrimonio_total": round(patrimonio_total, 2),
                "total_investido": round(total_investido_acumulado, 2),
                "juros_gerados": round(juros_gerados_acumulados, 2)
            })
            
        return evolucao_anual
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/simulations")
def list_simulations():
    db = SessionLocal()
    sims = db.query(SimulacaoFinanceira).order_by(SimulacaoFinanceira.data_criacao.desc()).limit(10).all()
    db.close()
    return sims

@app.post("/reports/generate")
def get_report(data: PayrollInput):
    try:
        filename = generate_full_report(salary=data.salario_bruto)
        return FileResponse(
            path=filename, 
            filename="Relatorio_Jubarte_Final.xlsx",
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
