import sqlite3
import bcrypt

# Function to hash a password
def hash_password(password):
    # bcrypt generates a salt automatically
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Function to verify a password against the stored hash
def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode(), stored_hash)

# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect("user_management.db")
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    finally:
        conn.close()

# Function to login a user (verify username and password)
def login_user(username, password):
    conn = sqlite3.connect("user_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored_hash = cursor.fetchone()
    conn.close()

    if stored_hash:
        if verify_password(password, stored_hash[0]):
            print("Login successful!")
            return True
        else:
            print("Invalid password.")
            return False
    else:
        print("User not found.")
        return False

# Register the user "cornell" with password "stokes"
if __name__ == "__main__":
    register_user("cornell", "stokes")