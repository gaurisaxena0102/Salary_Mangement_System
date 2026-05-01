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
    if conn is None:
        print("Database Connection Failed")
        return
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
    if conn is None:
        print("Database Connection Failed")
        return
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
    if conn is None:
        print("Database Connection Failed")
        return
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
    if conn is None:
        print("Database Connection Failed")
        return
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


def employee_count_per_department():
    conn = get_connection()
    if conn is None:
        print("Database Connection Failed")
        return
    cursor = conn.cursor()
    query = """
    Select d.departmentName, count(e.employeeID) AS TotalEmployees
    From department d
    LEFT JOIN employee e ON d.departmentID = e.departmentID
    Group by departmentName
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print("No Departments found. ")
        else:
            print("\n--- Employee Count per Department ---")
            for row in rows:
                print(f"{row[0]} -> {row[1]}")
    except Exception as e:
        print("Error ", e)
    finally:
        cursor.close()
        conn.close()


def department_salary_report():
    conn = get_connection()
    if conn is None:
        print("Database Connection Failed")
        return
    cursor = conn.cursor()
    query = """
    SELECT d.departmentName,
    count(e.EmployeeID) AS ToatalEmployees,
    SUM(s.BasicSalary + s .HRA + s.DA + s.Bonus - s.Tax - s.PF) AS TotalSalary,
    AVG(s.BasicSalary + s .HRA + s.DA + s.Bonus - s.Tax - s.PF) AS AvgSalary
    FROM Department d
    Left Join Employee e on d.departmentID=e.departmentID
    Left Join Salary s on e.employeeID =s.EmployeeID
    GROUP BY d.departmentName
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print("No data found ")
        else:
            print("\n--- Department Salary Report ---")
            for row in rows:
                print("Department : ", row[0])
                print("Total Employees : ", row[1])
                print("Total Salary : ", float(row[2]) if row[2] else 0)
                print("Average Salary : ", float(row[3]) if row[3] else 0)
                print("-----------------------------")

    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()
