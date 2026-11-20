# PlastikTrack: Plataforma de Inteligencia y Pronóstico de Demanda

[![Oracle Cloud Free Tier](https://img.shields.io/badge/Cloud-Oracle%20Cloud%20Always%20Free-red?style=flat-square&logo=oracle)](https://www.oracle.com/cloud/free/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Visualizaciones-Plotly-3F4F75?style=flat-square&logo=plotly)](https://plotly.com/)
[![E0](https://img.shields.io/badge/Entrega%20E0-COMPLETADO-brightgreen?style=flat-square)](docs/E0-propuesta.md)
[![E1](https://img.shields.io/badge/Entrega%20E1-COMPLETADO-brightgreen?style=flat-square)](docs/E1-dashboard.md)
[![E2](https://img.shields.io/badge/Entrega%20E2-COMPLETADO-brightgreen?style=flat-square)](docs/E2-modelos.md)
[![E3](https://img.shields.io/badge/Entrega%20E3-COMPLETADO-brightgreen?style=flat-square)](docs/E3-infraestructura.md)

Startup SaaS B2B de inteligencia de inventario y analítica predictiva diseñada específicamente para comercializadoras y distribuidoras mayoristas de bolsas, películas y desechables plásticos para el canal tradicional (tiendas de abarrotes y negocios de comida).

---

## 📌 Estado de Entregas del Proyecto Integrador

| Entrega | Hito / Módulo | Estado | Documentación y Evidencia Oficial |
| :--- | :--- | :---: | :--- |
| **E0** | **Propuesta de Negocio & Factibilidad FinOps:**<br>Lean Canvas de 9 bloques, entrevista al Distribuidor Javier Morales, cadena de preguntas Negocio $\to$ Analítica $\to$ Variable a predecir, e inventario base con salvaguarda presupuestal de $1.00 USD en OCI. | **[COMPLETADO]** | [`docs/E0-propuesta.md`](docs/E0-propuesta.md)<br>• Captura Tenancy: [`alerta_presupuesto_detalle.png`](docs/img/alerta_presupuesto_detalle.png)<br>• Captura Regla 100%: [`alerta_presupuesto_regla.png`](docs/img/alerta_presupuesto_regla.png) |
| **E1** | **Ingeniería de Datos, Data Lake en OCI y Dashboard:**<br>Generación sintética (638 días, 12 SKUs, 5 errores sembrados), pipeline determinista de limpieza (`limpiar_datos.py`), Data Lake en OCI Object Storage (`raw/` y `clean/`), Solicitud Preautenticada (PAR) y tablero Streamlit con 4 KPIs, 6 gráficas Plotly (FFT espectral) y 3 recomendaciones de negocio. | **[COMPLETADO]** | [`docs/E1-dashboard.md`](docs/E1-dashboard.md)<br>• Captura Capa Raw: [`data_lake_raw.png`](docs/img/data_lake_raw.png)<br>• Captura Capa Clean: [`data_lake_clean.png`](docs/img/data_lake_clean.png)<br>• Captura Dashboard: [`dashboard_e1.png`](docs/img/dashboard_e1.png) |
| **E2** | **Modelos Predictivos y Forecasting Avanzado:**<br>Análisis Exploratorio de Datos (EDA), pruebas estadísticas de hipótesis (Mann-Whitney y Kruskal-Wallis), validación temporal sin fuga (Backtesting 56 días) y modelo de Machine Learning (`HistGradientBoostingRegressor`) con reducción del 34% en WAPE y motor de recomendación de compra a 14 días. | **[COMPLETADO]** | [`docs/E2-modelos.md`](docs/E2-modelos.md)<br>• Reporte PDF: [`PlastikTrack_E2_Modelos_y_Pronostico.pdf`](docs/PlastikTrack_E2_Modelos_y_Pronostico.pdf)<br>• Notebook Ejecutado: [`EDA_PlastikTrack_Avance1.ipynb`](notebooks/EDA_PlastikTrack_Avance1.ipynb) |
| **E3** | **Infraestructura Cloud, Contenedores y Microservicios:**<br>Infraestructura como Código (IaC con Terraform en OCI Always Free), contenedores Docker multicapa (`services/modelos/Dockerfile`, `services/tablero/Dockerfile`), orquestación local con `docker-compose.yml`, manifiestos de Kubernetes (`k8s/`) con Ingress y HPA, y microservicio API REST de Inferencia en FastAPI con validación Pydantic v2. | **[COMPLETADO]** | [`docs/E3-infraestructura.md`](docs/E3-infraestructura.md)<br>• Reporte PDF: [`PlastikTrack_E3_Infraestructura_y_Despliegue.pdf`](docs/PlastikTrack_E3_Infraestructura_y_Despliegue.pdf)<br>• Terraform: [`infra/terraform/`](infra/terraform/)<br>• Kubernetes: [`k8s/`](k8s/) |

---

## 📁 Estructura del Repositorio

```text
data-startup-plastiktrack/
├── .streamlit/
│   ├── config.toml           # Configuración visual y tema dark de Streamlit
│   └── secrets.toml          # URL preautenticada (PAR) de OCI (ignorado por Git)
├── data/
│   └── sample/
│       └── ventas_sample.csv # Muestra oficial de 100 registros limpios en Git
├── docs/
│   ├── E0-propuesta.md       # Entrega E0 (Lean Canvas, Entrevista y FinOps)
│   ├── E1-dashboard.md       # Entrega E1 (Data Lake OCI, Calidad y Dashboard)
│   └── img/
│       ├── alerta_presupuesto_detalle.png
│       ├── alerta_presupuesto_regla.png
│       ├── data_lake_raw.png
│       ├── data_lake_clean.png
│       └── dashboard_e1.png
├── infra/
│   └── terraform/            # Infraestructura como Código (IaC) para OCI
├── k8s/                      # Manifiestos de despliegue en Kubernetes
├── notebooks/                # Experimentación y EDA estadístico
├── services/
│   ├── ingesta/              # Microservicio de ingesta transaccional
│   ├── modelos/              # Motores de inferencia a 7 y 14 días
│   ├── tablero/
│   │   └── app.py            # Dashboard interactivo Streamlit con 6 gráficos Plotly
│   └── worker/               # Tareas asíncronas de background
├── tests/
│   ├── test_pipeline.py      # Suite de validación de calidad de datos
│   └── test_oci_connection.py# Suite de prueba de conectividad a OCI Object Storage
├── .gitignore                # Reglas de exclusión para Git
├── generar_ventas.py         # Script generador sintético (7,686 registros con errores)
├── limpiar_datos.py          # Pipeline de limpieza y rectificación (7,656 registros limpios)
├── ventas_distribuidora.csv  # Dataset crudo con errores (ignorado en Git)
├── ventas_limpias.csv        # Dataset limpio oficial (ignorado en Git)
└── README.md                 # Documentación técnica general
```

---

## 🚀 Guía de Instalación y Ejecución Local

Sigue estos pasos para clonar el proyecto, instalar dependencias y levantar el tablero conectado a la nube:

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/data-startup-plastiktrack.git
cd data-startup-plastiktrack
```

### 2. Crear y Activar Entorno Virtual (Recomendado)
```bash
# En Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# En Linux / macOS:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install pandas numpy streamlit plotly
```

### 4. Configurar Conexión a la Nube (Secrets de OCI)
Crea el archivo `.streamlit/secrets.toml` con la URL preautenticada (PAR) oficial de OCI:
```toml
DATA_URL = "https://objectstorage.mx-queretaro-1.oraclecloud.com/p/74GB-ixKJxbu22BcKWdm6tBI_-DeOB4STAofZfkB4v3ybBZ0mumMz5EAnOWMA7bR/n/axlgvztnfk2d/b/datastartup-lake/o/clean/ventas_limpias.csv"
```
*(Nota: Este archivo está protegido en `.gitignore` y nunca se sube al repositorio público).*

### 5. Validar la Conectividad Cloud y Pruebas Automatizadas
Ejecuta la suite de pruebas para confirmar la descarga de los **7,656 registros** desde OCI:
```bash
# Validar conexión directa al Data Lake OCI
python tests/test_oci_connection.py

# Validar integridad local de reglas de datos
python tests/test_pipeline.py
```

### 6. Ejecutar el Tablero Streamlit
Inicia el panel interactivo:
```bash
streamlit run services/tablero/app.py
```
Abre en tu navegador: **[http://localhost:8501](http://localhost:8501)**

---

## 📊 Resumen Ejecutivo del Proyecto (Entregas E0 y E1)

* **Startup:** PlastikTrack
* **Early Adopter:** Distribuidor Javier Morales (Distribuidora de Plásticos y Desechables San Juan).
* **Problema Resuelto:** Quiebres de stock en bolsas de alta rotación en quincenas y capital inmovilizado en desechables de baja rotación.
* **Arquitectura Cloud:** **$0.00 USD / mes** en Oracle Cloud Infrastructure (OCI Always Free: 4 OCPU Ampere ARM, 24 GB RAM, 200 GB Storage).
* **Alerta FinOps:** Presupuesto activo de **$1.00 USD / mes** con alerta inmediata al 100% de gasto real (`docs/img/alerta_presupuesto_detalle.png`).
* **Data Lake OCI:** Separación en capas `raw/` y `clean/` en OCI Object Storage con acceso seguro PAR (`docs/img/data_lake_clean.png`).
* **Variable Objetivo:** `unidades_vendidas` diarias a horizontes de 7 y 14 días.
* **Hallazgos Analíticos:** Fuerte componente armónico semanal (7 días) y quincenal (15.2 días) identificado mediante Transformada Rápida de Fourier (FFT), con picos de +28% en quincenas y concentración de ventas en Lunes, Miércoles y Viernes.
