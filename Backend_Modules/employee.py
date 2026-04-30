# from db_connection import get_connection
from .db_connection import get_connection


def Add_employee(emp_id, name, email, phone, EmpType, dept_id):
    conn = get_connection()
    if conn is None:
        print("Database connection failed")
        return
    cursor = conn.cursor()
    query = """
    Insert into employee(employeeID, name, email, phone, EmpType, departmentID)
    values(%s,%s,%s,%s,%s,%s)
    """
    try:
        cursor.execute(query, (emp_id, name, email, phone, EmpType, dept_id))
        conn.commit()
        print("Employee added successfully")
    except Exception as e:
        print("Error : ", e)

    finally:
        print("\n\n")
        cursor.close()
        conn.close()


def get_Employees():
    conn = get_connection()
    if conn is None:
        print("Database connection failed")
        return
    cursor = conn.cursor()
    query = "Select * from employee"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print("------------------------")
            print("Employee ID -> ", row[0])
            print("Name -> ", row[1])
            print("Email -> ", row[2])
            print("Mobile Number -> ", row[3])
            print("Employee Type -> ", row[4])
            print("------------------------")
            print("\n")
    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()


def get_employee_by_id(emp_id):
    conn = get_connection()
    if conn is None:
        print("Database connection failed")
        return None
    cursor = conn.cursor()
    query = "Select * from employee where EmployeeID =%s"
    try:
        cursor.execute(query, (emp_id,))
        rows = cursor.fetchone()
        if rows == None:
            print("Employee not found ")
        print("------------------------")
        print("Employee ID -> ", rows[0])
        print("Name -> ", rows[1])
        print("Email -> ", rows[2])
        print("Mobile Number -> ", rows[3])
        print("Employee Type -> ", rows[4])
        print("------------------------")
        print("\n")

    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()


def search_employee_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    select EmployeeID, Name, Email,Phone,EmpType,DepartmentID
    FROM Employee
    WHERE LOWER(Name) like LOWER(%s)
    """
    try:
        cursor.execute(query, ("%" + name + "%",))
        rows = cursor.fetchall()
        if not rows:
            print("No Employee Found")
        else:
            for row in rows:
                print(
                    f"""
                ------------------------
                EmployeeID : {row[0]}
                Name : {row[1]}
                Email : {row[2]}
                Phone : {row[3]}
                Type : {row[4]}
                Department : {row[5]}
                ------------------------
                """
                )
                print("\n")
    except Exception as e:
        print("Error ", e)
    finally:
        cursor.close()
        conn.close()


def count_employees(dept_ID):
    conn = get_connection()
    cursor = conn.cursor()
    query = "Select count(*) from employee Where departmentID=%s "
    cursor.execute(query, (dept_ID,))
    count = cursor.fetchone()[0]
    query = "Select departmentName from department where departmentID=%s"
    cursor.execute(query, (dept_ID,))
    dept = cursor.fetchone()

    print("Total Employees in ", dept[0], " Department : ", count)
    print("\n")
    cursor.close()
    conn.close()


def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "Delete from employee where employeeID=%s"
    try:
        cursor.execute(query, (emp_id,))
        conn.commit()
        print("Employee Deleted")
    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()
