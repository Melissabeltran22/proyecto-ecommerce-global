"""
Script de extraccion de datos de 3 fuentes heterogeneas
- Fuente 1: CSV/Excel (transacciones)
- Fuente 2: API REST World Bank (indicadores economicos)
- Fuente 3: API REST Exchange Rates (tasas de cambio)
"""

import pandas as pd
import requests
import json
import time
from datetime import datetime

print("Iniciando extraccion de datos de 3 fuentes")
print("-" * 70)

# FUENTE 1: EXCEL - Transacciones E-Commerce
print("\nFuente 1: Cargando datos de Excel...")

try:
    df_retail = pd.read_excel('data/raw/online_retail.xlsx')
    print(f"Excel cargado exitosamente: {len(df_retail)} filas")
    
    # Backup en CSV
    df_retail.to_csv('data/raw/retail_backup.csv', index=False)
    print("Backup CSV creado")
    
except FileNotFoundError:
    print("ERROR: No se encuentra el archivo data/raw/online_retail.xlsx")
    print("Descargalo de: https://archive.ics.uci.edu/ml/datasets/online+retail")
    exit(1)

# FUENTE 2: API REST - World Bank
print("\nFuente 2: Extrayendo datos del World Bank API...")

def get_worldbank_indicator(indicator, countries, years):
    """
    Extrae un indicador especifico del World Bank API
    
    Parametros:
    - indicator: codigo del indicador (ej: NY.GDP.PCAP.CD)
    - countries: lista de codigos ISO de paises
    - years: lista de años a consultar
    
    Retorna:
    - DataFrame con los datos extraidos
    """
    all_data = []
    
    for country in countries:
        url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
        params = {
            'format': 'json',
            'per_page': 500,
            'date': f"{min(years)}:{max(years)}"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if len(data) > 1 and data[1]:
                for record in data[1]:
                    all_data.append({
                        'Country_Code': record['country']['id'],
                        'Country_Name': record['country']['value'],
                        'Indicator': indicator,
                        'Year': record['date'],
                        'Value': record['value']
                    })
                print(f"  {country}: {len(data[1])} registros")
            else:
                print(f"  {country}: Sin datos disponibles")
                
        except Exception as e:
            print(f"  {country}: Error - {str(e)}")
        
        time.sleep(0.2)
    
    return pd.DataFrame(all_data)

# Mapeo de paises del dataset a codigos ISO
country_codes = [
    'GBR', 'DEU', 'FRA', 'ESP', 'NLD', 'BEL', 'CHE', 'PRT', 
    'AUS', 'NOR', 'ITA', 'SWE', 'DNK', 'FIN', 'AUT', 'JPN',
    'SGP', 'CYP', 'GRC', 'POL', 'USA', 'IRL', 'ZAF'
]

print(f"Extrayendo datos para {len(country_codes)} paises...")

# Extraer 3 indicadores diferentes
print("  Indicador 1: GDP per Capita")
df_gdp = get_worldbank_indicator('NY.GDP.PCAP.CD', country_codes, [2010, 2011])

print("  Indicador 2: Internet Users (% poblacion)")
df_internet = get_worldbank_indicator('IT.NET.USER.ZS', country_codes, [2010, 2011])

print("  Indicador 3: Poblacion total")
df_population = get_worldbank_indicator('SP.POP.TOTL', country_codes, [2010, 2011])

# Guardar datos crudos de la API
df_gdp.to_csv('data/raw/worldbank_gdp.csv', index=False)
df_internet.to_csv('data/raw/worldbank_internet.csv', index=False)
df_population.to_csv('data/raw/worldbank_population.csv', index=False)

total_wb_records = len(df_gdp) + len(df_internet) + len(df_population)
print(f"World Bank API: {total_wb_records} registros totales extraidos")

# FUENTE 3: API REST - Exchange Rates
print("\nFuente 3: Extrayendo tasas de cambio...")

def get_exchange_rate(base_currency, target_currencies):
    """
    Obtiene tasas de cambio actuales
    
    Parametros:
    - base_currency: moneda base (ej: GBP)
    - target_currencies: lista de monedas objetivo
    
    Retorna:
    - diccionario con las tasas
    """
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        rates = {}
        for target in target_currencies:
            rates[f"{base_currency}_to_{target}"] = data['rates'].get(target)
        
        rates['date'] = data['date']
        return rates
        
    except Exception as e:
        print(f"  Error obteniendo tasas: {str(e)}")
        return None

# Obtener tasas actuales
current_rates = get_exchange_rate('GBP', ['USD', 'EUR'])

if current_rates:
    print(f"  GBP/USD: {current_rates['GBP_to_USD']}")
    print(f"  GBP/EUR: {current_rates['GBP_to_EUR']}")
    print(f"  Fecha: {current_rates['date']}")

# Para el analisis historico 2010-2011, usar tasas promedio del periodo
# Fuente: datos historicos del Banco Central Europeo
exchange_rates_2011 = {
    'GBP_to_USD': 1.60,
    'EUR_to_USD': 1.39,
    'AUD_to_USD': 1.03,
    'JPY_to_USD': 0.0124,
    'date': '2011-12-31',
    'source': 'Historical average 2011'
}

# Guardar tasas actuales y historicas
with open('data/raw/exchange_rates_current.json', 'w') as f:
    json.dump(current_rates, f, indent=2)

with open('data/raw/exchange_rates_2011.json', 'w') as f:
    json.dump(exchange_rates_2011, f, indent=2)

print("Tasas de cambio guardadas (actuales e historicas)")

# RESUMEN FINAL
print("\n" + "=" * 70)
print("EXTRACCION COMPLETADA")
print("=" * 70)
print(f"\nDatos extraidos:")
print(f"  Fuente 1 (Excel):        {len(df_retail)} transacciones")
print(f"  Fuente 2 (World Bank):   {total_wb_records} registros")
print(f"  Fuente 3 (Exchange API): Tasas obtenidas")
print(f"\nArchivos guardados en data/raw/")
print("=" * 70)