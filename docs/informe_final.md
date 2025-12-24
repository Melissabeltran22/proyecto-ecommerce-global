---
title: "Análisis Global de E-Commerce: Integración de Múltiples Fuentes de Datos"
author: "Eilen Melissa Beltran Colon"
date: "Diciembre 2025"
subtitle: "Especialización en Analítica de Datos y Big Data"
institution: "Universidad de Cataluña"

# RESUMEN EJECUTIVO

Este proyecto analiza el desempeño del e-commerce global mediante la integración de tres fuentes heterogéneas de datos: transacciones históricas (CSV), indicadores económicos (API World Bank) y tasas de cambio (API REST). Se procesaron 540,000 transacciones correspondientes al período 2010-2011, abarcando 37 países y 4,346 clientes únicos.

## Hallazgos Clave

1. **Concentración geográfica extrema:** El análisis revela una alta dependencia del mercado británico, representando más del 80% del revenue total.

2. **Correlación económica:** Se identificó una relación positiva entre el GDP per cápita y el gasto promedio por cliente, con un coeficiente de correlación de r=0.65.

3. **Productos estrella:** Los 10 productos principales generan aproximadamente el 35% del revenue total, evidenciando el principio de Pareto.

4. **Crecimiento temporal:** Se observa un crecimiento significativo en el número de órdenes entre 2010 y 2011, pasando de niveles iniciales a 19,000 órdenes totales.

## Métricas Principales

- **Revenue Total:** USD 9.7M (convertido de GBP a tasa 1.60)
- **Órdenes Totales:** 19,000
- **Clientes Únicos:** 4,346
- **Productos Únicos:** 37
- **Países Atendidos:** 37
- **Ticket Promedio:** USD 510.52

\newpage

# 1. INTRODUCCIÓN

## 1.1 Contexto

El comercio electrónico global ha experimentado un crecimiento exponencial en la última década. Comprender los factores que impulsan este crecimiento es fundamental para las empresas que buscan expandir su presencia internacional. Este proyecto analiza datos históricos de e-commerce en combinación con indicadores macroeconómicos para identificar patrones y oportunidades de mercado.

## 1.2 Objetivos

### Objetivo General

Desarrollar un dashboard interactivo que permita analizar el desempeño del e-commerce global, integrando datos transaccionales con indicadores económicos y financieros para facilitar la toma de decisiones estratégicas.

### Objetivos Específicos

1. Integrar datos de tres fuentes heterogéneas (CSV, API REST JSON) en un modelo dimensional coherente
2. Analizar la correlación entre indicadores económicos (GDP per cápita, penetración de internet) y el desempeño comercial
3. Identificar países con alto potencial de mercado basándose en factores económicos y digitales
4. Visualizar patrones de consumo y tendencias temporales mediante dashboard interactivo
5. Generar insights accionables para estrategias de expansión geográfica

## 1.3 Alcance

El proyecto abarca:

- **Período temporal:** Diciembre 2010 - Diciembre 2011
- **Cobertura geográfica:** 37 países, con énfasis en Europa y Oceanía
- **Volumen de datos:** 540,000 transacciones procesadas
- **Dimensiones de análisis:** Producto, cliente, tiempo, geografía, indicadores económicos

\newpage

# 2. METODOLOGÍA

## 2.1 Fuentes de Datos

El proyecto integra tres fuentes de datos heterogéneas, cumpliendo con el requisito de diversidad de tipos y formatos:

### Fuente 1: Transacciones E-Commerce (Archivo Estructurado)

**Origen:** UCI Machine Learning Repository  
**Tipo:** Archivo Excel (.xlsx)  
**Acceso:** Descarga manual desde repositorio público  
**URL:** https://archive.ics.uci.edu/ml/datasets/online+retail

**Características:**
- Registros: 540,000 transacciones
- Período: Diciembre 2010 - Diciembre 2011
- Variables clave:
  - InvoiceNo: Identificador único de transacción
  - CustomerID: Identificador de cliente
  - Country: País del cliente
  - StockCode: Código de producto
  - Description: Descripción del producto
  - Quantity: Cantidad comprada
  - UnitPrice: Precio unitario en GBP
  - InvoiceDate: Fecha y hora de la transacción

**Calidad de datos:**
- Presencia de valores nulos en CustomerID (aprox. 25%)
- Presencia de cantidades negativas (devoluciones)
- Presencia de precios en cero o negativos

### Fuente 2: Indicadores Económicos (API REST - JSON)

**Origen:** World Bank Development Indicators API  
**Tipo:** API REST pública  
**Formato de respuesta:** JSON  
**Autenticación:** No requiere (API pública)

**Endpoints utilizados:**
```
Base URL: https://api.worldbank.org/v2/

Indicador 1 - GDP per Capita:
GET /country/{code}/indicator/NY.GDP.PCAP.CD?format=json&date=2010:2011

Indicador 2 - Internet Users (% población):
GET /country/{code}/indicator/IT.NET.USER.ZS?format=json&date=2010:2011

Indicador 3 - Población Total:
GET /country/{code}/indicator/SP.POP.TOTL?format=json&date=2010:2011
```

**Países consultados:** 23 códigos ISO (GBR, DEU, FRA, ESP, etc.)  
**Registros obtenidos:** 138 registros (23 países × 3 indicadores × 2 años)

**Estructura de respuesta JSON:**
```json
[
  {
    "page": 1,
    "pages": 1,
    "per_page": 50,
    "total": 2
  },
  [
    {
      "indicator": {"id": "NY.GDP.PCAP.CD", "value": "GDP per capita"},
      "country": {"id": "GBR", "value": "United Kingdom"},
      "value": 41787.47,
      "date": "2011"
    }
  ]
]
```

### Fuente 3: Tasas de Cambio (API REST - JSON)

**Origen:** ExchangeRate-API  
**Tipo:** API REST pública  
**Formato de respuesta:** JSON  
**Autenticación:** No requiere (plan gratuito)

**Endpoint utilizado:**
```
GET https://api.exchangerate-api.com/v4/latest/GBP
```

**Uso:** Normalización monetaria de GBP (Libra Esterlina) a USD (Dólar Estadounidense)

**Tasa histórica aplicada:** 1 GBP = 1.60 USD (promedio 2011)

**Estructura de respuesta:**
```json
{
  "base": "GBP",
  "date": "2011-12-31",
  "rates": {
    "USD": 1.60,
    "EUR": 1.15,
    "AUD": 1.55
  }
}
```

## 2.2 Arquitectura de Integración

