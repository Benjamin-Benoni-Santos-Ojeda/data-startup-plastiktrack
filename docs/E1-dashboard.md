# E1: Dashboard Analítico e Inteligencia de Negocio

**Proyecto Integrador:** DATA STARTUP  
**Entrega:** E1 (Ingeniería de Datos, Almacenamiento en Nube y Tablero de Control)  
**Roles:** Cloud Lead (Benjamin Benoni Santos Ojeda - 25460724) & Data Lead (Juan Carrillo Orozco - 25460331)  
**Fecha:** Octubre / Noviembre 2026  
**Empresa / Caso de Estudio:** PlastikTrack (Distribuidor Javier Morales)

---

## 1. Almacenamiento en la Nube: Data Lake en Oracle Cloud Infrastructure (OCI)

Para dar soporte escalable, seguro y de costo cero ($0.00 USD) a la plataforma PlastikTrack, el almacenamiento de datos se estructuró como un **Data Lake Cloud-Native** alojado en el servicio **OCI Object Storage** (Región: `mx-queretaro-1`, Bucket: `datastartup-lake`, Namespace: `axlgvztnfk2d`).

El diseño implementa una arquitectura desacoplada por capas o zonas de madurez del dato:

```mermaid
flowchart LR
    A["Fuente Transaccional<br>(POS / Notas de Javier)"] --> B["Zona raw/<br>ventas_distribuidora.csv<br>(Inmutable - 16,498 filas)"]
    B --> C["Pipeline ETL / Limpieza<br>limpiar_datos.py"]
    C --> D["Zona clean/<br>ventas_limpias.csv<br>(Curado - 16,428 filas)"]
    D --> E["Acceso Seguro PAR<br>(Solo Lectura)"]
    E --> F["Tablero Streamlit<br>services/tablero/app.py"]
```

### Arquitectura de Capas:

1. **Zona `raw/` (Capa Bronce / Inmutable):**
   * **Propósito:** Registro fidedigno e inalterable del dato origen (*Source of Truth*). Preserva las transacciones históricas generadas tal como fueron registradas en mostrador.
   * **Archivo:** `raw/ventas_distribuidora.csv` (16,498 registros, 894 KB).
   * **Auditoría:** Contiene intencionalmente las anomalías operativas de captura (duplicados, nulos, negativos, atípicos e inconsistencias de minúsculas/espacios) para evaluación de calidad y trazabilidad histórica.
   * **Seguridad:** Permisos de escritura restringidos exclusivamente al proceso de ingesta.

![Data Lake OCI - Zona Raw](img/data_lake_raw.png)
*Figura 1: Evidencia del bucket en OCI con la carpeta raw/ y el archivo ventas_distribuidora.csv cargado.*

---

2. **Zona `clean/` (Capa Oro / Servido Analítico):**
   * **Propósito:** Repositorio de alta fidelidad con datos curados, normalizados, imputados y validados algorítmicamente, listos para inferencia y visualización ejecutiva.
   * **Archivo:** `clean/ventas_limpias.csv` (16,428 registros limpios, 856 KB).
   * **Reglas de Calidad Aplicadas:** 0 nulos, 0 duplicados por clave `[fecha, producto]`, unidades estrictamente positivas y acotadas (< 500 u), nombres estandarizados en formato Título y recálculo determinista del total.

![Data Lake OCI - Zona Clean](img/data_lake_clean.png)
*Figura 2: Evidencia del bucket en OCI con la carpeta clean/ y el archivo ventas_limpias.csv generado.*

---

### Mecanismo de Conexión Segura (Pre-Authenticated Request - PAR)

El consumo de datos desde el tablero Streamlit hacia la zona `clean/` se diseñó bajo estrictos estándares de ciberseguridad y gobierno en la nube:

1. **Solicitud Preautenticada (PAR) de Solo Lectura:**
   Se generó un endpoint con token criptográfico temporal en OCI con permisos restringidos exclusivamente a lectura (`Object Read`) sobre el objeto específico `clean/ventas_limpias.csv`.
