import os
import json
import subprocess
import sys

def get_do_token():
    token = os.getenv('DO_TOKEN')
    if not token:
        print("Warning: DigitalOcean API token (DO_TOKEN) not found in environment variables.")
        print("Some features may not work without the API token.")
    return token

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

def get_app_info(app_name, app_type, droplet_ip):
    print(f"Gathering information about the {app_type} '{app_name}'...")
    app_info = {
        "name": app_name,
        "type": app_type,
    }
    
    # Get Apache configuration for the app
    try:
        apache_config = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /etc/apache2/sites-available/{app_name}.conf"], capture_output=True, text=True, check=True)
        app_info["apache_config"] = apache_config.stdout
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve Apache configuration for {app_name}")
        app_info["apache_config"] = "Unable to retrieve Apache configuration"
    
    # For web apps, get virtual environment information
    if app_type == "web_app":
        try:
            venv_info = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"/usr/local/bin/manage_venv.sh list | grep {app_name}"], capture_output=True, text=True, check=True)
            app_info["virtual_environment"] = venv_info.stdout.strip()
        except subprocess.CalledProcessError:
            print(f"Warning: Unable to retrieve virtual environment information for {app_name}")
            app_info["virtual_environment"] = "Unable to retrieve virtual environment information"
    
    return app_info

def get_project_dependencies(app_name, droplet_ip):
    print(f"Gathering project dependencies for '{app_name}'...")
    try:
        dependencies = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/venvs/{app_name}/requirements.txt"], capture_output=True, text=True, check=True)
        return dependencies.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve project dependencies for {app_name}")
        return "Unable to retrieve project dependencies"

def get_database_info(app_name, droplet_ip):
    print(f"Gathering database information for '{app_name}'...")
    # This is a placeholder. In a real scenario, you'd need to securely retrieve and store this information.
    return {
        "type": "MySQL",
        "name": f"{app_name}_db",
        "user": f"{app_name}_user",
        "connection_string": "mysql://user:password@localhost:3306/dbname"
    }

def get_environment_variables(app_name, droplet_ip):
    print(f"Gathering environment variables for '{app_name}'...")
    try:
        env_vars = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/venvs/{app_name}/.env"], capture_output=True, text=True, check=True)
        return env_vars.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve environment variables for {app_name}")
        return "Unable to retrieve environment variables"

def get_project_structure(app_name, droplet_ip):
    print(f"Gathering project structure for '{app_name}'...")
    try:
        structure = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"tree /opt/venvs/{app_name} -L 2"], capture_output=True, text=True, check=True)
        return structure.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve project structure for {app_name}")
        return "Unable to retrieve project structure"

def get_application_entry_points(app_name, droplet_ip):
    print(f"Gathering application entry points for '{app_name}'...")
    try:
        entry_points = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/venvs/{app_name}/wsgi.py"], capture_output=True, text=True, check=True)
        return entry_points.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve application entry points for {app_name}")
        return "Unable to retrieve application entry points"

def get_logging_configuration(app_name, droplet_ip):
    print(f"Gathering logging configuration for '{app_name}'...")
    try:
        logging_config = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /opt/venvs/{app_name}/logging.conf"], capture_output=True, text=True, check=True)
        return logging_config.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve logging configuration for {app_name}")
        return "Unable to retrieve logging configuration"

def get_monitoring_info(app_name, droplet_ip):
    print(f"Gathering monitoring information for '{app_name}'...")
    # This is a placeholder. In a real scenario, you'd provide actual monitoring dashboard URLs or endpoints.
    return {
        "monitoring_dashboard": f"https://monitoring.yourdomain.com/dashboard/{app_name}",
        "performance_metrics_endpoint": f"https://api.yourdomain.com/metrics/{app_name}"
    }

