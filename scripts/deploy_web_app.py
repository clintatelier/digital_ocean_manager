import os
import subprocess
import sys
from gather_deployment_info import gather_and_output_info

def check_app_directory(app_name, app_type):
    app_dir = f"../web_apps/{app_name}" if app_type == "web" else f"../static_sites/{app_name}"
    if not os.path.exists(app_dir):
        print(f"Error: The directory for {app_name} does not exist.")
        print(f"Please create your {'web app' if app_type == 'web' else 'static site'} in the {app_dir} directory.")
        return False
    return True

def create_virtual_environment(droplet_ip, app_name):
    print(f"Creating virtual environment '{app_name}' on the droplet...")
    try:
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"/usr/local/bin/manage_venv.sh create {app_name}"], check=True)
        print(f"Virtual environment '{app_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False
    return True

def deploy_app_files(droplet_ip, app_name, app_dir):
    print(f"Deploying app files for '{app_name}' to the droplet...")
    try:
        # Create app directory on the droplet
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"mkdir -p /var/www/{app_name}"], check=True)
        
        # Copy app files to the droplet
        subprocess.run(["scp", "-r", f"{app_dir}/*", f"root@{droplet_ip}:/var/www/{app_name}/"], check=True)
        print(f"App files for '{app_name}' copied to the droplet successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error deploying app files: {e}")
        return False
    return True

def install_app_dependencies(droplet_ip, app_name):
    print(f"Installing dependencies for '{app_name}'...")
    try:
        # Activate virtual environment and install dependencies
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", 
                        f"source /opt/venvs/{app_name}/bin/activate && pip install -r /var/www/{app_name}/requirements.txt"], check=True)
        print(f"Dependencies for '{app_name}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    return True

def configure_apache(droplet_ip, app_name, app_type):
    print(f"Configuring Apache for '{app_name}'...")
    # Create Apache configuration for the app
    config = f"""<VirtualHost *:80>
    ServerName {app_name}.yourdomain.com
    DocumentRoot /var/www/{app_name}
    
    <Directory /var/www/{app_name}>
        Options FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    {"" if app_type == "static" else f"WSGIDaemonProcess {app_name} python-home=/opt/venvs/{app_name} python-path=/var/www/{app_name}"}
    {"" if app_type == "static" else f"WSGIProcessGroup {app_name}"}
    {"" if app_type == "static" else f"WSGIScriptAlias / /var/www/{app_name}/app.wsgi"}

    ErrorLog ${{APACHE_LOG_DIR}}/{app_name}_error.log
    CustomLog ${{APACHE_LOG_DIR}}/{app_name}_access.log combined
</VirtualHost>"""
    
    try:
        # Write the configuration to a file on the droplet
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"echo '{config}' > /etc/apache2/sites-available/{app_name}.conf"], check=True)
        
        # Enable the site and reload Apache
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"a2ensite {app_name}.conf"], check=True)
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", "systemctl reload apache2"], check=True)
        
        print(f"Apache configured for '{app_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring Apache: {e}")
        return False
    return True

def deploy_web_app(app_name, droplet_ip, app_type):
    print(f"\nStarting deployment of {app_type} app '{app_name}' to droplet at {droplet_ip}...")
    
    app_dir = f"../web_apps/{app_name}" if app_type == "web" else f"../static_sites/{app_name}"
    
    if not check_app_directory(app_name, app_type):
        return

    try:
        # Create virtual environment (for web apps only)
        if app_type == "web":
            if not create_virtual_environment(droplet_ip, app_name):
                return
        
        # Deploy app files
        if not deploy_app_files(droplet_ip, app_name, app_dir):
            return
        
        # Install dependencies (for web apps only)
        if app_type == "web":
            if not install_app_dependencies(droplet_ip, app_name):
                return
        
        # Configure Apache
        if not configure_apache(droplet_ip, app_name, app_type):
            return

        print(f"\n{app_type.capitalize()} app '{app_name}' deployed successfully to the droplet")

        # Gather and output deployment information
        output_file = gather_and_output_info(app_name, f"{app_type}_app", droplet_ip)
        print(f"Deployment information saved to {output_file}")

        print(f"\nYour {app_type} app '{app_name}' should now be accessible at: http://{droplet_ip}")
        print("Note: For production use, you should set up a domain name and configure SSL/TLS.")

    except Exception as e:
        print(f"Unexpected error during deployment: {e}")

def main():
    print("Welcome to the Web App Deployment Script!")
    print("This script will help you deploy your web app or static site to your DigitalOcean droplet.")
    
    app_name = input("\nEnter the name of your web app or static site: ")
    droplet_ip = input("Enter the IP address of your DigitalOcean droplet: ")
    app_type = input("Enter the type of app (web/static): ").lower()
    
    if app_type not in ["web", "static"]:
        print("Invalid app type. Please enter 'web' or 'static'.")
        sys.exit(1)

    print(f"\nPreparing to deploy {app_type} app '{app_name}' to droplet at {droplet_ip}")
    confirm = input("Do you want to continue? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Deployment cancelled.")
        sys.exit(0)

    deploy_web_app(app_name, droplet_ip, app_type)

if __name__ == '__main__':
    main()