2. **Protección de Credenciales en `.streamlit/secrets.toml`:**
   La URL preautenticada se administra a través del gestor de configuración de Streamlit:
   ```toml
   DATA_URL = "https://objectstorage.mx-queretaro-1.oraclecloud.com/p/74GB-ixKJxbu22BcKWdm6tBI_-DeOB4STAofZfkB4v3ybBZ0mumMz5EAnOWMA7bR/n/axlgvztnfk2d/b/datastartup-lake/o/clean/ventas_limpias.csv"
   ```
3. **Aislamiento en Git:**
   El archivo `.streamlit/secrets.toml` está explícitamente incorporado en `.gitignore`, impidiendo cualquier fuga accidental de claves o URIs en el repositorio público de GitHub.
4. **Lectura con Caché en Memoria y Resiliencia Local:**
   La aplicación invoca `pd.read_csv(url)` decorada con `@st.cache_data`, optimizando la transferencia saliente (egress), minimizando latencias y ofreciendo tolerancia a fallos con fallback local a `ventas_limpias.csv`.

---

## 2. Resumen del Pipeline de Calidad de Datos (Remediación de Errores)

El script `limpiar_datos.py` procesó el dataset crudo proveniente de la capa `raw/` para generar la capa `clean/`, solventando los 5 defectos detectados:

| Defecto Detectado | Impacto en Crudo | Estrategia de Remediación Aplicada | Registros Afectados | Estado Final |
| :--- | :--- | :--- | :--- | :--- |
| **Formato y Espacios** | Nombres con minúsculas o espacios (`"bolsa camiseta color"`) | `.str.strip().str.title()` | 70 registros | 100% Homogéneo (12 SKUs) |
| **Duplicados** | Filas redundantes con misma fecha y producto | Detección por clave de negocio `[fecha, producto]` con `.drop_duplicates(keep='first')` | 70 filas eliminadas | 16,428 filas únicas |
| **Negativos** | Unidades < 0 (ej. -35) debidas a notas de devolución | Corrección a valor absoluto positivo (`.abs()`) | 35 registros | Unidades > 0 |
| **Atípicos Contextuales** | Registros extremos centinelas (>=500 u) o ratio > 3x vs grupo | Detección por contexto `[producto, dia_semana, es_quincena]` y acotamiento a la mediana | 25 registros | Máximo representativo |
| **Nulos (NaN)** | Filas con `unidades = NaN` (90) o `precio = NaN` (12) | Imputación contextual con mediana de grupo y forward/backward fill por SKU | 102 registros | 0 valores nulos |
| **Total Inconsistente** | Descuadre en importes transaccionados | Recálculo estricto: `total = unidades * precio_unitario` | 16,428 registros | 100% Consistente |

---

## 3. Especificaciones Técnicas del Tablero Streamlit (`services/tablero/app.py`)

El tablero interactivo se estructuró para dotar a Javier de herramientas directas de diagnóstico y pronóstico comercial con base en los datos reales.

### A. Los 4 KPIs Estratégicos:
1. **Ventas Totales Acumuladas:** Monitor de ingresos brutos acumulados (**$18,672,916.50 MXN**) y volumen físico total despachado (**411,524 unidades**).
2. **Ticket Diario Promedio:** Facturación media por jornada operativa (**$13,639.82 MXN/día**), referencia para dimensionar el capital diario de cobranza.
3. **Producto Estrella:** Identificación automática del SKU con mayor rotación e ingreso (*Bolsa Negra Camiseta*, **57,251 unidades** acumuladas y **$2,204,163.50 MXN**).
4. **Variación Semanal (%):** Tasa de aceleración de demanda calculando la variación de los últimos 7 días contra la ventana semanal previa (+4.12%).

### B. Las 6 Visualizaciones Plotly y Análisis Exploratorio:
1. **Línea de Tendencia Diaria:** Despliega las ventas temporales diarias de los 1,369 días operativos contrastadas con Medias Móviles de 7 días (ciclo semanal operativo) y 30 días (tendencia mensual).
2. **Histograma de Distribución con Regla de Sturges:**
   Calcula la cantidad de intervalos óptima para $N=1,369$ días mediante:
   $$k = \lceil \log_2(N) \rceil + 1 = 11 + 1 = 12 \text{ clases}$$
   Evidenciando una distribución unimodal asimétrica positiva con cola derecha en días de quincena y alta demanda.
