# from db_connection import get_connection
from .db_connection import get_connection


# ADD EMPLOYEE FUNCTION FOR ADDING NEW EMPLOYEES IN THE DATABASE
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


# USED TO UPDATE THE PERMANENT EMPLOYEE TABLE AFTER ADDING THE NEW EMPLOYEE
def add_permanent_employee(emp_id, basic, bonus, pf):
    conn = get_connection()
    if conn is None:
        print("Database Connection failed ")
        return
    cursor = conn.cursor()
    query = """
    INSERT INTO permanent_employee(employeeId,BasixSalary,bonus,PF)
    VALUES(%s,%s,%s,%s)
    """
    try:
        cursor.execute(query, (emp_id, basic, bonus, pf))
        conn.commit()
        print("Permanent employee details added successfully")
    except Exception as e:
        print("Error ", e)
    finally:
        cursor.close()
        conn.close()


# USED TO UPDATE THE INTERN EMPLOYEE TABLE AFTER ADDING THE NEW EMPLOYEE


def add_intern_employee(emp_id, duration):
    conn = get_connection()
    if conn is None:
        print("Database connection failed")
        return
    cursor = conn.cursor()

    query = """
    INSERT INTO INTERN(EmployeeID, Internship_Duration)
    VALUES(%s,%s)
    """
    try:
        cursor.execute(query, (emp_id, duration))
        conn.commit()
        print("Intern Details Added successfully")
    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()


# THIS FUNCTION WILL DISPLAY THE DATA OF ALL THE EMPLOYEES FROM THE EMPLOYEE TABLE
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


# THIS FUNCTION WILL DISPLAY THE DATA OF THE EMPLOYEE WHOSE EMPLOYEE_ID WILL BE ENTERED
def get_employee_by_id(emp_id):
    conn = get_connection()
    if conn is None:
        print("Database connection failed")
        return None
    cursor = conn.cursor()
    query = "Select * from employee where EmployeeID =%s"
    try:
        cursor.execute(query, (emp_id,))
        row = cursor.fetchone()
        if row == None:
            print("Employee not found ")
        if row:

            print("------------------------")
            print("Employee ID -> ", row[0])
            print("Name -> ", row[1])
            print("Email -> ", row[2])
            print("Mobile Number -> ", row[3])
            print("Employee Type -> ", row[4])
            print("------------------------")
            print("\n")
            return row
        else:
            print("Employee not found ")
            return None
    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()


# THIS FUNCTION GIVES THE DATA OF THE EMPLOYEE WHOSE NAME WILL BE ENTERED
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
                print(f"""
                ------------------------
                EmployeeID : {row[0]}
                Name : {row[1]}
                Email : {row[2]}
                Phone : {row[3]}
                Type : {row[4]}
                Department : {row[5]}
                ------------------------
                """)
                print("\n")
    except Exception as e:
        print("Error ", e)
    finally:
        cursor.close()
        conn.close()


# THIS GIVES THE TOTAL NUMBER OF EMPLOYEES IN A SPECIFIC DEPARTMENT
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


# THIS FUNCTION DELETES THE EMPLOYEE DATA
def delete_employee(emp_id):
    conn = get_connection()
    if conn is None:
        print("Databse connection failed ")
        return
    cursor = conn.cursor()
    query = "Delete from employee where employeeID=%s"
    try:
        cursor.execute(query, (emp_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print("Employee not found")
        else:
            print("Employee and Related data deleted Successfully")

    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()


# THIS FUNCTION IS USED TO UPDATE THE EMPLOYEE'S PHONE NUMBER OR DEPARTMENT
def update_employee(emp_id):
    conn = get_connection()
    if conn is None:
        print("Connection Failed ")
        return
    cursor = conn.cursor()
    print("\nWhat do you want to update?")
    print("1 -> Phone Number")
    print("2 -> Department")
    try:
        choice = int(input("Enter choice :"))
        if choice == 1:
            new_phone = int(input("Enter new Phone Number : "))
            query = "UPDATE Empliyee set phone = %s where EmployeeID=%s"
            cursor.execute(query, (new_phone, emp_id))
        elif choice == 2:
            print("Department Id ----- Department_Name ")
            print(" 1                        HR")
            print(" 2                        IT")
            print(" 3                        Finance")
            print(" 4                        Marketing")
            print(" 5                        Production")
            new_dept = int(input("Enter new Department ID : "))
            query = "UPDATE Employee Set DepartmentID =%s Where EmployeeID=%s"
            cursor.execute(query, (new_dept, emp_id))
        else:
            print("Invalid Choice ")
            return
        conn.commit()

        if cursor.rowcount == 0:
            print("Employee not found")
        else:
            print("Employee updated successfully")

    except Exception as e:
        print(
            "Error : ",
        )
    finally:
        cursor.close()
        conn.close()


# THIS FUNCTION WILL WILL ASK FOR CONFIRMATION FROM THE USER BEFORE UPDATING THE EMPLOYEE
def confirm_and_Update_employee():
    emp_id = int(input("enter Employee ID to update : "))

    # show employee details
    employee = get_employee_by_id(emp_id)
    if not employee:
        return
    confirm = input(
        f"\nDo you want to update {employee[1]}(ID : {employee[0]})? (yes/NO) : "
    )
    if confirm.lower() != "yes":
        print("Update cancelled ")
        return
    update_employee(emp_id)


# THIS FUNCTION WILL UPDATE THE SALARY FOR A CURRENT EMPLOYEE
def update_Salary(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        print("\nEnter new Salary Details : ")

        basic = float(input("Basic : "))
        hra = float(input("HRA : "))
        da = float(input("DA : "))
        bonus = float(input("Bonus : "))
        tax = float(input("Tax : "))
        pf = float(input("PF : "))

        query = """
        UPDATE SALARY 
        set BasicSalary=%s, HRA=%s, Bonus=%s,Tax=%s,PF=%s
        where EmployeeID=%s
        """
        cursor.execute(query, (basic, hra, da, bonus, tax, pf, emp_id))
        conn.commit()
        if cursor.rowcount == 0:
            print("Salary record not found ")
        else:
            print("Salary Updated successfully")
    except Exception as e:
        print("Error : ", e)
    finally:
        cursor.close()
        conn.close()
