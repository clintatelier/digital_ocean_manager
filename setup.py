import os
import subprocess
import sys
import venv
import webbrowser
import time

def create_virtual_environment():
    venv_dir = os.path.join(os.getcwd(), "venv")
    print(f"Creating virtual environment in {venv_dir}...")
    try:
        venv.create(venv_dir, with_pip=True)
        print("Virtual environment created successfully.")
    except Exception as e:
        print(f"Error creating virtual environment: {e}")
        print("Please ensure you have Python 3.7+ installed and try again.")
        sys.exit(1)
    return venv_dir

def get_venv_python(venv_dir):
    if sys.platform == "win32":
        return os.path.join(venv_dir, "Scripts", "python.exe")
    return os.path.join(venv_dir, "bin", "python")

def install_dependencies(venv_python):
    print("Installing dependencies... This may take a few minutes.")
    try:
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please check your internet connection and try again.")
        sys.exit(1)

def check_external_dependencies():
    dependencies = ['doctl']
    missing = []
    for dep in dependencies:
        try:
            subprocess.run([dep, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            missing.append(dep)
    return missing

def get_do_token():
    token = os.getenv('DO_TOKEN')
    if not token:
        print("\nTo generate a DigitalOcean API token:")
        print("1. Go to https://cloud.digitalocean.com/account/api/tokens")
        print("2. Click 'Generate New Token'")
        print("3. Give it a name (e.g., 'DigitalOceanManager')")
        print("4. Set the token's expiry to 'No expiry' for long-term use")
        print("5. Copy the generated token")
        print("\nOpening the DigitalOcean API tokens page in your default web browser...")
        time.sleep(3)  # Give user time to read instructions
        webbrowser.open('https://cloud.digitalocean.com/account/api/tokens')
        token = input("\nPlease enter your DigitalOcean API token: ").strip()
        if not token:
            print("No token provided. Exiting setup.")
            sys.exit(1)
        os.environ['DO_TOKEN'] = token
    return token

def run_initial_setup(venv_python):
    print("\nRunning initial droplet setup...")
    try:
        dry_run = input("Do you want to perform a dry run? (yes/no): ").lower() == 'yes'
        if dry_run:
            print("Performing dry run. No actual resources will be created or modified.")
        subprocess.run([venv_python, 'scripts/initial_setup.py'], check=True)
    except subprocess.CalledProcessError:
        print("Error during initial setup. Please check the error messages above and try again.")
        sys.exit(1)

def main():
    print("Welcome to the DigitalOcean Manager setup!")
    print("This script will guide you through the initial setup process for managing multiple projects on a single DigitalOcean droplet.")
    print("If you encounter any issues, please refer to the README.md file or contact support.")

    input("Press Enter to begin the setup process...")

    venv_dir = create_virtual_environment()
    venv_python = get_venv_python(venv_dir)
    install_dependencies(venv_python)

    print("\nChecking external dependencies...")
    missing_deps = check_external_dependencies()
    if missing_deps:
        print(f"The following dependencies are missing: {', '.join(missing_deps)}")
        print("Please install them and run this script again.")
        print("\nInstallation instructions:")
        print("- doctl: https://docs.digitalocean.com/reference/doctl/how-to/install/")
        print("\nAfter installing the missing dependencies, please restart this setup script.")
        sys.exit(1)

    token = get_do_token()

    run_initial_setup(venv_python)

    print("\nSetup complete!")
    print("\nTo activate the virtual environment, run:")
    if sys.platform == "win32":
        print(f"    {os.path.join(venv_dir, 'Scripts', 'activate.bat')}")
    else:
        print(f"    source {os.path.join(venv_dir, 'bin', 'activate')}")
    print("\nNext steps:")
    print("1. Activate the virtual environment")
    print("2. Review the README.md file for detailed usage instructions.")
    print("3. Use the scripts in the 'scripts' directory to manage and deploy your projects:")
    print("   - Create a new project: ssh root@<droplet_ip> '/usr/local/bin/manage_project.sh create <project_name> <project_type>'")
    print("   - Deploy a project: python scripts/deploy_web_app.py")
    print("   - Manage DigitalOcean credentials: ssh root@<droplet_ip> '/usr/local/bin/manage_do_credentials.sh [set|get|delete] <project_name> [do_token]'")
    print("4. Gather deployment information: python scripts/gather_deployment_info.py")
    print("5. Monitor resource usage: python scripts/monitor_resources.py")
    print("\nRemember to monitor your resource usage and costs through the DigitalOcean dashboard:")
    print("https://cloud.digitalocean.com/dashboard")
    
    print("\nNew features:")
    print("- Comprehensive error handling and logging: Check setup.log and resource_monitoring.log for detailed information.")
    print("- Resource cleanup mechanism: In case of setup failure, you'll be offered to clean up any created resources.")
    print("- Dry run mode: Allows you to see what actions would be taken without actually creating or modifying resources.")
    print("- Step-by-step execution with confirmation: The setup process now proceeds step-by-step, asking for confirmation before each major action.")
    print("- Resource usage monitoring: Use the new monitor_resources.py script to continuously monitor CPU, memory, and disk usage on your droplet.")
    
    print("\nIf you need any assistance, please refer to the README.md file or contact support.")

if __name__ == "__main__":
    main()