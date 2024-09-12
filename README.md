# DigitalOcean Manager

This project provides a comprehensive setup for managing various types of applications (web apps, static sites, and mobile apps) on DigitalOcean using a Kubernetes-based architecture. It automates many aspects of setup and deployment, but some manual steps are still required.

## Prerequisites

Before using this tool, you need to:

1. Create a DigitalOcean account and set up payment information
2. Install the following on your local machine:
   - Python 3.7+
   - `doctl` (DigitalOcean command-line tool)
   - `kubectl` (Kubernetes command-line tool)
   - Docker

## Quick Start

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/digital_ocean_manager.git
   cd digital_ocean_manager
   ```

2. Run the setup script:
   ```
   python setup.py
   ```

3. Follow the prompts to complete the setup process. The script will:
   - Create a virtual environment
   - Install all required Python dependencies
   - Guide you through generating a DigitalOcean API token
   - Help you set up a container registry
   - Create a Kubernetes cluster

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate.bat
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

## What's Automated vs. Manual

### Automated:
- Virtual environment creation
- Python dependency installation
- Kubernetes cluster creation
- Deployment of web apps, static sites, and mobile app builds
- Gathering and outputting deployment information

### Manual (requires DigitalOcean web interface):
- Account creation and payment setup
- API token generation
- Initial container registry setup
- Resource monitoring and cost management

## Version Control

This project uses Git for version control. A `.gitignore` file has been included to prevent unnecessary files from being tracked. The `.gitignore` file excludes:

- Virtual environment directories (venv/, env/)
- Environment variable and API key files (*.env, .env)
- Python-related files (__pycache__/, *.pyc, etc.)
- OS-generated files (.DS_Store, Thumbs.db)
- IDE-specific files (.vscode/, .idea/)
- Other common files and directories that should not be version-controlled

Make sure to review the `.gitignore` file and adjust it if needed for your specific project requirements.

## Usage

After running the setup script and activating the virtual environment, you can use the following scripts to manage your applications:

### Deploying Web Apps

1. Prepare your web app in the `web_apps` directory
2. Run the deployment script:
   ```
   python scripts/deploy_web_app.py
   ```
3. Follow the prompts to specify your app name and container registry
4. After successful deployment, a JSON file with deployment information will be generated

### Deploying Static Sites

1. Prepare your static site in the `static_sites` directory
2. Run the deployment script:
   ```
   python scripts/deploy_static_site.py
   ```
3. Follow the prompts to specify your site name and container registry
4. After successful deployment, a JSON file with deployment information will be generated

### Building Mobile Apps

1. Prepare your mobile app in the `mobile_apps` directory
2. Run the build script:
   ```
   python scripts/deploy_mobile_app.py
   ```
3. Follow the prompts to specify your app name and target platform (Android/iOS)
4. Follow the provided instructions to distribute your app to the appropriate app store
5. After successful build, a JSON file with deployment information will be generated

## Deployment Information

After each successful deployment or build, the system generates a JSON file containing relevant deployment information. This file includes:

- DigitalOcean API Token (securely stored)
- Kubernetes cluster information
- Application-specific details (name, type, registry, etc.)
- Service information (for web apps and static sites)

The generated JSON file can be used by other tools or AI agents to manage and interact with the deployed applications. The file is named `{app_name}_deployment_info.json` and is saved in the same directory as the deployment scripts.

## Configuration Management

Environment-specific configurations are stored in the `config/` directory:

- `development.env`: Development environment configuration
- `staging.env`: Staging environment configuration
- `production.env`: Production environment configuration

Modify these files to suit your project's needs.

## Best Practices and Tips

1. Always use the virtual environment when working with this project
2. Regularly update the virtual environment: `pip install --upgrade -r requirements.txt`
3. Use version control (git) for your projects
4. Regularly backup your DigitalOcean resources and databases
5. Use meaningful names for your resources (apps, sites, etc.)
6. Monitor your resource usage to optimize costs and performance
7. Implement proper security measures, such as SSL certificates (automated with ingress)
8. Keep your DigitalOcean API token and container registry credentials secure
9. Securely manage the generated deployment information JSON files

## Maintenance

Regularly update the scripts and Kubernetes manifests to ensure compatibility with the latest DigitalOcean API and Kubernetes versions. Check for updates to the required Python packages and Docker images used in your projects.

## Support

If you encounter any issues or have questions about using this DigitalOcean Manager, please open an issue in this repository or contact your system administrator.

## Disclaimer

This tool is not officially associated with DigitalOcean. Always refer to DigitalOcean's official documentation and terms of service when managing your resources.

## Cost Considerations

The cost of running your projects on DigitalOcean can vary based on your specific needs and usage. Here's a rough estimate for running multiple projects:

1. Kubernetes Cluster: Starting at $30/month for a basic 3-node cluster
2. Container Registry: $5/month for the basic plan
3. Storage: $0.10/GB per month (e.g., $1 for 10GB)
4. Bandwidth: $0.01/GB for outbound transfer (e.g., $10 for 1TB)
5. Additional resources (e.g., CI/CD for mobile apps): Varies based on usage

Estimated total for a basic setup with multiple projects: $50-$100/month

Factors that can affect your costs:
- Number and size of your Kubernetes nodes
- Storage requirements
- Bandwidth usage
- Use of additional DigitalOcean services (e.g., managed databases, load balancers)
- Frequency and duration of mobile app builds

To manage and optimize your costs:
1. Regularly monitor your resource usage in the DigitalOcean dashboard
2. Use appropriate sized resources for your needs
3. Implement auto-scaling to handle traffic spikes efficiently
4. Optimize your applications for resource usage
5. Use DigitalOcean's billing alerts to stay informed about your spending

Remember to review DigitalOcean's current pricing as it may change over time: https://www.digitalocean.com/pricing
