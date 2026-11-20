"""
tests/test_api.py
Pruebas automatizadas para el microservicio de inferencia FastAPI de PlastikTrack.
Valida contratos Pydantic, respuestas HTTP, lógica de pronóstico y motor de compras a 14 días.
"""

import unittest
from fastapi.testclient import TestClient
from services.modelos.api import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "PlastikTrack" in data["service"]
    assert "/docs" in data["docs"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["uptime_seconds"] >= 0
    assert "HistGradientBoostingRegressor" in data["algorithm"]
    assert "OCI" in data["cloud_provider"]
    assert "wape_pct" in data["metrics"]

def test_get_skus_catalog():
    response = client.get("/api/v1/skus")
    assert response.status_code == 200
    skus = response.json()
    assert len(skus) == 12
    nombres = [s["producto"] for s in skus]
    assert "Bolsa Negra Camiseta" in nombres
    assert "Pelicula Plastica Emplaye" in nombres
    assert "Vasos Desechables" in nombres

def test_predict_demand_valid():
    payload = {
        "items": [
            {
                "producto": "Bolsa Negra Camiseta",
                "fecha": "2026-11-20",  # Viernes (Día de reparto)
                "precio_unitario": 42.0,
                "inventario_actual": 30
            },
            {
                "producto": "Bolsa Rollo Poliseda",
                "fecha": "2026-11-15",  # Quincena
                "precio_unitario": 36.0,
                "inventario_actual": 10
            }
        ]
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] == 2
    assert len(data["predictions"]) == 2
    assert data["predictions"][0]["demanda_predicha"] > 0
    assert data["predictions"][0]["es_dia_reparto"] is True
    assert data["predictions"][1]["es_quincena"] is True

def test_predict_unknown_sku():
    payload = {
        "items": [
            {"producto": "Bolsa Desconocida XYZ", "fecha": "2026-11-20"}
        ]
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 400
    assert "desconocido" in response.json()["detail"].lower()

def test_replenish_all_skus():
    payload = {
        "nivel_servicio_pct": 95.0
    }
    response = client.post("/api/v1/replenish", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["horizonte_dias"] == 14
    assert data["nivel_servicio_pct"] == 95.0
    assert data["factor_z"] == 1.65
    assert len(data["items"]) == 12
    assert data["total_unidades_sugeridas"] > 0
    assert data["inversion_total_mxn"] > 0

    # Verificar que el producto estrella tenga el pedido mayor
    estrella = next(i for i in data["items"] if i["producto"] == "Bolsa Negra Camiseta")
    assert estrella["pedido_sugerido"] > 0
    assert estrella["stock_seguridad"] > 0

def test_replenish_with_high_stock():
    # Si tenemos inventario suficiente (ej. 2000 bultos), el pedido sugerido debe ser 0
    payload = {
        "items": [
            {
                "producto": "Bolsa Negra Camiseta",
                "inventario_actual": 5000,
                "lead_time_dias": 14
            }
        ],
        "nivel_servicio_pct": 95.0
    }
    response = client.post("/api/v1/replenish", json=payload)
    assert response.status_code == 200
    data = response.json()
    item = data["items"][0]
    assert item["pedido_sugerido"] == 0
    assert item["costo_estimado_pedido_mxn"] == 0.0

def test_prometheus_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "plastiktrack_uptime_seconds" in response.text
    assert "plastiktrack_model_wape_pct" in response.text
