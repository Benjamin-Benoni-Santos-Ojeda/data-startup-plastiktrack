# =====================================================================
# PlastikTrack - Recursos de Infraestructura OCI (main.tf)
# Red VCN, Subredes, Firewall / Security List, Cómputo Always Free y Data Lake
# =====================================================================

# 1. Virtual Cloud Network (VCN)
resource "oci_core_vcn" "plastiktrack_vcn" {
  cidr_block     = var.vcn_cidr
  compartment_id = var.compartment_id
  display_name   = "${var.app_name}-vcn-${var.environment}"
  dns_label      = "plastiktrackvcn"

  freeform_tags = {
    "Project"     = "PlastikTrack"
    "Environment" = var.environment
    "ManagedBy"   = "Terraform"
  }
}

# 2. Internet Gateway para salida a Internet
resource "oci_core_internet_gateway" "plastiktrack_ig" {
  compartment_id = var.compartment_id
  display_name   = "${var.app_name}-igw"
  vcn_id         = oci_core_vcn.plastiktrack_vcn.id
  enabled        = true
}

# 3. Tabla de Ruteo Pública
resource "oci_core_route_table" "plastiktrack_public_rt" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.plastiktrack_vcn.id
  display_name   = "${var.app_name}-public-rt"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.plastiktrack_ig.id
  }
}

# 4. Lista de Seguridad (Firewall por Capas / Hardening)
resource "oci_core_security_list" "plastiktrack_sl" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.plastiktrack_vcn.id
  display_name   = "${var.app_name}-security-list"

  # Salida libre hacia Internet
  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
    stateless   = false
  }

  # Entrada: SSH (Puerto 22) restringido
  ingress_security_rules {
    protocol  = "6" # TCP
    source    = "0.0.0.0/0"
    stateless = false
    tcp_options {
      min = 22
      max = 22
    }
    description = "Acceso administrativo seguro SSH"
  }

  # Entrada: HTTP (Puerto 80) e HTTPS (443) para Ingress Controller
  ingress_security_rules {
    protocol  = "6"
    source    = "0.0.0.0/0"
    stateless = false
    tcp_options {
      min = 80
      max = 80
    }
    description = "Tráfico HTTP Ingress NGINX"
  }

  ingress_security_rules {
    protocol  = "6"
    source    = "0.0.0.0/0"
    stateless = false
    tcp_options {
      min = 443
      max = 443
    }
    description = "Tráfico HTTPS TLS Seguro"
  }

  # Entrada: API de Inferencia (Puerto 8000)
  ingress_security_rules {
    protocol  = "6"
    source    = "0.0.0.0/0"
    stateless = false
    tcp_options {
      min = 8000
      max = 8000
    }
    description = "Microservicio API de Inferencia FastAPI"
  }

  # Entrada: Dashboard Empresarial (Puerto 8501)
  ingress_security_rules {
    protocol  = "6"
    source    = "0.0.0.0/0"
    stateless = false
    tcp_options {
      min = 8501
      max = 8501
    }
    description = "Microservicio Dashboard Streamlit"
  }
}

# 5. Subred Pública
resource "oci_core_subnet" "plastiktrack_public_subnet" {
  cidr_block        = var.public_subnet_cidr
  compartment_id    = var.compartment_id
  vcn_id            = oci_core_vcn.plastiktrack_vcn.id
  display_name      = "${var.app_name}-public-subnet"
  dns_label         = "publicsub"
  route_table_id    = oci_core_route_table.plastiktrack_public_rt.id
  security_list_ids = [oci_core_security_list.plastiktrack_sl.id]
}

# 6. Bucket de Object Storage (Data Lake en Querétaro)
resource "oci_objectstorage_bucket" "datastartup_lake" {
  compartment_id = var.compartment_id
  name           = "${var.app_name}-lake"
  namespace      = "axlgvztnfk2d"
  storage_tier   = "Standard"
  versioning     = "Enabled"
  access_type    = "NoPublicAccess"

  freeform_tags = {
    "Project" = "PlastikTrack"
    "Capa"    = "DataLake-Raw-Clean"
  }
}

# 7. Instancia de Cómputo Always Free (Host para Docker / K3s)
resource "oci_core_instance" "k8s_node" {
  availability_domain = "AD-1"
  compartment_id      = var.compartment_id
  display_name        = "${var.app_name}-k8s-node"
  shape               = var.instance_shape

  shape_config {
    ocpus         = var.instance_ocpus
    memory_in_gbs = var.instance_memory_in_gbs
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.plastiktrack_public_subnet.id
    display_name     = "${var.app_name}-vnic"
    assign_public_ip = true
  }

  source_details {
    source_type = "image"
    source_id   = "ocid1.image.oc1.mx-queretaro-1.aaaaaaaaexampleubuntults"
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key
    user_data           = base64encode(<<-EOF
      #!/bin/bash
      apt-get update && apt-get install -y docker.io docker-compose curl
      systemctl enable docker
      systemctl start docker
      usermod -aG docker ubuntu
      # Instalación K3s lightweight Kubernetes
      curl -sfL https://get.k3s.io | sh -
    EOF
    )
  }

  freeform_tags = {
    "Project" = "PlastikTrack"
    "Tier"    = "AlwaysFree"
  }
}
