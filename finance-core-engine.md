# Plano de Projeto: Núcleo de Engenharia Financeira e Gestão CLT

## 🎯 Objetivo
Desenvolver o núcleo lógico de uma plataforma financeira de alta precisão, focada no mercado brasileiro (CLT, SAC/PRICE, EBITDA, VPL/TIR) utilizando Python e arquitetura limpa.

## 🏗️ Tipo de Projeto: BACKEND (Python)

## ✅ Critérios de Sucesso
- Precisão decimal absoluta em todos os cálculos (módulo `decimal`).
- Implementação correta das tabelas progressivas de INSS/IRRF (Padrão BR 2024/2025).
- Comparativo funcional entre amortização SAC e PRICE.
- Schema de banco de dados robusto para persistência de simulações.
- Cobertura de testes para casos de borda (divisão por zero, valores negativos).

## 🛠️ Tech Stack
- **Linguagem:** Python 3.12+
- **Aritmética:** Módulo `decimal` (precisão arbitrária)
- **Banco de Dados:** SQLAlchemy (compatível com SQLite/PostgreSQL)
- **Testes:** Pytest

## 📂 Estrutura de Arquivos Sugerida
```plaintext
finance_engine/
├── core/
│   ├── __init__.py
│   ├── math_utils.py       # Precisão decimal e validações
├── modules/
│   ├── __init__.py
│   ├── calculator.py       # Juros, Amortização, VPL, TIR
│   ├── payroll.py          # INSS, IRRF, FGTS, Custo Real (CLT)
│   ├── business.py         # EBITDA, Break-even, Cleanup
├── database/
│   ├── __init__.py
│   ├── models.py           # Schema SQLAlchemy
│   ├── session.py          # Configuração do banco
├── tests/
│   ├── test_calculator.py
│   ├── test_payroll.py
└── main.py                 # Ponto de entrada/Exemplos
```

## 📝 Task Breakdown

### Fase 1: Fundação e Core Math
- [ ] **Task 1: Setup do Projeto e Math Utils** 
  - Criar estrutura de pastas e configurar `decimal.getcontext()`.
  - Implementar validadores genéricos.
  - **Agente:** `backend-specialist` | **Verify:** `math_utils.py` existente.

### Fase 2: Módulo Financeiro (Engenharia)
- [ ] **Task 2: Calculadora de Juros e Amortização**
  - Implementar Juros Compostos com aportes.
  - Implementar geradores de tabela SAC e PRICE.
  - **Agente:** `backend-specialist` | **Verify:** Output de tabelas comparativas.
- [ ] **Task 3: Análise de Investimento (VPL/TIR)**
  - Implementar fórmulas de VPL e aproximação de TIR (estimativa Newton-Raphson).
  - **Agente:** `backend-specialist` | **Verify:** Testes com fluxos de caixa padrão.

### Fase 3: Módulo de Capital Humano (CLT)
- [ ] **Task 4: Motor de Folha de Pagamento**
  - Implementar faixas progressivas de INSS e IRRF (2024/2025).
  - Cálculo de Salário Líquido e Custo Empresa (Provisões).
  - **Agente:** `backend-specialist` | **Verify:** Bater valores com simuladores oficiais.

### Fase 4: Gestão Empresarial e DB
- [ ] **Task 5: Indicadores de Performance (EBITDA/Markup)**
  - Implementar cálculos de Break-even e precificação.
  - **Agente:** `backend-specialist` | **Verify:** Validação de margens.
- [ ] **Task 6: Schema de Banco de Dados**
  - Criar `models.py` para salvar Simulações, Funcionários e Empresas.
  - **Agente:** `database-architect` | **Verify:** `alembic` ou script de migração.

## 🏁 Phase X: Verificação Final
- [ ] Executar `pytest` em todos os módulos.
- [ ] Validar precisão de 4 casas decimais.
- [ ] Gerar JSON de exemplo para integração.
