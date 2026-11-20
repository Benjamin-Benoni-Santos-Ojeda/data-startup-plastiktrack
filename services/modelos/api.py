"""
services/modelos/api.py
Microservicio de Inferencia de Demanda de PlastikTrack.
Expone endpoints REST mediante FastAPI para predicción de demanda y cálculo de aprovisionamiento a 14 días.
"""

import os
import time
from datetime import datetime, date
from typing import List, Optional, Dict, Any
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_START_TIME = time.time()
MODEL_PATH = os.environ.get("MODEL_PATH", os.path.join(os.path.dirname(__file__), "modelo_demanda.joblib"))

# Carga de artefacto de modelo
if not os.path.exists(MODEL_PATH):
    # Si no existe en la ruta relativa, buscar en la raíz del proyecto
    alt_path = "services/modelos/modelo_demanda.joblib"
    if os.path.exists(alt_path):
        MODEL_PATH = alt_path

try:
    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
    FEATURES = artifact["features"]
    prod2code = artifact["prod2code"]
    code2prod = artifact["code2prod"]
    catalog_list = artifact["catalog"]
    model_metrics = artifact["metrics"]
    model_version = artifact.get("version", "1.0.0")
except Exception as e:
    model = None
    artifact = None
    FEATURES = []
    prod2code = {}
    code2prod = {}
    catalog_list = []
    model_metrics = {}
    model_version = "unavailable"

app = FastAPI(
    title="PlastikTrack - API de Inferencia y Forecast",
    description="Microservicio de Inteligencia Artificial para la predicción de demanda y optimización de compras a 14 días.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Esquemas Pydantic -----------------

class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    timestamp: str
    uptime_seconds: float
    model_version: str
    algorithm: str
    cloud_provider: str
    metrics: Dict[str, Any]

class SKUInfo(BaseModel):
    producto: str
    prod_cod: int
    precio_unitario: float
    unidades_promedio_diaria: float
    familia: str

class PredictItem(BaseModel):
    producto: str = Field(..., example="Bolsa Negra Camiseta")
    fecha: str = Field(..., example="2026-11-20")
    precio_unitario: Optional[float] = Field(None, example=42.0)
    inventario_actual: Optional[int] = Field(0, example=50)

class PredictionResult(BaseModel):
    producto: str
    fecha: str
    demanda_predicha: float
    es_quincena: bool
    es_dia_reparto: bool
    dia_semana: str
    precio_unitario: float

class PredictRequest(BaseModel):
    items: List[PredictItem]

class PredictResponse(BaseModel):
    total_items: int
    predictions: List[PredictionResult]
    latency_ms: float

class ReplenishItemInput(BaseModel):
    producto: str = Field(..., example="Bolsa Negra Camiseta")
    inventario_actual: int = Field(0, ge=0, example=120)
    lead_time_dias: int = Field(14, ge=1, le=30, example=14)

class ReplenishRequest(BaseModel):
    items: Optional[List[ReplenishItemInput]] = None
    nivel_servicio_pct: float = Field(95.0, ge=80.0, le=99.9, example=95.0)

class ReplenishOutputItem(BaseModel):
    producto: str
    familia: str
    precio_unitario: float
    pronostico_14d: int
    stock_seguridad: int
    inventario_actual: int
    pedido_sugerido: int
    costo_estimado_pedido_mxn: float

class ReplenishResponse(BaseModel):
    horizonte_dias: int
    nivel_servicio_pct: float
    factor_z: float
    total_unidades_sugeridas: int
    inversion_total_mxn: float
    items: List[ReplenishOutputItem]
    latency_ms: float

# ----------------- Funciones Auxiliares -----------------

DIAS_MAP = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}

def get_z_factor(service_level: float) -> float:
    # Mapeo estándar de distribución normal
    if service_level >= 99.0: return 2.33
    if service_level >= 97.5: return 1.96
    if service_level >= 95.0: return 1.65
    if service_level >= 90.0: return 1.28
    if service_level >= 85.0: return 1.04
    return 0.84

