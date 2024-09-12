import os
import subprocess
import time
from digitalocean import Manager, KubernetesCluster

def create_kubernetes_cluster(token, cluster_name, region, node_pool_name, node_size, node_count):
    manager = Manager(token=token)
    
    # Create the Kubernetes cluster
    cluster = KubernetesCluster(
        token=token,
        name=cluster_name,
        region=region,
        version="latest",
        node_pools=[
            {
                "size": node_size,
                "count": node_count,
                "name": node_pool_name,
            }
        ],
    )
    
    cluster.create()
    
    # Wait for the cluster to be ready
    while cluster.status['state'] != 'running':
        time.sleep(30)
        cluster.load()
    
    print(f"Kubernetes cluster '{cluster_name}' created successfully.")
    return cluster

def configure_kubectl(cluster):
    # Use doctl to configure kubectl
    subprocess.run(["doctl", "kubernetes", "cluster", "kubeconfig", "save", cluster.id], check=True)
    print("kubectl configured successfully.")

def install_ingress_controller():
    # Install NGINX Ingress Controller
    subprocess.run(["kubectl", "apply", "-f", "https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.0/deploy/static/provider/do/deploy.yaml"], check=True)
    print("NGINX Ingress Controller installed successfully.")

def main():
    token = os.getenv("DO_TOKEN")
    if not token:
        raise ValueError("DigitalOcean API token not found. Please set the DO_TOKEN environment variable.")
    
    cluster_name = input("Enter the name for your Kubernetes cluster: ")
    region = input("Enter the region for your cluster (e.g., nyc1): ")
    node_pool_name = input("Enter a name for the node pool: ")
    node_size = input("Enter the size for the nodes (e.g., s-2vcpu-4gb): ")
    node_count = int(input("Enter the number of nodes: "))
    
    cluster = create_kubernetes_cluster(token, cluster_name, region, node_pool_name, node_size, node_count)
    configure_kubectl(cluster)
    install_ingress_controller()
    
    print("Initial setup complete. Your Kubernetes cluster is ready to use.")

if __name__ == "__main__":
    main()