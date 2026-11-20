# =====================================================================
# PlastikTrack - Variables de Infraestructura Terraform
# =====================================================================

variable "tenancy_ocid" {
  description = "OCID del Tenancy en Oracle Cloud Infrastructure"
  type        = string
  default     = "ocid1.tenancy.oc1..aaaaaaaaxlgvztnfk2dexamplenotreal"
}

variable "user_ocid" {
  description = "OCID del usuario de despliegue en OCI"
  type        = string
  default     = "ocid1.user.oc1..aaaaaaaabbso25460724example"
}

variable "fingerprint" {
  description = "Fingerprint de la llave pública API de OCI"
  type        = string
  default     = "20:a1:4b:9c:88:ef:12:34:56:78:90:ab:cd:ef:12:34"
}

variable "private_key_path" {
  description = "Ruta local a la llave privada RSA de OCI"
  type        = string
  default     = "~/.oci/oci_api_key.pem"
}

variable "compartment_id" {
  description = "OCID del Compartimento raíz o de desarrollo"
  type        = string
  default     = "ocid1.compartment.oc1..aaaaaaaaplastiktrack"
}

variable "region" {
  description = "Región de despliegue en OCI (México - Querétaro)"
  type        = string
  default     = "mx-queretaro-1"
}

variable "app_name" {
  description = "Nombre base de la aplicación y prefijo de recursos"
  type        = string
  default     = "plastiktrack"
}

variable "environment" {
  description = "Entorno de ejecución (dev / staging / prod)"
  type        = string
  default     = "prod"
}

variable "vcn_cidr" {
  description = "Rango CIDR para la Virtual Cloud Network (VCN)"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Rango CIDR para la subred pública"
  type        = string
  default     = "10.0.1.0/24"
}

variable "instance_shape" {
  description = "Shape de cómputo en OCI (Always Free Ampere A1 o E2.1.Micro)"
  type        = string
  default     = "VM.Standard.A1.Flex"
}

variable "instance_ocpus" {
  description = "Número de OCPUs para instancia Ampere A1 (Hasta 4 en Always Free)"
  type        = number
  default     = 2
}

variable "instance_memory_in_gbs" {
  description = "Memoria RAM en GB (Hasta 24 GB en Always Free)"
  type        = number
  default     = 12
}

variable "ssh_public_key" {
  description = "Llave pública SSH para administración de la instancia"
  type        = string
  default     = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFakeKeyForTerraformValidationOnly PlastikTrackAdmin"
}
