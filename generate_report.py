import pandas as pd
from decimal import Decimal
from finance_engine.modules.calculator import FinancialCalculator
from finance_engine.modules.payroll import PayrollManager

def generate_full_report(salary=8000, loan_value=120000, months=12):
    print(f"--- GERANDO RELATÓRIO FINANCEIRO DETALHADO (2026) ---")
    
    # 1. CUSTO EMPRESA DETALHADO
    custo = PayrollManager.custo_total_empresa(salary)
    folha = PayrollManager.calcular_folha_detalhada(salary)
    
    # Criando DataFrame para detalhamento de custos
    df_custos = pd.DataFrame([
        {"Item": "Salário Bruto", "Valor (R$)": float(salary), "Tipo": "Provento"},
        {"Item": "INSS (Funcionário)", "Valor (R$)": -float(folha['desconto_inss']), "Tipo": "Desconto"},
        {"Item": "IRRF (Funcionário)", "Valor (R$)": -float(folha['desconto_irrf']), "Tipo": "Desconto"},
        {"Item": "Salário Líquido (Recebido)", "Valor (R$)": float(folha['salario_liquido']), "Tipo": "Resultado"},
        {"Item": "---", "Valor (R$)": 0, "Tipo": "---"},
        {"Item": "FGTS (8%)", "Valor (R$)": float(folha['fgts_recolhido']), "Tipo": "Encargo Empresa"},
        {"Item": "Provisão Férias/13º", "Valor (R$)": float(custo['provisoes_ferias_13']), "Tipo": "Encargo Empresa"},
        {"Item": "Encargos Sociais (CPP/RAT/S)", "Valor (R$)": float(custo['encargos_sociais']), "Tipo": "Encargo Empresa"},
        {"Item": "CUSTO TOTAL MENSAL", "Valor (R$)": float(custo['custo_total_mensal']), "Tipo": "TOTAL EMPRESA"}
    ])

    # 2. AMORTIZAÇÃO COMPARATIVA
    sac = FinancialCalculator.tabela_sac(loan_value, 12, months)
    price = FinancialCalculator.tabela_price(loan_value, 12, months)
    
    df_sac = pd.DataFrame(sac)
    df_price = pd.DataFrame(price)
    
    for df in [df_sac, df_price]:
        for col in ['prestacao', 'amortizacao', 'juros', 'saldo_devedor']:
            df[col] = df[col].apply(float)

    # 3. EXPORTAR PARA EXCEL MULTI-PÁGINA
    report_name = "Relatorio_Financeiro_Jubarte.xlsx"
    with pd.ExcelWriter(report_name) as writer:
        df_custos.to_excel(writer, sheet_name='Custo Funcionario', index=False)
        df_sac.to_excel(writer, sheet_name='Amortizacao SAC', index=False)
        df_price.to_excel(writer, sheet_name='Amortizacao PRICE', index=False)
    
    print(f"✅ Relatório '{report_name}' gerado com sucesso!")
    return report_name

if __name__ == "__main__":
    generate_full_report()
