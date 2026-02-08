from decimal import Decimal
from typing import Dict
from finance_engine.core.math_utils import to_decimal

class PayrollManager:
    """Gestor de Capital Humano - Padrão CLT Brasileiro (Projeção 2026)."""

    # Projeções para 2026
    # Fonte: Reforma da Renda (Lei 15.270/2025) e reajustes INPC
    TABELA_INSS = [
        (to_decimal('1621.00'), to_decimal('0.075'), Decimal('0')),
        (to_decimal('2902.84'), to_decimal('0.09'), Decimal('0')),
        (to_decimal('4354.27'), to_decimal('0.12'), Decimal('0')),
        (to_decimal('8475.55'), to_decimal('0.14'), Decimal('0')),
    ]
    TETO_INSS = to_decimal('8475.55')

    # IRRF 2026: Isenção até R$ 5.000,00
    # Nota: O governo utiliza redutores para bandas intermediárias (5k a 7.3k)
    # Implementação baseada na isenção total de 5k
    TABELA_IRRF = [
        (to_decimal('5000.00'), to_decimal('0'), Decimal('0')),
        (to_decimal('7350.00'), to_decimal('0.15'), to_decimal('750.00')), # Estimativa de redutor para transição
        (Decimal('inf'), to_decimal('0.275'), to_decimal('896.00')),
    ]
    DEDUCAO_DEPENDENTE = to_decimal('189.59')

    @classmethod
    def calcular_inss(cls, salario_bruto: Decimal) -> Decimal:
        """Cálculo progressivo do INSS."""
        valor = min(salario_bruto, cls.TETO_INSS)
        imposto = Decimal('0')
        anterior = Decimal('0')

        # Implementação da progressividade por faixas
        faixas = [
            (to_decimal('0'), to_decimal('1621.00'), to_decimal('0.075')),
            (to_decimal('1621.01'), to_decimal('2902.84'), to_decimal('0.09')),
            (to_decimal('2902.85'), to_decimal('4354.27'), to_decimal('0.12')),
            (to_decimal('4354.28'), to_decimal('8475.55'), to_decimal('0.14'))
        ]

        for inicio, fim, taxa in faixas:
            if valor > inicio:
                base = min(valor, fim) - inicio
                imposto += to_decimal(base) * to_decimal(taxa)
            else:
                break
        
        return to_decimal(imposto, '0.01')

    @classmethod
    def calcular_irrf(cls, base_irrf: Decimal) -> Decimal:
        """Cálculo do IRRF com base na tabela progressiva."""
        for limite, taxa, deducao in cls.TABELA_IRRF:
            if base_irrf <= limite:
                return to_decimal((base_irrf * taxa) - deducao, '0.01')
        return Decimal('0')

    @staticmethod
    def calcular_folha_detalhada(salario_bruto, dependentes=0, outros_descontos=0, beneficios=0) -> Dict:
        """Processamento completo de salário bruto para líquido."""
        bruto = to_decimal(salario_bruto)
        dep = int(dependentes)
        descontos_adicionais = to_decimal(outros_descontos)
        
        # 1. INSS
        inss = PayrollManager.calcular_inss(bruto)
        
        # 2. Base IRRF
        base_irrf = bruto - inss - (dep * PayrollManager.DEDUCAO_DEPENDENTE)
        base_irrf = max(Decimal('0'), base_irrf)
        
        # 3. IRRF
        irrf = PayrollManager.calcular_irrf(base_irrf)
        irrf = max(Decimal('0'), irrf)

        # 4. FGTS (Encargo Empresa, não desconta do funcionário)
        fgts = bruto * to_decimal('0.08')

        # 5. Salário Líquido
        liquido = bruto - inss - irrf - descontos_adicionais + to_decimal(beneficios)

        return {
            "salario_bruto": to_decimal(bruto, '0.01'),
            "desconto_inss": inss,
            "desconto_irrf": irrf,
            "outros_descontos": descontos_adicionais,
            "fgts_recolhido": to_decimal(fgts, '0.01'),
            "salario_liquido": to_decimal(liquido, '0.01')
        }

    @staticmethod
    def custo_total_empresa(salario_bruto, rat=0.02, sistema_s=0.058) -> Dict:
        """Cálculo do custo real de um funcionário para a empresa."""
        bruto = to_decimal(salario_bruto)
        
        # Encargos Fixos
        fgts = bruto * to_decimal('0.08')
        ferias_13_provisao = bruto * to_decimal('0.1111') # Provisão simplificada: (1/12 + 1/3*1/12 + 1/12)
        
        # Encargos Patronais (Empresa Normal)
        cpp = bruto * to_decimal('0.20')
        rat_valor = bruto * to_decimal(rat)
        sistema_s_valor = bruto * to_decimal(sistema_s)
        
        total_encargos = fgts + ferias_13_provisao + cpp + rat_valor + sistema_s_valor
        custo_total = bruto + total_encargos

        return {
            "salario_base": bruto,
            "encargos_sociais": to_decimal(cpp + rat_valor + sistema_s_valor, '0.01'),
            "fgts": to_decimal(fgts, '0.01'),
            "provisoes_ferias_13": to_decimal(ferias_13_provisao, '0.01'),
            "custo_total_mensal": to_decimal(custo_total, '0.01'),
            "percentual_sobre_bruto": to_decimal((custo_total / bruto - 1) * 100, '0.01')
        }
