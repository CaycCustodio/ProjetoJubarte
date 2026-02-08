import json
from finance_engine.modules.calculator import FinancialCalculator
from finance_engine.modules.payroll import PayrollManager
from finance_engine.modules.business import BusinessAnalytics
from finance_engine.database.session import init_db, SessionLocal
from finance_engine.database.models import SimulacaoFinanceira

def main():
    print("--- SIMULAÇÃO DE NÚCLEO FINANCEIRO (VERSÃO DB) ---")
    
    # Inicializa o banco de dados (Cria tabelas)
    init_db()
    db = SessionLocal()

    # 1. Exemplo de Folha de Pagamento (Salário de R$ 5.000,00)
    print("\n[1] Cálculo de Folha de Pagamento (Bruto: R$ 5.000,00 - 2026)")
    resultado_folha = PayrollManager.calcular_folha_detalhada(5000, dependentes=1)
    
    # Salvando no banco de dados para persistência
    nova_simulacao = SimulacaoFinanceira(
        tipo="PAYROLL_2026",
        parametros_entrada={"bruto": 5000, "dep": 1},
        resultados={k: str(v) for k, v in resultado_folha.items()},
        usuario_ref="ADMIN"
    )
    db.add(nova_simulacao)
    db.commit()
    print(f"-> Simulação salva no DB com ID: {nova_simulacao.id}")
    
    print(json.dumps({str(k): str(v) for k, v in resultado_folha.items()}, indent=4, ensure_ascii=False))

    # 2. Exemplo de Custo Real Empresa
    print("\n[2] Custo Real de um Funcionário (Bruto: R$ 5.000,00)")
    custo_empresa = PayrollManager.custo_total_empresa(5000)
    print(f"Custo Total Mensal: R$ {custo_empresa['custo_total_mensal']}")
    print(f"Percentual sobre bruto: {custo_empresa['percentual_sobre_bruto']}%")

    # 3. Comparativo Amortização (R$ 100.000,00 em 12 meses)
    print("\n[3] Comparativo Amortização (R$ 100.000,00 / 12 meses / 12% a.a.)")
    print("Primeira Prestação SAC:", FinancialCalculator.tabela_sac(100000, 12, 12)[0]['prestacao'])
    print("Prestação PRICE:", FinancialCalculator.tabela_price(100000, 12, 12)[0]['prestacao'])

    db.close()

if __name__ == "__main__":
    main()
