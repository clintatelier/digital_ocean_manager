# DigitalOcean Manager

! This project provides a comprehensive setup for managing multiple web applications and static sites on a single DigitalOcean droplet. It automates many aspects of setup, deployment, and management, utilizing project-specific environments for application isolation.

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
   - Set up the droplet with necessary software (Python, Node.js, PHP, Apache, MySQL, Docker)
   - Install and configure DigitalOcean monitoring and management tools
   - Install project management and DigitalOcean credentials management scripts on the droplet

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
- Local virtual environment creation
- Python dependency installation
- DigitalOcean droplet creation and initial setup
- Deployment of web apps and static sites
- Project management on the droplet
- DigitalOcean credentials management for each project
- Gathering and outputting comprehensive deployment information
- Setting up DigitalOcean monitoring and management tools

### Manual (requires DigitalOcean web interface):
- Account creation and payment setup
- API token generation
- Advanced resource monitoring and cost management

## Usage

After running the setup script and activating the virtual environment, you can use the following scripts to manage your projects:

### Deploying Web Apps and Static Sites

1. Prepare your web app or static site in a local directory
2. Run the deployment script:
   ```
   python scripts/deploy_web_app.py
   ```
3. Follow the prompts to specify your project name, type (python, node, php, or static), local directory path, and the droplet IP address
4. Choose between virtual environment or Docker deployment (see "Deployment Options" section below)
5. After successful deployment, a JSON file with comprehensive deployment information will be generated

### Deployment Options

When deploying your project, you have two options for environment isolation:

1. Virtual Environment (default):
   - Uses Python's built-in venv module for Python projects
   - Uses local Node.js installation for Node.js projects
   - Uses system-wide PHP installation for PHP projects
   - Provides lightweight isolation for project dependencies

2. Docker:
   - Uses Docker containers for complete environment isolation
   - Supports all project types (Python, Node.js, PHP, static)
   - Provides stronger isolation, including system-level dependencies

During deployment, you'll be prompted to choose between these options. Select the one that best fits your project's needs and your preferred workflow.

### Customizing Project Environments

#### For Virtual Environment deployments:
- Python: Modify the requirements.txt file in your project directory
- Node.js: Update the package.json file in your project directory
- PHP: If using Composer, update the composer.json file in your project directory

#### For Docker deployments:
- You can customize the Dockerfile for your project by creating a Dockerfile in your project's root directory before deployment
- If no custom Dockerfile is found, a default one will be created based on your project type

### Gathering Deployment Information

To collect detailed information about your deployed projects:

1. Run the gather deployment info script:
   ```
   python scripts/gather_deployment_info.py
   ```
2. Follow the prompts to specify your project name, type, and the droplet IP address
3. The script will generate a JSON file with comprehensive deployment information

## Project Management

The droplet is set up with a script to manage projects. You can use this script via SSH to create, delete, or list projects:

- Create a new project:
  ```
  ssh root@<droplet_ip> '/usr/local/bin/manage_project.sh create <project_name> <project_type>'
  ```

- Delete a project:
  ```
  ssh root@<droplet_ip> '/usr/local/bin/manage_project.sh delete <project_name>'
  ```

- List all projects:
  ```
  ssh root@<droplet_ip> '/usr/local/bin/manage_project.sh list'
  ```

This system allows you to manage multiple projects on the droplet, keeping each application isolated and preventing conflicts between different projects' dependencies.

## DigitalOcean Credentials Management

The droplet is also set up with a script to manage DigitalOcean credentials for each project. This allows developers to have full access to DigitalOcean features for their specific projects:

- Set DigitalOcean credentials for a project:
  ```
  ssh root@<droplet_ip> '/usr/local/bin/manage_do_credentials.sh set <project_name> <do_token>'
  ```

- Get DigitalOcean credentials for a project:
  ```
  ssh root@<droplet_ip> '/usr/local/bin/manage_do_credentials.sh get <project_name>'
  ```

- Delete DigitalOcean credentials for a project:
  ```
  ssh root@<droplet_ip> '/usr/local/bin/manage_do_credentials.sh delete <project_name>'
  ```

## VS Code Integration

For developers using Visual Studio Code, we've created a comprehensive guide on how to integrate this DigitalOcean Manager into your VS Code workflow. This guide covers:

- Setting up VS Code for remote development with your DigitalOcean droplet
- Local development and testing processes
- Syncing your local environment with the remote droplet
- Deploying and managing your projects using VS Code

To learn more about using this tool with VS Code, please refer to our [VS Code Workflow Integration Guide](vscode_workflow.md).

## Deployment Information and Pipeline Integration

The `{project_name}_deployment_info.json` file generated after deployment contains comprehensive information about your project and its environment. This includes:

1. DigitalOcean API Token (securely stored)
2. Droplet Information:
   - IP address
   - Operating System
3. Project Information:
   - Name
   - Type (python, node, php, or static)
   - Apache configuration
   - Virtual environment or Docker container details
4. Project Dependencies:
   - List of project-specific dependencies and their versions
