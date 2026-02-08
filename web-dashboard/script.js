// Configurações 2026
const RULES_2026 = {
    SALARIO_MINIMO: 1621.00,
    TETO_INSS: 8475.55,
    FAIXAS_INSS: [
        { max: 1621.00, tax: 0.075 },
        { max: 2902.84, tax: 0.09 },
        { max: 4354.27, tax: 0.12 },
        { max: 8475.55, tax: 0.14 }
    ],
    ISENCAO_IRRF: 5000.00
};

// State Management
let mainChart = null;

function formatBRL(val) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
}

// Logic: INSS 2026
function calculateINSS(salario) {
    const valorBase = Math.min(salario, RULES_2026.TETO_INSS);
    let imposto = 0;
    let anterior = 0;

    for (const faixa of RULES_2026.FAIXAS_INSS) {
        if (valorBase > anterior) {
            const baseFaixa = Math.min(valorBase, faixa.max) - anterior;
            imposto += baseFaixa * faixa.tax;
            anterior = faixa.max;
        } else {
            break;
        }
    }
    return imposto;
}

// Logic: IRRF 2026
function calculateIRRF(base) {
    if (base <= RULES_2026.ISENCAO_IRRF) return 0;

    // Simplificação da banda progressiva acima de 5k
    const diff = base - RULES_2026.ISENCAO_IRRF;
    return diff * 0.275; // Alíquota simplificada para simulação visual
}

// Connectivity: Backend API
const API_BASE = "http://localhost:8000";

let debounceTimer;

async function updateUI() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
        const bruto = parseFloat(document.getElementById('input-bruto').value) || 0;
        const dep = parseInt(document.getElementById('input-dep').value) || 0;

        try {
            // 1. Calcula Folha via API
            const response = await fetch(`${API_BASE}/calculate/payroll`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ salario_bruto: bruto, dependentes: dep })
            });
            const data = await response.json();

            // 2. Calcula Indicadores via API
            const resBiz = await fetch(`${API_BASE}/calculate/business`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ salario_bruto: bruto })
            });
            const bizData = await resBiz.json();

            // 3. Calcula Investimento 10 Anos
            const resInv = await fetch(`${API_BASE}/calculate/investment_10years`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ salario_bruto: bruto, dependentes: dep })
            });
            const invData = await resInv.json();

            // Atualiza Campos
            document.getElementById('val-inss').innerText = `- ${formatBRL(parseFloat(data.desconto_inss))}`;
            document.getElementById('val-irrf').innerText = `- ${formatBRL(parseFloat(data.desconto_irrf))}`;
            document.getElementById('val-liquido').innerText = formatBRL(parseFloat(data.salario_liquido));
            document.getElementById('val-custo-emp').innerText = formatBRL(parseFloat(bizData.custo_empresa.custo_total_mensal));

            // Injeta Tabela de Investimento
            const invBody = document.getElementById('investment-body');
            invBody.innerHTML = invData.map(row => `
                <tr>
                    <td>Ano ${row.ano}</td>
                    <td>${formatBRL(row.total_investido)}</td>
                    <td>${formatBRL(row.juros_gerados)}</td>
                    <td style="color: var(--accent); font-weight: 600;">${formatBRL(row.patrimonio_total)}</td>
                </tr>
            `).join('');

            // Log do ID da simulação salva no DB
            console.log(`Simulação sincronizada no Banco de Dados. ID: ${data.id}`);

            updateChartData(parseFloat(data.salario_liquido));
            updateCorrection();
        } catch (error) {
            console.error("Erro na sincronização com API:", error);
        }
    }, 300); // 300ms debounce
}

function updateCorrection() {
    const base = parseFloat(document.getElementById('input-base-corr').value) || 0;
    const indexador = document.getElementById('input-indexador').value;

    // Taxas Projetadas 2026-2030
    const taxas = {
        minimo: 0.04,   // Salário Mínimo Real (+4% a.a.)
        inflacao: 0.039, // IPCA (3.9% a.a.)
        igpm: 0.06      // IGP-m (6% a.a.)
    };

    const anos = 4;
    const taxa = taxas[indexador];
    const valorCorrigido = base * Math.pow((1 + taxa), anos);

    document.getElementById('val-corrigido').innerText = formatBRL(valorCorrigido);
}

async function downloadReport() {
    const bruto = parseFloat(document.getElementById('input-bruto').value) || 0;
    const btn = document.querySelector('.btn-primary');
    const originalText = btn.innerHTML;

    btn.innerHTML = '<span>⏳ Gerando...</span>';

    try {
        const response = await fetch(`${API_BASE}/reports/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ salario_bruto: bruto })
        });

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Relatorio_Jubarte_${bruto}.xlsx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (error) {
        alert("Erro ao gerar relatório. Verifique se o servidor API está rodando.");
    } finally {
        btn.innerHTML = originalText;
    }
}

function initChart() {
    const ctx = document.getElementById('mainChart').getContext('2d');

    mainChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: 12 }, (_, i) => `Mês ${i + 1}`),
            datasets: [
                {
                    label: 'Patrimônio Total',
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.4,
                    data: []
                },
                {
                    label: 'Total Investido',
                    borderColor: '#94a3b8',
                    borderDash: [5, 5],
                    data: []
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#94a3b8', font: { family: 'Inter' } } }
            },
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
            }
        }
    });
}

function updateChartData(valorBase) {
    if (!mainChart) return;

    const taxa = 0.008; // 0.8% ao mês (Coerente com API)
    const aporte = valorBase * 0.2; // 20% do LÍQUIDO
    let total = 0;
    let investido = 0;

    const dataTotal = [];
    const dataInvestido = [];

    for (let i = 0; i < 12; i++) {
        investido += aporte;
        total = (total + aporte) * (1 + taxa);
        dataTotal.push(total);
        dataInvestido.push(investido);
    }

    mainChart.data.datasets[0].data = dataTotal;
    mainChart.data.datasets[1].data = dataInvestido;
    mainChart.update();
}

// Event Listeners
document.getElementById('input-bruto').addEventListener('input', updateUI);
document.getElementById('input-dep').addEventListener('input', updateUI);
document.getElementById('input-base-corr').addEventListener('input', updateCorrection);
document.getElementById('input-indexador').addEventListener('change', updateCorrection);

// Initial Load
window.addEventListener('load', () => {
    initChart();
    updateUI();
});
