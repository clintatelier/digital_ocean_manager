import digitalocean
import secrets
import string

def generate_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(20))

def add_new_application(cluster_id, app_name):
    manager = digitalocean.Manager(token="YOUR_API_TOKEN")
    cluster = manager.get_database_cluster(cluster_id)

    # Create new database
    db = cluster.create_database(app_name)

    # Create new user
    password = generate_password()
    user = cluster.create_user(app_name, password)

    # Grant user access to the database
    cluster.grant_user_access(user, db)

    print(f"\nAccess Information for {app_name}:")
    print(f"Host: {cluster.connection_string.split('@')[1].split(':')[0]}")
    print(f"Port: 5432")
    print(f"Database: {app_name}")
    print(f"Username: {app_name}")
    print(f"Password: {password}")

if __name__ == "__main__":
    cluster_id = input("Enter the cluster ID: ")
    app_name = input("Enter the new application name: ")
    add_new_application(cluster_id, app_name)