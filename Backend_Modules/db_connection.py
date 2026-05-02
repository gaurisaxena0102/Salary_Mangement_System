import mysql.connector
import config


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
        )

        if conn.is_connected():
            return conn
        else:
            print("Connection Failed")

    except Exception as e:
        print("Error:", e)
        return None
