import os
import subprocess
import yaml
from kubernetes import client, config
from gather_deployment_info import gather_and_output_info

def build_and_push_image(app_name, registry):
    # Build the Docker image
    subprocess.run(["docker", "build", "-t", f"{registry}/{app_name}:latest", f"../web_apps/{app_name}"], check=True)
    
    # Push the image to the registry
    subprocess.run(["docker", "push", f"{registry}/{app_name}:latest"], check=True)

def create_kubernetes_manifests(app_name, registry):
    # Create deployment YAML
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": app_name},
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": app_name}},
            "template": {
                "metadata": {"labels": {"app": app_name}},
                "spec": {
                    "containers": [{
                        "name": app_name,
                        "image": f"{registry}/{app_name}:latest",
                        "ports": [{"containerPort": 8000}]
                    }]
                }
            }
        }
    }

    # Create service YAML
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": f"{app_name}-service"},
        "spec": {
            "selector": {"app": app_name},
            "ports": [{"port": 80, "targetPort": 8000}],
            "type": "ClusterIP"
        }
    }

    # Write manifests to files
    with open(f"{app_name}-deployment.yaml", "w") as f:
        yaml.dump(deployment, f)
    with open(f"{app_name}-service.yaml", "w") as f:
        yaml.dump(service, f)

def apply_kubernetes_manifests(app_name):
    # Apply the Kubernetes manifests
    subprocess.run(["kubectl", "apply", "-f", f"{app_name}-deployment.yaml"], check=True)
    subprocess.run(["kubectl", "apply", "-f", f"{app_name}-service.yaml"], check=True)

def deploy_web_app(app_name, registry):
    try:
        # Build and push Docker image
        build_and_push_image(app_name, registry)

        # Create Kubernetes manifest files
        create_kubernetes_manifests(app_name, registry)

        # Apply Kubernetes manifests
        apply_kubernetes_manifests(app_name)

        print(f"Web app {app_name} deployed successfully to Kubernetes cluster")

        # Gather and output deployment information
        output_file = gather_and_output_info(app_name, "web_app", registry)
        print(f"Deployment information saved to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error deploying web app: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    # Load Kubernetes configuration
    config.load_kube_config()

    app_name = input("Enter the name of your web app: ")
    registry = input("Enter your DigitalOcean container registry (e.g., registry.digitalocean.com/your-registry): ")
    
    deploy_web_app(app_name, registry)