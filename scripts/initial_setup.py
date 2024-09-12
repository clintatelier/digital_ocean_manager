import os
import subprocess
import time
import logging
from digitalocean import Manager, Droplet, SSHKey, APIError

# Set up logging
logging.basicConfig(filename='setup.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SetupError(Exception):
    """Custom exception for setup errors"""
    pass

def create_droplet(token, droplet_name, region, size, image, dry_run=False):
    manager = Manager(token=token)
    
    logging.info(f"Creating droplet '{droplet_name}'...")
    try:
        if dry_run:
            logging.info(f"Dry run: Would create droplet '{droplet_name}' in region {region} with size {size} and image {image}")
            return None

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
        logging.info("Waiting for the droplet to be ready. This may take a few minutes...")
        while droplet.status != 'active':
            time.sleep(30)
            droplet.load()
        
        logging.info(f"Droplet '{droplet_name}' created successfully with monitoring enabled.")
        return droplet
    except APIError as e:
        logging.error(f"Error creating droplet: {e}")
        raise SetupError(f"Failed to create droplet: {e}")

def setup_droplet(droplet, dry_run=False):
    logging.info("Setting up the droplet with necessary software...")
    commands = [
        "apt update && apt upgrade -y",
        "apt install -y python3-venv nodejs npm php",
        "npm install -g n && n lts",
        "apt install -y apache2",
        "systemctl enable apache2",
        "apt install -y mysql-server",
        "systemctl enable mysql",
        "apt install -y php-mysql",
        "systemctl restart apache2",
        "curl -sSL https://agent.digitalocean.com/install.sh | sh",
        "snap install doctl",
        "curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash",
        "apt install -y docker.io",
        "systemctl enable docker",
        "apt install -y python3-pip",
        "apt install -y git",
    ]
    
    for command in commands:
        try:
            if dry_run:
                logging.info(f"Dry run: Would execute command: {command}")
            else:
                subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet.ip_address}", command], check=True)
                logging.info(f"Successfully executed command: {command}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command '{command}': {e}")
            raise SetupError(f"Failed to set up droplet: {e}")
    
    logging.info("Droplet setup completed successfully.")
    return True

def setup_project_management(droplet, dry_run=False):
    logging.info("Setting up project management tools...")
    commands = [
        "mkdir -p /opt/projects",
        "mkdir -p /opt/venvs",
        "mkdir -p /opt/configs",
        """cat << EOF > /usr/local/bin/manage_project.sh
#!/bin/bash

function create_project() {
    project_name=\$1
    project_type=\$2
    mkdir -p /opt/projects/\$project_name
    python3 -m venv /opt/venvs/\$project_name
    echo "{\\"name\\": \\"\$project_name\\", \\"type\\": \\"\$project_type\\"}" > /opt/configs/\$project_name.json
    echo "Project \$project_name created successfully."
}

function delete_project() {
    project_name=\$1
    rm -rf /opt/projects/\$project_name
    rm -rf /opt/venvs/\$project_name
    rm -f /opt/configs/\$project_name.json
    echo "Project \$project_name deleted successfully."
}

function list_projects() {
    echo "Projects:"
    for config in /opt/configs/*.json; do
        project_name=\$(basename \$config .json)
        project_type=\$(jq -r .type \$config)
        echo "- \$project_name (\$project_type)"
    done
}

case \$1 in
    create)
        create_project \$2 \$3
        ;;
    delete)
        delete_project \$2
        ;;
    list)
        list_projects
        ;;
    *)
        echo "Usage: \$0 {create|delete|list} [project_name] [project_type]"
        exit 1
esac
EOF""",
        "chmod +x /usr/local/bin/manage_project.sh"
    ]
    
    for command in commands:
        try:
            if dry_run:
                logging.info(f"Dry run: Would execute command: {command}")
            else:
                subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet.ip_address}", command], check=True)
                logging.info(f"Successfully executed command: {command}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command: {e}")
            raise SetupError(f"Failed to set up project management: {e}")
    
    logging.info("Project management setup completed successfully.")
    return True

