# from db_connection import get_connection
from .db_connection import get_connection


def add_department(dept_id, dept_name):
    conn = get_connection()
    if conn is None:
        print("Database connection failed")
        return
    cursor = conn.cursor()
    query = "Insert into department (DepartmentID, DepartmentName) Values(%s,%s)"

    try:
        cursor.execute(query, (dept_id, dept_name))
        conn.commit()
        print("Department Added successfully ")
    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()


def get_departments():
    conn = get_connection()
    cursor = conn.cursor()
    query = "Select* from department"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print("No department found")
        else:
            for row in rows:
                print("Department_ID : ", row[0], "  Name : ", row[1])
    except Exception as e:
        print("Error ", e)
    finally:
        cursor.close()
        conn.close()


def get_department_by_id(dept_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "Select * from department where departmentID = %s"
    try:
        cursor.execute(query, (dept_id,))
        row = cursor.fetchone()
        if row:
            print("Department_ID : ", row[0], " Name : ", row[1])
        else:
            print("Department not found")
    except Exception as e:
        print("Error ", e)
    finally:
        cursor.close()
        conn.close()


def count_departments():
    conn = get_connection()
    cursor = conn.cursor()

    query = "Select count(*) from department"
    try:
        cursor.execute(query)
        count = cursor.fetchone()
        print("Total Departments : ", count[0])
    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()


def show_department_employees(dept_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "Select* from employee where departmentID=%s"
    try:
        cursor.execute(query, (dept_id,))
        rows = cursor.fetchall()

        if not rows:
            print("No Employees Found in this Department")
        else:
            for row in rows:
                print(row)
    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()
