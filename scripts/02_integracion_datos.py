"""
Script de integracion y limpieza de las 3 fuentes de datos
Genera tablas procesadas listas para Power BI
"""

import pandas as pd
import numpy as np
import json

print("Iniciando integracion de 3 fuentes")
print("-" * 70)

# CARGAR DATOS RAW
print("\nCargando datos de las 3 fuentes...")

# Fuente 1: Transacciones
df_retail = pd.read_csv('data/raw/retail_backup.csv')
print(f"  Transacciones: {len(df_retail)} filas")

# Fuente 2: World Bank
df_gdp = pd.read_csv('data/raw/worldbank_gdp.csv')
df_internet = pd.read_csv('data/raw/worldbank_internet.csv')
df_population = pd.read_csv('data/raw/worldbank_population.csv')
print(f"  World Bank GDP: {len(df_gdp)} registros")
print(f"  World Bank Internet: {len(df_internet)} registros")
print(f"  World Bank Population: {len(df_population)} registros")

# Fuente 3: Exchange Rates
with open('data/raw/exchange_rates_2011.json', 'r') as f:
    exchange_rates = json.load(f)
print(f"  Exchange Rates: {len(exchange_rates)} tasas cargadas")

# LIMPIEZA DE TRANSACCIONES
print("\nLimpiando datos de transacciones...")

df_clean = df_retail.copy()
initial_rows = len(df_clean)

df_clean = df_clean.dropna(subset=['CustomerID'])
df_clean = df_clean[df_clean['Quantity'] > 0]
df_clean = df_clean[df_clean['UnitPrice'] > 0]

print(f"  Filas: {initial_rows} -> {len(df_clean)} (eliminadas: {initial_rows - len(df_clean)})")

# Crear columnas calculadas
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
df_clean['TotalPrice_GBP'] = df_clean['Quantity'] * df_clean['UnitPrice']
df_clean['Country'] = df_clean['Country'].str.strip().str.title()

# Aplicar conversion a USD
df_clean['TotalPrice_USD'] = df_clean['TotalPrice_GBP'] * exchange_rates['GBP_to_USD']

# Dimensiones temporales
df_clean['Year'] = df_clean['InvoiceDate'].dt.year
df_clean['Month'] = df_clean['InvoiceDate'].dt.month
df_clean['Quarter'] = df_clean['InvoiceDate'].dt.quarter
df_clean['YearMonth'] = df_clean['InvoiceDate'].dt.to_period('M').astype(str)

print(f"  Conversion a USD aplicada (tasa: {exchange_rates['GBP_to_USD']})")

# PREPARAR DATOS WORLD BANK
print("\nProcesando datos del World Bank...")

# Filtrar año 2011
df_gdp_2011 = df_gdp[df_gdp['Year'] == '2011'][['Country_Name', 'Value']].copy()
df_gdp_2011.columns = ['Country_Name', 'GDP_PerCapita']

df_internet_2011 = df_internet[df_internet['Year'] == '2011'][['Country_Name', 'Value']].copy()
df_internet_2011.columns = ['Country_Name', 'Internet_Users_Pct']

df_pop_2011 = df_population[df_population['Year'] == '2011'][['Country_Name', 'Value']].copy()
df_pop_2011.columns = ['Country_Name', 'Population']

# Combinar indicadores
df_wb = df_gdp_2011.merge(df_internet_2011, on='Country_Name', how='outer')
df_wb = df_wb.merge(df_pop_2011, on='Country_Name', how='outer')

print(f"  Indicadores combinados: {len(df_wb)} paises")

# AGREGAR METRICAS POR PAIS
print("\nCalculando metricas por pais...")

country_metrics = df_clean.groupby('Country').agg({
    'TotalPrice_USD': 'sum',
    'TotalPrice_GBP': 'sum',
    'InvoiceNo': 'nunique',
    'CustomerID': 'nunique',
    'StockCode': 'nunique'
}).reset_index()

country_metrics.columns = ['Country', 'Revenue_USD', 'Revenue_GBP', 
                          'Total_Orders', 'Total_Customers', 'Unique_Products']

country_metrics['Avg_Order_Value_USD'] = country_metrics['Revenue_USD'] / country_metrics['Total_Orders']
country_metrics['Revenue_Per_Customer_USD'] = country_metrics['Revenue_USD'] / country_metrics['Total_Customers']

print(f"  Metricas calculadas para {len(country_metrics)} paises")

# INTEGRACION FINAL
print("\nIntegrando las 3 fuentes...")

