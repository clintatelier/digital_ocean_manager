import os
import json
import subprocess
from kubernetes import client, config

def get_do_token():
    return os.getenv('DO_TOKEN')

def get_kubernetes_info():
    config.load_kube_config()
    k8s_config = config.kube_config.load_kube_config()
    current_context = config.list_kube_config_contexts()[1]
    cluster_info = current_context['context']['cluster']
    return {
        "cluster_name": cluster_info,
        "api_endpoint": k8s_config.host,
    }

def get_app_info(app_name, app_type, registry=None):
    app_info = {
        "name": app_name,
        "type": app_type,
    }
    if registry:
        app_info["registry"] = registry
    
    if app_type in ["web_app", "static_site"]:
        v1 = client.CoreV1Api()
        try:
            service = v1.read_namespaced_service(f"{app_name}-service", "default")
            app_info["service_name"] = service.metadata.name
            app_info["service_type"] = service.spec.type
            app_info["service_port"] = service.spec.ports[0].port
        except client.exceptions.ApiException:
            app_info["service_info"] = "Service not found"
    
    return app_info

def gather_and_output_info(app_name, app_type, registry=None):
    deployment_info = {
        "do_token": get_do_token(),
        "kubernetes_info": get_kubernetes_info(),
        "app_info": get_app_info(app_name, app_type, registry)
    }

    output_file = f"{app_name}_deployment_info.json"
    with open(output_file, 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print(f"Deployment information has been saved to {output_file}")
    return output_file

if __name__ == "__main__":
    app_name = input("Enter the app name: ")
    app_type = input("Enter the app type (web_app, static_site, or mobile_app): ")
    registry = input("Enter the container registry (if applicable, otherwise press Enter): ")
    
    output_file = gather_and_output_info(app_name, app_type, registry)
    print(f"Deployment information saved to {output_file}")