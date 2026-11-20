# =====================================================================
# PlastikTrack - Dockerfile para Microservicio de Inferencia (FastAPI)
# Base ligera Python 3.12 Slim con optimizaciones de producción
# =====================================================================

FROM python:3.12-slim AS base

WORKDIR /app

# Instalar dependencias del sistema y limpiar cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos y cache de pip
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar artefacto de modelo y código fuente del servicio
COPY services/modelos/modelo_demanda.joblib /app/services/modelos/modelo_demanda.joblib
COPY services/modelos/api.py /app/services/modelos/api.py
COPY services/modelos/__init__.py /app/services/modelos/__init__.py

# Usuario no privilegiado para seguridad en contenedores
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/services/modelos/modelo_demanda.joblib \
    PORT=8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "services.modelos.api:app", "--host", "0.0.0.0", "--port", "8000"]
