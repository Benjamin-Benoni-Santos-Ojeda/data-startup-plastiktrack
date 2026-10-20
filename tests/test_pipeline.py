"""
tests/test_pipeline.py
Pruebas automatizadas de consistencia de datos y reglas de calidad para PlastikTrack.
"""

import os
import pandas as pd
import numpy as np

def test_ventas_limpias_integridad():
    ruta = "ventas_limpias.csv"
    assert os.path.exists(ruta), f"No existe el archivo {ruta}"
    
    df = pd.read_csv(ruta)
    
    # 1. Dimensión esperada: 638 días * 12 productos = 7,656 registros
    assert len(df) == 7656, f"Se esperaban 7656 registros, se obtuvieron {len(df)}"
    
    # 2. Sin nulos en ninguna columna
    assert df.isna().sum().sum() == 0, "Existen valores nulos en el dataset limpio"
    
    # 3. Sin duplicados
    assert df.duplicated().sum() == 0, "Existen registros duplicados en el dataset limpio"
    
    # 4. Unidades estrictamente positivas y acotadas (< 500)
    assert (df["unidades"] <= 0).sum() == 0, "Existen valores negativos o cero en unidades"
    assert (df["unidades"] >= 500).sum() == 0, "Existen valores atípicos (>=500) sin acotar"
    
    # 5. Estandarización de formato título
    assert (df["producto"] != df["producto"].str.title()).sum() == 0, "Hay productos sin formato Título"
    
    # 6. Recálculo exacto del total
    totales_esperados = (df["unidades"] * df["precio_unitario"]).round(2)
    assert np.allclose(df["total"], totales_esperados), "El total no coincide con unidades * precio_unitario"

def test_sample_dataset():
    ruta = "data/sample/ventas_sample.csv"
    assert os.path.exists(ruta), f"No existe el archivo de muestra {ruta}"
    df_sample = pd.read_csv(ruta)
    assert len(df_sample) == 100, f"La muestra debe tener 100 filas, tiene {len(df_sample)}"

if __name__ == "__main__":
    test_ventas_limpias_integridad()
    test_sample_dataset()
    print("Todas las pruebas pasaron exitosamente.")
