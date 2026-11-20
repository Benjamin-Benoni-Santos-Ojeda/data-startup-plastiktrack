# =====================================================================
# PlastikTrack - Outputs de Infraestructura Terraform
# =====================================================================

output "vcn_id" {
  description = "OCID de la Red Virtual (VCN) creada en OCI"
  value       = oci_core_vcn.plastiktrack_vcn.id
}

output "public_subnet_id" {
  description = "OCID de la Subred Pública"
  value       = oci_core_subnet.plastiktrack_public_subnet.id
}

output "node_public_ip" {
  description = "Dirección IP pública asignada a la instancia de cómputo / clúster"
  value       = oci_core_instance.k8s_node.public_ip
}

output "data_lake_bucket_name" {
  description = "Nombre del bucket Data Lake creado en OCI Object Storage"
  value       = oci_objectstorage_bucket.datastartup_lake.name
}

output "api_endpoint" {
  description = "URL pública de acceso a la API REST de Inferencia"
  value       = "http://${oci_core_instance.k8s_node.public_ip}:8000"
}

output "tablero_endpoint" {
  description = "URL pública de acceso al Tablero Streamlit"
  value       = "http://${oci_core_instance.k8s_node.public_ip}:8501"
}