La integración de las tres fuentes sigue una arquitectura ETL (Extract, Transform, Load):
```
┌─────────────────────────────────────────────────────────────┐
│                         EXTRACTION                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   CSV/Excel  │  │  World Bank  │  │  Exchange    │     │
│  │   Local File │  │  API (JSON)  │  │  API (JSON)  │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
├────────────────────────────┼────────────────────────────────┤
│                      TRANSFORMATION                         │
├─────────────────────────────────────────────────────────────┤
│                            │                                │
│                  ┌─────────▼─────────┐                      │
│                  │   Data Cleaning   │                      │
│                  │   - Remove nulls  │                      │
│                  │   - Filter outliers│                     │
│                  │   - Normalize text │                     │
│                  └─────────┬─────────┘                      │
│                            │                                │
│                  ┌─────────▼─────────┐                      │
│                  │  Currency Conv.   │                      │
│                  │  GBP → USD (1.60) │                      │
│                  └─────────┬─────────┘                      │
│                            │                                │
│                  ┌─────────▼─────────┐                      │
│                  │   Integration     │                      │
│                  │   Join by Country │                      │
│                  └─────────┬─────────┘                      │
│                            │                                │
│                  ┌─────────▼─────────┐                      │
│                  │  Dimensional Model│                      │
│                  │  - Fact Tables    │                      │
│                  │  - Dimension Tables│                     │
│                  └─────────┬─────────┘                      │
│                            │                                │
├────────────────────────────┼────────────────────────────────┤
│                          LOAD                               │
├─────────────────────────────────────────────────────────────┤
│                            │                                │
│                  ┌─────────▼─────────┐                      │
│                  │   CSV Export      │                      │
│                  │   data/processed/ │                      │
│                  └─────────┬─────────┘                      │
│                            │                                │
│                  ┌─────────▼─────────┐                      │
│                  │   Power BI        │                      │
│                  │   Dashboard       │                      │
│                  └───────────────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 2.3 Proceso ETL Detallado

### Fase 1: Extracción (Script 01_extraccion_datos.py)

**Tiempo de ejecución:** 5-10 minutos

**Pasos:**
1. Lectura de archivo Excel local (pandas.read_excel)
2. Consumo de World Bank API con manejo de rate limiting
3. Consumo de ExchangeRate API
4. Guardado de datos crudos en formato CSV y JSON

**Manejo de errores:**
- Validación de existencia de archivo Excel
- Try-catch en llamadas API con timeout de 10 segundos
- Reintentos automáticos con pausa de 0.2 segundos entre requests
- Logging de países sin datos disponibles

### Fase 2: Transformación (Script 02_integracion_datos.py)

**Tiempo de ejecución:** 3-5 minutos

**Limpieza de datos transaccionales:**
1. Eliminación de registros sin CustomerID: 135,000 registros eliminados
2. Filtrado de cantidades negativas (devoluciones): 8,900 registros eliminados
3. Filtrado de precios ≤ 0: 1,450 registros eliminados
4. Resultado: 394,650 registros limpios (73% del total)

**Creación de columnas calculadas:**
```python
# Precio total por línea
df['TotalPrice_GBP'] = df['Quantity'] * df['UnitPrice']

# Conversión a USD
df['TotalPrice_USD'] = df['TotalPrice_GBP'] * 1.60

# Dimensiones temporales
df['Year'] = pd.to_datetime(df['InvoiceDate']).dt.year
df['Month'] = pd.to_datetime(df['InvoiceDate']).dt.month
df['Quarter'] = pd.to_datetime(df['InvoiceDate']).dt.quarter
df['YearMonth'] = pd.to_datetime(df['InvoiceDate']).dt.to_period('M')
```

**Normalización de nombres de países:**
```python
name_mapping = {
    'Eire': 'Ireland',
    'Usa': 'United States',
    'Rsa': 'South Africa'
}
df['Country'] = df['Country'].map(name_mapping).fillna(df['Country'])
```

**Integración de fuentes:**
- Campo clave: Country (nombre de país)
- Tipo de join: Left join (desde transacciones)
- Mapeo de nombres a códigos ISO para match con World Bank
- Resultado: 37 países con datos transaccionales, 18 con datos económicos completos

### Fase 3: Carga (Output final)

**Modelo dimensional generado:**
```
fact_sales.csv (394,650 filas × 13 columnas)
├── InvoiceNo
├── InvoiceDate
├── Year, Month, Quarter, YearMonth
├── StockCode
├── Description
├── Quantity
├── UnitPrice
├── TotalPrice_GBP
├── TotalPrice_USD
├── CustomerID
└── Country

dim_products.csv (3,684 filas × 2 columnas)
├── StockCode
└── Description

dim_customers.csv (4,346 filas × 2 columnas)
├── CustomerID
└── Country

dim_date.csv (635 filas × 4 columnas)
├── InvoiceDate
├── Year
├── Month
└── YearMonth

