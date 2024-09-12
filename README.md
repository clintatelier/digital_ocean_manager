# DigitalOcean Manager

This project provides a flexible setup for managing various DigitalOcean resources, including droplets (virtual machines), databases, and firewalls. It allows for easy setup and management of a complete infrastructure under a single DigitalOcean account.

## Setup

1. Install the required dependencies:
   ```
   pip install digitalocean
   ```

2. Ensure you have a DigitalOcean account and an API token. You can create an API token in the DigitalOcean control panel under API > Tokens/Keys.

## Usage

### Initial Setup

1. Run the `initial_setup.py` script:
   ```
   python initial_setup.py
   ```
2. Enter your DigitalOcean API token when prompted.
3. This script will create:
   - A droplet (virtual machine) that can host websites, applications, or control panels
   - A PostgreSQL database cluster
   - A firewall to secure your resources

### Managing Resources

1. Run the `manage_resources.py` script:
   ```
   python manage_resources.py
   ```
2. Enter your DigitalOcean API token when prompted.
3. Choose from the following options:
   - List Droplets
   - List Databases
   - Create Droplet
   - Create Database
   - Delete Droplet
   - Delete Database

## Features

- **Droplet Management**: Create, list, and delete droplets (virtual machines) that can host websites, applications, or control panels.
- **Database Management**: Create, list, and delete databases within your PostgreSQL cluster.
- **Firewall Setup**: Automatically configure a firewall to secure your infrastructure.
- **Centralized Management**: Manage all your DigitalOcean resources from a single interface.

## Best Practices

- Keep your API token secure and never share it publicly.
- Regularly review and update your resources to ensure optimal performance and security.
- Use meaningful names for your droplets and databases to easily identify their purposes.
- Monitor your resource usage to optimize costs and performance.

## Maintenance

Regularly update the scripts to ensure compatibility with the latest DigitalOcean API. Check for updates to the `python-digitalocean` library and other dependencies.

## Support

If you encounter any issues or have questions about using this DigitalOcean Manager, please open an issue in this repository or contact your system administrator.

## Disclaimer

This tool is not officially associated with DigitalOcean. Always refer to DigitalOcean's official documentation and terms of service when managing your resources.