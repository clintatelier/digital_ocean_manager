import os
import json
import subprocess
import sys

def get_do_token(project_name, droplet_ip):
    print(f"Retrieving DigitalOcean API token for project '{project_name}'...")
    try:
        token = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"/usr/local/bin/manage_do_credentials.sh get {project_name}"], capture_output=True, text=True, check=True)
        return token.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve DigitalOcean API token for project '{project_name}'")
        return None

def get_droplet_info(droplet_ip):
    print(f"Gathering information about the droplet at {droplet_ip}...")
    droplet_info = {
        "ip_address": droplet_ip,
    }
    
    # Get OS information
    try:
        os_info = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", "cat /etc/os-release"], capture_output=True, text=True, check=True)
        for line in os_info.stdout.split('\n'):
            if line.startswith('PRETTY_NAME='):
                droplet_info["os"] = line.split('=')[1].strip('"')
                break
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve OS information from the droplet at {droplet_ip}")
        droplet_info["os"] = "Unable to retrieve OS information"

    return droplet_info

def get_project_info(project_name, project_type, droplet_ip):
    print(f"Gathering information about the {project_type} project '{project_name}'...")
    project_info = {
        "name": project_name,
        "type": project_type,
    }
    
    # Get Apache configuration for the project
    try:
        apache_config = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /etc/apache2/sites-available/{project_name}.conf"], capture_output=True, text=True, check=True)
        project_info["apache_config"] = apache_config.stdout
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve Apache configuration for {project_name}")
        project_info["apache_config"] = "Unable to retrieve Apache configuration"
    
    # Get virtual environment information
    if project_type != "static":
        try:
            venv_info = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"ls -l /opt/venvs/{project_name}"], capture_output=True, text=True, check=True)
            project_info["virtual_environment"] = venv_info.stdout.strip()
        except subprocess.CalledProcessError:
            print(f"Warning: Unable to retrieve virtual environment information for {project_name}")
            project_info["virtual_environment"] = "Unable to retrieve virtual environment information"
    
    return project_info

def get_project_dependencies(project_name, project_type, droplet_ip):
    print(f"Gathering project dependencies for '{project_name}'...")
    try:
        if project_type == "python":
            dependencies = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/projects/{project_name}/requirements.txt"], capture_output=True, text=True, check=True)
        elif project_type == "node":
            dependencies = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/projects/{project_name}/package.json"], capture_output=True, text=True, check=True)
        elif project_type == "php":
            dependencies = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/projects/{project_name}/composer.json"], capture_output=True, text=True, check=True)
        else:
            return "No dependencies for static projects"
        return dependencies.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve project dependencies for {project_name}")
        return "Unable to retrieve project dependencies"

def get_database_info(project_name, droplet_ip):
    print(f"Gathering database information for '{project_name}'...")
    # This is a placeholder. In a real scenario, you'd need to securely retrieve and store this information.
    return {
        "type": "MySQL",
        "name": f"{project_name}_db",
        "user": f"{project_name}_user",
        "connection_string": "mysql://user:password@localhost:3306/dbname"
    }

def get_environment_variables(project_name, droplet_ip):
    print(f"Gathering environment variables for '{project_name}'...")
    try:
        env_vars = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/projects/{project_name}/.env"], capture_output=True, text=True, check=True)
        return env_vars.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve environment variables for {project_name}")
        return "Unable to retrieve environment variables"

def get_project_structure(project_name, droplet_ip):
    print(f"Gathering project structure for '{project_name}'...")
    try:
        structure = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"tree /opt/projects/{project_name} -L 2"], capture_output=True, text=True, check=True)
        return structure.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve project structure for {project_name}")
        return "Unable to retrieve project structure"

def get_application_entry_points(project_name, project_type, droplet_ip):
    print(f"Gathering application entry points for '{project_name}'...")
    try:
        if project_type == "python":
            entry_points = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/projects/{project_name}/wsgi.py"], capture_output=True, text=True, check=True)
        elif project_type == "node":
            entry_points = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/projects/{project_name}/app.js"], capture_output=True, text=True, check=True)
        elif project_type == "php":
            entry_points = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/projects/{project_name}/index.php"], capture_output=True, text=True, check=True)
        else:
            return "No specific entry point for static projects"
        return entry_points.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve application entry points for {project_name}")
        return "Unable to retrieve application entry points"

def get_logging_configuration(project_name, droplet_ip):
    print(f"Gathering logging configuration for '{project_name}'...")
    try:
        logging_config = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/projects/{project_name}/logging.conf"], capture_output=True, text=True, check=True)
        return logging_config.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve logging configuration for {project_name}")
        return "Unable to retrieve logging configuration"

