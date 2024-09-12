import os
import subprocess
import yaml
from kubernetes import client, config

def build_and_push_image(site_name, registry):
    # Build the Docker image
    subprocess.run(["docker", "build", "-t", f"{registry}/{site_name}:latest", f"../static_sites/{site_name}"], check=True)
    
    # Push the image to the registry
    subprocess.run(["docker", "push", f"{registry}/{site_name}:latest"], check=True)

def create_kubernetes_manifests(site_name, registry):
    # Create deployment YAML
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": site_name},
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": site_name}},
            "template": {
                "metadata": {"labels": {"app": site_name}},
                "spec": {
                    "containers": [{
                        "name": site_name,
                        "image": f"{registry}/{site_name}:latest",
                        "ports": [{"containerPort": 80}]
                    }]
                }
            }
        }
    }

    # Create service YAML
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": f"{site_name}-service"},
        "spec": {
            "selector": {"app": site_name},
            "ports": [{"port": 80, "targetPort": 80}],
            "type": "ClusterIP"
        }
    }

    # Create ingress YAML
    ingress = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": f"{site_name}-ingress",
            "annotations": {
                "kubernetes.io/ingress.class": "nginx",
                "cert-manager.io/cluster-issuer": "letsencrypt-prod"
            }
        },
        "spec": {
            "rules": [{
                "host": f"{site_name}.example.com",
                "http": {
                    "paths": [{
                        "path": "/",
                        "pathType": "Prefix",
                        "backend": {
                            "service": {
                                "name": f"{site_name}-service",
                                "port": {"number": 80}
                            }
                        }
                    }]
                }
            }],
            "tls": [{
                "hosts": [f"{site_name}.example.com"],
                "secretName": f"{site_name}-tls"
            }]
        }
    }

    # Write manifests to files
    with open(f"{site_name}-deployment.yaml", "w") as f:
        yaml.dump(deployment, f)
    with open(f"{site_name}-service.yaml", "w") as f:
        yaml.dump(service, f)
    with open(f"{site_name}-ingress.yaml", "w") as f:
        yaml.dump(ingress, f)

def apply_kubernetes_manifests(site_name):
    # Apply the Kubernetes manifests
    subprocess.run(["kubectl", "apply", "-f", f"{site_name}-deployment.yaml"], check=True)
    subprocess.run(["kubectl", "apply", "-f", f"{site_name}-service.yaml"], check=True)
    subprocess.run(["kubectl", "apply", "-f", f"{site_name}-ingress.yaml"], check=True)

def deploy_static_site(site_name, registry):
    try:
        # Build and push Docker image
        build_and_push_image(site_name, registry)

        # Create Kubernetes manifest files
        create_kubernetes_manifests(site_name, registry)

        # Apply Kubernetes manifests
        apply_kubernetes_manifests(site_name)

        print(f"Static site {site_name} deployed successfully to Kubernetes cluster")
        print(f"Access your site at: https://{site_name}.example.com")
    except subprocess.CalledProcessError as e:
        print(f"Error deploying static site: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    # Load Kubernetes configuration
    config.load_kube_config()

    site_name = input("Enter the name of your static site: ")
    registry = input("Enter your DigitalOcean container registry (e.g., registry.digitalocean.com/your-registry): ")
    
    deploy_static_site(site_name, registry)