# Mapeo de nombres
name_mapping = {
    'United Kingdom': 'United Kingdom',
    'Germany': 'Germany',
    'France': 'France',
    'Eire': 'Ireland',
    'Spain': 'Spain',
    'Netherlands': 'Netherlands',
    'Belgium': 'Belgium',
    'Switzerland': 'Switzerland',
    'Portugal': 'Portugal',
    'Australia': 'Australia',
    'Norway': 'Norway',
    'Italy': 'Italy',
    'Sweden': 'Sweden',
    'Denmark': 'Denmark',
    'Finland': 'Finland',
    'Austria': 'Austria',
    'Japan': 'Japan',
    'Singapore': 'Singapore',
    'Cyprus': 'Cyprus',
    'Greece': 'Greece',
    'Poland': 'Poland',
    'Usa': 'United States',
    'Rsa': 'South Africa'
}

country_metrics['Country_WB'] = country_metrics['Country'].map(name_mapping)

# Merge con World Bank
integrated = country_metrics.merge(
    df_wb,
    left_on='Country_WB',
    right_on='Country_Name',
    how='left'
)

integrated = integrated[[
    'Country', 'Revenue_USD', 'Revenue_GBP', 'Total_Orders', 'Total_Customers',
    'Unique_Products', 'Avg_Order_Value_USD', 'Revenue_Per_Customer_USD',
    'GDP_PerCapita', 'Internet_Users_Pct', 'Population'
]]

# Metricas combinadas
integrated['Market_Potential_M'] = (
    integrated['GDP_PerCapita'] * integrated['Population'] / 1000000
).fillna(0)

print(f"  Dataset integrado: {len(integrated)} paises")
print(f"  Paises con datos completos: {integrated[['GDP_PerCapita', 'Internet_Users_Pct']].notna().all(axis=1).sum()}")

# GUARDAR TABLAS PROCESADAS
print("\nGuardando tablas procesadas...")

# Tablas para Power BI
fact_sales = df_clean[[
    'InvoiceNo', 'InvoiceDate', 'Year', 'Month', 'Quarter', 'YearMonth',
    'StockCode', 'Description', 'Quantity', 'UnitPrice',
    'TotalPrice_GBP', 'TotalPrice_USD', 'CustomerID', 'Country'
]].copy()

dim_products = df_clean[['StockCode', 'Description']].drop_duplicates()
dim_customers = df_clean[['CustomerID', 'Country']].drop_duplicates()
dim_date = df_clean[['InvoiceDate', 'Year', 'Month', 'Quarter', 'YearMonth']].drop_duplicates().sort_values('InvoiceDate')

fact_sales.to_csv('data/processed/fact_sales.csv', index=False)
dim_products.to_csv('data/processed/dim_products.csv', index=False)
dim_customers.to_csv('data/processed/dim_customers.csv', index=False)
dim_date.to_csv('data/processed/dim_date.csv', index=False)
integrated.to_csv('data/processed/integrated_analysis.csv', index=False)

print("  fact_sales.csv")
print("  dim_products.csv")
print("  dim_customers.csv")
print("  dim_date.csv")
print("  integrated_analysis.csv")

# Metadata
metadata = {
    'timestamp': pd.Timestamp.now().isoformat(),
    'sources': {
        'source_1': {
            'type': 'CSV/Excel',
            'name': 'UCI Online Retail Dataset',
            'records': len(df_retail),
            'description': 'Transacciones de e-commerce 2010-2011'
        },
        'source_2': {
            'type': 'API REST',
            'name': 'World Bank Development Indicators API',
            'records': len(df_wb),
            'description': 'Indicadores economicos (GDP, Internet, Poblacion)'
        },
        'source_3': {
            'type': 'API REST',
            'name': 'ExchangeRate-API',
            'records': len(exchange_rates),
            'description': 'Tasas de cambio para conversion monetaria'
        }
    },
    'exchange_rates_used': exchange_rates,
    'final_records': len(fact_sales),
    'countries_analyzed': len(integrated),
    'integration_date': pd.Timestamp.now().strftime('%Y-%m-%d')
}

with open('data/processed/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("  metadata.json")

# RESUMEN
print("\n" + "=" * 70)
print("INTEGRACION COMPLETADA")
print("=" * 70)
print(f"\nDatos procesados:")
print(f"  Transacciones: {len(fact_sales)}")
print(f"  Productos: {len(dim_products)}")
print(f"  Clientes: {len(dim_customers)}")
print(f"  Paises: {len(integrated)}")
print(f"  Tasa de conversion: 1 GBP = {exchange_rates['GBP_to_USD']} USD")
print(f"\nFuentes integradas:")
print(f"  1. CSV/Excel - Transacciones e-commerce")
print(f"  2. API REST - World Bank (GDP, Internet, Poblacion)")
print(f"  3. API REST - Exchange Rates (GBP -> USD)")
print(f"\nArchivos listos para Power BI en data/processed/")
print("=" * 70)