"""
services/modelos/generar_figuras_e3.py
Genera diagramas de arquitectura en alta resolución (300 DPI) para la entrega E3.
- e3_fig1_arquitectura_cloud.png: Arquitectura de Infraestructura en Oracle Cloud (OCI)
- e3_fig2_flujo_microservicios.png: Desacoplamiento de Microservicios y Contenedores Docker
- e3_fig3_k8s_cluster.png: Topología del Clúster Kubernetes y Autoescalado (HPA)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    os.makedirs("docs/img", exist_ok=True)
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['figure.dpi'] = 300

    # ==========================================
    # FIGURA 1: Arquitectura de Nube OCI (IaC)
    # ==========================================
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Fondo OCI Tenancy
    tenancy = patches.FancyBboxPatch((0.5, 0.5), 11, 6, boxstyle="round,pad=0.2",
                                     ec="#C74634", fc="#FFF5F5", lw=2, ls="--")
    ax.add_patch(tenancy)
    ax.text(0.8, 6.2, "Oracle Cloud Infrastructure (OCI) - Región México Querétaro (mx-queretaro-1)",
            fontsize=12, weight="bold", color="#C74634")
    ax.text(0.8, 5.9, "Tenancy: Siempre Gratuita (Always Free) · Alerta FinOps Activa ($1.00 USD/mes)",
            fontsize=9, color="#6B7280")

    # VCN Box
    vcn = patches.FancyBboxPatch((1.0, 1.0), 7.5, 4.6),
    vcn_patch = patches.FancyBboxPatch((1.0, 1.0), 7.5, 4.6, boxstyle="round,pad=0.2",
                                       ec="#2563EB", fc="#EFF6FF", lw=1.8)
    ax.add_patch(vcn_patch)
    ax.text(1.3, 5.3, "Virtual Cloud Network (VCN): 10.0.0.0/16", fontsize=11, weight="bold", color="#1E40AF")

    # Internet Gateway
    igw = patches.FancyBboxPatch((1.5, 4.0), 2.2, 0.9, boxstyle="round,pad=0.1", ec="#10B981", fc="#D1FAE5", lw=1.5)
    ax.add_patch(igw)
    ax.text(2.6, 4.5, "Internet Gateway\n(0.0.0.0/0)", ha="center", va="center", fontsize=9, weight="bold", color="#065F46")

    # Security List
    sl = patches.FancyBboxPatch((4.3, 4.0), 3.8, 0.9, boxstyle="round,pad=0.1", ec="#D97706", fc="#FEF3C7", lw=1.5)
    ax.add_patch(sl)
    ax.text(6.2, 4.5, "Security List / Firewall\nPuertos: 22 (SSH), 80/443, 8000 (API), 8501 (Tablero)",
            ha="center", va="center", fontsize=8, weight="bold", color="#92400E")

    # Subred Pública
    subnet = patches.FancyBboxPatch((1.4, 1.3), 6.7, 2.4, boxstyle="round,pad=0.15", ec="#3B82F6", fc="#DBEAFE", lw=1.5)
    ax.add_patch(subnet)
    ax.text(1.7, 3.4, "Subred Pública: 10.0.1.0/24 (publicsub)", fontsize=10, weight="bold", color="#1E3A8A")

    # Instancia de Cómputo Always Free
    vm = patches.FancyBboxPatch((1.8, 1.6), 5.9, 1.5, boxstyle="round,pad=0.1", ec="#4F46E5", fc="#EEF2FF", lw=1.5)
    ax.add_patch(vm)
    ax.text(4.75, 2.5, "Instancia VM.Standard.A1.Flex (Ampere A1 ARM64)\n2 OCPUs · 12 GB RAM · Ubuntu 22.04 LTS\nMotor de Contenedores Docker + Clúster Ligero K3s",
            ha="center", va="center", fontsize=9, weight="bold", color="#312E81")

    # Object Storage (Fuera de la VCN)
    oss = patches.FancyBboxPatch((9.0, 1.0), 2.3, 4.6, boxstyle="round,pad=0.2", ec="#059669", fc="#ECFDF5", lw=1.8)
    ax.add_patch(oss)
    ax.text(10.15, 5.2, "OCI Object\nStorage", ha="center", va="center", fontsize=11, weight="bold", color="#065F46")
    
    # Buckets
    b1 = patches.FancyBboxPatch((9.2, 3.4), 1.9, 1.1, boxstyle="round,pad=0.1", ec="#10B981", fc="#FFFFFF", lw=1.2)
    ax.add_patch(b1)
    ax.text(10.15, 3.95, "Capa raw/\nventas_distribuidora\n(Original auditado)", ha="center", va="center", fontsize=7.5)

    b2 = patches.FancyBboxPatch((9.2, 1.8), 1.9, 1.1, boxstyle="round,pad=0.1", ec="#10B981", fc="#FFFFFF", lw=1.2)
    ax.add_patch(b2)
    ax.text(10.15, 2.35, "Capa clean/\nventas_limpias.csv\n(PAR URL Segura)", ha="center", va="center", fontsize=7.5)

    # Conectores
    ax.annotate("", xy=(4.3, 4.45), xytext=(3.7, 4.45), arrowprops=dict(arrowstyle="->", lw=1.5, color="#10B981"))
    ax.annotate("", xy=(4.75, 3.1), xytext=(4.75, 4.0), arrowprops=dict(arrowstyle="->", lw=1.5, color="#D97706"))
    ax.annotate("", xy=(9.0, 2.35), xytext=(7.7, 2.35), arrowprops=dict(arrowstyle="<->", lw=1.5, color="#059669", ls="--"))

    plt.title("Figura 1: Arquitectura de Infraestructura en la Nube (Terraform en OCI Always Free)",
              fontsize=12, weight="bold", pad=15)
    plt.savefig("docs/img/e3_fig1_arquitectura_cloud.png", bbox_inches="tight")
    plt.close()

    # ==========================================
    # FIGURA 2: Arquitectura de Microservicios Docker
    # ==========================================
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Docker Host Container Network
    dnet = patches.FancyBboxPatch((0.5, 0.5), 11, 5, boxstyle="round,pad=0.2", ec="#0284C7", fc="#F0F9FF", lw=2)
    ax.add_patch(dnet)
    ax.text(0.8, 5.1, "Docker Engine / docker-compose.yml · Red Aislada 'plastiktrack-net' (Bridge)",
            fontsize=11, weight="bold", color="#0369A1")

    # Contenedor 1: Streamlit Dashboard
    c1 = patches.FancyBboxPatch((1.0, 1.2), 4.2, 3.4, boxstyle="round,pad=0.15", ec="#EF4444", fc="#FEF2F2", lw=1.8)
    ax.add_patch(c1)
    ax.text(3.1, 4.2, "Microservicio Frontend\nTablero Empresarial (Streamlit)", ha="center", va="center",
            fontsize=10, weight="bold", color="#991B1B")
    ax.text(3.1, 2.7, "• Imagen: python:3.12-slim\n• Puerto Expuesto: 8501\n• 4 KPIs Ejecutivos\n• 6 Gráficos Plotly Interactivos\n• Healthcheck: /_stcore/health\n• Usuario no root (appuser)",
            ha="center", va="center", fontsize=8.5, color="#1F2937")

    # Contenedor 2: API de Inferencia FastAPI
    c2 = patches.FancyBboxPatch((6.8, 1.2), 4.2, 3.4, boxstyle="round,pad=0.15", ec="#10B981", fc="#ECFDF5", lw=1.8)
    ax.add_patch(c2)
    ax.text(8.9, 4.2, "Microservicio Backend de IA\nAPI de Inferencia (FastAPI)", ha="center", va="center",
            fontsize=10, weight="bold", color="#065F46")
    ax.text(8.9, 2.7, "• Imagen: python:3.12-slim\n• Puerto Expuesto: 8000\n• Modelo: HistGradientBoosting (E2)\n• Endpoints: /health, /predict, /replenish\n• Contratos Validados con Pydantic\n• Healthcheck: /health",
            ha="center", va="center", fontsize=8.5, color="#1F2937")

    # Flechas de comunicación interna
    ax.annotate("Peticiones REST HTTP\n(http://api-modelos:8000)", xy=(6.8, 2.9), xytext=(5.2, 2.9),
                ha="center", va="bottom",
                arrowprops=dict(arrowstyle="->", lw=2, color="#0284C7"),
                fontsize=8.5, weight="bold", color="#0369A1")
    ax.annotate("Forecast & Pedidos Sugeridos", xy=(5.2, 2.3), xytext=(6.8, 2.3),
                ha="center", va="top",
                arrowprops=dict(arrowstyle="->", lw=2, color="#10B981"),
                fontsize=8.5, weight="bold", color="#047857")

    plt.title("Figura 2: Desacoplamiento de Microservicios y Contenedores en Docker Compose",
              fontsize=12, weight="bold", pad=15)
    plt.savefig("docs/img/e3_fig2_flujo_microservicios.png", bbox_inches="tight")
    plt.close()

    # ==========================================
    # FIGURA 3: Clúster Kubernetes y Autoescalado (HPA)
    # ==========================================
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Clúster k8s
    k8s = patches.FancyBboxPatch((0.5, 0.5), 11, 6, boxstyle="round,pad=0.2", ec="#326CE5", fc="#F8FAFC", lw=2)
    ax.add_patch(k8s)
    ax.text(0.8, 6.2, "Clúster Kubernetes (K3s) · Namespace: plastiktrack",
            fontsize=12, weight="bold", color="#326CE5")

    # Ingress NGINX
    ing = patches.FancyBboxPatch((1.0, 4.4), 10, 1.2, boxstyle="round,pad=0.1", ec="#4B5563", fc="#E5E7EB", lw=1.5)
    ax.add_patch(ing)
    ax.text(6.0, 5.0, "NGINX Ingress Controller (Ruteo HTTP Externo)", ha="center", va="center",
            fontsize=10, weight="bold", color="#111827")
    ax.text(3.5, 4.6, "Ruta / ➔ Tablero Service", ha="center", va="center", fontsize=8.5, color="#4B5563")
    ax.text(8.5, 4.6, "Ruta /api/v1, /docs, /health ➔ API Service", ha="center", va="center", fontsize=8.5, color="#4B5563")

    # Tablero Service & Pod
    ts = patches.FancyBboxPatch((1.0, 2.8), 4.5, 1.2, boxstyle="round,pad=0.1", ec="#DC2626", fc="#FEE2E2", lw=1.2)
    ax.add_patch(ts)
    ax.text(3.25, 3.4, "Service: tablero-service (ClusterIP:8501)", ha="center", va="center", fontsize=9, weight="bold", color="#991B1B")

    tp = patches.FancyBboxPatch((1.0, 1.0), 4.5, 1.4, boxstyle="round,pad=0.1", ec="#DC2626", fc="#FFFFFF", lw=1.2)
    ax.add_patch(tp)
    ax.text(3.25, 1.7, "Pod: tablero-deployment (1 Réplica)\nContenedor Streamlit · Probes de Salud Activos",
            ha="center", va="center", fontsize=8.5, color="#1F2937")

    # API Service & Pods con HPA
    asvc = patches.FancyBboxPatch((6.5, 2.8), 4.5, 1.2, boxstyle="round,pad=0.1", ec="#059669", fc="#D1FAE5", lw=1.2)
    ax.add_patch(asvc)
    ax.text(8.75, 3.4, "Service: api-service (ClusterIP:8000)", ha="center", va="center", fontsize=9, weight="bold", color="#065F46")

    ap = patches.FancyBboxPatch((6.5, 1.0), 4.5, 1.4, boxstyle="round,pad=0.1", ec="#059669", fc="#FFFFFF", lw=1.2)
    ax.add_patch(ap)
    ax.text(8.75, 1.7, "Pods: api-modelos-deployment (2 a 6 Réplicas)\nHorizontal Pod Autoscaler (HPA: CPU > 70%)\nRollingUpdate: maxSurge=1, maxUnavailable=0",
            ha="center", va="center", fontsize=8.5, color="#1F2937")

    # Flechas de conexión
    ax.annotate("", xy=(3.25, 4.0), xytext=(3.25, 4.4), arrowprops=dict(arrowstyle="->", lw=1.5, color="#4B5563"))
    ax.annotate("", xy=(3.25, 2.4), xytext=(3.25, 2.8), arrowprops=dict(arrowstyle="->", lw=1.5, color="#DC2626"))
    ax.annotate("", xy=(8.75, 4.0), xytext=(8.75, 4.4), arrowprops=dict(arrowstyle="->", lw=1.5, color="#4B5563"))
    ax.annotate("", xy=(8.75, 2.4), xytext=(8.75, 2.8), arrowprops=dict(arrowstyle="->", lw=1.5, color="#059669"))

    plt.title("Figura 3: Topología del Clúster Kubernetes con Ingress, Servicios y Autoescalado Horizontal (HPA)",
              fontsize=12, weight="bold", pad=15)
    plt.savefig("docs/img/e3_fig3_k8s_cluster.png", bbox_inches="tight")
    plt.close()

    print("Diagramas de arquitectura E3 generados exitosamente en docs/img/")

if __name__ == "__main__":
    main()
