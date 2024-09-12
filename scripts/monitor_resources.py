import psutil
import time
import logging
from digitalocean import Droplet, Manager
import os

# Set up logging
logging.basicConfig(filename='resource_monitoring.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_droplet_info():
    token = os.getenv("DO_TOKEN")
    if not token:
        logging.error("DigitalOcean API token not found")
        return None

    manager = Manager(token=token)
    droplets = manager.get_all_droplets()
    if not droplets:
        logging.error("No droplets found")
        return None

    return droplets[0]  # Assuming we're monitoring the first droplet

def monitor_resources(warning_threshold=80, check_interval=60):
    droplet = get_droplet_info()
    if not droplet:
        logging.error("Failed to get droplet information")
        return

    logging.info(f"Starting resource monitoring for droplet: {droplet.name}")
    
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent

        logging.info(f"CPU usage: {cpu_percent}%")
        logging.info(f"Memory usage: {memory_percent}%")
        logging.info(f"Disk usage: {disk_percent}%")

        if cpu_percent > warning_threshold:
            logging.warning(f"High CPU usage detected: {cpu_percent}%")
        if memory_percent > warning_threshold:
            logging.warning(f"High memory usage detected: {memory_percent}%")
        if disk_percent > warning_threshold:
            logging.warning(f"High disk usage detected: {disk_percent}%")

        # Get DigitalOcean specific metrics
        droplet.load()
        do_cpu_usage = droplet.cpu()
        do_memory_usage = droplet.memory()
        do_disk_usage = droplet.disk_usage()

        logging.info(f"DigitalOcean CPU usage: {do_cpu_usage}")
        logging.info(f"DigitalOcean Memory usage: {do_memory_usage}")
        logging.info(f"DigitalOcean Disk usage: {do_disk_usage}")

        time.sleep(check_interval)

if __name__ == "__main__":
    monitor_resources()