# ----------------- Endpoints -----------------

@app.get("/", tags=["General"])
def read_root():
    return {
        "service": "PlastikTrack Inference API",
        "description": "API REST de Microservicios para Demanda y Cadena de Suministro",
        "version": model_version,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["General"])
def health():
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Modelo no cargado.")
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        uptime_seconds=round(time.time() - APP_START_TIME, 2),
        model_version=model_version,
        algorithm="HistGradientBoostingRegressor (scikit-learn)",
        cloud_provider="Oracle Cloud Infrastructure (OCI Free Tier) / Kubernetes",
        metrics=model_metrics
    )

@app.get("/api/v1/skus", response_model=List[SKUInfo], tags=["Catálogo"])
def get_skus():
    if not catalog_list:
        raise HTTPException(status_code=500, detail="Catálogo no disponible.")
    return [SKUInfo(**c) for c in catalog_list]

@app.post("/api/v1/predict", response_model=PredictResponse, tags=["Inferencia"])
def predict_demand(req: PredictRequest):
    t0 = time.time()
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo predictivo no disponible.")

    catalog_dict = {c["producto"]: c for c in catalog_list}
    results = []

    for item in req.items:
        if item.producto not in prod2code:
            raise HTTPException(
                status_code=400,
                detail=f"Producto '{item.producto}' desconocido. Consulte /api/v1/skus para ver productos válidos."
            )
        try:
            dt = datetime.strptime(item.fecha, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Formato de fecha inválido '{item.fecha}'. Use YYYY-MM-DD.")

        cat = catalog_dict.get(item.producto, {})
        precio = item.precio_unitario if item.precio_unitario is not None else cat.get("precio_unitario", 40.0)
        base_u = cat.get("unidades_promedio_diaria", 25.0)

        dia_sem = dt.weekday()
        dia_m = dt.day
        mes = dt.month
        es_quin = int((13 <= dia_m <= 16) or (dia_m >= 28))
        es_rep = int(dia_sem in (0, 2, 4))
        tend = (dt - datetime(2023, 1, 1)).days

        # Construir vector de características
        row = {
            "prod_cod": prod2code[item.producto],
            "dia_semana": dia_sem,
            "dia_mes": dia_m,
            "mes": mes,
            "es_quincena": es_quin,
            "es_dia_reparto": es_rep,
            "tendencia": max(tend, 0),
            "precio_unitario": precio,
            "lag_14": base_u * (1.2 if es_quin else 0.95),
            "lag_21": base_u,
            "media_28_lag14": base_u
        }

        X = pd.DataFrame([row])[FEATURES]
        pred_val = float(np.clip(model.predict(X)[0], 0, None))

        results.append(PredictionResult(
            producto=item.producto,
            fecha=item.fecha,
            demanda_predicha=round(pred_val, 2),
            es_quincena=bool(es_quin),
            es_dia_reparto=bool(es_rep),
            dia_semana=DIAS_MAP.get(dia_sem, ""),
            precio_unitario=precio
        ))

    latency = (time.time() - t0) * 1000.0
    return PredictResponse(
        total_items=len(results),
        predictions=results,
        latency_ms=round(latency, 2)
    )

@app.post("/api/v1/replenish", response_model=ReplenishResponse, tags=["Cadena de Suministro"])
def calculate_replenishment(req: ReplenishRequest):
    t0 = time.time()
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible.")

    catalog_dict = {c["producto"]: c for c in catalog_list}
    z_factor = get_z_factor(req.nivel_servicio_pct)
    sigma_error = float(model_metrics.get("rmse", 5.0))

    # Si no especifica items, calcular para los 12 SKUs completos
    if not req.items or len(req.items) == 0:
        target_items = [ReplenishItemInput(producto=c["producto"], inventario_actual=0, lead_time_dias=14) for c in catalog_list]
    else:
        target_items = req.items

    output_items = []
    total_unidades = 0
    total_inversion = 0.0

    today = date.today()
    future_dates = [pd.Timestamp(today) + pd.Timedelta(days=i) for i in range(1, 15)]

    for target in target_items:
        prod_name = target.producto
        if prod_name not in prod2code:
            raise HTTPException(status_code=400, detail=f"Producto '{prod_name}' inválido.")
        cat = catalog_dict.get(prod_name, {})
        precio = cat.get("precio_unitario", 45.0)
        base_u = cat.get("unidades_promedio_diaria", 25.0)

        # Simular los 14 días acumulados
        daily_preds = []
        for dt in future_dates:
            dia_sem = dt.weekday()
            dia_m = dt.day
            mes = dt.month
            es_quin = int((13 <= dia_m <= 16) or (dia_m >= 28))
            es_rep = int(dia_sem in (0, 2, 4))
            tend = (dt - pd.Timestamp("2023-01-01")).days

            row = {
                "prod_cod": prod2code[prod_name],
                "dia_semana": dia_sem,
                "dia_mes": dia_m,
                "mes": mes,
                "es_quincena": es_quin,
                "es_dia_reparto": es_rep,
                "tendencia": max(tend, 0),
                "precio_unitario": precio,
                "lag_14": base_u * (1.2 if es_quin else 0.95),
                "lag_21": base_u,
                "media_28_lag14": base_u
            }
            X = pd.DataFrame([row])[FEATURES]
            p = float(np.clip(model.predict(X)[0], 0, None))
            daily_preds.append(p)

        forecast_14d = int(round(sum(daily_preds)))
        # Fórmula analítica de Stock de Seguridad
        safety_stock = int(round(z_factor * sigma_error * np.sqrt(target.lead_time_dias)))
        # Fórmula de Pedido Sugerido
        suggested = max(0, forecast_14d + safety_stock - target.inventario_actual)
        costo_pedido = round(suggested * precio, 2)

        total_unidades += suggested
        total_inversion += costo_pedido

        output_items.append(ReplenishOutputItem(
            producto=prod_name,
            familia=cat.get("familia", "General"),
            precio_unitario=round(precio, 2),
            pronostico_14d=forecast_14d,
            stock_seguridad=safety_stock,
            inventario_actual=target.inventario_actual,
            pedido_sugerido=suggested,
            costo_estimado_pedido_mxn=costo_pedido
        ))

    latency = (time.time() - t0) * 1000.0
    return ReplenishResponse(
        horizonte_dias=14,
        nivel_servicio_pct=req.nivel_servicio_pct,
        factor_z=z_factor,
        total_unidades_sugeridas=total_unidades,
        inversion_total_mxn=round(total_inversion, 2),
        items=output_items,
        latency_ms=round(latency, 2)
    )

@app.get("/metrics", tags=["Observabilidad"])
def metrics():
    """Endpoint de métricas en formato texto para scraping de Prometheus"""
    uptime = time.time() - APP_START_TIME
    wape = model_metrics.get("wape_pct", 12.0)
    mae = model_metrics.get("mae", 3.8)
    rmse = model_metrics.get("rmse", 5.3)
    content = (
        f"# HELP plastiktrack_uptime_seconds Tiempo activo del servicio en segundos\n"
        f"# TYPE plastiktrack_uptime_seconds gauge\n"
        f"plastiktrack_uptime_seconds {uptime:.2f}\n"
        f"# HELP plastiktrack_model_wape_pct WAPE en conjunto de prueba\n"
        f"# TYPE plastiktrack_model_wape_pct gauge\n"
        f"plastiktrack_model_wape_pct {wape}\n"
        f"# HELP plastiktrack_model_mae MAE en conjunto de prueba\n"
        f"# TYPE plastiktrack_model_mae gauge\n"
        f"plastiktrack_model_mae {mae}\n"
        f"# HELP plastiktrack_model_rmse RMSE en conjunto de prueba\n"
        f"# TYPE plastiktrack_model_rmse gauge\n"
        f"plastiktrack_model_rmse {rmse}\n"
    )
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("services.modelos.api:app", host="0.0.0.0", port=8000, reload=True)
