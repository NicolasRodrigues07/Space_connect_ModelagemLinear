# GS2026.1 - Programação Aplicada ao Monitoramento de Missão Espacial
# Análise Estatística - Sensor AMT00102 (Magnetômetro)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from scipy import stats

# 1. CARREGAMENTO DOS DADOS
print("Carregando dados...")
stats_6h = pd.read_parquet('AMT00102_stats_6h.parquet')
stats_6h = stats_6h.dropna()

# Variáveis de análise
# Contínua : value_mean  (média do campo magnético nT por janela de 6h)
# Discreta : value_count (número de leituras por janela de 6h)
v_cont  = stats_6h['value_mean']
v_disc  = stats_6h['value_count'].astype(int)

print(f"Registros disponíveis: {len(stats_6h)}")
print(f"Período: {stats_6h.index.min().date()} a {stats_6h.index.max().date()}")

# -----------------------------------------------------------------------------
# EXERCÍCIO 02 - TABELAS DE DISTRIBUIÇÃO DE FREQUÊNCIAS
# -----------------------------------------------------------------------------

# (a) Variável Quantitativa *DISCRETA:* value_count 
print("\n===Tabela de Distribuição de Frequências (Discreta)===")

freq_disc = v_disc.value_counts().sort_index()
# Agrupa valores menores que 1000 como "< 1000" pra simplificar
bins_disc = {
    'Menos de 100': v_disc[v_disc < 100].count(),
    '100 a 499':    v_disc[(v_disc >= 100) & (v_disc < 500)].count(),
    '500 a 999':    v_disc[(v_disc >= 500) & (v_disc < 1000)].count(),
    '1000 a 1349':  v_disc[(v_disc >= 1000) & (v_disc < 1350)].count(),
    '1350':         v_disc[v_disc == 1350].count(),
    'Acima de 1350':v_disc[v_disc > 1350].count(),
}
# Cria DataFrame para exibir a tabela
tdf_disc = pd.DataFrame({
    'Classe': list(bins_disc.keys()),
    'Fi (freq. absoluta)': list(bins_disc.values()),
})
tdf_disc['Fr (freq. relativa %)'] = (tdf_disc['Fi (freq. absoluta)'] / len(v_disc) * 100).round(2) # Calcula frequência relativa em porcentagem
tdf_disc['Fac (freq. acumulada)'] = tdf_disc['Fi (freq. absoluta)'].cumsum() 
print(tdf_disc.to_string(index=False)) #Sem index(IDs) para exibir a tabela limpa

# (b) Variável Quantitativa *CONTÍNUA:* value_mean
print("\n===Tabela de Distribuição de Frequências (Contínua)===")

n_classes = 7
counts, bin_edges = np.histogram(v_cont, bins=n_classes)
# Cria o texto dos intervalos pegando o início e o fim de cada um dos 7 grupos
classes = [f"{bin_edges[i]:.1f} a {bin_edges[i+1]:.1f}" for i in range(n_classes)]
tdf_cont = pd.DataFrame({
    'Classe (nT)': classes,
    'Fi (freq. absoluta)': counts,
    'Fr (freq. relativa %)': (counts / len(v_cont) * 100).round(2),
    'Fac (freq. acumulada)': counts.cumsum(),
})
print(tdf_cont.to_string(index=False))

# -----------------------------------------------------------------------------
# EXERCÍCIO 03 - GRÁFICOS
# -----------------------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico 1: Histograma da variável contínua 
ax1 = axes[0]
ax1.hist(v_cont, bins=40, color='steelblue', edgecolor='white', alpha=0.85)
ax1.set_title('Distribuição da Média do Campo Magnético (6h)', fontsize=13, fontweight='bold')
ax1.set_xlabel('Valor Médio (nT)', fontsize=11)
ax1.set_ylabel('Frequência', fontsize=11)
ax1.axvline(v_cont.mean(), color='red', linestyle='--', linewidth=1.5, label=f'Média: {v_cont.mean():.1f} nT')
ax1.axvline(v_cont.median(), color='orange', linestyle='--', linewidth=1.5, label=f'Mediana: {v_cont.median():.1f} nT')
ax1.legend(fontsize=10)
ax1.grid(axis='y', alpha=0.3)

# Gráfico 2: Evolução temporal da média mensal 
ax2 = axes[1]
mensal = v_cont.resample('ME').mean()
ax2.plot(mensal.index, mensal.values, color='darkorange', linewidth=1.8, marker='o', markersize=3)
ax2.set_title('Evolução da Média Mensal do Campo Magnético', fontsize=13, fontweight='bold')
ax2.set_xlabel('Data', fontsize=11)
ax2.set_ylabel('Valor Médio (nT)', fontsize=11)
ax2.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.6, label='Linha zero')
ax2.legend(fontsize=10)
ax2.grid(alpha=0.3)
fig.autofmt_xdate()

plt.tight_layout()
plt.savefig('graficos_AMT00102.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nGráficos salvos em graficos_AMT00102.png")

# -----------------------------------------------------------------------------
# EXERCÍCIO 04 - ESTATÍSTICA DESCRITIVA
# -----------------------------------------------------------------------------

def estatisticas_completas(serie, nome):
    print(f"\n{'='*55}")
    print(f"  Análise Univariada: {nome}")
    print(f"{'='*55}")

    media   = serie.mean()
    mediana = serie.median()
    moda    = serie.mode()[0]
    vmin    = serie.min()
    vmax    = serie.max()
    amplitude = vmax - vmin
    variancia = serie.var()
    desvio  = serie.std()
    cv      = (desvio / media * 100) if media != 0 else float('nan')
    q1      = serie.quantile(0.25)
    q2      = serie.quantile(0.50)
    q3      = serie.quantile(0.75)

    print(f"\n  Medidas de Tendência Central")
    print(f"    Média    : {media:.4f}")
    print(f"    Mediana  : {mediana:.4f}")
    print(f"    Moda     : {moda:.4f}")

    print(f"\n  Medidas de Dispersão")
    print(f"    Mínimo         : {vmin:.4f}")
    print(f"    Máximo         : {vmax:.4f}")
    print(f"    Amplitude      : {amplitude:.4f}")
    print(f"    Variância      : {variancia:.4f}")
    print(f"    Desvio Padrão  : {desvio:.4f}")
    print(f"    Coef. Variação : {cv:.2f}%")

    print(f"\n  Medidas Separatrizes (Quartis)")
    print(f"    Q1 (25%) : {q1:.4f}")
    print(f"    Q2 (50%) : {q2:.4f}")
    print(f"    Q3 (75%) : {q3:.4f}")
    print(f"    IQR      : {q3 - q1:.4f}")

    return {
        'media': media, 'mediana': mediana, 'moda': moda,
        'min': vmin, 'max': vmax, 'amplitude': amplitude,
        'variancia': variancia, 'desvio': desvio, 'cv': cv,
        'q1': q1, 'q2': q2, 'q3': q3
    }

est_cont = estatisticas_completas(v_cont,  "Campo Magnético Médio por Janela 6h (nT)")
est_disc = estatisticas_completas(v_disc.astype(float), "Contagem de Leituras por Janela 6h")

print("\nAnálise concluída!")

stats_6h.to_csv('AMT00102_stats_6h.csv')
print("CSV gerado!")