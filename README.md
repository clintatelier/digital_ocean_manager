# Digital Ocean Manager

This project provides a comprehensive setup for managing various types of applications (web apps, mobile apps, and static sites) on DigitalOcean. It includes scripts for initial setup, resource management, and deployment for different project types.

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/digital_ocean_manager.git
   cd digital_ocean_manager
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your DigitalOcean API token:
   - Create an API token in the DigitalOcean control panel (API > Tokens/Keys)
   - Set the token as an environment variable:
     ```
     export DO_TOKEN=your_digitalocean_api_token
     ```

## Directory Structure

- `config/`: Configuration files for different environments
- `scripts/`: Utility scripts for managing DigitalOcean resources and deployments
- `web_apps/`: Templates and resources for web applications
- `mobile_apps/`: Templates and resources for mobile applications
- `static_sites/`: Templates and resources for static websites

## Usage

### Initial Setup

Run the initial setup script to create your DigitalOcean infrastructure:

```
python scripts/initial_setup.py
```

This script will create a droplet, a database cluster, and set up a firewall.

### Managing Resources

Use the resource management script to list, create, or delete DigitalOcean resources:

```
python scripts/manage_resources.py
```

Follow the prompts to perform various actions on your DigitalOcean resources.

### Web Apps

1. Copy the web app template:
   ```
   cp web_apps/template_web_app.py web_apps/your_app_name.py
   ```

2. Modify `your_app_name.py` as needed for your specific web application.

3. Deploy your web app:
   ```
   python scripts/deploy_web_app.py
   ```

### Mobile Apps

1. Copy the React Native template:
   ```
   cp mobile_apps/template_react_native_app.js mobile_apps/your_app_name/App.js
   ```

2. Modify `App.js` and add other necessary files for your mobile app.

3. Build and deploy your mobile app:
   ```
   python scripts/deploy_mobile_app.py
   ```

### Static Sites

1. Copy the static site template:
   ```
   cp static_sites/index.html static_sites/your_site_name/index.html
   ```

2. Modify `index.html` and add other static assets as needed.

3. Deploy your static site:
   ```
   python scripts/deploy_static_site.py
   ```

## Configuration Management

Environment-specific configurations are stored in the `config/` directory:

- `development.env`: Development environment configuration
- `staging.env`: Staging environment configuration
- `production.env`: Production environment configuration

Modify these files to suit your project's needs.

## Best Practices and Tips

1. Always use version control (git) for your projects.
2. Regularly backup your DigitalOcean resources and databases.
3. Use meaningful names for your droplets, databases, and other resources.
4. Monitor your resource usage to optimize costs and performance.
5. Implement proper security measures, such as firewalls and SSL certificates.
6. Keep your DigitalOcean API token secure and never commit it to version control.

## Support

If you encounter any issues or have questions about using this Digital Ocean Manager, please open an issue in this repository or contact your system administrator.

## Disclaimer

This tool is not officially associated with DigitalOcean. Always refer to DigitalOcean's official documentation and terms of service when managing your resources.