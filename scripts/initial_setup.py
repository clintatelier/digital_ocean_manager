import os
import subprocess
import time
from digitalocean import Manager, Droplet, SSHKey, APIError

def create_droplet(token, droplet_name, region, size, image):
    manager = Manager(token=token)
    
    print(f"Creating droplet '{droplet_name}'...")
    try:
        # Create the Droplet with monitoring enabled
        droplet = Droplet(
            token=token,
            name=droplet_name,
            region=region,
            size=size,
            image=image,
            ssh_keys=manager.get_all_sshkeys(),
            monitoring=True,  # Enable DigitalOcean monitoring
            tags=["managed"]  # Add tag for management tools
        )
        
        droplet.create()
        
        # Wait for the droplet to be ready
        print("Waiting for the droplet to be ready. This may take a few minutes...")
        while droplet.status != 'active':
            time.sleep(30)
            droplet.load()
        
        print(f"Droplet '{droplet_name}' created successfully with monitoring enabled.")
        return droplet
    except APIError as e:
        print(f"Error creating droplet: {e}")
        return None

def setup_droplet(droplet):
    print("Setting up the droplet with necessary software...")
    # Install necessary software and set up the environment
    commands = [
        "apt update && apt upgrade -y",
        "apt install -y python3-venv nodejs npm php",
        "npm install -g n && n lts",  # Install Node.js version manager
        "apt install -y apache2",  # Install Apache for hosting static sites
        "systemctl enable apache2",
        "apt install -y mysql-server",  # Install MySQL for database management
        "systemctl enable mysql",
        "apt install -y php-mysql",  # Install PHP MySQL extension
        "systemctl restart apache2",
        # Install DigitalOcean monitoring agent
        "curl -sSL https://agent.digitalocean.com/install.sh | sh",
        # Install DigitalOcean CLI (doctl) for management
        "snap install doctl",
        # Install DigitalOcean Metrics Agent for advanced metrics
        "curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash",
    ]
    
    for command in commands:
        try:
            subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet.ip_address}", command], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command '{command}': {e}")
            return False
    
    print("Droplet setup completed successfully.")
    return True

def setup_virtual_environments(droplet):
    print("Setting up virtual environment management...")
    # Set up a directory for virtual environments
    try:
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet.ip_address}", "mkdir -p /opt/venvs"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environments directory: {e}")
        return False
    
    # Create a script to manage virtual environments
    venv_script = """#!/bin/bash
    
    function create_venv() {
        python3 -m venv /opt/venvs/$1
        /opt/venvs/$1/bin/pip install --upgrade pip
    }
    
    function delete_venv() {
        rm -rf /opt/venvs/$1
    }
    
    function list_venvs() {
        ls -l /opt/venvs
    }
    
    case $1 in
        create)
            create_venv $2
            ;;
        delete)
            delete_venv $2
            ;;
        list)
            list_venvs
            ;;
        *)
            echo "Usage: $0 {create|delete|list} [venv_name]"
            exit 1
    esac
    """
    
    try:
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet.ip_address}", f"echo '{venv_script}' > /usr/local/bin/manage_venv.sh"], check=True)
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet.ip_address}", "chmod +x /usr/local/bin/manage_venv.sh"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment management script: {e}")
        return False
    
    print("Virtual environment management script created successfully.")
    return True

def main():
    print("Welcome to the DigitalOcean Droplet Setup!")
    print("This script will guide you through creating and setting up your droplet.")
    
    token = os.getenv("DO_TOKEN")
    if not token:
        print("DigitalOcean API token not found. Please make sure you've set the DO_TOKEN environment variable.")
        return

    droplet_name = input("Enter a name for your DigitalOcean droplet: ")
    
    print("\nAvailable regions:")
    print("nyc1, nyc3 - New York")
    print("sfo2, sfo3 - San Francisco")
    print("ams3 - Amsterdam")
    print("sgp1 - Singapore")
    print("lon1 - London")
    print("fra1 - Frankfurt")
    print("tor1 - Toronto")
    print("blr1 - Bangalore")
    region = input("Enter the region for your droplet (e.g., nyc1): ")
    
    print("\nAvailable droplet sizes:")
    print("s-1vcpu-1gb - 1 vCPU, 1 GB RAM, 25 GB SSD")
    print("s-1vcpu-2gb - 1 vCPU, 2 GB RAM, 50 GB SSD")
    print("s-2vcpu-2gb - 2 vCPU, 2 GB RAM, 60 GB SSD")
    print("s-2vcpu-4gb - 2 vCPU, 4 GB RAM, 80 GB SSD")
    size = input("Enter the size for the droplet (e.g., s-1vcpu-1gb): ")
    
    print("\nRecommended image:")
    print("ubuntu-20-04-x64 - Ubuntu 20.04 LTS x64")
    image = input("Enter the image for the droplet (press Enter for ubuntu-20-04-x64): ") or "ubuntu-20-04-x64"
    
    droplet = create_droplet(token, droplet_name, region, size, image)
    if not droplet:
        print("Failed to create droplet. Please check your inputs and try again.")
        return

    if not setup_droplet(droplet):
        print("Failed to set up droplet. Please check the error messages above and try again.")
        return

    if not setup_virtual_environments(droplet):
        print("Failed to set up virtual environments. Please check the error messages above and try again.")
        return
    
    print("\nInitial setup complete!")
    print(f"Your droplet is ready to use at IP: {droplet.ip_address}")
    print("\nTo manage virtual environments on your droplet, use the following command:")
    print(f"ssh root@{droplet.ip_address} '/usr/local/bin/manage_venv.sh [create|delete|list] [venv_name]'")
    print("\nFor example, to create a new virtual environment named 'myapp':")
    print(f"ssh root@{droplet.ip_address} '/usr/local/bin/manage_venv.sh create myapp'")
    print("\nDigitalOcean monitoring and management tools have been enabled for your droplet.")
    print("You can view monitoring data and manage your droplet in the DigitalOcean dashboard.")
    print("\nPlease refer to the README.md and droplet_monitoring.md files for more information on how to use, monitor, and manage your new droplet.")

if __name__ == "__main__":
    main()