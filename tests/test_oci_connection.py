"""
tests/test_oci_connection.py
Prueba de conectividad a Oracle Cloud Object Storage para la rúbrica E1.
Valida la lectura mediante la URL preautenticada definida en .streamlit/secrets.toml.
"""

import tomllib
import pandas as pd

def test_oci_connectivity():
    # 1. Leer secrets.toml
    with open('.streamlit/secrets.toml', 'rb') as f:
        secrets = tomllib.load(f)

    url = secrets.get('DATA_URL')
    print("=" * 65)
    print("      TEST DE CONEXIÓN A ORACLE CLOUD OBJECT STORAGE (E1)")
    print("=" * 65)
    print(f"URL de Secrets:\n{url}\n")

    # 2. Descargar dataset con pandas
    print("Descargando dataset desde el bucket datastartup-lake/clean...")
    df = pd.read_csv(url)

    print(f"[OK] Registros descargados:      {len(df)}")
    print(f"[OK] Cobertura temporal:         {df['fecha'].nunique()} días continuos")
    print(f"[OK] Catálogo de productos:      {df['producto'].nunique()} SKUs")
    print(f"[OK] Valores nulos en dataset:   {df.isna().sum().sum()}")
    print(f"[OK] Total acumulado en ventas:  ${df['total'].sum():,.2f} MXN")

    # 3. Aserciones de integridad
    assert len(df) == 7656, f"Se esperaban 7,656 registros, se obtuvieron {len(df)}"
    assert df.isna().sum().sum() == 0, "Se detectaron valores nulos en el dataset descargado"
    assert "clean/ventas_limpias.csv" in url, "La URL no apunta a la ruta clean/ventas_limpias.csv"
    
    print("-" * 65)
    print("RESULTADO: CONEXIÓN EXITOSA Y VALIDACIÓN COMPLETA (RÚBRICA E1)")
    print("=" * 65)

if __name__ == "__main__":
    test_oci_connectivity()