3. **Mapa de Calor (Día de la Semana vs Quincena / Mes):** Matriz que evidencia los días pico de reparto (Lunes, Miércoles y Viernes con +20% a +25% de demanda) a lo largo de cada ciclo mensual y quincenal.
4. **Dispersión Unidades vs Importe:** Gráfico de cuadrantes por familia de producto donde el radio de la burbuja representa el precio unitario, contrastando volumen masivo vs rentabilidad.
5. **Análisis Espectral con Transformada Rápida de Fourier (FFT):**
   Utilizando `np.fft.rfft` sobre la serie centrada (detrended), revela con precisión matemática dos armónicos dominantes:
   * **Pico en 7.0 días:** Ciclo de reposición semanal de las tiendas de abarrotes.
   * **Pico en 15.2 días:** Ciclo quincenal de pago salarial en el comercio minorista (+25% de demanda).
6. **Mix de Ingresos por Producto:** Ranking horizontal de facturación acumulada por SKU y desglose por familias funcionales (Bolsas Camiseta 38.6%, Bolsas Rollo 32.9%, Desechables y Empaque 28.5%).

---

## 4. Recomendaciones Estratégicas de Negocio para Javier

1. **Blindaje de Stock en Quincenas:**
   El análisis espectral con FFT y la prueba de hipótesis Mann-Whitney confirman un incremento sostenido de **+25% en demanda durante los ciclos de quincena** (días 13–16 y 28–31). Javier debe programar órdenes de compra a fábrica los días **10 y 25 de cada mes** incorporando un búfer de seguridad de +30% en líneas de alta rotación (*Bolsa Negra Camiseta* y *Bolsa Rollo Baja Densidad*), erradicando las compras de emergencia a otros distribuidores que merman el 15% del margen neto.

2. **Consolidación de Rutas de Reparto en Días Pico:**
   El mapa de calor temporal demuestra que los días **Lunes (+22%), Miércoles (+19%) y Viernes (+28%)** concentran más del 65% del flujo total de entregas. Se recomienda reestructurar los turnos de choferes y cargas de camionetas la tarde previa para despachar a primera hora y optimizar el consumo de combustible diésel, liberando los martes y jueves para cobranza y prospección de nuevas tiendas.

3. **Combos Comerciales para Liquidación de Desechables:**
   Las líneas de *Contenedor Térmico Unicel*, *Charolas Desechables* y *Vasos Desechables* presentan la menor velocidad de rotación (apenas 10% del volumen total) pero absorben más del 40% del espacio cúbico de la bodega. Se recomienda implementar una estrategia de **combos comerciales** (ej. bonificar 1 paquete de vasos desechables con descuento del 6% por cada 8 bultos de bolsa camiseta), dinamizando la rotación de tarimas y liberando capital de trabajo estancado.

---

## 5. Pruebas Automatizadas y Verificación

El proyecto cuenta con suites de validación automatizada que aseguran la reproducibilidad y conformidad de la entrega:
* **Prueba de Calidad Local:** `python tests/test_pipeline.py`
* **Prueba de Conectividad Cloud OCI:** `python tests/test_oci_connection.py`

---

## 6. Evidencia del Producto: Dashboard Empresarial en Ejecución

A continuación se documenta la interfaz en producción del panel de control de **PlastikTrack** ejecutándose en Streamlit, con telemetría en tiempo real y lectura de los datos de la distribuidora:

![Dashboard Empresarial PlastikTrack](img/dashboard_e1.png)

*Figura 3: Panel de control ejecutivo en Streamlit con métricas KPI, análisis espectral con Transformada Rápida de Fourier (picos en 7.0 y 15.2 días), visualizaciones interactivas de demanda y telemetría de 16,428 registros limpios.*
