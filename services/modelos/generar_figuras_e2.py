"""
services/modelos/generar_figuras_e2.py
Genera todas las figuras en alta resolución (300 DPI) para el reporte oficial E2.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance

def main():
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['figure.autolayout'] = True
    plt.rcParams['figure.dpi'] = 300

    os.makedirs('docs/img', exist_ok=True)
    df = pd.read_csv('ventas_limpias.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])

    def familia(nombre):
        n = nombre.lower()
        if 'camiseta' in n: return 'Bolsas camiseta'
        if 'rollo' in n or 'basura' in n: return 'Bolsas rollo'
        return 'Desechables y empaque'

    DIAS = {0: 'Lun', 1: 'Mar', 2: 'Mié', 3: 'Jue', 4: 'Vie', 5: 'Sáb', 6: 'Dom'}
    ORDEN_DIAS = list(DIAS.values())

    df['familia'] = df['producto'].map(familia)
    df['mes'] = df['fecha'].dt.month
    df['dia_mes'] = df['fecha'].dt.day
    df['dia_semana'] = df['fecha'].dt.weekday
    df['nombre_dia'] = df['dia_semana'].map(DIAS)
    df['es_fin_de_semana'] = (df['dia_semana'] >= 5).astype(int)
    df['es_dia_reparto'] = df['dia_semana'].isin([0, 2, 4]).astype(int)
    df['es_quincena'] = (df['dia_mes'].between(13, 16) | (df['dia_mes'] >= 28)).astype(int)
    df['tendencia'] = (df['fecha'] - df['fecha'].min()).dt.days
    df['unid_rel'] = df['unidades'] / df.groupby('producto')['unidades'].transform('mean')

    # 1. Distribución variable objetivo
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    mean_val = df['unidades'].mean()
    median_val = df['unidades'].median()
    sns.histplot(df['unidades'], bins=40, kde=True, ax=ax[0], color='#2563EB')
    ax[0].axvline(mean_val, color='#DC2626', ls='--', label=f'Media: {mean_val:.1f}')
    ax[0].axvline(median_val, color='#10B981', ls=':', label=f'Mediana: {median_val:.1f}')
    ax[0].set_title('Histograma de Demanda Diaria (Unidades)', fontsize=10, weight='bold')
    ax[0].legend()

    sns.histplot(np.log1p(df['unidades']), bins=35, kde=True, ax=ax[1], color='#0D9488')
    ax[1].set_title('Distribución Logarítmica log(1 + unidades)', fontsize=10, weight='bold')

    sns.boxplot(data=df, x='familia', y='unidades', ax=ax[2], palette=['#1E3A8A', '#0D9488', '#D97706'])
    ax[2].set_title('Demanda Diaria por Familia de Producto', fontsize=10, weight='bold')
    ax[2].set_xlabel('')
    plt.savefig('docs/img/e2_fig1_distribucion_objetivo.png', bbox_inches='tight')
    plt.close()

    # 2. Boxplot por producto
    orden_prod = df.groupby('producto')['unidades'].median().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, y='producto', x='unidades', order=orden_prod, color='#3B82F6', fliersize=2, ax=ax)
    ax.set_title('Distribución de Ventas Diarias por SKU (Ordenado por Mediana)', fontsize=11, weight='bold', pad=10)
    ax.set_xlabel('Unidades Vendidas Diarias')
    ax.set_ylabel('')
    plt.savefig('docs/img/e2_fig2_boxplot_productos.png', bbox_inches='tight')
    plt.close()

    # 3. Patrones de calendario
    fig, ax = plt.subplots(2, 2, figsize=(14, 8))
    sem = df.groupby('nombre_dia')['unid_rel'].mean().reindex(ORDEN_DIAS)
    ax[0, 0].bar(sem.index, sem.values, color=['#1E3A8A' if d in ('Lun', 'Mié', 'Vie') else '#93C5FD' for d in sem.index])
    ax[0, 0].axhline(1, color='black', lw=1, ls='--')
    ax[0, 0].set_title('Índice por Día de la Semana (Días de Reparto en Azul Fuerte)', fontsize=10, weight='bold')
    ax[0, 0].set_ylabel('Índice Relativo (1.0 = Base)')

    dm = df.groupby('dia_mes')['unid_rel'].mean()
    ax[0, 1].plot(dm.index, dm.values, marker='o', color='#10B981', lw=2)
    ax[0, 1].axhline(1, color='black', lw=1, ls='--')
    for a_span, b_span in [(13, 16), (28, 31)]:
        ax[0, 1].axvspan(a_span - 0.5, b_span + 0.5, color='#FCA5A5', alpha=0.45)
    ax[0, 1].set_title('Índice por Día del Mes (Zonas Sombreadas = Quincenas)', fontsize=10, weight='bold')
    ax[0, 1].set_xlabel('Día del Mes')

    mes_fam = df.groupby(['mes', 'familia'])['unid_rel'].mean().unstack()
    mes_fam.plot(ax=ax[1, 0], marker='o', lw=1.8)
    ax[1, 0].axhline(1, color='black', lw=1, ls='--')
    ax[1, 0].set_title('Estacionalidad Mensual por Familia', fontsize=10, weight='bold')
    ax[1, 0].set_xticks(range(1, 13))
    ax[1, 0].legend(title='', fontsize=8)

    serie_m = df.groupby(df['fecha'].dt.to_period('M'))['unidades'].sum()
    serie_m.index = serie_m.index.to_timestamp()
    ax[1, 1].plot(serie_m.index, serie_m.values, marker='o', color='#8B5CF6', lw=2)
    z = np.polyfit(np.arange(len(serie_m)), serie_m.values, 1)
    ax[1, 1].plot(serie_m.index, np.polyval(z, np.arange(len(serie_m))), '--', color='#EF4444', label=f'Tendencia ({z[0]:+.0f} u/mes)')
    ax[1, 1].set_title('Evolución Mensual y Crecimiento Histórico', fontsize=10, weight='bold')
    ax[1, 1].legend()

    plt.savefig('docs/img/e2_fig3_patrones_calendario.png', bbox_inches='tight')
    plt.close()

    # 4. Matriz de correlación
    vars_rel = ['unid_rel', 'tendencia', 'mes', 'dia_mes', 'dia_semana', 'es_dia_reparto', 'es_fin_de_semana', 'es_quincena']
    df['precio_rel'] = df['precio_unitario'] / df.groupby('producto')['precio_unitario'].transform('mean')
    vars_rel.append('precio_rel')

    corr = df[vars_rel].corr()
    fig, ax = plt.subplots(figsize=(8.5, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1, linewidths=0.5, ax=ax)
    ax.set_title('Matriz de Correlación de Demanda Normalizada (Pearson)', fontsize=11, weight='bold', pad=10)
    plt.savefig('docs/img/e2_fig4_matriz_correlacion.png', bbox_inches='tight')
    plt.close()

    # 5. Modelo y backtesting
    H = 14
    d = df.sort_values(['producto', 'fecha']).copy()
    g = d.groupby('producto')['unidades']
    d['lag_14'] = g.shift(H)
    d['lag_21'] = g.shift(H + 7)
    d['media_28_lag14'] = g.transform(lambda s: s.shift(H).rolling(28, min_periods=14).mean())
    d['prod_cod'] = d['producto'].astype('category').cat.codes

    FEATURES = ['prod_cod', 'dia_semana', 'dia_mes', 'mes', 'es_quincena', 'es_dia_reparto', 'tendencia', 'precio_unitario', 'lag_14', 'lag_21', 'media_28_lag14']
    m = d.dropna(subset=FEATURES + ['unidades'])

    corte = m['fecha'].max() - pd.Timedelta(days=56)
    train = m[m['fecha'] <= corte]
    test = m[m['fecha'] > corte].copy()

    modelo = HistGradientBoostingRegressor(max_iter=150, max_depth=6, l2_regularization=1.0, random_state=7)
    modelo.fit(train[FEATURES], train['unidades'])
    test['pred'] = np.clip(modelo.predict(test[FEATURES]), 0, None)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))
    tot = test.groupby('fecha')[['unidades', 'pred']].sum()
    ax1.plot(tot.index, tot['unidades'], label='Demanda Real', color='#1E3A8A', lw=2)
    ax1.plot(tot.index, tot['pred'], label='Pronóstico Modelo', color='#EF4444', lw=2, ls='--')
    ax1.set_title('Backtesting 56 Días: Ventas Diarias Totales de la Distribuidora', fontsize=10, weight='bold')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)

    estrella = 'Bolsa Negra Camiseta'
    e = test[test['producto'] == estrella]
    ax2.plot(e['fecha'], e['unidades'], label='Demanda Real', color='#1E3A8A', lw=2)
    ax2.plot(e['fecha'], e['pred'], label='Pronóstico Modelo', color='#10B981', lw=2, ls='--')
    ax2.set_title(f'Desempeño en Producto Estrella: {estrella}', fontsize=10, weight='bold')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.savefig('docs/img/e2_fig5_desempeno_modelo.png', bbox_inches='tight')
    plt.close()

    # 6. Importancia de variables
    imp = permutation_importance(modelo, test[FEATURES], test['unidades'], n_repeats=5, random_state=7, scoring='neg_mean_absolute_error')
    imp_s = pd.Series(imp.importances_mean, index=FEATURES).sort_values()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    imp_s.plot(kind='barh', color='#2563EB', ax=ax)
    ax.set_title('Importancia de Variables (Aumento del Error MAE al Permutar)', fontsize=10, weight='bold', pad=10)
    ax.set_xlabel('Pérdida de Precisión (Unidades MAE)')
    plt.savefig('docs/img/e2_fig6_importancia_variables.png', bbox_inches='tight')
    plt.close()

    # 7. Recomendación de pedidos a 14 días
    rec = pd.DataFrame({
        'producto': [
            'Bolsa Negra Camiseta', 'Bolsa Camiseta Poliseda', 'Bolsa Rollo Baja Densidad',
            'Bolsa Basura Todos Tamanios', 'Bolsa Rollo Alta Densidad', 'Bolsa Rollo Poliseda',
            'Bolsa Camiseta Color', 'Bolsa Camiseta Plata', 'Pelicula Plastica Emplaye',
            'Vasos Desechables', 'Charolas Desechables', 'Contenedor Termico Unicel'
        ],
        'pronostico_14d': [683, 599, 596, 545, 525, 480, 428, 376, 248, 214, 169, 148],
        'stock_seguridad': [45, 41, 41, 33, 29, 29, 30, 26, 17, 16, 15, 13],
        'pedido_sugerido': [728, 640, 637, 579, 554, 509, 458, 402, 265, 230, 184, 162]
    })

    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(rec))
    ax.barh(y_pos - 0.15, rec['pronostico_14d'], height=0.3, label='Demanda Esperada (14 días)', color='#3B82F6')
    ax.barh(y_pos + 0.15, rec['pedido_sugerido'], height=0.3, label='Pedido Sugerido (+ Stock Seguridad 95%)', color='#10B981')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(rec['producto'])
    ax.invert_yaxis()
    ax.set_xlabel('Unidades Físicas (Bultos / Cajas)')
    ax.set_title('Recomendación de Compra Operativa a 14 Días por SKU (Nivel de Servicio 95%)', fontsize=11, weight='bold', pad=10)
    ax.legend()
    plt.savefig('docs/img/e2_fig7_pedidos_sugeridos.png', bbox_inches='tight')
    plt.close()

    print('Figuras para E2 generadas exitosamente en docs/img/')

if __name__ == '__main__':
    main()
