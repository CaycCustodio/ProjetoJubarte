from decimal import Decimal
from typing import List, Dict
from finance_engine.core.math_utils import to_decimal, validate_positive, validate_not_zero

class FinancialCalculator:
    """Calculadora de Engenharia Financeira de Alta Precisão."""

    @staticmethod
    def juros_compostos(principal, taxa_mensal, meses, aporte_mensal=0) -> Dict:
        """
        Cálculo de Juros Compostos com Aportes Mensais.
        Fórmula: M = P(1 + i)^n + A * (((1 + i)^n - 1) / i)
        """
        P = to_decimal(principal)
        i = to_decimal(taxa_mensal)
        n = int(meses)
        A = to_decimal(aporte_mensal)

        validate_positive(P, "Montante inicial")
        validate_positive(i, "Taxa")
        validate_positive(n, "Tempo")

        # Ajuste da taxa (ex: 1.5% -> 0.015)
        taxa_dec = i / 100

        # Montante do Principal
        montante_principal = P * (1 + taxa_dec) ** n

        # Montante dos Aportes (Série de Pagamentos)
        if taxa_dec > 0:
            montante_aportes = A * (((1 + taxa_dec) ** n - 1) / taxa_dec)
        else:
            montante_aportes = A * n

        total = montante_principal + montante_aportes
        juros_ganhos = total - (P + (A * n))

        return {
            "montante_total": to_decimal(total, '0.01'),
            "total_investido": to_decimal(P + (A * n), '0.01'),
            "juros_ganhos": to_decimal(juros_ganhos, '0.01')
        }

    @staticmethod
    def tabela_sac(valor_financiado, taxa_anual, meses) -> List[Dict]:
        """Gera tabela de amortização Sistema de Amortização Constante."""
        V = to_decimal(valor_financiado)
        n = int(meses)
        i_anual = to_decimal(taxa_anual) / 100
        i_mensal = (1 + i_anual) ** to_decimal('0.0833333333') - 1 # (1+i)^(1/12)-1

        amortizacao = V / n
        saldo_devedor = V
        tabela = []

        for mes in range(1, n + 1):
            juros = saldo_devedor * i_mensal
            prestacao = amortizacao + juros
            saldo_devedor -= amortizacao
            
            tabela.append({
                "mes": mes,
                "prestacao": to_decimal(prestacao, '0.01'),
                "amortizacao": to_decimal(amortizacao, '0.01'),
                "juros": to_decimal(juros, '0.01'),
                "saldo_devedor": to_decimal(max(0, saldo_devedor), '0.01')
            })
        
        return tabela

    @staticmethod
    def tabela_price(valor_financiado, taxa_anual, meses) -> List[Dict]:
        """Gera tabela de amortização Sistema PRICE (Prestações Iguais)."""
        V = to_decimal(valor_financiado)
        n = int(meses)
        i_anual = to_decimal(taxa_anual) / 100
        i_mensal = (1 + i_anual) ** to_decimal('0.0833333333') - 1

        # Fórmula Prestação: PMT = V * [ (i * (1+i)^n) / ((1+i)^n - 1) ]
        fator = (1 + i_mensal) ** n
        prestacao = V * (i_mensal * fator) / (fator - 1)
        
        saldo_devedor = V
        tabela = []

        for mes in range(1, n + 1):
            juros = saldo_devedor * i_mensal
            amortizacao = prestacao - juros
            saldo_devedor -= amortizacao

            tabela.append({
                "mes": mes,
                "prestacao": to_decimal(prestacao, '0.01'),
                "amortizacao": to_decimal(amortizacao, '0.01'),
                "juros": to_decimal(juros, '0.01'),
                "saldo_devedor": to_decimal(max(0, saldo_devedor), '0.01')
            })

        return tabela

    @staticmethod
    def vpl(taxa_desconto, fluxos: List[float]) -> Decimal:
        """Calcula o Valor Presente Líquido."""
        i = to_decimal(taxa_desconto) / 100
        total = Decimal('0')
        for t, cf in enumerate(fluxos):
            total += to_decimal(cf) / ((1 + i) ** t)
        return to_decimal(total, '0.01')

    @staticmethod
    def tir(fluxos: List[float], estimativa=0.1) -> Decimal:
        """Calcula a Taxa Interna de Retorno usando Newton-Raphson approximation."""
        # Simplificação: Em um ambiente real usaríamos scipy.optimize.irr
        # Mas manteremos o core em pure Python/Decimal para precisão
        def npv(rate):
            return sum(to_decimal(cf) / ((1 + to_decimal(rate)) ** t) for t, cf in enumerate(fluxos))

        def d_npv(rate):
            return sum(to_decimal(-t * cf) / ((1 + to_decimal(rate)) ** (t + 1)) for t, cf in enumerate(fluxos))

        rate = to_decimal(estimativa)
        for _ in range(100):
            current_npv = npv(rate)
            if abs(current_npv) < 0.0001:
                return to_decimal(rate * 100, '0.0001')
            diff = d_npv(rate)
            if diff == 0: break
            rate = rate - (current_npv / diff)
        
        return to_decimal(rate * 100, '0.0001')
