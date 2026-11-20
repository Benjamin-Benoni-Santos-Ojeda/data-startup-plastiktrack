# Manifiestos de Kubernetes (k8s) para PlastikTrack

Este directorio contiene los manifiestos declarativos de orquestación para desplegar los microservicios de **PlastikTrack** en un clúster de **Kubernetes / K3s** en Oracle Cloud Infrastructure (OCI).

## Manifiestos Incluidos
| Archivo | Objeto Kubernetes | Función |
| :--- | :--- | :--- |
| `00-namespace.yaml` | `Namespace` | Aislamiento lógico del entorno (`plastiktrack`). |
| `01-configmap.yaml` | `ConfigMap` | Variables de entorno centralizadas (URLs internas, endpoints, buckets). |
| `02-api-deployment.yaml` | `Deployment` | Despliegue de la API de inferencia (2 réplicas, probes de salud, rolling update). |
| `03-api-service.yaml` | `Service (ClusterIP)` | Abstracción de red interna en puerto 8000 para balanceo hacia la API. |
| `04-tablero-deployment.yaml` | `Deployment` | Despliegue del Dashboard Streamlit con límites de recursos. |
| `05-tablero-service.yaml` | `Service (ClusterIP)` | Abstracción de red interna en puerto 8501 para el Dashboard. |
| `06-ingress.yaml` | `Ingress` | Enrutador unificado HTTP (NGINX Ingress) dividiendo `/` para tablero y `/api/v1` para la API. |
| `07-hpa.yaml` | `HorizontalPodAutoscaler` | Autoescalado horizontal de 2 a 6 réplicas al superar 70% de CPU. |

## Despliegue en Clúster
```bash
# Aplicar todos los manifiestos en orden
kubectl apply -f k8s/

# Verificar estado de los pods y servicios
kubectl get pods -n plastiktrack -o wide
kubectl get svc,ingress,hpa -n plastiktrack
```
