import digitalocean
import time

# Initialize the DigitalOcean client
manager = digitalocean.Manager(token="YOUR_API_TOKEN")

def create_database_cluster():
    cluster = digitalocean.DatabaseCluster(
        token=manager.token,
        name="shared-app-cluster",
        engine="pg",  # PostgreSQL
        version="14",  # or latest version
        size="db-s-2vcpu-4gb",  # Adjust size based on your needs
        region="nyc1",  # Choose appropriate region
        num_nodes=1
    )
    cluster.create()
    
    while cluster.status != "online":
        time.sleep(15)
        cluster.load()
    
    print(f"Database cluster created. Connection string: {cluster.connection_string}")
    return cluster

def setup_firewall(cluster):
    firewall = digitalocean.Firewall(
        token=manager.token,
        name="database-firewall",
        inbound_rules=[
            {
                "protocol": "tcp",
                "ports": "5432",
                "sources": {
                    "addresses": ["0.0.0.0/0"]  # Allow all IPs, adjust as needed
                }
            }
        ],
        outbound_rules=[
            {
                "protocol": "tcp",
                "ports": "all",
                "destinations": {
                    "addresses": ["0.0.0.0/0", "::/0"]
                }
            }
        ]
    )
    firewall.create()
    print("Firewall created and configured.")

def main():
    cluster = create_database_cluster()
    setup_firewall(cluster)
    
    print("\nCluster Information:")
    print(f"Host: {cluster.connection_string.split('@')[1].split(':')[0]}")
    print(f"Port: 5432")
    print(f"Initial Admin Username: {cluster.user}")
    print(f"Initial Admin Password: {cluster.password}")
    
    print("\nSetup complete! Use the add_new_application.py script to add new applications to this cluster.")

if __name__ == "__main__":
    main()