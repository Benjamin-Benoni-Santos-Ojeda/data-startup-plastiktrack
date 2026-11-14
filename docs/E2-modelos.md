# E2: Modelos Predictivos, EDA y Recomendación de Compras

**Proyecto Integrador:** DATA STARTUP  
**Entrega:** E2 (Análisis Exploratorio de Datos, Modelado Predictivo y Forecasting de Demanda)  
**Roles:** Cloud Lead (Benjamin Benoni Santos Ojeda - 25460724) & Data Lead (Juan Carrillo Orozco - 25460331)  
**Fecha:** Noviembre 2026  
**Empresa / Caso de Estudio:** PlastikTrack (Distribuidor Javier Morales)

---

## 1. Definición del Problema y Justificación Práctica

### 1.1 Contexto en la Cadena de Suministro de Plásticos
En el comercio mayorista tradicional de empaques y desechables plásticos (bolsas de polietileno, películas estirables y unicel), los distribuidores abastecen a miles de pequeños comercios (tiendas de abarrotes, fondas, pollerías y recauderías). Este eslabón enfrenta tres restricciones operativas determinantes:
1. **Lotes Mínimos de Compra:** Los fabricantes venden por millares, bultos o cajas completas; un error de cálculo se traduce en decenas de unidades sobrantes o faltantes.
2. **Tiempo de Reposición (Lead Time) de 7 a 14 días:** Lo que no se planifica con anticipación genera desabasto durante las ventanas de mayor demanda.
3. **Pronóstico Empírico:** Las decisiones se toman tradicionalmente "al tanteo" mediante recorridos visuales en bodega, provocando quiebres de inventario en días pico (+28% en quincena) y sobreinventario en desechables de baja rotación.

### 1.2 Formulación de la Variable Objetivo
* **Variable a Predecir:** `unidades` (variable cuantitativa entera continua, no negativa, por SKU y día).
* **Tipo de Problema:** **Regresión Supervisada**. Se descarta la clasificación binaria (quiebre / no quiebre) debido a que la decisión de compra requiere magnitudes físicas exactas para calcular el stock de seguridad.
* **Horizonte Operativo:** **14 días** (sincronizado con el tiempo de entrega de fábrica).
* **Métricas de Éxito:** **WAPE** (Weighted Absolute Percentage Error), **MAE** (Mean Absolute Error) y **RMSE**.

---

## 2. Dataset y Preparación de Datos

* **Historial Analizado:** **16,428 registros curados** en un panel continuo de **1,369 días** (1 de enero de 2023 al 30 de septiembre de 2026, 45 meses).
* **Catálogo:** **12 productos oficiales** clasificados en 3 familias funcionales (Bolsas Camiseta, Bolsas Rollo, y Desechables y Empaque).
* **Ingeniería de Características (Features sin fuga de información):**
  - Temporales / Calendario: `dia_semana`, `dia_mes`, `mes`, `es_quincena` (días 13–16 y 28–31), `es_dia_reparto` (lunes, miércoles, viernes), `tendencia`.
  - Categóricas: `prod_cod` (código del SKU).
  - Económicas: `precio_unitario`.
  - Rezagos Autorregresivos: `lag_14` (demanda de hace 14 días), `lag_21` (demanda de hace 21 días) y `media_28_lag14` (media móvil de 28 días conocida al momento de emitir la orden).

---

## 3. Pruebas Estadísticas de Hipótesis

Para fundamentar la inclusión de las variables exógenas en los modelos, se aplicaron pruebas de hipótesis rigurosas:
1. **Efecto Quincena vs Día Ordinario (Prueba de Mann-Whitney $U$):**  
   Demanda relativa $1.200$ vs $0.936$ ($+28.2\%$).  
   Estadístico $U$, $p = 1.06 \times 10^{-258} < 0.001$ $\to$ **Altamente Significativo**.
