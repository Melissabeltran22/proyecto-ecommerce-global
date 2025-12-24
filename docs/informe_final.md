---
title: "Análisis Global de E-Commerce: Integración de Múltiples Fuentes de Datos"
author: "Eilen Melissa Beltran Colon"
date: "Diciembre 2025"
subtitle: "Especialización en Analítica de Datos y Big Data"
institution: "Universidad de Cataluña"
---

\newpage

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
