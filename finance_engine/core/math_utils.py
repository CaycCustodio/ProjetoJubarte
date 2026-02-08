from decimal import Decimal, getcontext, ROUND_HALF_UP

# Configuração de precisão financeira (Mínimo 4 casas decimais para intermediários)
# Utilizamos ROUND_HALF_UP por ser o padrão contábil comum no Brasil
getcontext().prec = 28  # Precisão total para evitar erros de arredondamento em cascata

def to_decimal(value, quantize=None) -> Decimal:
    """Converte um valor para Decimal com segurança."""
    if value is None:
        return Decimal('0')
    
    d = Decimal(str(value))
    if quantize:
        return d.quantize(Decimal(quantize), rounding=ROUND_HALF_UP)
    return d

def validate_positive(value, name="Campo"):
    """Valida se o valor é positivo."""
    if value < 0:
        raise ValueError(f"{name} não pode ser negativo.")

def validate_not_zero(value, name="Campo"):
    """Valida se o valor não é zero (evitar divisão por zero)."""
    if value == 0:
        raise ValueError(f"{name} não pode ser zero.")
