# VS Code Workflow Integration Guide

This guide explains how to incorporate the DigitalOcean Manager into your development workflow using Visual Studio Code (VS Code). It covers the process from local development and testing to deployment on the DigitalOcean droplet.

## Setup

1. Ensure you have completed the initial setup as described in the README.md file.
2. Install the "Remote - SSH" extension in VS Code.

## Development Workflow

### 1. Local Development

1. Open your project folder in VS Code.
2. Create or modify your web application or static site in the appropriate directory (`web_apps/` or `static_sites/`).
3. Use VS Code's integrated terminal to activate your local virtual environment:
   ```
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate.bat  # On Windows
   ```

### 2. Testing Locally

1. For web applications, set up a local development server. For example, if using Flask:
   ```python
   from flask import Flask
   app = Flask(__name__)

   @app.route('/')
   def hello():
       return "Hello, World!"

   if __name__ == '__main__':
       app.run(debug=True)
   ```
2. Run your local server and test your application in your web browser.

### 3. Connecting to the Remote Droplet

1. In VS Code, open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P).
2. Type "Remote-SSH: Connect to Host" and select it.
3. Enter `root@<your-droplet-ip>` and press Enter.
4. VS Code will open a new window connected to your droplet.

### 4. Syncing Files

1. In the remote VS Code window, open the folder where your application will be deployed (e.g., `/var/www/your-app-name`).
2. Use VS Code's built-in file explorer to upload your local files to the remote folder.

### 5. Testing on the Droplet

1. In the remote VS Code window, open an integrated terminal.
2. Activate the appropriate virtual environment:
   ```
   source /opt/venvs/your-app-name/bin/activate
   ```
3. Run your application or start your web server to test.

### 6. Deployment

When you're ready to deploy:

1. Ensure all your changes are synced to the droplet.
2. In your local VS Code window, run the deployment script:
   ```
   python scripts/deploy_web_app.py
   ```
3. Follow the prompts, using the droplet IP and app name you've been working with.

### 7. Post-Deployment

After deployment:

1. Run the gather deployment info script:
   ```
   python scripts/gather_deployment_info.py
   ```
2. Use the generated JSON file to update any CI/CD pipelines or monitoring tools.

## Tips for Efficient Workflow

1. Use VS Code's "Remote - SSH" extension to edit files directly on the droplet when needed.
2. Set up VS Code tasks for common operations like running tests or starting local servers.
3. Use VS Code's Source Control features to manage your git repository.
4. Consider setting up a staging environment on a separate droplet for testing before production deployment.

## Troubleshooting

- If you encounter permission issues when editing files on the droplet, ensure you're connected as the root user or have the necessary permissions.
- If your local and remote environments get out of sync, use the `gather_deployment_info.py` script to get the current state of your deployment.

Remember to always backup your data and test thoroughly before deploying to production. Refer to the main README.md and other documentation files for more detailed information on specific components of the DigitalOcean Manager.