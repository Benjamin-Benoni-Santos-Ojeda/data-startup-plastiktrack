"""
tests/test_infra.py
Validación automatizada de sintaxis y coherencia para Docker, Docker Compose, Terraform y Kubernetes.
"""

import os
import yaml

def test_dockerfiles_exist_and_valid():
    dockerfiles = [
        "services/modelos/Dockerfile",
        "services/tablero/Dockerfile",
        "services/worker/Dockerfile"
    ]
    for df in dockerfiles:
        assert os.path.exists(df), f"Falta {df}"
        with open(df, "r", encoding="utf-8") as f:
            content = f.read()
            assert "FROM python:" in content
            assert "WORKDIR /app" in content

def test_docker_compose_valid():
    compose_path = "docker-compose.yml"
    assert os.path.exists(compose_path)
    with open(compose_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        assert "services" in data
        assert "api-modelos" in data["services"]
        assert "tablero" in data["services"]
        assert "networks" in data
        assert "plastiktrack-net" in data["networks"]

def test_terraform_files_exist():
    tf_files = [
        "infra/terraform/provider.tf",
        "infra/terraform/variables.tf",
        "infra/terraform/main.tf",
        "infra/terraform/outputs.tf"
    ]
    for tf in tf_files:
        assert os.path.exists(tf), f"Falta {tf}"
        with open(tf, "r", encoding="utf-8") as f:
            content = f.read()
            assert len(content) > 50

def test_k8s_manifests_valid_yaml():
    k8s_files = [
        "k8s/00-namespace.yaml",
        "k8s/01-configmap.yaml",
        "k8s/02-api-deployment.yaml",
        "k8s/03-api-service.yaml",
        "k8s/04-tablero-deployment.yaml",
        "k8s/05-tablero-service.yaml",
        "k8s/06-ingress.yaml",
        "k8s/07-hpa.yaml"
    ]
    for kf in k8s_files:
        assert os.path.exists(kf), f"Falta {kf}"
        with open(kf, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
            assert "apiVersion" in doc, f"Falta apiVersion en {kf}"
            assert "kind" in doc, f"Falta kind en {kf}"
            assert "metadata" in doc, f"Falta metadata en {kf}"
            assert doc["metadata"].get("namespace", "plastiktrack") in ["plastiktrack", None]
