# 🐋 Jubarte Finance - Core Engine 2026

O **Jubarte Finance** é uma plataforma de engenharia financeira e gestão de capital humano desenvolvida com foco em **precisão matemática absoluta**. O projeto integra cálculos complexos da legislação brasileira (CLT 2026), sistemas de amortização bancária e análises de viabilidade de negócios em uma interface moderna e intuitiva.

---

## 🏗️ Estrutura do Projeto

A arquitetura foi desenhada seguindo os princípios de **Clean Architecture**, separando a lógica de negócio (Core) da infraestrutura (DB/API) e da interface (Web).

```bash
.
├── finance_engine/          # Módulo principal (Motor de Inteligência)
│   ├── core/                # Utilitários de base matemática
│   │   └── math_utils.py    # Garante precisão de 28 casas decimais (Decimal)
│   ├── modules/             # Regras de Negócio Estratégicas
│   │   ├── calculator.py    # Eng. Financeira (Amortização SAC/PRICE, VPL, TIR)
│   │   ├── payroll.py       # CLT 2026 (INSS Progressivo, IRRF Isenção 5k)
│   │   └── business.py      # Business Analytics (Break-even, EBITDA, Markup)
│   └── database/            # Camada de Persistência
│       ├── models.py        # Esquema do Banco (Alchemy ORM)
│       └── session.py       # Gestão de Sessão (SQLite/Postgres)
├── web-dashboard/           # Interface Visual (Frontend)
│   ├── index.html           # Tela principal (Glassmorphism design)
│   ├── style.css            # Estilização Premium & Animações
│   └── script.js            # Lógica reativa e integração com API
├── api.py                   # Servidor REST (FastAPI) - A ponte entre Python e Web
├── main.py                  # Script de demonstração via Terminal
├── generate_report.py       # Gerador de relatórios profissionais (Excel)
└── README.md                # Guia do sistema (Você está aqui)
```

---

## 🚀 Funcionalidades Chave

### 1. Motor CLT 2026
Calculadora integrada com as projeções da Reforma Tributária:
*   **Isenção de IRRF**: Aplicada para rendimentos até R$ 5.000,00.
*   **INSS Progressivo**: Tabelas atualizadas com cálculo por faixas.
*   **Custo Real Empresa**: Cálculo do *overhead* (encargos, provisões e impostos patronais).

### 2. Engenharia Financeira
*   **SAC vs PRICE**: Comparativo detalhado de sistemas de amortização.
*   **VPL e TIR**: Análise de retorno sobre investimento.
*   **Correção Monetária**: Projeção de poder de compra (IPCA, IGP-M, Salário Mínimo).

### 3. Persistência & Relatórios
*   **Histórico no DB**: Todas as simulações são gravadas no banco de dados.
*   **Exportação Excel**: Geração de relatórios com múltiplas abas e tabelas prontas para apresentação.

---

## 🛠️ Guia de Instalação

Siga os passos abaixo para rodar o projeto em sua máquina local:

### 1. Pré-requisitos
*   **Python 3.12+** instalado.
*   **Navegador Moderno** (Chrome, Firefox ou Edge).

### 2. Configuração do Ambiente
Abra o terminal na pasta do projeto e execute:

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # No macOS/Linux
# .\venv\Scripts\activate  # No Windows

# Instalar dependências
pip install fastapi uvicorn sqlalchemy pandas openpyxl chart.js
```

### 3. Executando o Sistema

Para o funcionamento completo, você precisa rodar dois processos simultâneos:

**Passo A: Iniciar o Backend (Inteligência e DB)**
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 api.py
```
*O servidor estará disponível em `http://localhost:8000`*

**Passo B: Iniciar o Frontend (Dashboard Visual)**
Em um novo terminal:
```bash
python3 -m http.server 8080 --directory web-dashboard
```
*Acesse o dashboard em `http://localhost:8080`*

---

## 💎 Design System
O projeto utiliza um sistema visual baseado em **Glassmorphism**, com:
*   Efeitos de blur e transparência.
*   Tipografia `Outfit` e `Inter` para legibilidade premium.
*   Padrões de cor HSL harmonizados para modo escuro.

---

## ⚖️ Conformidade Matemática
Todos os cálculos utilizam o módulo `decimal` do Python com arredondamento `ROUND_HALF_UP`, seguindo os padrões contábeis oficiais para evitar os erros de precisão comuns em valores `float`.
