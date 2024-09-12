import digitalocean
import os
import paramiko

def deploy_static_site(site_name, droplet_id, ssh_key_path):
    # Initialize DigitalOcean client
    token = os.getenv('DO_TOKEN')
    manager = digitalocean.Manager(token=token)

    # Get the droplet
    droplet = manager.get_droplet(droplet_id)

    # Connect to the droplet via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(droplet.ip_address, username='root', key_filename=ssh_key_path)

    # Deploy the static site (example commands, adjust as needed)
    ssh.exec_command(f'mkdir -p /var/www/{site_name}')
    sftp = ssh.open_sftp()
    local_path = f'../static_sites/{site_name}/'
    remote_path = f'/var/www/{site_name}/'
    
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            remote_file = os.path.join(remote_path, os.path.relpath(local_file, local_path))
            sftp.put(local_file, remote_file)

    sftp.close()

    # Configure Nginx (example configuration, adjust as needed)
    nginx_config = f"""
    server {{
        listen 80;
        server_name {site_name};
        root /var/www/{site_name};
        index index.html;
    }}
    """
    ssh.exec_command(f'echo "{nginx_config}" > /etc/nginx/sites-available/{site_name}')
    ssh.exec_command(f'ln -s /etc/nginx/sites-available/{site_name} /etc/nginx/sites-enabled/')
    ssh.exec_command('nginx -t && systemctl reload nginx')

    ssh.close()

    print(f"Static site {site_name} deployed successfully to droplet {droplet_id}")

if __name__ == '__main__':
    site_name = input("Enter the name of your static site: ")
    droplet_id = input("Enter the ID of the target droplet: ")
    ssh_key_path = input("Enter the path to your SSH private key: ")
    deploy_static_site(site_name, droplet_id, ssh_key_path)