import os
import subprocess
import sys
import venv
import webbrowser

def create_virtual_environment():
    venv_dir = os.path.join(os.getcwd(), "venv")
    print(f"Creating virtual environment in {venv_dir}...")
    venv.create(venv_dir, with_pip=True)
    return venv_dir

def get_venv_python(venv_dir):
    if sys.platform == "win32":
        return os.path.join(venv_dir, "Scripts", "python.exe")
    return os.path.join(venv_dir, "bin", "python")

def install_dependencies(venv_python):
    print("Installing dependencies...")
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])

def check_external_dependencies():
    dependencies = ['doctl', 'kubectl', 'docker']
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
        print("4. Copy the generated token")
        webbrowser.open('https://cloud.digitalocean.com/account/api/tokens')
        token = input("\nPlease enter your DigitalOcean API token: ").strip()
        os.environ['DO_TOKEN'] = token
    return token

def setup_container_registry():
    print("\nTo set up a DigitalOcean Container Registry:")
    print("1. Go to https://cloud.digitalocean.com/registry")
    print("2. Click 'Create Registry'")
    print("3. Choose a name for your registry")
    print("4. Select a subscription plan")
    webbrowser.open('https://cloud.digitalocean.com/registry')
    input("\nPress Enter once you've created your container registry...")

def run_initial_setup(venv_python):
    subprocess.run([venv_python, 'scripts/initial_setup.py'])

def main():
    print("Welcome to the DigitalOcean Manager setup!")

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
        print("- kubectl: https://kubernetes.io/docs/tasks/tools/")
        print("- Docker: https://docs.docker.com/get-docker/")
        sys.exit(1)

    token = get_do_token()
    if not token:
        print("No DigitalOcean API token provided. Exiting.")
        sys.exit(1)

    setup_container_registry()

    print("\nRunning initial Kubernetes cluster setup...")
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
    print("3. Use the scripts in the 'scripts' directory to deploy your applications.")
    print("\nRemember to monitor your resource usage and costs through the DigitalOcean dashboard:")
    print("https://cloud.digitalocean.com/dashboard")

if __name__ == "__main__":
    main()