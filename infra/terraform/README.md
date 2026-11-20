# Infraestructura como Código (IaC) - Terraform para PlastikTrack

Este directorio contiene la definición modular y reproducible de la infraestructura en la nube bajo **Oracle Cloud Infrastructure (OCI Always Free Tier)** para la entrega **E3**.

## Recursos Provisionados
1. **Red VCN y Conectividad:**
   - Virtual Cloud Network (`10.0.0.0/16`) con DNS label `plastiktrackvcn`.
   - Internet Gateway con tabla de ruteo para salida a Internet (`0.0.0.0/0`).
   - Subred pública (`10.0.1.0/24`) con asignación automática de IP pública.
2. **Seguridad y Hardening:**
   - Listas de seguridad con principio de mínimo privilegio.
   - Puertos abiertos controlados: `22` (SSH administrativo), `80/443` (Ingress NGINX), `8000` (FastAPI Inferencia) y `8501` (Dashboard Streamlit).
3. **Almacenamiento (Data Lake):**
   - Bucket `plastiktrack-lake` en OCI Object Storage (Querétaro) con versionado habilitado y acceso controlado mediante Solicitudes Preautenticadas (PAR).
4. **Cómputo Always Free:**
   - Instancia OCI Ampere A1 (2 OCPUs, 12 GB RAM) con script de inicialización Cloud-Init para Docker y motor ligero K3s (Kubernetes).

## Comandos de Ejecución
```bash
# 1. Inicializar plugins del proveedor OCI
terraform init

# 2. Validar sintaxis y coherencia declarativa
terraform validate

# 3. Visualizar plan de aprovisionamiento
terraform plan

# 4. Desplegar infraestructura
terraform apply -auto-approve

# 5. Destruir infraestructura al finalizar pruebas (Responsabilidad FinOps)
terraform destroy -auto-approve
```
