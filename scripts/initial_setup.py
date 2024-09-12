import digitalocean
import time

class DigitalOceanManager:
    def __init__(self, api_token):
        self.manager = digitalocean.Manager(token=api_token)

    def create_droplet(self, name, region, size, image):
        droplet = digitalocean.Droplet(
            token=self.manager.token,
            name=name,
            region=region,
            size=size,
            image=image
        )
        droplet.create()
        return droplet

    def create_database_cluster(self, name, engine, size, region, num_nodes):
        cluster = digitalocean.DatabaseCluster(
            token=self.manager.token,
            name=name,
            engine=engine,
            version="14",  # or latest version
            size=size,
            region=region,
            num_nodes=num_nodes
        )
        cluster.create()
        return cluster

    def setup_firewall(self, name, droplet_ids=None):
        firewall = digitalocean.Firewall(
            token=self.manager.token,
            name=name,
            inbound_rules=[
                {
                    "protocol": "tcp",
                    "ports": "80",
                    "sources": {"addresses": ["0.0.0.0/0", "::/0"]}
                },
                {
                    "protocol": "tcp",
                    "ports": "443",
                    "sources": {"addresses": ["0.0.0.0/0", "::/0"]}
                },
                {
                    "protocol": "tcp",
                    "ports": "22",
                    "sources": {"addresses": ["0.0.0.0/0", "::/0"]}
                }
            ],
            outbound_rules=[
                {
                    "protocol": "tcp",
                    "ports": "all",
                    "destinations": {"addresses": ["0.0.0.0/0", "::/0"]}
                }
            ],
            droplet_ids=droplet_ids
        )
        firewall.create()
        return firewall

def main():
    api_token = input("Enter your DigitalOcean API token: ")
    do_manager = DigitalOceanManager(api_token)

    # Create a droplet
    droplet = do_manager.create_droplet(
        name="my-web-server",
        region="nyc1",
        size="s-1vcpu-1gb",
        image="ubuntu-20-04-x64"
    )
    print(f"Droplet created: {droplet.name} (ID: {droplet.id})")

    # Wait for the droplet to be active
    while droplet.status != "active":
        time.sleep(5)
        droplet.load()

    # Create a database cluster
    cluster = do_manager.create_database_cluster(
        name="my-db-cluster",
        engine="pg",
        size="db-s-1vcpu-1gb",
        region="nyc1",
        num_nodes=1
    )
    print(f"Database cluster created: {cluster.name} (ID: {cluster.id})")

    # Setup firewall
    firewall = do_manager.setup_firewall("my-firewall", droplet_ids=[droplet.id])
    print(f"Firewall created: {firewall.name} (ID: {firewall.id})")

    print("\nSetup complete!")
    print(f"Droplet IP: {droplet.ip_address}")
    print(f"Database connection string: {cluster.connection_string}")

if __name__ == "__main__":
    main()