import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Stonecold.123",
            database="flask_project"
        )
        print("Database Connected Successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        conn.close()
