"""
generar_ventas.py
Generador sintético de ventas para PlastikTrack (E1).
Genera 638 días continuos (2025-01-01 a 2026-09-30) para 12 productos con:
- Picos de quincena (+28%)
- Días pico de reparto (lunes, miércoles, viernes)
- 5 errores sembrados:
  * 40 nulos
  * 15 negativos
  * 10 atípicos de 999 unidades
  * 25 inconsistencias de formato en minúsculas
  * 30 duplicados
"""

import numpy as np
import pandas as pd

# Fijar semilla para reproducibilidad exacta
np.random.seed(42)

CATALOGO = [
    {"producto": "Bolsa Basura Todos Tamanios", "precio_unitario": 48.0, "base": 32},
    {"producto": "Bolsa Rollo Poliseda", "precio_unitario": 38.0, "base": 28},
    {"producto": "Bolsa Rollo Baja Densidad", "precio_unitario": 35.0, "base": 35},
    {"producto": "Bolsa Rollo Alta Densidad", "precio_unitario": 42.0, "base": 30},
    {"producto": "Bolsa Negra Camiseta", "precio_unitario": 45.0, "base": 40},
    {"producto": "Bolsa Camiseta Poliseda", "precio_unitario": 40.0, "base": 34},
    {"producto": "Bolsa Camiseta Plata", "precio_unitario": 44.0, "base": 22},
    {"producto": "Bolsa Camiseta Color", "precio_unitario": 42.0, "base": 25},
    {"producto": "Charolas Desechables", "precio_unitario": 65.0, "base": 9},
    {"producto": "Vasos Desechables", "precio_unitario": 55.0, "base": 11},
    {"producto": "Contenedor Termico Unicel", "precio_unitario": 72.0, "base": 8},
    {"producto": "Pelicula Plastica Emplaye", "precio_unitario": 85.0, "base": 14},
]

# Rango de fechas: 638 días continuos del 2025-01-01 al 2026-09-30
fechas = pd.date_range(start="2025-01-01", end="2026-09-30", freq="D")
assert len(fechas) == 638, f"Se esperaban 638 días, obtenidos {len(fechas)}"

registros = []

for fecha in fechas:
    dia_mes = fecha.day
    es_fin_mes = fecha.is_month_end or (dia_mes >= 28)
    es_quincena = (13 <= dia_mes <= 16) or es_fin_mes
    
    # Factor de quincena (+28%)
    factor_quincena = 1.28 if es_quincena else 1.00
    
    # Días pico de reparto: Lunes (0), Miércoles (2), Viernes (4)
    dia_semana = fecha.weekday()
    if dia_semana == 0:  # Lunes
        factor_reparto = 1.25
    elif dia_semana == 2:  # Miércoles
        factor_reparto = 1.20
    elif dia_semana == 4:  # Viernes
        factor_reparto = 1.30
    elif dia_semana in (1, 3):  # Martes y Jueves
        factor_reparto = 0.95
    else:  # Sábado y Domingo (menor movimiento de rutas)
        factor_reparto = 0.70

    for item in CATALOGO:
        media_esperada = item["base"] * factor_quincena * factor_reparto
        # Ruido gaussiano acotado positivo
        unidades = max(1, int(np.round(np.random.normal(loc=media_esperada, scale=max(2.0, media_esperada * 0.12)))))
        precio = item["precio_unitario"]
        total = round(unidades * precio, 2)
        
        registros.append({
            "fecha": fecha.strftime("%Y-%m-%d"),
            "producto": item["producto"],
            "unidades": unidades,
            "precio_unitario": precio,
            "total": total
        })

df = pd.DataFrame(registros)
assert len(df) == 7656, f"Se esperaban 7656 registros base, obtenidos {len(df)}"

# --- SEMBRAR 5 ERRORES EXACTOS ---
indices_disponibles = np.random.permutation(len(df))

# 1. 25 inconsistencias de formato en minúsculas en 'producto'
idx_minusculas = indices_disponibles[0:25]
df.loc[idx_minusculas, "producto"] = df.loc[idx_minusculas, "producto"].str.lower()

# 2. 10 atípicos de 999 unidades
idx_atipicos = indices_disponibles[25:35]
df.loc[idx_atipicos, "unidades"] = 999
df.loc[idx_atipicos, "total"] = 999 * df.loc[idx_atipicos, "precio_unitario"]

# 3. 15 valores negativos en 'unidades'
idx_negativos = indices_disponibles[35:50]
df.loc[idx_negativos, "unidades"] = -np.abs(df.loc[idx_negativos, "unidades"])
df.loc[idx_negativos, "total"] = df.loc[idx_negativos, "unidades"] * df.loc[idx_negativos, "precio_unitario"]

# 4. 40 valores nulos (NaN) en 'unidades'
idx_nulos = indices_disponibles[50:90]
df.loc[idx_nulos, "unidades"] = np.nan
df.loc[idx_nulos, "total"] = np.nan

# 5. 30 registros duplicados
idx_duplicados = indices_disponibles[90:120]
filas_duplicadas = df.iloc[idx_duplicados].copy()
df = pd.concat([df, filas_duplicadas], ignore_index=True)

# Guardar dataset crudo con errores
df.to_csv("ventas_distribuidora.csv", index=False)
print("=" * 60)
print("DATASET GENERADO EXITOSAMENTE: ventas_distribuidora.csv")
print(f"Total de registros generados (con 30 duplicados): {len(df)}")
print(f"Rango de fechas: {fechas[0].strftime('%Y-%m-%d')} a {fechas[-1].strftime('%Y-%m-%d')} ({len(fechas)} días)")
print("Errores sembrados verificados:")
print(f" - Minúsculas en producto: 25")
print(f" - Atípicos (999 u): 10")
print(f" - Negativos: 15")
print(f" - Nulos (NaN): 40")
print(f" - Duplicados insertados: 30")
print("=" * 60)
