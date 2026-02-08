from decimal import Decimal
from typing import Dict
from finance_engine.core.math_utils import to_decimal, validate_not_zero

class BusinessAnalytics:
    """Indicadores de Performance e Precificação Empresarial."""

    @staticmethod
    def calcular_ebitda(receita_liquida, custos_variaveis, despesas_fixas) -> Decimal:
        """Cálculo simplificado do EBITDA (LAJIDA)."""
        receita = to_decimal(receita_liquida)
        custos = to_decimal(custos_variaveis)
        despesas = to_decimal(despesas_fixas)
        
        ebitda = receita - custos - despesas
        return to_decimal(ebitda, '0.01')

    @staticmethod
    def ponto_equilibrio(custos_fixos, margem_contribuicao_percentual) -> Decimal:
        """
        Calcula o Break-even Point (Ponto de Equilíbrio).
        Receita Necessária = Custos Fixos / Margem de Contribuição %
        """
        fixos = to_decimal(custos_fixos)
        margem = to_decimal(margem_contribuicao_percentual) / 100
        
        validate_not_zero(margem, "Margem de contribuição")
        
        be_point = fixos / margem
        return to_decimal(be_point, '0.01')

    @staticmethod
    def precificacao_markup(custo_unitario, impostos_venda_perc, despesas_venda_perc, margem_lucro_perc) -> Dict:
        """
        Cálculo de Preço de Venda via Markup Divisor.
        Fórmula Preço = Custo / (1 - (Impostos + Despesas + Lucro))
        """
        custo = to_decimal(custo_unitario)
        imp = to_decimal(impostos_venda_perc) / 100
        desp = to_decimal(despesas_venda_perc) / 100
        lucro = to_decimal(margem_lucro_perc) / 100
        
        divisor = 1 - (imp + desp + lucro)
        
        if divisor <= 0:
            raise ValueError("As margens e impostos somados igualam ou superam 100%, impossibilitando o lucro.")
            
        preco_venda = custo / divisor
        markup_fator = 1 / divisor
        
        return {
            "preco_venda": to_decimal(preco_venda, '0.01'),
            "markup_fator": to_decimal(markup_fator, '0.0000'),
            "lucro_nominal": to_decimal(preco_venda * lucro, '0.01')
        }
