"""
limpiar_datos.py
Pipeline de limpieza y calidad de datos para PlastikTrack (E1).
Corrige las anomalías identificadas en ventas_distribuidora.csv:
1. Elimina registros duplicados (subset fecha + producto).
2. Estandariza nombres de producto a formato Título y remueve espacios sobrantes.
3. Corrige unidades negativas a valores absolutos positivos.
4. Acota atípicos contextuales (>=500 o ratio > 3x vs mediana de grupo) a la mediana representativa.
5. Imputa valores nulos en unidades (con mediana de producto × día × quincena) y en precio_unitario (ffill/bfill).
6. Recalcula el total consistente = unidades * precio_unitario.
7. Guarda ventas_limpias.csv en raíz y data/sample/ventas_sample.csv (100 filas).
"""

import os
import pandas as pd
import numpy as np

def limpiar_datos():
    archivo_origen = "ventas_distribuidora.csv"
    if not os.path.exists(archivo_origen):
        raise FileNotFoundError(f"No se encontró el archivo {archivo_origen}.")

    df_crudo = pd.read_csv(archivo_origen)
    total_inicial = len(df_crudo)

    # 1. Estandarizar nombres a formato título y remover espacios
    df_crudo["producto_std"] = df_crudo["producto"].str.strip().str.title()
    inconsistencias_nombre = int((df_crudo["producto"] != df_crudo["producto_std"]).sum())

    df = df_crudo.copy()
    df["producto"] = df["producto_std"]
    df["fecha"] = pd.to_datetime(df["fecha"])

    # 2. Eliminar duplicados por clave de negocio (fecha + producto)
    duplicados_detectados = int(df.duplicated(subset=["fecha", "producto"], keep="first").sum())
    df = df.drop_duplicates(subset=["fecha", "producto"], keep="first").sort_values(["fecha", "producto"]).reset_index(drop=True)

    # 3. Corregir negativos a positivos
    mascara_negativos = df["unidades"] < 0
    negativos_detectados = int(mascara_negativos.sum())
    df.loc[mascara_negativos, "unidades"] = df.loc[mascara_negativos, "unidades"].abs()

    # Variables de calendario para agrupamiento contextual
    df["dia_semana"] = df["fecha"].dt.weekday
    df["dia_mes"] = df["fecha"].dt.day
    df["es_quincena"] = (df["dia_mes"].between(13, 16) | (df["dia_mes"] >= 28)).astype(int)

    # 4. Detección y acotamiento de atípicos contextuales
    keys = ["producto", "dia_semana", "es_quincena"]
    validos = df[df["unidades"].notna() & (df["unidades"] > 0) & (df["unidades"] < 500)]
    med_grupo = validos.groupby(keys)["unidades"].median().rename("mediana_grupo").reset_index()
    df = df.drop(columns=["mediana_grupo"], errors="ignore").merge(med_grupo, on=keys, how="left")
    df["ratio_vs_grupo"] = df["unidades"] / df["mediana_grupo"]

    df["atipico_ctx"] = (df["unidades"] >= 500) | (df["ratio_vs_grupo"] > 3)
    atipicos_detectados = int(df["atipico_ctx"].sum())

    # 5. Imputar nulos y atípicos en unidades
    nulos_unidades = int(df["unidades"].isna().sum())
    nulos_precio = int(df["precio_unitario"].isna().sum())

    df["fue_imputado"] = (df["unidades"].isna() | df["atipico_ctx"]).astype(int)
    reemplazo = df["mediana_grupo"].fillna(df.groupby("producto")["unidades"].transform("median")).round()
    df.loc[df["fue_imputado"] == 1, "unidades"] = reemplazo[df["fue_imputado"] == 1]
    df["unidades"] = df["unidades"].astype(int)

    # Imputar nulos en precio_unitario (ffill + bfill por producto)
    df = df.sort_values(["producto", "fecha"])
    df["precio_unitario"] = df.groupby("producto")["precio_unitario"].transform(lambda s: s.ffill().bfill())
    df = df.sort_values(["fecha", "producto"]).reset_index(drop=True)

    # 6. Recalcular total = unidades * precio_unitario
    df["total"] = (df["unidades"] * df["precio_unitario"]).round(2)

    # Formatear columnas finales
    columnas_finales = ["fecha", "producto", "unidades", "precio_unitario", "total"]
    df_final = df[columnas_finales].copy()
    df_final["fecha"] = df_final["fecha"].dt.strftime("%Y-%m-%d")

    # Verificaciones de calidad
    assert len(df_final) == 16428, f"Error: Se esperaban 16,428 registros limpios, se obtuvieron {len(df_final)}"
    assert df_final["unidades"].isna().sum() == 0, "Error: Quedaron nulos en unidades"
    assert df_final["precio_unitario"].isna().sum() == 0, "Error: Quedaron nulos en precio_unitario"
    assert (df_final["unidades"] <= 0).sum() == 0, "Error: Quedaron unidades <= 0"
    assert (df_final["unidades"] >= 500).sum() == 0, "Error: Quedaron atípicos >= 500"

    # Guardar ventas_limpias.csv en la raíz
    df_final.to_csv("ventas_limpias.csv", index=False)

    # Guardar data/sample/ventas_sample.csv con 100 filas
    os.makedirs("data/sample", exist_ok=True)
    sample_df = df_final.head(100).copy()
    sample_df.to_csv("data/sample/ventas_sample.csv", index=False)

    # Imprimir reporte detallado en terminal
    print("=" * 65)
    print("           REPORTE OFICIAL DE LIMPIEZA DE DATOS (E1)")
    print("                      PLASTIKTRACK")
    print("=" * 65)
    print(f"Filas iniciales crudas:                    {total_inicial}")
    print(f"1. Registros duplicados eliminados:        {duplicados_detectados}")
    print(f"2. Formatos de producto estandarizados:    {inconsistencias_nombre}")
    print(f"3. Valores negativos corregidos a positivo:{negativos_detectados}")
    print(f"4. Valores atípicos contextuales acotados: {atipicos_detectados}")
    print(f"5. Nulos en unidades imputados:            {nulos_unidades}")
    print(f"   Nulos en precio imputados (ffill/bfill):{nulos_precio}")
    print(f"6. Recálculo 'total = unidades * precio':  Completado al 100%")
    print("-" * 65)
    print(f"Total de registros finales limpios:        {len(df_final)}")
    print(f"Total ingresos acumulados ($ MXN):         ${df_final['total'].sum():,.2f}")
    print(f"Total unidades vendidas:                   {df_final['unidades'].sum():,} u")
    print(f"Dataset limpio guardado en:                ventas_limpias.csv")
    print(f"Muestra (100 filas) guardada en:           data/sample/ventas_sample.csv")
    print("=" * 65)

if __name__ == "__main__":
    limpiar_datos()
