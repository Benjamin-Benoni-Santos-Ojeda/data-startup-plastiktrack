"""
limpiar_datos.py
Pipeline de limpieza y calidad de datos para PlastikTrack (E1).
Corrige los 5 errores sembrados en ventas_distribuidora.csv:
1. Elimina duplicados.
2. Estandariza nombres de producto a formato Título.
3. Corrige unidades negativas a positivas.
4. Acota atípicos (>=500) a la mediana por producto.
5. Imputa valores nulos con la mediana por producto.
6. Recalcula el total = unidades * precio_unitario.
7. Guarda ventas_limpias.csv en raíz y data/sample/ventas_sample.csv (100 filas).
"""

import os
import pandas as pd
import numpy as np

def limpiar_datos():
    archivo_origen = "ventas_distribuidora.csv"
    if not os.path.exists(archivo_origen):
        raise FileNotFoundError(f"No se encontró el archivo {archivo_origen}. Ejecuta primero generar_ventas.py.")

    df_crudo = pd.read_csv(archivo_origen)
    total_inicial = len(df_crudo)

    # 1. Eliminar duplicados
    duplicados_detectados = int(df_crudo.duplicated().sum())
    df = df_crudo.drop_duplicates().copy().reset_index(drop=True)
    total_sin_duplicados = len(df)

    # 2. Estandarizar nombres a formato título
    mascara_minusculas = df["producto"] != df["producto"].str.title()
    inconsistencias_nombre = int(mascara_minusculas.sum())
    df["producto"] = df["producto"].str.title()

    # 3. Corregir negativos a positivos
    mascara_negativos = df["unidades"] < 0
    negativos_detectados = int(mascara_negativos.sum())
    df.loc[mascara_negativos, "unidades"] = df.loc[mascara_negativos, "unidades"].abs()

    # 4. Calcular medianas por producto para acotar atípicos e imputar nulos
    # Excluimos atípicos (>=500) y nulos para calcular la mediana representativa
    valores_validos = df[(df["unidades"] < 500) & (df["unidades"].notna()) & (df["unidades"] > 0)]
    medianas_producto = valores_validos.groupby("producto")["unidades"].median().round().to_dict()

    # 4.1 Acotar atípicos (>= 500)
    mascara_atipicos = df["unidades"] >= 500
    atipicos_detectados = int(mascara_atipicos.sum())
    for prod, mediana in medianas_producto.items():
        filtro = mascara_atipicos & (df["producto"] == prod)
        df.loc[filtro, "unidades"] = mediana

    # 5. Imputar nulos con la mediana por producto
    mascara_nulos = df["unidades"].isna()
    nulos_detectados = int(mascara_nulos.sum())
    for prod, mediana in medianas_producto.items():
        filtro = mascara_nulos & (df["producto"] == prod)
        df.loc[filtro, "unidades"] = mediana

    # Convertir unidades a entero
    df["unidades"] = df["unidades"].astype(int)

    # 6. Recalcular total = unidades * precio_unitario
    df["total"] = (df["unidades"] * df["precio_unitario"]).round(2)

    # Verificaciones finales
    assert len(df) == 7656, f"Error: Se esperaban 7,656 registros limpios, se obtuvieron {len(df)}"
    assert df["unidades"].isna().sum() == 0, "Error: Quedaron nulos en unidades"
    assert (df["unidades"] <= 0).sum() == 0, "Error: Quedaron unidades <= 0"
    assert (df["unidades"] >= 500).sum() == 0, "Error: Quedaron atípicos >= 500"

    # Guardar ventas_limpias.csv en la raíz
    df.to_csv("ventas_limpias.csv", index=False)

    # Guardar data/sample/ventas_sample.csv con 100 filas
    os.makedirs("data/sample", exist_ok=True)
    sample_df = df.head(100).copy()
    sample_df.to_csv("data/sample/ventas_sample.csv", index=False)

    # Imprimir reporte detallado en terminal
    print("=" * 65)
    print("           REPORTE OFICIAL DE LIMPIEZA DE DATOS (E1)")
    print("                      PLASTIKTRACK")
    print("=" * 65)
    print(f"Filas iniciales (con errores):             {total_inicial}")
    print(f"1. Registros duplicados eliminados:        {duplicados_detectados}")
    print(f"2. Formatos de producto estandarizados:    {inconsistencias_nombre}")
    print(f"3. Valores negativos corregidos a positivo:{negativos_detectados}")
    print(f"4. Valores atípicos (>=500) acotados:      {atipicos_detectados}")
    print(f"5. Valores nulos imputados con mediana:    {nulos_detectados}")
    print(f"6. Recálculo 'total = unidades * precio':  Completado al 100%")
    print("-" * 65)
    print(f"Total de registros finales limpios:        {len(df)}")
    print(f"Dataset limpio guardado en:                ventas_limpias.csv")
    print(f"Muestra (100 filas) guardada en:           data/sample/ventas_sample.csv")
    print("=" * 65)

if __name__ == "__main__":
    limpiar_datos()
