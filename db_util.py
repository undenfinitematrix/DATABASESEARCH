import pymysql

def get_db_connection_util():
    """
    Create a connection to the MySQL database.
    Returns a connection object or None if connection fails.
    """
    try:
        connection = pymysql.connect(
            host="localhost",  # XAMPP MySQL host
            user="root",       # Your MySQL username
            password="",  # Your MySQL password
            database="databasework",  # Your database name
            port=3306         # Change if your MySQL uses a different port
        )
        return connection
    except pymysql.Error as err:
        print("❌ Database connection failed:", err)
        return None

# =========================
# TEST CONNECTION
# =========================
if __name__ == "__main__":
    conn = get_db_connection_util()
    if conn:
        print("✅ Successfully connected to the database!")
        conn.close()
    else:
        print("❌ Could not connect to the database.")
