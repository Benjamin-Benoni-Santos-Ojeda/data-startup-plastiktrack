"""
services/modelos/entrenar_modelo.py
Entrena el modelo HistGradientBoostingRegressor con los 16,428 registros curados
y guarda los artefactos en services/modelos/modelo_demanda.joblib
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

def train_and_save():
    os.makedirs('services/modelos', exist_ok=True)
    df = pd.read_csv('ventas_limpias.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])

    def familia(nombre):
        n = nombre.lower()
        if 'camiseta' in n: return 'Bolsas camiseta'
        if 'rollo' in n or 'basura' in n: return 'Bolsas rollo'
        return 'Desechables y empaque'

    df['familia'] = df['producto'].map(familia)
    df['mes'] = df['fecha'].dt.month
    df['dia_mes'] = df['fecha'].dt.day
    df['dia_semana'] = df['fecha'].dt.weekday
    df['es_fin_de_semana'] = (df['dia_semana'] >= 5).astype(int)
    df['es_dia_reparto'] = df['dia_semana'].isin([0, 2, 4]).astype(int)
    df['es_quincena'] = (df['dia_mes'].between(13, 16) | (df['dia_mes'] >= 28)).astype(int)
    df['tendencia'] = (df['fecha'] - df['fecha'].min()).dt.days

    H = 14
    d = df.sort_values(['producto', 'fecha']).copy()
    g = d.groupby('producto')['unidades']
    d['lag_14'] = g.shift(H)
    d['lag_21'] = g.shift(H + 7)
    d['media_28_lag14'] = g.transform(lambda s: s.shift(H).rolling(28, min_periods=14).mean())
    
    # Mapeo de producto a código
    prods = sorted(d['producto'].unique().tolist())
    prod2code = {p: i for i, p in enumerate(prods)}
    code2prod = {i: p for i, p in enumerate(prods)}
    d['prod_cod'] = d['producto'].map(prod2code)

    FEATURES = ['prod_cod', 'dia_semana', 'dia_mes', 'mes', 'es_quincena', 'es_dia_reparto', 'tendencia', 'precio_unitario', 'lag_14', 'lag_21', 'media_28_lag14']
    m = d.dropna(subset=FEATURES + ['unidades'])

    corte = m['fecha'].max() - pd.Timedelta(days=56)
    train = m[m['fecha'] <= corte]
    test = m[m['fecha'] > corte]

    model = HistGradientBoostingRegressor(max_iter=150, max_depth=6, l2_regularization=1.0, random_state=7)
    model.fit(train[FEATURES], train['unidades'])

    # Métricas en prueba
    test_preds = np.clip(model.predict(test[FEATURES]), 0, None)
    mae = float(np.mean(np.abs(test['unidades'] - test_preds)))
    rmse = float(np.sqrt(np.mean((test['unidades'] - test_preds) ** 2)))
    wape = float(np.sum(np.abs(test['unidades'] - test_preds)) / np.sum(test['unidades']) * 100)

    # Catálogo y precios de referencia
    catalog = (
        df.groupby('producto')
        .agg(
            precio_unitario=('precio_unitario', 'median'),
            unidades_promedio_diaria=('unidades', 'mean'),
            familia=('familia', 'first')
        )
        .reset_index()
    )
    catalog['prod_cod'] = catalog['producto'].map(prod2code)

    artifact = {
        'model': model,
        'features': FEATURES,
        'prod2code': prod2code,
        'code2prod': code2prod,
        'catalog': catalog.to_dict(orient='records'),
        'metrics': {
            'mae': round(mae, 2),
            'rmse': round(rmse, 2),
            'wape_pct': round(wape, 2),
            'test_days': 56,
            'train_samples': len(train),
            'test_samples': len(test)
        },
        'version': '1.0.0',
        'algorithm': 'HistGradientBoostingRegressor'
    }

    joblib.dump(artifact, 'services/modelos/modelo_demanda.joblib')
    print(f"Modelo guardado exitosamente. WAPE={wape:.2f}%, MAE={mae:.2f}, RMSE={rmse:.2f}")

if __name__ == '__main__':
    train_and_save()
