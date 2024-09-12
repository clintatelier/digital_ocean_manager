import digitalocean
import os
import paramiko

def deploy_web_app(app_name, droplet_id, ssh_key_path):
    # Initialize DigitalOcean client
    token = os.getenv('DO_TOKEN')
    manager = digitalocean.Manager(token=token)

    # Get the droplet
    droplet = manager.get_droplet(droplet_id)

    # Connect to the droplet via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(droplet.ip_address, username='root', key_filename=ssh_key_path)

    # Deploy the web app (example commands, adjust as needed)
    ssh.exec_command(f'git clone https://github.com/yourusername/{app_name}.git')
    ssh.exec_command(f'cd {app_name} && pip install -r requirements.txt')
    ssh.exec_command(f'cd {app_name} && python manage.py migrate')
    ssh.exec_command(f'cd {app_name} && gunicorn {app_name}.wsgi:application')

    ssh.close()

    print(f"Web app {app_name} deployed successfully to droplet {droplet_id}")

if __name__ == '__main__':
    app_name = input("Enter the name of your web app: ")
    droplet_id = input("Enter the ID of the target droplet: ")
    ssh_key_path = input("Enter the path to your SSH private key: ")
    deploy_web_app(app_name, droplet_id, ssh_key_path)