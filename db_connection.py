import mysql.connector


def get_connection():
    try:

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="gauri01",
            database="Salary_Management",
        )
        if conn.is_connected():

            # print("Connection Established ")
            return conn
        else:
            print("connection Failed")
    except Exception as e:
        print("Error ", e)
        return None


# get_connection()
