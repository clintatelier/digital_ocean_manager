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

def gather_and_output_info(app_name, app_type, droplet_ip):
    print(f"\nGathering deployment information for {app_type} '{app_name}' on droplet {droplet_ip}...")
    
    deployment_info = {
        "do_token": get_do_token(),
        "droplet_info": get_droplet_info(droplet_ip),
        "app_info": get_app_info(app_name, app_type, droplet_ip)
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
    print("This script will collect information about your deployed application and the droplet it's hosted on.")

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