def get_backup_recovery_info(app_name, droplet_ip):
    print(f"Gathering backup and recovery information for '{app_name}'...")
    # This is a placeholder. In a real scenario, you'd provide actual backup procedures and recovery steps.
    return {
        "backup_procedure": "Daily automated backups at 2 AM UTC",
        "recovery_steps": "1. Stop the application\n2. Restore from latest backup\n3. Restart the application"
    }

def get_ssl_tls_config(app_name, droplet_ip):
    print(f"Gathering SSL/TLS configuration for '{app_name}'...")
    try:
        ssl_config = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /etc/apache2/sites-available/{app_name}-le-ssl.conf"], capture_output=True, text=True, check=True)
        return ssl_config.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve SSL/TLS configuration for {app_name}")
        return "Unable to retrieve SSL/TLS configuration"

def get_custom_domain_info(app_name, droplet_ip):
    print(f"Gathering custom domain information for '{app_name}'...")
    try:
        domain_info = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cat /etc/apache2/sites-available/{app_name}.conf | grep ServerName"], capture_output=True, text=True, check=True)
        return domain_info.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve custom domain information for {app_name}")
        return "Unable to retrieve custom domain information"

def get_cron_jobs(app_name, droplet_ip):
    print(f"Gathering cron jobs for '{app_name}'...")
    try:
        cron_jobs = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"crontab -l | grep {app_name}"], capture_output=True, text=True, check=True)
        return cron_jobs.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Warning: Unable to retrieve cron jobs for {app_name}")
        return "Unable to retrieve cron jobs"

def get_third_party_integrations(app_name, droplet_ip):
    print(f"Gathering third-party integrations for '{app_name}'...")
    # This is a placeholder. In a real scenario, you'd need to securely retrieve and store this information.
    return {
        "external_apis": [
            {"name": "Example API", "endpoint": "https://api.example.com", "api_key": "your-api-key-here"}
        ]
    }

def gather_and_output_info(app_name, app_type, droplet_ip):
    print(f"\nGathering deployment information for {app_type} '{app_name}' on droplet {droplet_ip}...")
    
    deployment_info = {
        "do_token": get_do_token(),
        "droplet_info": get_droplet_info(droplet_ip),
        "app_info": get_app_info(app_name, app_type, droplet_ip),
        "project_dependencies": get_project_dependencies(app_name, droplet_ip),
        "database_info": get_database_info(app_name, droplet_ip),
        "environment_variables": get_environment_variables(app_name, droplet_ip),
        "project_structure": get_project_structure(app_name, droplet_ip),
        "application_entry_points": get_application_entry_points(app_name, droplet_ip),
        "logging_configuration": get_logging_configuration(app_name, droplet_ip),
        "monitoring_info": get_monitoring_info(app_name, droplet_ip),
        "backup_recovery_info": get_backup_recovery_info(app_name, droplet_ip),
        "ssl_tls_config": get_ssl_tls_config(app_name, droplet_ip),
        "custom_domain_info": get_custom_domain_info(app_name, droplet_ip),
        "cron_jobs": get_cron_jobs(app_name, droplet_ip),
        "third_party_integrations": get_third_party_integrations(app_name, droplet_ip)
    }

    output_file = f"{app_name}_deployment_info.json"
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
    print("This script will collect comprehensive information about your deployed application and the droplet it's hosted on.")

    app_name = input("\nEnter the app name: ")
    while True:
        app_type = input("Enter the app type (web_app or static_site): ").lower()
        if app_type in ['web_app', 'static_site']:
            break
        print("Invalid app type. Please enter 'web_app' or 'static_site'.")

    droplet_ip = input("Enter the droplet IP address: ")

    output_file = gather_and_output_info(app_name, app_type, droplet_ip)
    
    if output_file:
        print("\nNext steps:")
        print(f"1. Review the contents of {output_file} to ensure all information is correct.")
        print("2. Use this information for monitoring, maintenance, or future deployments.")
        print("3. Keep this file secure, as it contains sensitive information about your deployment.")
    else:
        print("\nFailed to gather deployment information. Please check the errors above and try again.")

if __name__ == "__main__":
    main()