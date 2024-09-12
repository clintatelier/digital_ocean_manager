import digitalocean

class DigitalOceanManager:
    def __init__(self, api_token):
        self.manager = digitalocean.Manager(token=api_token)

    def list_droplets(self):
        return self.manager.get_all_droplets()

    def list_databases(self):
        return self.manager.get_all_databases()

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

    def create_database(self, cluster_id, db_name):
        cluster = self.manager.get_database_cluster(cluster_id)
        return cluster.create_database(db_name)

    def delete_droplet(self, droplet_id):
        droplet = self.manager.get_droplet(droplet_id)
        return droplet.destroy()

    def delete_database(self, cluster_id, db_name):
        cluster = self.manager.get_database_cluster(cluster_id)
        return cluster.delete_database(db_name)

def main():
    api_token = input("Enter your DigitalOcean API token: ")
    do_manager = DigitalOceanManager(api_token)

    while True:
        print("\n1. List Droplets")
        print("2. List Databases")
        print("3. Create Droplet")
        print("4. Create Database")
        print("5. Delete Droplet")
        print("6. Delete Database")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            droplets = do_manager.list_droplets()
            for droplet in droplets:
                print(f"Droplet: {droplet.name} (ID: {droplet.id}, IP: {droplet.ip_address})")

        elif choice == '2':
            databases = do_manager.list_databases()
            for db in databases:
                print(f"Database: {db.name} (ID: {db.id})")

        elif choice == '3':
            name = input("Enter droplet name: ")
            region = input("Enter region (e.g., nyc1): ")
            size = input("Enter size (e.g., s-1vcpu-1gb): ")
            image = input("Enter image (e.g., ubuntu-20-04-x64): ")
            droplet = do_manager.create_droplet(name, region, size, image)
            print(f"Droplet created: {droplet.name} (ID: {droplet.id})")

        elif choice == '4':
            cluster_id = input("Enter database cluster ID: ")
            db_name = input("Enter new database name: ")
            db = do_manager.create_database(cluster_id, db_name)
            print(f"Database created: {db.name}")

        elif choice == '5':
            droplet_id = input("Enter droplet ID to delete: ")
            do_manager.delete_droplet(droplet_id)
            print(f"Droplet {droplet_id} deleted")

        elif choice == '6':
            cluster_id = input("Enter database cluster ID: ")
            db_name = input("Enter database name to delete: ")
            do_manager.delete_database(cluster_id, db_name)
            print(f"Database {db_name} deleted from cluster {cluster_id}")

        elif choice == '7':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()