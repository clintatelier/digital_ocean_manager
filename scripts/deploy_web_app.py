import os
import subprocess
import sys
import json
from gather_deployment_info import gather_and_output_info

def check_project_exists(droplet_ip, project_name):
    print(f"Checking if project '{project_name}' exists...")
    try:
        result = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"/usr/local/bin/manage_project.sh list | grep {project_name}"], capture_output=True, text=True)
        return project_name in result.stdout
    except subprocess.CalledProcessError:
        return False

def create_project(droplet_ip, project_name, project_type):
    print(f"Creating project '{project_name}' of type '{project_type}'...")
    try:
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"/usr/local/bin/manage_project.sh create {project_name} {project_type}"], check=True)
        print(f"Project '{project_name}' created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating project: {e}")
        return False

def deploy_project_files(droplet_ip, project_name, local_dir):
    print(f"Deploying project files for '{project_name}' to the droplet...")
    try:
        # Create project directory on the droplet
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"mkdir -p /opt/projects/{project_name}"], check=True)
        
        # Copy project files to the droplet
        subprocess.run(["scp", "-r", f"{local_dir}/*", f"root@{droplet_ip}:/opt/projects/{project_name}/"], check=True)
        print(f"Project files for '{project_name}' copied to the droplet successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error deploying project files: {e}")
        return False
    return True

def setup_virtual_environment(droplet_ip, project_name, project_type):
    print(f"Setting up virtual environment for '{project_name}'...")
    try:
        if project_type == "python":
            subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", 
                            f"python3 -m venv /opt/venvs/{project_name} && source /opt/venvs/{project_name}/bin/activate && pip install -r /opt/projects/{project_name}/requirements.txt"], check=True)
        elif project_type == "node":
            subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", 
                            f"cd /opt/projects/{project_name} && npm install"], check=True)
        elif project_type == "php":
            # For PHP, we assume dependencies are managed by Composer
            subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", 
                            f"cd /opt/projects/{project_name} && composer install"], check=True)
        print(f"Virtual environment for '{project_name}' set up successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up virtual environment: {e}")
        return False
    return True

def setup_docker_environment(droplet_ip, project_name, project_type):
    print(f"Setting up Docker environment for '{project_name}'...")
    try:
        # Create Dockerfile
        dockerfile_content = get_dockerfile_content(project_type)
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"echo '{dockerfile_content}' > /opt/projects/{project_name}/Dockerfile"], check=True)
        
        # Build Docker image
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"cd /opt/projects/{project_name} && docker build -t {project_name} ."], check=True)
        
        # Stop and remove existing container if it exists
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"docker stop {project_name} || true && docker rm {project_name} || true"], check=True)
        
        # Run new container
        port = "80" if project_type == "static" else "8080"
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"docker run -d --name {project_name} -p {port}:{port} {project_name}"], check=True)
        
        print(f"Docker environment for '{project_name}' set up successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up Docker environment: {e}")
        return False
    return True

def get_dockerfile_content(project_type):
    if project_type == "python":
        return """
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
"""
    elif project_type == "node":
        return """
FROM node:14
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
CMD ["node", "app.js"]
"""
    elif project_type == "php":
        return """
FROM php:7.4-apache
COPY . /var/www/html/
"""
    else:  # static
        return """
FROM nginx:alpine
COPY . /usr/share/nginx/html
"""

def configure_apache(droplet_ip, project_name, project_type):
    print(f"Configuring Apache for '{project_name}'...")
    config = f"""<VirtualHost *:80>
    ServerName {project_name}.yourdomain.com
    DocumentRoot /opt/projects/{project_name}
    
    <Directory /opt/projects/{project_name}>
        Options FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    {"" if project_type == "static" else f"WSGIDaemonProcess {project_name} python-home=/opt/venvs/{project_name} python-path=/opt/projects/{project_name}"}
    {"" if project_type == "static" else f"WSGIProcessGroup {project_name}"}
    {"" if project_type == "static" else f"WSGIScriptAlias / /opt/projects/{project_name}/app.wsgi"}

    ErrorLog ${{APACHE_LOG_DIR}}/{project_name}_error.log
    CustomLog ${{APACHE_LOG_DIR}}/{project_name}_access.log combined
</VirtualHost>"""
    
    try:
        # Write the configuration to a file on the droplet
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"echo '{config}' > /etc/apache2/sites-available/{project_name}.conf"], check=True)
        
        # Enable the site and reload Apache
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", f"a2ensite {project_name}.conf"], check=True)
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet_ip}", "systemctl reload apache2"], check=True)
        
        print(f"Apache configured for '{project_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring Apache: {e}")
        return False
    return True

def deploy_project(project_name, project_type, droplet_ip, local_dir, use_docker):
    print(f"\nStarting deployment of {project_type} project '{project_name}' to droplet at {droplet_ip}...")
    
    if not os.path.exists(local_dir):
        print(f"Error: The local directory '{local_dir}' does not exist.")
        return False

    if check_project_exists(droplet_ip, project_name):
        print(f"Project '{project_name}' already exists on the droplet.")
        overwrite = input("Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != 'y':
            print("Deployment cancelled.")
            return False
    else:
        if not create_project(droplet_ip, project_name, project_type):
            return False

    try:
        if not deploy_project_files(droplet_ip, project_name, local_dir):
            return False
        
        if use_docker:
            if not setup_docker_environment(droplet_ip, project_name, project_type):
                return False
        else:
            if not setup_virtual_environment(droplet_ip, project_name, project_type):
                return False
            if not configure_apache(droplet_ip, project_name, project_type):
                return False

        print(f"\nProject '{project_name}' deployed successfully to the droplet")

        # Gather and output deployment information
        output_file = gather_and_output_info(project_name, project_type, droplet_ip)
        print(f"Deployment information saved to {output_file}")

        print(f"\nYour project '{project_name}' should now be accessible at: http://{droplet_ip}")
        print("Note: For production use, you should set up a domain name and configure SSL/TLS.")

        return True

    except Exception as e:
        print(f"Unexpected error during deployment: {e}")
        return False

def main():
    print("Welcome to the Project Deployment Script!")
    print("This script will help you deploy your project to your DigitalOcean droplet.")
    
    project_name = input("\nEnter the name of your project: ")
    droplet_ip = input("Enter the IP address of your DigitalOcean droplet: ")
    
    print("\nSupported project types:")
    print("1. Python")
    print("2. Node.js")
    print("3. PHP")
    print("4. Static HTML")
    
    while True:
        project_type_choice = input("Enter the number corresponding to your project type: ")
        if project_type_choice in ['1', '2', '3', '4']:
            break
        print("Invalid choice. Please enter a number between 1 and 4.")

    project_type_map = {'1': 'python', '2': 'node', '3': 'php', '4': 'static'}
    project_type = project_type_map[project_type_choice]
    
    local_dir = input("Enter the local directory path of your project: ")
    
    use_docker = input("Do you want to use Docker for deployment? (y/n): ").lower() == 'y'
    
    print(f"\nPreparing to deploy {project_type} project '{project_name}' to droplet at {droplet_ip}")
    print(f"Using {'Docker' if use_docker else 'virtual environment'} for isolation")
    confirm = input("Do you want to continue? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Deployment cancelled.")
        sys.exit(0)

    if deploy_project(project_name, project_type, droplet_ip, local_dir, use_docker):
        print("\nDeployment completed successfully!")
    else:
        print("\nDeployment failed. Please check the error messages above and try again.")

if __name__ == '__main__':
    main()