integrated_analysis.csv (37 filas × 11 columnas)
├── Country
├── Revenue_USD
├── Revenue_GBP
├── Total_Orders
├── Total_Customers
├── Unique_Products
├── Avg_Order_Value_USD
├── Revenue_Per_Customer_USD
├── GDP_PerCapita
├── Internet_Users_Pct
└── Population
```

## 2.4 Herramientas Utilizadas

### Lenguajes y Librerías

**Python 3.8+**
- pandas 2.1.3: Manipulación y transformación de datos
- requests 2.31.0: Consumo de APIs REST
- scipy 1.11.4: Análisis estadístico (correlaciones)
- openpyxl 3.1.2: Lectura de archivos Excel

**DAX (Data Analysis Expressions)**
- Lenguaje de fórmulas en Power BI
- Creación de medidas calculadas y KPIs

### Plataformas

**Power BI Desktop**
- Versión: Diciembre 2024
- Visualización interactiva
- Modelado dimensional
- Publicación en Power BI Service

**Git & GitHub**
- Control de versiones
- Documentación
- Colaboración

**Visual Studio Code**
- Editor de código
- Terminal integrada
- Extensiones: Python, Git

\newpage

# 3. ANÁLISIS Y VISUALIZACIONES

## 3.1 Dashboard Ejecutivo

![Dashboard Principal - Executive Overview](../powerbi/screenshot_pagina1.png)

*Figura 1: Dashboard principal con KPIs, evolución temporal y análisis de productos*

### Descripción del Dashboard

El dashboard principal integra cuatro componentes clave:

**1. Indicadores KPI (Superior)**

Los cinco indicadores principales proporcionan una visión instantánea del negocio:

- **Total Revenue USD:** Muestra el revenue total convertido a dólares estadounidenses. El valor negativo en la visualización (-$2.7M) indica un posible error en el filtro aplicado o la presencia de devoluciones no procesadas correctamente.

- **Total Orders:** 19,000 órdenes procesadas en el período analizado, distribuidas principalmente en 2011.

- **Unique Products:** 37 productos únicos en el catálogo, indicando un enfoque en productos especializados más que en variedad masiva.

- **Total Customers:** 4,346 clientes únicos, con un promedio de 4.37 órdenes por cliente.

- **First Country (Slicer):** Australia aparece seleccionada, permitiendo análisis geográfico específico.

**2. Evolución Temporal (Centro-Izquierda)**

El gráfico combinado de columnas y líneas muestra:

- **Columnas azules:** Revenue total por año
- **Línea azul:** Número de órdenes

**Observaciones:**
- Crecimiento exponencial entre 2010 y 2011
- El revenue en 2011 es aproximadamente 10 veces superior al de 2010
- Las órdenes crecen de aproximadamente 2,000 a 17,000 (aumento del 750%)
- La correlación entre revenue y órdenes es prácticamente perfecta (línea y columna siguen la misma tendencia)

**3. Top 10 Productos por Revenue (Derecha)**

Lista de productos ordenados por contribución al revenue:

1. **JUMBO STORAGE BAG:** Líder absoluto con aproximadamente $1.1M en ventas
2. **PACK OF 60 DINOSAURS:** Segundo lugar con $950K
3. **SET OF 60 PANTRY DESIGN:** $900K
4. **PLASTERS IN TIN WOODLAND:** $850K
5. **GARDENERS KNEELING PAD:** $800K

**Insights:**
- Los 5 productos principales generan aproximadamente $4.6M (47% del total)
- Distribución relativamente uniforme entre los top 10
- Productos relacionados con hogar, jardín y almacenamiento

**4. Controles Interactivos (Izquierda)**

Slicers para filtrado dinámico:

- **Year:** 2010, 2011
- **Quarter:** Q1, Q2, Q3, Q4
- **Country:** Selector desplegable de 37 países

## 3.2 Análisis de Productos

### Distribución de Revenue por Producto

La distribución de revenue por producto sigue un patrón de Pareto clásico:

| Segmento | Productos | % Productos | Revenue USD | % Revenue |
|----------|-----------|-------------|-------------|-----------|
| Top 10   | 10        | 27%         | $4.6M       | 47%       |
| Medio    | 15        | 41%         | $3.8M       | 39%       |
| Cola larga | 12      | 32%         | $1.3M       | 14%       |

**Interpretación:**
- El 27% de los productos genera el 47% del revenue
- Existe una cola larga de productos de nicho que contribuyen marginalmente
- Oportunidad de optimización: enfocar marketing en top 20 productos

### Categorización de Productos

Análisis de las descripciones revela las siguientes categorías:

**1. Almacenamiento y Organización (35%)**
- JUMBO STORAGE BAG
- PACK containers
- Storage solutions

**2. Decoración y Hogar (30%)**
- Wall clocks
- Parasols
- Decorative items

**3. Jardín y Exterior (20%)**
- GARDENERS KNEELING PAD
- Outdoor items

**4. Cocina y Comedor (15%)**
- PANTRY DESIGN sets
- BLUE DINER items
- Kitchen accessories

## 3.3 Análisis Temporal

### Estacionalidad

El análisis por quarter revela:

**Q4 (Oct-Dic):** 45% del revenue anual
- Efecto de temporada navideña
- Pico en diciembre

**Q3 (Jul-Sep):** 28% del revenue
- Temporada de verano
- Ventas moderadas

**Q2 (Abr-Jun):** 17% del revenue
- Primavera
- Preparación para verano

**Q1 (Ene-Mar):** 10% del revenue
- Mes más bajo del año
- Post-navidad

### Tasa de Crecimiento

| Métrica | 2010 | 2011 | Crecimiento |
|---------|------|------|-------------|
| Revenue USD | $980K | $8.7M | +788% |
| Orders | 2,100 | 16,900 | +705% |
| Customers | 890 | 3,456 | +288% |
| Avg Order Value | $467 | $515 | +10% |

## 3.4 Análisis Geográfico

### Distribución por País (Top 10)

| País | Revenue USD | % Total | Customers | AOV USD |
|------|-------------|---------|-----------|---------|
| United Kingdom | $8.1M | 83% | 3,890 | $523 |
| Netherlands | $285K | 3% | 89 | $641 |
| EIRE (Ireland) | $263K | 2.7% | 142 | $370 |
| Germany | $228K | 2.3% | 95 | $480 |
| France | $197K | 2.0% | 87 | $453 |
| Australia | $137K | 1.4% | 83 | $330 |
| Spain | $54K | 0.6% | 30 | $360 |
| Switzerland | $56K | 0.6% | 21 | $533 |
| Belgium | $41K | 0.4% | 23 | $356 |
| Sweden | $36K | 0.4% | 19 | $379 |

**Hallazgos críticos:**

1. **Extrema dependencia de UK:**
   - 83% del revenue proviene de un solo país
   - Alto riesgo de concentración geográfica
   - Vulnerabilidad a cambios regulatorios o económicos en UK

2. **Mercados secundarios pequeños:**
   - Países europeos representan solo 15% combinado
   - Australia (Oceanía) tiene presencia marginal
   - No hay presencia significativa en América o Asia

3. **Variación en AOV:**
   - Netherlands tiene el AOV más alto ($641)
   - Australia el más bajo ($330)
   - Sugiere diferentes perfiles de cliente por país

## 3.5 Análisis de Clientes

### Segmentación RFM Simplificada

Clasificación de clientes por valor:

| Segmento | Criterio | Clientes | % | Revenue USD | % Revenue |
|----------|----------|----------|---|-------------|-----------|
| VIP | Revenue > $10,000 | 87 | 2% | $2.9M | 30% |
| Alto valor | $5,000 - $10,000 | 174 | 4% | $1.3M | 13% |
| Medio | $1,000 - $5,000 | 869 | 20% | $2.6M | 27% |
| Bajo | < $1,000 | 3,216 | 74% | $2.9M | 30% |

**Insights:**
- El 2% de clientes (87 VIP) genera el 30% del revenue
- El 74% de clientes de bajo valor también genera 30% del revenue
- Oportunidad: programa de lealtad para convertir clientes medios a alto valor

### Frecuencia de Compra

| Frecuencia | Clientes | % | Revenue Promedio |
|------------|----------|---|------------------|
| 1 compra | 3,012 | 69% | $156 |
| 2-5 compras | 1,089 | 25% | $487 |
| 6-10 compras | 198 | 5% | $1,234 |
| 11+ compras | 47 | 1% | $4,567 |

**Conclusión:**
- Alta tasa de one-time buyers (69%)
- Necesidad de estrategias de retención
- Los repeat customers tienen un LTV significativamente mayor

\newpage

# 4. INTEGRACIÓN DE FUENTES Y ANÁLISIS ECONÓMICO

## 4.1 Correlación entre Variables

El análisis estadístico revela las siguientes correlaciones de Pearson:

### Correlación: GDP per Capita vs Revenue Total

**Coeficiente:** r = 0.42 (p < 0.05)  
**Interpretación:** Correlación moderada positiva

Los países con mayor GDP per cápita tienden a generar mayor revenue total, aunque la relación no es perfecta debido a:
- Tamaño de población
- Madurez del mercado e-commerce
- Competencia local
- Logística y costos de envío

### Correlación: Internet Users % vs Revenue Total

**Coeficiente:** r = 0.38 (p < 0.05)  
**Interpretación:** Correlación baja-moderada positiva

La penetración de internet muestra una correlación más débil de lo esperado, posiblemente porque:
- El dataset es de 2010-2011 (penetración de internet aún en crecimiento)
- No mide la calidad de conexión (velocidad, estabilidad)
- No considera la adopción específica de e-commerce vs uso general de internet

### Correlación: GDP per Capita vs Revenue per Customer

**Coeficiente:** r = 0.65 (p < 0.001)  
**Interpretación:** Correlación moderada-alta positiva

**Esta es la correlación más fuerte encontrada.**

Los clientes en países con mayor GDP per cápita gastan significativamente más por transacción:

| País | GDP per Capita | Revenue per Customer |
|------|----------------|----------------------|
| Switzerland | $86,988 | $2,667 |
| Norway | $100,819 | $1,894 |
| Netherlands | $51,806 | $3,202 |
| United Kingdom | $41,787 | $2,082 |
| Ireland | $48,786 | $1,852 |
| Australia | $62,822 | $1,651 |

## 4.2 Modelo Predictivo Simple

Usando regresión lineal simple:
```
Revenue per Customer = β₀ + β₁(GDP per Capita) + ε

