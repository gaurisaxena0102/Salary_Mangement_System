# from db_connection import get_connection
from .db_connection import get_connection


def add_salary(salary_ID, emp_id, basic, hra, da, bonus, tax, pf):
    conn = get_connection()
    if conn is None:
        print("Database connection Failed")
        return

    cursor = conn.cursor()
    query = """
    INSERT INTO SALARY 
    (salaryID, EmployeeID, BasicSalary , HRA, DA, Bonus, Tax, PF)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """
    try:
        cursor.execute(query, (salary_ID, emp_id, basic, hra, da, bonus, tax, pf))
        conn.commit()
        print("Salary Added Successfully")
    except Exception as e:
        print("Error : ", e)
    finally:
        print("\n\n")
        cursor.close()
        conn.close()


def get_all_Salaries():
    conn = get_connection()
    cursor = conn.cursor()

    query = "Select* from Salary"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        query = """
            SELECT *,
            (BasicSalary + HRA + DA + Bonus - Tax - PF) AS Net_Salary
            FROM Salary
            """
        cursor.execute(query)
        netSal = cursor.fetchone()
        if not rows:
            print("No salary Record found")
        else:
            for row in rows:
                print("Salary ID:", row[0])
                print("Employee ID:", row[1])
                print("Basic Salary:", float(row[2]))
                print("HRA:", float(row[3]))
                print("DA:", float(row[4]))
                print("Bonus:", float(row[5]))
                print("Tax:", float(row[6]))
                print("PF:", float(row[7]))
                print("Net Salary : ", float(netSal[0]))
                print("------------------------")
    except Exception as e:
        print("Error : ", e)
    finally:
        print("\n\n")
        cursor.close()
        conn.close()


# def get_salary_by_employee(emp_id):
#     conn = get_connection()
#     cursor = conn.cursor()

#     query = "Select * from salary where EmployeeID =%s"
#     try:
#         cursor.execute(query, (emp_id,))
#         row = cursor.fetchone()
#         query2 = """
#             SELECT *,
#             (BasicSalary + HRA + DA + Bonus - Tax - PF) AS Net_Salary
#             FROM Salary
#             """
#         cursor.execute(query2)
#         netSal = cursor.fetchone()

#         if row:
#             print("SalaryID : ", row[0])
#             print("EmployeeID : ", row[1])
#             print("Basic Salary : ", float(row[2]))
#             print("HRA : ", float(row[3]))
#             print("DA : ", float(row[4]))
#             print("Bonus : ", float(row[5]))
#             print("Tax : ", float(row[6]))
#             print("PF:", float(row[7]))
#             print("Net Salary : ", float(netSal[0]))
#             print("------------------------")


#         else:
#             print("Salary record not found ")
#     except Exception as e:
#         print("Error : ", e)
#     finally:
#         print("\n\n")
#         cursor.close()
#         conn.close()
def get_salary_by_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT *,
        (BasicSalary + HRA + DA + Bonus - Tax - PF) AS Net_Salary
        FROM Salary
        WHERE EmployeeID = %s
    """

    try:
        cursor.execute(query, (emp_id,))
        rows = cursor.fetchall()  # ✅ fetch ALL rows

        if rows:
            for row in rows:
                print("\nSalaryID :", row[0])
                print("EmployeeID :", row[1])
                print("Basic Salary :", float(row[2]))
                print("HRA :", float(row[3]))
                print("DA :", float(row[4]))
                print("Bonus :", float(row[5]))
                print("Tax :", float(row[6]))
                print("PF :", float(row[7]))
                print("------------------------")
                print("Net Salary :", float(row[8]))  # ✅ correct index
                print("------------------------")
        else:
            print("Salary record not found")

    except Exception as e:
        print("Error :", e)

    finally:
        print("\n\n")
        cursor.close()
        conn.close()


def get_salary_report():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    Select e.employeeID, e.Name, s.BasicSalary, s.HRA,s.Bonus, s.Tax, s.PF,
    (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS Net_Salary
    From Employee e
    Join Salary s ON e.EmployeeID = s.EmployeeID
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print("Employee ID : ", row[0])
            print("Name : ", row[1])
            print("Net Salary : ", row[2])
            print("------------------------")
    except Exception as e:
        print("Error : ", e)
    finally:
        print("\n\n")
        cursor.close()
        conn.close()


def get_salary_in_range(min_salary, max_Salary):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """ 
        SELECT e.Name , 
        (s.BasicSalary + s.HRA + s.DA + s.Bonus -s.Tax - s.PF ) AS NetSalary
        From employee e 
        join Salary s ON e.employeeID = s.EmployeeID
        WHERE (s.BasicSalary + s.HRA + s.DA + s.Bonus -s.Tax - s.PF )
        BETWEEN %s AND %s
        """
        cursor.execute(query, (min_salary, max_Salary))
        rows = cursor.fetchall()
        if not rows:
            print("No Employees found in this Range ")
        else:
            for row in rows:
                print("Name : ", row[0])
                print("Net Salary : ", float(row[1]))
                print("-------------------")
    except Exception as e:
        print("Error : ", e)
    finally:
        print("\n\n")
        cursor.close()
        conn.close()


def average_salary():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    Select Avg(BasicSalary + HRA + DA + Bonus - Tax - PF)
    from salary
    """
    try:
        cursor.execute(query)
        avg = cursor.fetchone()
        print("Average Salary : ", float(avg[0]))
    except Exception as e:
        print("Error : ", e)
    finally:
        print("\n\n")
        cursor.close()
        conn.close()


def highest_paid_Employee():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    Select e.EmployeeID, e.Name,
    (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax -s.PF) AS NetSalary
    From employee e
    Join Salary s ON e.EmployeeID=s.EmployeeID
    Order By NetSalary Desc
    LIMIT 1 
    """
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            print("Highest Paid Employee : ")
            print("Employee ID : ", row[0])
            print("Name : ", row[1])
            print("Salary : ", row[2])
    except Exception as e:
        print("Error : ", e)
    finally:
        print("\n\n")
        cursor.close()
        conn.close()
