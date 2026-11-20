# =====================================================================
# PlastikTrack - Dockerfile para Worker Asíncrono de Reentrenamiento
# =====================================================================

FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY services/ /app/services/
COPY limpiar_datos.py /app/limpiar_datos.py

RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1

CMD ["python", "services/modelos/entrenar_modelo.py"]