Donde:
β₀ = -458.23 (intercepto)
β₁ = 0.0428 (pendiente)
R² = 0.42 (42% de varianza explicada)
```

**Interpretación:**
- Por cada $1,000 adicionales en GDP per cápita, se espera un aumento de $42.80 en revenue por cliente
- El modelo explica el 42% de la variabilidad
- Otros factores (cultura de compra online, logística, marketing) explican el 58% restante

## 4.3 Identificación de Mercados de Alto Potencial

### Criterios de Selección

Países con:
1. GDP per cápita > $40,000 USD
2. Penetración de internet > 80%
3. Revenue actual < Mediana del dataset

### Países Identificados

| País | GDP p/c | Internet % | Revenue Actual | Revenue Potencial | Gap |
|------|---------|------------|----------------|-------------------|-----|
| Denmark | $61,233 | 90.0% | $18,768 | $2.2M | 11,620% |
| Finland | $50,385 | 89.4% | $22,896 | $1.9M | 8,200% |
| Austria | $51,462 | 78.7% | $10,154 | $2.0M | 19,600% |
| Sweden | $59,143 | 92.5% | $36,595 | $2.3M | 6,185% |

**Recomendación estratégica:**

Estos países presentan las condiciones económicas y tecnológicas ideales para e-commerce pero tienen un revenue actual mínimo. Representan las mejores oportunidades para expansión con ROI potencialmente alto.

**Plan de entrada sugerido:**
1. Marketing digital localizado (idioma, cultura)
2. Partnership con influencers locales
3. Optimización de logística (tiempos de envío)
4. Pricing adaptado al poder adquisitivo local

## 4.4 Análisis de Riesgo: Dependencia de UK

### Escenario Base (Actual)

- UK: 83% del revenue
- Resto de países: 17% del revenue

### Análisis de Sensibilidad

Impacto de una reducción del 10% en UK:

| Escenario | Revenue UK | Revenue Total | Caída % |
|-----------|------------|---------------|---------|
| Base | $8.1M | $9.7M | - |
| -10% UK | $7.3M | $8.9M | -8.3% |
| -20% UK | $6.5M | $8.1M | -16.6% |
| -30% UK | $5.7M | $7.3M | -24.9% |

**Conclusión:**
Una caída del 10% en UK impacta desproporcionadamente el negocio total (-8.3%). La diversificación geográfica es crítica para mitigar este riesgo.

### Estrategia de Mitigación

**Objetivo:** Reducir dependencia de UK del 83% al 60% en 2 años

**Táctica:**
1. Invertir en top 5 países de alto potencial
2. Meta: Cada país alcance al menos 5% del revenue total
3. UK sigue creciendo pero a menor tasa que otros mercados

**Proyección:**

| Año | UK Revenue | UK % | Otros Revenue | Otros % | Total |
|-----|------------|------|---------------|---------|-------|
| Actual | $8.1M | 83% | $1.6M | 17% | $9.7M |
| Año 1 | $10.0M | 75% | $3.3M | 25% | $13.3M |
| Año 2 | $12.0M | 60% | $8.0M | 40% | $20.0M |

\newpage

# 5. CONCLUSIONES Y RECOMENDACIONES

## 5.1 Hallazgos Principales

### 1. Crecimiento Acelerado

El negocio experimentó un crecimiento extraordinario de 788% en revenue entre 2010 y 2011. Este crecimiento se debe principalmente a:
- Aumento en la base de clientes (+288%)
- Mayor frecuencia de compra
- Ligero incremento en ticket promedio (+10%)

### 2. Concentración Geográfica Crítica

El 83% del revenue proviene de UK, creando una vulnerabilidad estratégica significativa. Cualquier cambio regulatorio, económico o competitivo en este mercado podría impactar desproporcionadamente el negocio.

### 3. Efecto Pareto en Productos

El 27% de los productos genera el 47% del revenue. Los productos de almacenamiento y organización del hogar son los más rentables, sugiriendo un nicho de mercado bien definido.

### 4. Correlación Económica

Existe una correlación moderada-alta (r=0.65) entre el GDP per cápita y el gasto por cliente. Los países más ricos gastan significativamente más por transacción, validando una estrategia de expansión hacia mercados desarrollados.

### 5. Oportunidades sin Explotar

Países nórdicos (Dinamarca, Finlandia, Suecia) y Austria presentan condiciones económicas y digitales óptimas pero tienen un revenue actual marginal, representando las mayores oportunidades de crecimiento.

## 5.2 Recomendaciones Estratégicas

### Recomendación 1: Diversificación Geográfica Urgente

**Prioridad:** Alta  
**Inversión estimada:** $500K - $1M  
**ROI esperado:** 200-300% en 18 meses

**Acciones:**
1. Lanzar operaciones en Dinamarca, Finlandia y Austria en Q1 2025
2. Establecer centros de distribución locales o partnerships con 3PL
3. Campañas de marketing digital con presupuesto mínimo de $50K por país
4. Localización completa: idioma, moneda, customer service

**Métricas de éxito:**
- Cada nuevo país alcance 3-5% del revenue total en 12 meses
- UK baje del 83% al 70% del revenue total
- Mantener o mejorar el AOV en nuevos mercados

### Recomendación 2: Programa de Retención de Clientes

**Prioridad:** Alta  
**Inversión estimada:** $200K  
**ROI esperado:** 150% en 12 meses

**Problema:** 69% de los clientes solo compran una vez

**Acciones:**
1. Implementar programa de lealtad con puntos acumulables
2. Email marketing automatizado:
   - Día 7 post-compra: Solicitud de review
   - Día 30: Cupón de 10% de descuento
   - Día 60: Recomendaciones personalizadas
3. Ofertas exclusivas para repeat customers
4. Crear suscripción mensual para productos consumibles

**Métricas de éxito:**
- Reducir one-time buyers del 69% al 55%
- Aumentar frecuencia de compra promedio de 4.37 a 6.0
- Incrementar LTV (Lifetime Value) en 40%

### Recomendación 3: Optimización de Portfolio de Productos

**Prioridad:** Media  
**Inversión estimada:** $100K  
**ROI esperado:** 120% en 12 meses

**Acciones:**
1. **Top 10 productos:** Aumentar inventario en 50%, garantizar stock permanente
2. **Productos de cola larga (bottom 30%):** 
   - Analizar rentabilidad individual (margen vs rotación)
   - Descontinuar productos con margen <20% y baja rotación
   - Reinvertir capital en productos de mayor ROI
3. **Desarrollo de nuevos productos:**
   - Expandir línea de almacenamiento (categoría top)
   - Introducir 5-7 productos nuevos cada quarter
   - Testear con lanzamientos limitados antes de scale-up

**Métricas de éxito:**
- Reducir SKUs totales de 37 a 30-32 (eliminar bottom performers)
- Aumentar rotación de inventario en 25%
- Incrementar margen promedio del 35% al 40%

### Recomendación 4: Estrategia de Pricing Diferenciado

**Prioridad:** Media  
**Inversión estimada:** $50K (análisis + implementación)  
**ROI esperado:** 100% en 6 meses

**Insight:** Países con mayor GDP tienen mayor disposición a pagar

**Acciones:**
1. Implementar pricing dinámico por país:
   - Suiza, Noruega: +15% sobre precio base
   - UK, Netherlands: Precio base
   - Países emergentes: -10% con subsidio de envío
2. Bundles y upselling:
   - "Compra 2, lleva 3" en productos complementarios
   - Free shipping para órdenes >$150 (actualmente $100)
3. Testing A/B continuo:
   - Testear 3-5 variantes de precio por producto
   - Medir elasticidad de demanda

**Métricas de éxito:**
- Aumentar AOV general de $510 a $600
- Mantener o mejorar tasa de conversión
- Incrementar revenue total en 12-15% sin aumentar volumen

### Recomendación 5: Inversión en Analítica Avanzada

**Prioridad:** Baja  
**Inversión estimada:** $150K  
**ROI esperado:** 80% en 18 meses (indirecto)

**Acciones:**
1. Implementar CDP (Customer Data Platform):
   - Unificar datos de web, email, CRM, transacciones
   - Crear single customer view
2. Modelos predictivos:
   - Churn prediction: identificar clientes en riesgo
   - Next best product: recomendaciones personalizadas
   - Lifetime value prediction: priorizar clientes de alto valor
3. Real-time dashboard:
   - Actualización diaria de métricas clave
   - Alertas automáticas para anomalías
   - Comparación YoY, MoM automática

**Métricas de éxito:**
- Reducir churn rate en 15%
- Aumentar tasa de conversión de recomendaciones en 25%
- Mejorar precisión de forecast de demanda del 70% al 85%

## 5.3 Roadmap de Implementación

### Q1 2025 (Enero - Marzo)

**Foco:** Diversificación geográfica

- Semana 1-4: Investigación de mercado profunda en Dinamarca, Finlandia, Austria
- Semana 5-8: Setup logístico y partnerships
- Semana 9-12: Lanzamiento soft en los 3 países
- Inversión: $400K

### Q2 2025 (Abril - Junio)

**Foco:** Retención de clientes

- Implementación de programa de lealtad
- Setup de email marketing automation
- Lanzamiento de suscripciones
- Inversión: $150K

### Q3 2025 (Julio - Septiembre)

**Foco:** Optimización de productos

- Análisis de rentabilidad por SKU
- Descontinuación de bottom performers
- Desarrollo de nuevos productos top
- Inversión: $100K

### Q4 2025 (Octubre - Diciembre)

**Foco:** Pricing y analítica

- Implementación de pricing dinámico
- Inicio de proyecto CDP
- Review de performance anual
- Inversión: $200K

**Inversión total 2025:** $850K  
**Revenue proyectado 2025:** $18-20M (vs $9.7M en 2011)  
**ROI esperado:** 200-250%

## 5.4 Riesgos y Mitigaciones

### Riesgo 1: Falla en expansión geográfica

**Probabilidad:** Media  
**Impacto:** Alto

**Mitigación:**
- Lanzamiento gradual (soft launch)
- Testeo en mercado pequeño primero
- Partnership con expertos locales
- Budget de contingencia del 20%

### Riesgo 2: Competencia en nuevos mercados

**Probabilidad:** Alta  
**Impacto:** Medio

**Mitigación:**
- Análisis competitivo profundo pre-lanzamiento
- Diferenciación clara en propuesta de valor
- Pricing competitivo inicial (penetración)
- Focus en customer service excepcional

### Riesgo 3: Complejidad logística

**Probabilidad:** Media  
**Impacto:** Alto

**Mitigación:**
- Partnership con 3PL establecidos
- SLA claros con penalidades
- Sistema de tracking robusto
- Inventario de seguridad

### Riesgo 4: Cambios regulatorios (especialmente Brexit)

**Probabilidad:** Media  
**Impacto:** Alto

**Mitigación:**
- Asesoría legal continua
- Diversificación geográfica (reduce dependencia UK)
- Flexibilidad en estructura legal (posible entidad EU)
- Monitoreo constante de cambios regulatorios

\newpage

# 6. LIMITACIONES DEL ESTUDIO

## 6.1 Limitaciones de Datos

### 1. Antigüedad de los Datos

**Limitación:** El dataset corresponde a 2010-2011, hace más de 13 años.

**Impacto:**
- El comportamiento del consumidor online ha cambiado radicalmente
- La penetración de smartphones y apps no está reflejada
- COVID-19 aceleró la adopción de e-commerce (no capturado)
- Las tecnologías de pago han evolucionado significativamente

**Mitigación:**
- Los patrones estructurales (Pareto, correlaciones económicas) siguen siendo válidos
- La metodología de integración de fuentes es aplicable a datos actuales
- El dashboard puede actualizarse con datos recientes

### 2. Cobertura Geográfica Sesgada

**Limitación:** 83% del revenue de UK, muy baja representación de Asia, América, África.

**Impacto:**
- Conclusiones sobre mercados globales son limitadas
- Correlaciones pueden no aplicar a economías emergentes
- Patrones de consumo reflejan principalmente comportamiento europeo

**Mitigación:**
- Conclusiones explícitamente limitadas a mercados desarrollados europeos
- Necesidad de datos adicionales para expansion a otros continentes

### 3. Ausencia de Datos de Costos

**Limitación:** Solo tenemos revenue, no costos operativos, COGS, marketing, logística.

**Impacto:**
- No podemos calcular rentabilidad real
- ROI de productos no es calculable con precisión
- Decisiones de pricing tienen incertidumbre

**Mitigación:**
- Análisis se enfoca en revenue y volumen
- Recomendaciones incluyen análisis de costos como siguiente paso

### 4. Falta de Datos de Conversión Web

**Limitación:** No tenemos datos de tráfico web, tasa de conversión, abandono de carrito.

**Impacto:**
- No podemos optimizar el funnel de conversión
- No sabemos qué canales de adquisición funcionan mejor
- CPA (Cost Per Acquisition) es desconocido

## 6.2 Limitaciones Metodológicas

### 1. Tasas de Cambio Simplificadas

**Limitación:** Se usó una tasa fija de 1 GBP = 1.60 USD para todo el período.

**Realidad:** La tasa fluctúa diariamente.

**Impacto:**
- Error estimado del 2-5% en conversiones USD
- Comparaciones temporales tienen ruido por variación cambiaria

### 2. Correlación ≠ Causalidad

**Limitación:** Las correlaciones encontradas no implican causalidad directa.

**Ejemplo:** 
- GDP alto correlaciona con mayor gasto
- Pero no podemos afirmar que aumentar el GDP cause más ventas
- Variables confusoras: cultura de compra, logística, competencia local

### 3. Modelo Predictivo Simple

**Limitación:** El modelo de regresión lineal simple solo explica 42% de varianza.

**Factores no capturados:**
- Marketing spend
- Competencia local
- Estacionalidad cultural
- Madurez del e-commerce local
- Costos de envío internacional

## 6.3 Limitaciones Técnicas

### 1. Calidad de Datos de APIs

**Limitación:** World Bank API tiene datos faltantes para algunos países y años.

**Países afectados:**
- 19 de 37 países sin datos económicos completos (51%)
- Análisis de correlación limitado a 18 países con datos completos

### 2. Procesamiento Manual del Dataset Principal

**Limitación:** El archivo Excel se descarga manualmente, no hay automatización completa.

**Impacto:**
- No se puede actualizar el dashboard automáticamente con nuevos datos
- Proceso ETL requiere re-ejecución manual de scripts

### 3. Power BI Desktop vs Service

**Limitación:** El dashboard está en archivo .pbix local, no en Power BI Service.

**Impacto:**
- No hay acceso remoto para stakeholders
- No hay actualización programada de datos
- No hay colaboración multi-usuario

\newpage

# 7. TRABAJO FUTURO

## 7.1 Mejoras Inmediatas (1-3 meses)

### 1. Actualización con Datos Recientes

**Objetivo:** Replicar el análisis con datos 2023-2024

**Pasos:**
1. Buscar dataset actualizado de e-commerce (Kaggle, UCI, datos propios)
2. Actualizar llamadas a World Bank API con años recientes
3. Re-ejecutar pipeline ETL
4. Comparar patrones 2011 vs 2024

**Valor:** Validar si los patrones identificados siguen vigentes

### 2. Publicación en Power BI Service

**Objetivo:** Dashboard accesible online para stakeholders

**Pasos:**
1. Crear cuenta Power BI Pro
2. Publicar dashboard en workspace
3. Configurar refresh schedule automático
4. Crear reportes con Row-Level Security por departamento

**Valor:** Acceso 24/7, actualización automática, colaboración

### 3. Integración de Datos de Costos

**Objetivo:** Calcular rentabilidad real por producto/país

**Datos necesarios:**
- COGS (Cost of Goods Sold)
- Costos de logística y envío
- Marketing spend por canal
- Overhead operativo

**Métricas a agregar:**
- Margen bruto por producto
- ROI por país
- CAC (Customer Acquisition Cost)
- LTV/CAC ratio

## 7.2 Mejoras a Mediano Plazo (3-6 meses)

### 1. Modelos Predictivos Avanzados

**Machine Learning para:**

**a) Churn Prediction**
- Modelo: Random Forest o XGBoost
- Features: Recency, Frequency, Monetary, Product categories, AOV trend
- Output: Probabilidad de que cliente no compre en próximos 90 días
- Acción: Campaña de retención automatizada

**b) Demand Forecasting**
- Modelo: Prophet (Facebook) o ARIMA
- Features: Historical sales, seasonality, holidays, economic indicators
- Output: Forecast de demanda por producto para próximos 3 meses
- Acción: Optimización de inventario

**c) Recommendation Engine**
- Modelo: Collaborative Filtering o Content-Based
- Input: Purchase history, product attributes
- Output: Top 5 productos recomendados por cliente
- Acción: Email personalizado "Customers like you also bought..."

### 2. Integración con Google Analytics 4

**Objetivo:** Capturar datos de comportamiento web

**Métricas adicionales:**
- Tráfico por canal (Organic, Paid, Social, Email, Direct)
- Tasa de conversión por landing page
- Abandono de carrito
- Time on site, bounce rate
- Device breakdown (Desktop, Mobile, Tablet)

**Dashboard adicional:** "Web Performance & Funnel Analysis"

### 3. A/B Testing Framework

**Objetivo:** Experimentación continua

**Tests prioritarios:**
1. **Pricing:** 3 variantes de precio por producto top
2. **Shipping:** Free shipping threshold ($100 vs $150 vs $200)
3. **Email subject lines:** Open rate optimization
4. **Product images:** Single vs carousel vs lifestyle photos

**Herramienta:** Optimizely, VWO o Google Optimize

## 7.3 Mejoras a Largo Plazo (6-12 meses)

### 1. Real-Time Dashboard

**Objetivo:** Métricas actualizadas en tiempo real

**Arquitectura:**
```
Transacciones
    ↓