5. Database Information:
   - Database type, name, and connection details
6. Environment Variables:
   - List of environment variables used by the project
7. Project Structure:
   - Overview of the project's directory structure
8. Application Entry Points:
   - Main application file or entry point
9. Logging Configuration:
   - Log file locations and logging setup
10. Monitoring and Performance:
    - Links to monitoring dashboards and performance metrics endpoints
11. Backup and Recovery Information:
    - Backup procedures and recovery steps
12. SSL/TLS Configuration:
    - SSL certificate information and web server SSL configuration
13. Custom Domain Information:
    - Details about custom domain setup (if applicable)
14. Cron Jobs or Scheduled Tasks:
    - List of scheduled tasks associated with the project
15. Third-party Service Integrations:
    - Details of external services the project depends on

This comprehensive information allows you to:

1. Deploy updates to specific projects with all necessary context
2. Monitor project status and resource usage effectively
3. Manage resources and scale projects as needed
4. Troubleshoot issues by having all relevant information in one place
5. Maintain consistent environments across development, staging, and production
6. Automate deployment and management tasks in CI/CD pipelines

You can integrate this JSON file into your CI/CD pipelines for automated deployment and management tasks.

## Configuration Management

Environment-specific configurations are stored in the `config/` directory:

- `development.env`: Configuration for the development environment
- `staging.env`: Configuration for the staging environment
- `production.env`: Configuration for the production environment
- `template.env`: A template file with all possible configuration options

These files contain environment variables that are used to configure your projects for different deployment stages. They help maintain consistency across different environments and make it easier to manage environment-specific settings.

### Usage

1. Copy the `template.env` file and rename it to match your environment (e.g., `development.env`, `staging.env`, or `production.env`).
2. Edit the new file to set the appropriate values for your environment.
3. When deploying your project, specify which environment configuration to use.

### Example Configuration

A typical configuration file might look like this:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_dev
DB_USER=devuser
DB_PASSWORD=secretpassword

REDIS_HOST=localhost
REDIS_PORT=6379

DEBUG=True
LOG_LEVEL=DEBUG

API_KEY=your_api_key_here
```

Modify these files to suit your project's needs. Be sure to keep sensitive information (like API keys and passwords) secure and never commit them to version control.

## Best Practices and Tips

1. Always use the virtual environment when working with this project
2. Regularly update dependencies: `pip install --upgrade -r requirements.txt`
3. Use version control (git) for your projects
4. Regularly backup your DigitalOcean droplet and databases
5. Use meaningful names for your resources (projects, sites, etc.)
6. Monitor your resource usage to optimize costs and performance
7. Implement proper security measures, such as SSL certificates
8. Keep your DigitalOcean API tokens secure
9. Securely manage the generated deployment information JSON files
10. Regularly review and update Apache configurations for optimal performance
11. Use the comprehensive deployment information for troubleshooting and maintenance
12. Utilize DigitalOcean's built-in monitoring tools to track droplet performance

## Maintenance

- Regularly update the scripts to ensure compatibility with the latest DigitalOcean API
- Keep your droplet's software up to date by regularly running system updates
- Check for updates to the required Python packages used in your projects
- Periodically review and optimize your deployed projects for better resource utilization
- Regularly review and update the gather_deployment_info.py script to ensure it captures all necessary information
- Monitor and manage your droplet using DigitalOcean's dashboard and CLI tools

## Support

If you encounter any issues or have questions about using this DigitalOcean Manager, please open an issue in this repository or contact your system administrator.

## Disclaimer

This tool is not officially associated with DigitalOcean. Always refer to DigitalOcean's official documentation and terms of service when managing your resources.

## Cost Considerations

Using a single DigitalOcean droplet can be more cost-effective than a Kubernetes cluster. Here's an estimated cost breakdown:

- Basic Droplet (1 GB RAM, 1 vCPU, 25 GB SSD): $5 per month
- Standard Droplet (2 GB RAM, 1 vCPU, 50 GB SSD): $10 per month
- Standard Droplet (2 GB RAM, 2 vCPUs, 60 GB SSD): $15 per month
- Standard Droplet (4 GB RAM, 2 vCPUs, 80 GB SSD): $20 per month

Additional costs to consider:
- Bandwidth: 1 TB transfer included, $0.01/GB after that
- Monitoring: Free for basic metrics, $0.007 per hour ($5 per month) for advanced metrics if enabled
- Backups: 20% of the droplet cost if enabled

Estimated total for a basic setup with multiple projects: $10-$30 per month

To optimize costs:
1. Monitor resource usage in the DigitalOcean dashboard
2. Choose an appropriate droplet size based on your needs
3. Optimize your projects for efficient resource use
4. Use DigitalOcean's billing alerts to stay informed about your spending

Always review DigitalOcean's current pricing: https://www.digitalocean.com/pricing

## Version Control

This project uses Git for version control. The included `.gitignore` file prevents tracking of unnecessary files. Review and adjust the `.gitignore` file as needed for your specific requirements.

For the latest changes and updates, please refer to the CHANGELOG.md file in this repository.

