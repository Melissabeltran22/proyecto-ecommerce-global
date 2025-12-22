"""
Script de analisis estadistico para el informe
Genera metricas y correlaciones de las 3 fuentes integradas
"""

import pandas as pd
import json
from scipy.stats import pearsonr
import numpy as np

print("=" * 70)
print("ANALISIS ESTADISTICO")
print("=" * 70)

# Cargar datos procesados
df_integrated = pd.read_csv('data/processed/integrated_analysis.csv')
df_sales = pd.read_csv('data/processed/fact_sales.csv')

# Cargar metadata
with open('data/processed/metadata.json', 'r') as f:
    metadata = json.load(f)

print("\nFUENTES DE DATOS UTILIZADAS:")
print("-" * 70)
for key, source in metadata['sources'].items():
    print(f"{source['name']}")
    print(f"  Tipo: {source['type']}")
    print(f"  Registros: {source['records']}")
    print(f"  Descripcion: {source['description']}")
    print()

print(f"Tasa de cambio aplicada: 1 GBP = {metadata['exchange_rates_used']['GBP_to_USD']} USD")
print(f"Fecha de integracion: {metadata['integration_date']}")

print("\n" + "=" * 70)
print("KPIS PRINCIPALES")
print("=" * 70)

total_revenue_usd = df_integrated['Revenue_USD'].sum()
total_revenue_gbp = df_integrated['Revenue_GBP'].sum()
total_customers = df_integrated['Total_Customers'].sum()
total_orders = df_integrated['Total_Orders'].sum()
num_countries = len(df_integrated)
unique_products = df_sales['StockCode'].nunique()

print(f"Revenue Total (USD):         ${total_revenue_usd:,.2f}")
print(f"Revenue Total (GBP):         £{total_revenue_gbp:,.2f}")
print(f"Total Clientes:              {total_customers:,}")
print(f"Total Ordenes:               {total_orders:,}")
print(f"Paises Atendidos:            {num_countries}")
print(f"Productos Unicos:            {unique_products:,}")
print(f"Ticket Promedio (USD):       ${total_revenue_usd/total_orders:,.2f}")
print(f"Revenue por Cliente (USD):   ${total_revenue_usd/total_customers:,.2f}")

print("\n" + "=" * 70)
print("ANALISIS DE CORRELACIONES")
print("=" * 70)

df_complete = df_integrated.dropna(subset=['GDP_PerCapita', 'Internet_Users_Pct', 'Revenue_USD'])

if len(df_complete) >= 3:
    corr_gdp_rev, p_gdp = pearsonr(df_complete['GDP_PerCapita'], df_complete['Revenue_USD'])
    corr_int_rev, p_int = pearsonr(df_complete['Internet_Users_Pct'], df_complete['Revenue_USD'])
    corr_pop_rev, p_pop = pearsonr(df_complete['Population'], df_complete['Revenue_USD'])
    corr_gdp_aov, p_gdp_aov = pearsonr(df_complete['GDP_PerCapita'], df_complete['Revenue_Per_Customer_USD'])
    
    print(f"\nCorrelacion GDP per Capita vs Revenue:           r = {corr_gdp_rev:.3f} (p={p_gdp:.4f})")
    print(f"Correlacion Internet Users % vs Revenue:         r = {corr_int_rev:.3f} (p={p_int:.4f})")
    print(f"Correlacion Population vs Revenue:               r = {corr_pop_rev:.3f} (p={p_pop:.4f})")
    print(f"Correlacion GDP vs Revenue per Customer:         r = {corr_gdp_aov:.3f} (p={p_gdp_aov:.4f})")
    
    print("\nInterpretacion:")
    correlations = [
        ('GDP per Capita', abs(corr_gdp_rev)),
        ('Internet Users %', abs(corr_int_rev)),
        ('Population', abs(corr_pop_rev))
    ]
    best = max(correlations, key=lambda x: x[1])
    print(f"  Mejor predictor de Revenue: {best[0]} (r={best[1]:.3f})")
    
    # Guardar resultados
    results = {
        'correlations': {
            'gdp_revenue': {'r': float(corr_gdp_rev), 'p': float(p_gdp)},
            'internet_revenue': {'r': float(corr_int_rev), 'p': float(p_int)},
            'population_revenue': {'r': float(corr_pop_rev), 'p': float(p_pop)},
            'gdp_aov': {'r': float(corr_gdp_aov), 'p': float(p_gdp_aov)}
        },
        'best_predictor': best[0]
    }
    
    with open('data/processed/statistical_results.json', 'w') as f:
        json.dump(results, f, indent=2)

print("\n" + "=" * 70)
print("TOP 5 PAISES POR REVENUE")
print("=" * 70)

top5 = df_integrated.nlargest(5, 'Revenue_USD')
print(f"{'Pais':<20} {'Revenue (USD)':<15} {'GDP per Capita':<15} {'Internet %':<12}")
print("-" * 70)
for idx, row in top5.iterrows():
    print(f"{row['Country']:<20} ${row['Revenue_USD']:>13,.0f}   "
          f"${row['GDP_PerCapita']:>12,.0f}   "
          f"{row['Internet_Users_Pct']:>10.1f}%")

print("\n" + "=" * 70)
print("PAISES CON ALTO POTENCIAL")
print("(Alto GDP/Internet pero bajo revenue actual)")
print("=" * 70)

potential = df_complete[
    ((df_complete['GDP_PerCapita'] > 40000) | (df_complete['Internet_Users_Pct'] > 80)) &
    (df_complete['Revenue_USD'] < df_complete['Revenue_USD'].median())
].sort_values('GDP_PerCapita', ascending=False)

if len(potential) > 0:
    print(f"{'Pais':<20} {'GDP per Capita':<15} {'Internet %':<12} {'Revenue (USD)':<15}")
    print("-" * 70)
    for idx, row in potential.head(5).iterrows():
        print(f"{row['Country']:<20} ${row['GDP_PerCapita']:>12,.0f}   "
              f"{row['Internet_Users_Pct']:>10.1f}%   "
              f"${row['Revenue_USD']:>13,.0f}")
else:
    print("No se encontraron paises en esta categoria")

print("\n" + "=" * 70)
print("Resultados guardados en data/processed/statistical_results.json")
print("=" * 70)