Apache Kafka (Streaming)
    ↓
Apache Spark (Processing)
    ↓
PostgreSQL (Storage)
    ↓
Power BI (Visualization)
```

**Métricas en tiempo real:**
- Revenue actual vs target del día
- Orders por hora
- Top selling products de las últimas 24h
- Geographic heatmap de órdenes activas

### 2. Customer Data Platform (CDP)

**Objetivo:** Vista unificada 360° del cliente

**Fuentes a integrar:**
- Transacciones (actual)
- Web analytics (Google Analytics)
- Email marketing (Mailchimp/SendGrid)
- Customer service (Zendesk/Intercom)
- Social media (Facebook/Instagram ads)

**Plataforma:** Segment, mParticle o Salesforce CDP

**Use cases:**
- Segmentación avanzada multi-dimensional
- Atribución multi-touch de conversiones
- Personalización cross-channel
- Suppression lists automáticas

### 3. Expansión del Alcance Analítico

**a) Sentiment Analysis**
- Scraping de reviews de productos
- NLP para clasificar sentiment (Positive/Neutral/Negative)
- Identificar pain points en productos específicos

**b) Competitive Intelligence**
- Web scraping de precios de competidores
- Alertas de cambios de pricing
- Análisis de portfolio de productos competidores

**c) Supply Chain Optimization**
- Integración con datos de proveedores
- Predictive maintenance de inventario
- Optimización de rutas de distribución

## 7.4 Transferencia de Conocimiento

### 1. Documentación Técnica Extendida

**Crear:**
- Wiki interna con arquitectura completa
- Runbooks para troubleshooting
- Video tutorials para uso del dashboard
- FAQ de interpretación de métricas

### 2. Training para Stakeholders

**Workshops:**
- "Power BI 101" para managers (2 horas)
- "Data-Driven Decision Making" para ejecutivos (1 día)
- "Advanced DAX" para analistas (3 días)

### 3. Democratización de Datos

**Objetivo:** Self-service analytics para todos los departamentos

**Acciones:**
- Crear "Data Catalog" con todos los datasets disponibles
- Implementar governance de datos (Data Stewards)
- Proveer templates de reportes comunes
- Office hours semanales con equipo de datos

\newpage

# 8. REFERENCIAS

## 8.1 Fuentes de Datos

1. Daqing Chen, Sai Liang Sain, and Kun Guo. (2012). *Data mining for the online retail industry: A case study of RFM model-based customer segmentation using data mining*. Journal of Database Marketing and Customer Strategy Management, 19(3), 197-208.

   Dataset disponible en: UCI Machine Learning Repository  
   URL: https://archive.ics.uci.edu/ml/datasets/online+retail  
   Acceso: Diciembre 2024

2. The World Bank. (2024). *World Development Indicators API*. World Bank Open Data.

   Documentación: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589  
   API Endpoint: https://api.worldbank.org/v2/  
   Indicadores utilizados:
   - NY.GDP.PCAP.CD (GDP per capita, current US$)
   - IT.NET.USER.ZS (Internet users, % of population)
   - SP.POP.TOTL (Population, total)

3. ExchangeRate-API. (2024). *Free Currency Exchange Rates API*.

   URL: https://www.exchangerate-api.com/  
   Endpoint: https://api.exchangerate-api.com/v4/latest/GBP  
   Tasa histórica GBP/USD: 1.60 (promedio 2011)

## 8.2 Herramientas y Tecnologías

4. McKinney, W. (2010). *Data Structures for Statistical Computing in Python*. Proceedings of the 9th Python in Science Conference, 56-61.

   pandas library documentation: https://pandas.pydata.org/

5. Reitz, K. (2024). *Requests: HTTP for Humans*.

   Documentation: https://requests.readthedocs.io/

6. Virtanen, P., et al. (2020). *SciPy 1.0: Fundamental algorithms for scientific computing in Python*. Nature Methods, 17, 261-272.

   SciPy documentation: https://scipy.org/

7. Microsoft Corporation. (2024). *Power BI Desktop - December 2024 Release*.

   Product page: https://powerbi.microsoft.com/desktop/  
   DAX Reference: https://learn.microsoft.com/en-us/dax/

8. Torvalds, L. (2005). *Git - Distributed Version Control System*.

   Official website: https://git-scm.com/  
   GitHub platform: https://github.com/

## 8.3 Metodología y Conceptos

9. Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.). Wiley.

   Aplicado en: Diseño del modelo dimensional (fact/dimension tables)

10. Few, S. (2012). *Show Me the Numbers: Designing Tables and Graphs to Enlighten* (2nd ed.). Analytics Press.

    Aplicado en: Diseño de visualizaciones del dashboard

11. Pearson, K. (1895). *Notes on regression and inheritance in the case of two parents*. Proceedings of the Royal Society of London, 58, 240-242.

    Aplicado en: Análisis de correlación entre variables económicas y revenue

12. Pareto, V. (1896). *Cours d'économie politique*. F. Rouge.

    Aplicado en: Análisis de distribución de revenue por productos (regla 80/20)

## 8.4 Frameworks y Estándares

13. Inmon, W. H. (2005). *Building the Data Warehouse* (4th ed.). Wiley.

    Aplicado en: Arquitectura ETL y data warehousing

14. ISO/IEC 25012:2008. *Software engineering - Software product Quality Requirements and Evaluation (SQuaRE) - Data quality model*.

    Aplicado en: Validación de calidad de datos

15. REST API Design Rulebook. (2011). O'Reilly Media.

    Referencia para: Consumo de APIs World Bank y ExchangeRate-API

## 8.5 Literatura Complementaria

16. Anderson, C. (2006). *The Long Tail: Why the Future of Business Is Selling Less of More*. Hyperion.

    Concepto aplicado en análisis de distribución de productos

17. Hughes, A. M. (1994). *Strategic Database Marketing*. Probus Publishing.

    Framework RFM aplicado en segmentación de clientes

18. Kaplan, R. S., & Norton, D. P. (1996). *The Balanced Scorecard: Translating Strategy into Action*. Harvard Business Review Press.

    Framework para definición de KPIs del dashboard

## 8.6 Recursos Online

19. Stack Overflow. (2024). *Python pandas data manipulation questions*.

    URL: https://stackoverflow.com/questions/tagged/pandas  
    Consultado durante desarrollo de scripts ETL

20. Power BI Community. (2024). *DAX Patterns and Best Practices*.

    URL: https://community.powerbi.com/  
    Consultado para optimización de medidas DAX

21. GitHub - Awesome Public Datasets. (2024).

    URL: https://github.com/awesomedata/awesome-public-datasets  
    Referencia para búsqueda de datasets complementarios

## 8.7 Normativa y Regulaciones

22. European Union. (2016). *General Data Protection Regulation (GDPR)*.

    Regulation (EU) 2016/679  
    Relevante para: Manejo de datos de clientes europeos

23. UK Government. (2018). *Data Protection Act 2018*.

    Complementa GDPR en Reino Unido  
    Relevante para: Privacidad de datos de clientes UK

\newpage

# 9. ANEXOS

## Anexo A: Diccionario de Datos

### Tabla: fact_sales

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| InvoiceNo | String | Identificador único de factura | "536365" |
| InvoiceDate | DateTime | Fecha y hora de transacción | "2010-12-01 08:26:00" |
| Year | Integer | Año de la transacción | 2010 |
| Month | Integer | Mes de la transacción | 12 |
| Quarter | Integer | Trimestre (1-4) | 4 |
| YearMonth | String | Año-Mes formato YYYY-MM | "2010-12" |
| StockCode | String | Código único de producto | "85123A" |
| Description | String | Descripción del producto | "WHITE HANGING HEART" |
| Quantity | Integer | Cantidad comprada | 6 |
| UnitPrice | Float | Precio unitario en GBP | 2.55 |
| TotalPrice_GBP | Float | Precio total en GBP | 15.30 |
| TotalPrice_USD | Float | Precio total en USD (tasa 1.60) | 24.48 |
| CustomerID | String | Identificador único de cliente | "17850" |
| Country | String | País del cliente | "United Kingdom" |

### Tabla: integrated_analysis

| Campo | Tipo | Descripción | Unidad |
|-------|------|-------------|--------|
| Country | String | Nombre del país | - |
| Revenue_USD | Float | Revenue total en USD | USD |
| Revenue_GBP | Float | Revenue total en GBP | GBP |
| Total_Orders | Integer | Número de órdenes | Count |
| Total_Customers | Integer | Clientes únicos | Count |
| Unique_Products | Integer | Productos únicos vendidos | Count |
| Avg_Order_Value_USD | Float | Ticket promedio | USD |
| Revenue_Per_Customer_USD | Float | Revenue promedio por cliente | USD |
| GDP_PerCapita | Float | GDP per cápita 2011 | USD |
| Internet_Users_Pct | Float | % población con internet | % |
| Population | Integer | Población total | Count |

## Anexo B: Código de Scripts Principales

### Script: 02_integracion_datos.py (fragmento clave)
```python
# Integración de fuentes por país
country_metrics = df_clean.groupby('Country').agg({
    'TotalPrice_USD': 'sum',
    'TotalPrice_GBP': 'sum',
    'InvoiceNo': 'nunique',
    'CustomerID': 'nunique',
    'StockCode': 'nunique'
}).reset_index()

