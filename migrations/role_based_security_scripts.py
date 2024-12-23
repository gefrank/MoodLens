import sqlite3
import os

db_file_path = "instance/moodlens.db"

def setup_roles_and_users_tables():
    """Create roles and user_roles tables, and populate initial roles."""
    if not os.path.exists(db_file_path):
        raise FileNotFoundError(f"Database not found at {db_file_path}")

    # Connect to the database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Create the roles table
    create_roles_table = """
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER NOT NULL PRIMARY KEY,
        role_name TEXT NOT NULL UNIQUE
    );
    """
    cursor.execute(create_roles_table)

    # Create the user_roles table
    create_user_roles_table = """
    CREATE TABLE IF NOT EXISTS user_roles (
        user_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        PRIMARY KEY (user_id, role_id),
        FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
    );
    """
    cursor.execute(create_user_roles_table)

    # Insert initial roles into the roles table
    initial_roles = [
        (1, 'admin'),
        (2, 'customer_service_admin')
    ]

    for role in initial_roles:
        try:
            cursor.execute("INSERT INTO roles (id, role_name) VALUES (?, ?);", role)
        except sqlite3.IntegrityError:
            # Role already exists, skip
            pass

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Roles and user_roles tables have been set up successfully.")

if __name__ == "__main__":
    setup_roles_and_users_tables()
