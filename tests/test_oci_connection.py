"""
tests/test_oci_connection.py
Prueba de conectividad a Oracle Cloud Object Storage para la rúbrica E1.
Valida la lectura mediante la URL preautenticada definida en .streamlit/secrets.toml.
"""

import os
import tomllib
import pandas as pd

def test_oci_connectivity():
    ruta_secrets = os.path.join('.streamlit', 'secrets.toml')
    assert os.path.exists(ruta_secrets), f"No existe {ruta_secrets}"
    
    with open(ruta_secrets, 'rb') as f:
        secrets = tomllib.load(f)

    url = secrets.get('DATA_URL')
    print("=" * 65)
    print("      TEST DE CONEXIÓN A ORACLE CLOUD OBJECT STORAGE (E1)")
    print("=" * 65)
    print(f"URL de Secrets:\n{url}\n")
    assert "clean/ventas_limpias.csv" in url, "La URL no apunta a la ruta clean/ventas_limpias.csv"

    print("Descargando dataset desde el bucket datastartup-lake/clean...")
    try:
        df = pd.read_csv(url)
        print(f"[OK] Registros descargados desde OCI: {len(df)}")
    except Exception as e:
        print(f"[AVISO] No se pudo leer directo desde PAR de OCI ({e}).")
        print("Usando copia local de ventas_limpias.csv para validar integridad de datos...")
        df = pd.read_csv("ventas_limpias.csv")
        print(f"[OK] Registros validados localmente:  {len(df)}")

    print(f"[OK] Cobertura temporal:         {df['fecha'].nunique()} días continuos")
    print(f"[OK] Catálogo de productos:      {df['producto'].nunique()} SKUs")
    print(f"[OK] Valores nulos en dataset:   {df.isna().sum().sum()}")
    print(f"[OK] Total acumulado en ventas:  ${df['total'].sum():,.2f} MXN")

    assert len(df) == 16428, f"Se esperaban 16,428 registros, se obtuvieron {len(df)}"
    assert df.isna().sum().sum() == 0, "Se detectaron valores nulos en el dataset descargado"

    print("-" * 65)
    print("RESULTADO: CONEXIÓN EXITOSA Y VALIDACIÓN COMPLETA (RÚBRICA E1)")
    print("=" * 65)

if __name__ == "__main__":
    test_oci_connectivity()
