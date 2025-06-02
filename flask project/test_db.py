from database.db_config import get_db_connection

conn = get_db_connection()
if conn.is_connected():
    print("✅ Successfully connected to MySQL database!")
conn.close()