def setup_do_credentials(droplet, dry_run=False):
    logging.info("Setting up DigitalOcean credentials management...")
    commands = [
        """cat << EOF > /usr/local/bin/manage_do_credentials.sh
#!/bin/bash

function set_credentials() {
    project_name=\$1
    do_token=\$2
    echo "{\\"do_token\\": \\"\$do_token\\"}" > /opt/configs/\$project_name\_do_credentials.json
    echo "DigitalOcean credentials set for project \$project_name."
}

function get_credentials() {
    project_name=\$1
    if [ -f "/opt/configs/\${project_name}_do_credentials.json" ]; then
        jq -r .do_token "/opt/configs/\${project_name}_do_credentials.json"
    else
        echo "No DigitalOcean credentials found for project \$project_name."
    fi
}

function delete_credentials() {
    project_name=\$1
    rm -f "/opt/configs/\${project_name}_do_credentials.json"
    echo "DigitalOcean credentials deleted for project \$project_name."
}

case \$1 in
    set)
        set_credentials \$2 \$3
        ;;
    get)
        get_credentials \$2
        ;;
    delete)
        delete_credentials \$2
        ;;
    *)
        echo "Usage: \$0 {set|get|delete} [project_name] [do_token]"
        exit 1
esac
EOF""",
        "chmod +x /usr/local/bin/manage_do_credentials.sh"
    ]
    
    for command in commands:
        try:
            if dry_run:
                logging.info(f"Dry run: Would execute command: {command}")
            else:
                subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"root@{droplet.ip_address}", command], check=True)
                logging.info(f"Successfully executed command: {command}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command: {e}")
            raise SetupError(f"Failed to set up DigitalOcean credentials management: {e}")
    
    logging.info("DigitalOcean credentials management setup completed successfully.")
    return True

def cleanup_resources(droplet):
    logging.info("Cleaning up resources...")
    try:
        droplet.destroy()
        logging.info(f"Droplet {droplet.name} has been destroyed.")
    except APIError as e:
        logging.error(f"Error destroying droplet: {e}")

def main():
    logging.info("Starting DigitalOcean Droplet Setup")
    print("Welcome to the DigitalOcean Droplet Setup!")
    print("This script will guide you through creating and setting up your droplet for multi-project hosting.")
    
    token = os.getenv("DO_TOKEN")
    if not token:
        logging.error("DigitalOcean API token not found")
        print("DigitalOcean API token not found. Please make sure you've set the DO_TOKEN environment variable.")
        return

    dry_run = input("Do you want to perform a dry run? (yes/no): ").lower() == 'yes'
    if dry_run:
        logging.info("Performing dry run")
        print("Performing dry run. No actual resources will be created or modified.")

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
    
    try:
        droplet = create_droplet(token, droplet_name, region, size, image, dry_run)
        if not dry_run and droplet:
            if input("Droplet created. Continue with setup? (yes/no): ").lower() != 'yes':
                raise SetupError("Setup cancelled by user")

            if setup_droplet(droplet, dry_run):
                if input("Droplet setup complete. Set up project management? (yes/no): ").lower() != 'yes':
                    raise SetupError("Setup cancelled by user")

                if setup_project_management(droplet, dry_run):
                    if input("Project management setup complete. Set up DigitalOcean credentials management? (yes/no): ").lower() != 'yes':
                        raise SetupError("Setup cancelled by user")

                    if setup_do_credentials(droplet, dry_run):
                        logging.info("Initial setup complete")
                        print("\nInitial setup complete!")
                        print(f"Your droplet is ready to use at IP: {droplet.ip_address}")
                        print("\nTo manage projects on your droplet, use the following command:")
                        print(f"ssh root@{droplet.ip_address} '/usr/local/bin/manage_project.sh [create|delete|list] [project_name] [project_type]'")
                        print("\nTo manage DigitalOcean credentials for projects, use the following command:")
                        print(f"ssh root@{droplet.ip_address} '/usr/local/bin/manage_do_credentials.sh [set|get|delete] [project_name] [do_token]'")
                        print("\nDigitalOcean monitoring and management tools have been enabled for your droplet.")
                        print("You can view monitoring data and manage your droplet in the DigitalOcean dashboard.")
                        print("\nPlease refer to the README.md and droplet_monitoring.md files for more information on how to use, monitor, and manage your new multi-project droplet.")
    except SetupError as e:
        logging.error(f"Setup failed: {e}")
        print(f"Setup failed: {e}")
        if not dry_run and droplet:
            if input("Do you want to clean up created resources? (yes/no): ").lower() == 'yes':
                cleanup_resources(droplet)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")
        if not dry_run and droplet:
            if input("Do you want to clean up created resources? (yes/no): ").lower() == 'yes':
                cleanup_resources(droplet)

if __name__ == "__main__":
    main()