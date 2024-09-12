# DigitalOcean Manager

This project provides a comprehensive setup for managing web applications and static sites on a single DigitalOcean droplet. It automates many aspects of setup and deployment, utilizing virtual environments for application isolation.

## Prerequisites

Before using this tool, you need to:

1. Create a DigitalOcean account and set up payment information
2. Install the following on your local machine:
   - Python 3.7+
   - `doctl` (DigitalOcean command-line tool)

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
   - Create a single DigitalOcean droplet
   - Set up the droplet with necessary software (Python, Node.js, PHP, Apache, MySQL)

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
- DigitalOcean droplet creation and initial setup
- Deployment of web apps and static sites
- Virtual environment management on the droplet
- Gathering and outputting deployment information

### Manual (requires DigitalOcean web interface):
- Account creation and payment setup
- API token generation
- Resource monitoring and cost management

## Usage

After running the setup script and activating the virtual environment, you can use the following scripts to manage your applications:

### Deploying Web Apps and Static Sites

1. Prepare your web app in the `web_apps` directory or your static site in the `static_sites` directory
2. Run the deployment script:
   ```
   python scripts/deploy_web_app.py
   ```
3. Follow the prompts to specify your app name, type (web app or static site), and the droplet IP address
4. After successful deployment, a JSON file with deployment information will be generated

### Gathering Deployment Information

To collect information about your deployed applications:

1. Run the gather deployment info script:
   ```
   python scripts/gather_deployment_info.py
   ```
2. Follow the prompts to specify your app name, type, and the droplet IP address
3. The script will generate a JSON file with detailed deployment information

## VS Code Integration

For developers using Visual Studio Code, we've created a comprehensive guide on how to integrate this DigitalOcean Manager into your VS Code workflow. This guide covers:

- Setting up VS Code for remote development with your DigitalOcean droplet
- Local development and testing processes
- Syncing your local environment with the remote droplet
- Deploying and managing your applications using VS Code

To learn more about using this tool with VS Code, please refer to our [VS Code Workflow Integration Guide](vscode_workflow.md).

## Virtual Environment Management

The droplet is set up with a script to manage virtual environments for your applications. You can use this script via SSH to create, delete, or list virtual environments:

- Create a new virtual environment:
  ```
  ssh root@<droplet_ip> '/usr/local/bin/manage_venv.sh create <app_name>'
  ```

- Delete a virtual environment:
  ```
  ssh root@<droplet_ip> '/usr/local/bin/manage_venv.sh delete <app_name>'
  ```

- List all virtual environments:
  ```
  ssh root@<droplet_ip> '/usr/local/bin/manage_venv.sh list'
  ```

## Deployment Information and Pipeline Integration

The `{app_name}_deployment_info.json` file generated after deployment contains:

- DigitalOcean API Token (securely stored)
- Droplet information (IP address, OS)
- Application-specific details (name, type, Apache configuration)
- Virtual environment information (for web apps)

You can use this information in your CI/CD pipelines for various tasks such as:

1. Deploying updates
2. Monitoring application status
3. Managing resources and scaling

Refer to the "Deployment Information and Pipeline Integration" section in the project documentation for detailed examples.

## Configuration Management

Environment-specific configurations are stored in the `config/` directory:

- `development.env`: Development environment configuration
- `staging.env`: Staging environment configuration
- `production.env`: Production environment configuration

Modify these files to suit your project's needs.

## Best Practices and Tips

1. Always use the virtual environment when working with this project
2. Regularly update dependencies: `pip install --upgrade -r requirements.txt`
3. Use version control (git) for your projects
4. Regularly backup your DigitalOcean droplet and databases
5. Use meaningful names for your resources (apps, sites, etc.)
6. Monitor your resource usage to optimize costs and performance
7. Implement proper security measures, such as SSL certificates
8. Keep your DigitalOcean API token secure
9. Securely manage the generated deployment information JSON files

## Maintenance

- Regularly update the scripts to ensure compatibility with the latest DigitalOcean API
- Keep your droplet's software up to date by regularly running system updates
- Check for updates to the required Python packages used in your projects

## Support

If you encounter any issues or have questions about using this DigitalOcean Manager, please open an issue in this repository or contact your system administrator.

## Disclaimer

This tool is not officially associated with DigitalOcean. Always refer to DigitalOcean's official documentation and terms of service when managing your resources.

## Cost Considerations

Using a single DigitalOcean droplet can be more cost-effective than a Kubernetes cluster:

- Droplet: Starting at $5/month (1GB RAM, 1 vCPU, 25GB SSD)
- Additional storage: From $10/month for 100GB block storage
- Bandwidth: 1TB included, then $0.01/GB for outbound transfer

Estimated total for a basic setup with multiple projects: $10-$30/month

To optimize costs:
1. Monitor resource usage in the DigitalOcean dashboard
2. Choose an appropriate droplet size
3. Optimize your applications for efficient resource use
4. Use DigitalOcean's billing alerts

Always review DigitalOcean's current pricing: https://www.digitalocean.com/pricing

## Version Control

This project uses Git for version control. The included `.gitignore` file prevents tracking of unnecessary files. Review and adjust the `.gitignore` file as needed for your specific requirements.

For the latest changes and updates, please refer to the CHANGELOG.md file in this repository.