def get_monitoring_info(project_name, droplet_ip):
    print(f"Gathering monitoring information for '{project_name}'...")
    # This is a placeholder. In a real scenario, you'd provide actual monitoring dashboard URLs or endpoints.
    return {
        "monitoring_dashboard": f"https://monitoring.yourdomain.com/dashboard/{project_name}",
        "performance_metrics_endpoint": f"https://api.yourdomain.com/metrics/{project_name}"
    }

def get_backup_recovery_info(project_name, droplet_ip):
    print(f"Gathering backup and recovery information for '{project_name}'...")
    # This is a placeholder. In a real scenario, you'd provide actual backup procedures and recovery steps.
    return {
        "backup_procedure": "Daily automated backups at 2 AM UTC",
        "recovery_steps": "1. Stop the application\n2. Restore from latest backup\n3. Restart the application"
    }

def get_ssl_tls_config(project_name, droplet_ip):
    print(f"Gathering SSL/TLS configuration for '{project_name}'...")
    try:
        ssl_config = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /etc/apache2/sites-available/{project_name}-le-ssl.conf"], capture_output=True, text=True, check=True)
        return ssl_config.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve SSL/TLS configuration for {project_name}")
        return "Unable to retrieve SSL/TLS configuration"

def get_custom_domain_info(project_name, droplet_ip):
    print(f"Gathering custom domain information for '{project_name}'...")
    try:
        domain_info = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /etc/apache2/sites-available/{project_name}.conf | grep ServerName"], capture_output=True, text=True, check=True)
        return domain_info.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve custom domain information for {project_name}")
        return "Unable to retrieve custom domain information"

def get_cron_jobs(project_name, droplet_ip):
    print(f"Gathering cron jobs for '{project_name}'...")
    try:
        cron_jobs = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"crontab -l | grep {project_name}"], capture_output=True, text=True, check=True)
        return cron_jobs.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve cron jobs for {project_name}")
        return "Unable to retrieve cron jobs"

def get_third_party_integrations(project_name, droplet_ip):
    print(f"Gathering third-party integrations for '{project_name}'...")
    # This is a placeholder. In a real scenario, you'd need to securely retrieve and store this information.
    return {
        "external_apis": [
            {"name": "Example API", "endpoint": "https://api.example.com", "api_key": "your-api-key-here"}
        ]
    }

def gather_and_output_info(project_name, project_type, droplet_ip):
    print(f"\nGathering deployment information for {project_type} project '{project_name}' on droplet {droplet_ip}...")
    
    deployment_info = {
        "do_token": get_do_token(project_name, droplet_ip),
        "droplet_info": get_droplet_info(droplet_ip),
        "project_info": get_project_info(project_name, project_type, droplet_ip),
        "project_dependencies": get_project_dependencies(project_name, project_type, droplet_ip),
        "database_info": get_database_info(project_name, droplet_ip),
        "environment_variables": get_environment_variables(project_name, droplet_ip),
        "project_structure": get_project_structure(project_name, droplet_ip),
        "application_entry_points": get_application_entry_points(project_name, project_type, droplet_ip),
        "logging_configuration": get_logging_configuration(project_name, droplet_ip),
        "monitoring_info": get_monitoring_info(project_name, droplet_ip),
        "backup_recovery_info": get_backup_recovery_info(project_name, droplet_ip),
        "ssl_tls_config": get_ssl_tls_config(project_name, droplet_ip),
        "custom_domain_info": get_custom_domain_info(project_name, droplet_ip),
        "cron_jobs": get_cron_jobs(project_name, droplet_ip),
        "third_party_integrations": get_third_party_integrations(project_name, droplet_ip)
    }

    output_file = f"{project_name}_deployment_info.json"
    try:
        with open(output_file, 'w') as f:
            json.dump(deployment_info, f, indent=2)
        print(f"\nDeployment information has been saved to {output_file}")
    except IOError as e:
        print(f"Error: Unable to write deployment information to {output_file}")
        print(f"Error details: {e}")
        return None

    return output_file

def main():
    print("Welcome to the Deployment Information Gathering Tool!")
    print("This script will collect comprehensive information about your deployed project and the droplet it's hosted on.")

    project_name = input("\nEnter the project name: ")
    while True:
        project_type = input("Enter the project type (python, node, php, or static): ").lower()
        if project_type in ['python', 'node', 'php', 'static']:
            break
        print("Invalid project type. Please enter 'python', 'node', 'php', or 'static'.")

    droplet_ip = input("Enter the droplet IP address: ")

    output_file = gather_and_output_info(project_name, project_type, droplet_ip)
    
    if output_file:
        print("\nNext steps:")
        print(f"1. Review the contents of {output_file} to ensure all information is correct.")
        print("2. Use this information for monitoring, maintenance, or future deployments.")
        print("3. Keep this file secure, as it contains sensitive information about your deployment.")
    else:
        print("\nFailed to gather deployment information. Please check the errors above and try again.")

if __name__ == "__main__":
    main()