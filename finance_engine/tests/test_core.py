import pytest
from decimal import Decimal
from finance_engine.modules.payroll import PayrollManager
from finance_engine.modules.calculator import FinancialCalculator

def test_isencao_irrf_2026():
    """Valida se salários até R$ 5.000,00 estão isentos de IRRF em 2026."""
    resultado = PayrollManager.calcular_folha_detalhada(5000)
    assert resultado['desconto_irrf'] == Decimal('0.00')

def test_inss_progressivo_2026():
    """Valida o cálculo do INSS na primeira faixa de 2026."""
    # Salário Mínimo 2026: R$ 1.621,00 * 7.5% = 121.575 (121.58)
    inss = PayrollManager.calcular_inss(Decimal('1621.00'))
    assert inss == Decimal('121.58')

def test_juros_compostos_precisao():
    """Valida a precisão da calculadora financeira."""
    res = FinancialCalculator.juros_compostos(1000, 10, 2) # 1000 * 1.1 * 1.1 = 1210
    assert res['montante_total'] == Decimal('1210.00')

def test_divisao_por_zero_protecao():
    """Garante que validações de segurança funcionam."""
    from finance_engine.modules.business import BusinessAnalytics
    with pytest.raises(ValueError, match="Margem de contribuição não pode ser zero"):
        BusinessAnalytics.ponto_equilibrio(1000, 0)