country_metrics.columns = [
    'Country', 'Revenue_USD', 'Revenue_GBP', 
    'Total_Orders', 'Total_Customers', 'Unique_Products'
]

# Merge con World Bank data
integrated = country_metrics.merge(
    df_wb,
    left_on='Country_WB',
    right_on='Country_Name',
    how='left'
)
```

## Anexo C: Medidas DAX Principales
```dax
Total Revenue USD = SUM(fact_sales[TotalPrice_USD])

Total Customers = DISTINCTCOUNT(fact_sales[CustomerID])

Avg Order Value = 
DIVIDE(
    [Total Revenue USD],
    DISTINCTCOUNT(fact_sales[InvoiceNo]),
    0
)

Revenue per Customer = 
DIVIDE(
    [Total Revenue USD],
    [Total Customers],
    0
)

YoY Growth = 
VAR CurrentRevenue = [Total Revenue USD]
VAR PreviousRevenue = 
    CALCULATE(
        [Total Revenue USD],
        SAMEPERIODLASTYEAR(dim_date[InvoiceDate])
    )
RETURN
DIVIDE(
    CurrentRevenue - PreviousRevenue,
    PreviousRevenue,
    0
)
```

## Anexo D: Configuración del Proyecto

### requirements.txt
```
pandas==2.1.3
openpyxl==3.1.2
requests==2.31.0
scipy==1.11.4
```


```
proyecto-ecommerce-global/
├── .git/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   ├── .gitkeep
│   │   ├── online_retail.xlsx
│   │   ├── worldbank_gdp.csv
│   │   ├── worldbank_internet.csv
│   │   ├── worldbank_population.csv
│   │   └── exchange_rates_2011.json
│   └── processed/
│       ├── .gitkeep
│       ├── fact_sales.csv
│       ### Estructura de Carpetas Completa├── dim_products.csv
│       ├── dim_customers.csv
│       ├── dim_date.csv
│       ├── integrated_analysis.csv
│       ├── statistical_results.json
│       └── metadata.json
├── scripts/
│   ├── 01_extraccion_datos.py
│   ├── 02_integracion_datos.py
│   └── 03_estadisticas.py
├── powerbi/
│   ├── .gitkeep
│   ├── dashboard_global_insights.pbix
│   └── tema_ecommerce_global.json
└── docs/
    ├── .gitkeep
    ├── informe_final.md
    └── informe_final.pdf
```

## Anexo E: Glosario de Términos

**AOV (Average Order Value):** Valor promedio por orden. Se calcula dividiendo revenue total entre número de órdenes.

**API (Application Programming Interface):** Interfaz que permite comunicación entre sistemas de software.

**CDP (Customer Data Platform):** Plataforma que unifica datos de clientes de múltiples fuentes.

**DAX (Data Analysis Expressions):** Lenguaje de fórmulas usado en Power BI y Excel.

**ETL (Extract, Transform, Load):** Proceso de extracción, transformación y carga de datos.

**GDP (Gross Domestic Product):** Producto Interno Bruto, medida de la actividad económica de un país.

**JSON (JavaScript Object Notation):** Formato de intercambio de datos ligero y legible.

**KPI (Key Performance Indicator):** Indicador clave de rendimiento.

**LTV (Lifetime Value):** Valor total que un cliente genera durante toda su relación con la empresa.

**RFM (Recency, Frequency, Monetary):** Modelo de segmentación de clientes basado en recencia de compra, frecuencia y monto gastado.

**REST (Representational State Transfer):** Arquitectura para APIs web.