2. **Efecto Días de Reparto (Lunes, Miércoles, Viernes vs Resto):**  
   Demanda relativa $1.267$ vs $0.800$ ($+58.4\%$).  
   Estadístico $U$, $p = 0.000 < 0.001$ $\to$ **Altamente Significativo**.
3. **Variabilidad entre Días de la Semana (Kruskal-Wallis):**  
   $H = 9,080.7$, $p = 0.000 < 0.001$.
4. **Variabilidad entre Meses del Año (Kruskal-Wallis):**  
   $H = 492.7$, $p = 1.18 \times 10^{-98} < 0.001$ (Pico en mes 12).

---

## 4. Comparativa de Modelos Predictivos y Backtesting

Se aplicó una partición temporal estricta:
* **Entrenamiento:** 15,024 registros (28/01/2023 al 02/07/2026).
* **Prueba (Backtesting):** 1,080 registros (03/07/2026 al 30/09/2026, 56 días de prueba).

| Modelo / Enfoque | MAE (u) | RMSE (u) | WAPE (%) | $R^2$ |
| :--- | :---: | :---: | :---: | :---: |
| **Referencia 1: Venta hace 14 días (`lag_14`)** | 5.11 | 7.30 | 16.67% | 0.82 |
| **Referencia 2: Media Móvil 28 días (`MA28`)** | 8.18 | 10.80 | 26.70% | 0.61 |
| **Modelo Propuesto (HistGradientBoostingRegressor)** | **3.37** | **4.87** | **11.00%** | **0.92** |

> [!NOTE]  
> El modelo de Gradient Boosting reduce el error ponderado (**WAPE**) en un **34.0%** respecto a la línea base ingenua de hace 14 días.

---

## 5. Motor de Recomendación de Compras a 14 Días

El pronóstico se transforma directamente en una decisión de aprovisionamiento mediante la fórmula de gestión de inventarios:
$$\text{Pedido Sugerido} = \text{Pronóstico a 14 días} + \text{Stock de Seguridad} - \text{Inventario Disponible}$$
$$\text{Stock de Seguridad} = Z \times \sigma_{\text{error}} \times \sqrt{14} \quad (Z = 1.65 \implies 95\% \text{ de nivel de servicio})$$

### Plan de Pedidos para el Período 01/10/2026 al 14/10/2026:

| Producto (SKU) | Pronóstico 14 Días | Stock Seguridad (95%) | Inventario Disponible | Pedido Sugerido (Bultos) |
| :--- | :---: | :---: | :---: | :---: |
| **Bolsa Negra Camiseta** | 683 | 45 | 0 | **728** |
| **Bolsa Camiseta Poliseda** | 599 | 41 | 0 | **640** |
| **Bolsa Rollo Baja Densidad** | 596 | 41 | 0 | **637** |
| **Bolsa Basura Todos Tamanios** | 545 | 33 | 0 | **579** |
| **Bolsa Rollo Alta Densidad** | 525 | 29 | 0 | **554** |
| **Bolsa Rollo Poliseda** | 480 | 29 | 0 | **509** |
| **Bolsa Camiseta Color** | 428 | 30 | 0 | **458** |
| **Bolsa Camiseta Plata** | 376 | 26 | 0 | **402** |
| **Pelicula Plastica Emplaye** | 248 | 17 | 0 | **265** |
| **Vasos Desechables** | 214 | 16 | 0 | **230** |
| **Charolas Desechables** | 169 | 15 | 0 | **184** |
| **Contenedor Termico Unicel** | 148 | 13 | 0 | **162** |

---

## 6. Verificación y Reproducibilidad
* **Notebook Oficial Ejecutado:** [`notebooks/EDA_PlastikTrack_Avance1.ipynb`](notebooks/EDA_PlastikTrack_Avance1.ipynb)
* **Script de Modelado:** [`services/modelos/generar_figuras_e2.py`](services/modelos/generar_figuras_e2.py)
* **Reporte PDF:** `PlastikTrack_E2_Modelos_y_Pronostico.pdf`
