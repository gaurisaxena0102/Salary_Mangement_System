from Backend_Modules import department as dept
from Backend_Modules import employee as emp
from Backend_Modules import Salary as sal


def main_menu():
    while True:
        print("SALARY MANAGEMENT SYSTEM ")
        print("1 -> Employee Operationns ")
        print("2 -> Department Operations ")
        print("3 -> Salary Operations ")
        print("4 -> Exit ")

        choice = int(input("Enter your choice :"))
        match choice:
            case 1:
                employee_menu()
            case 2:
                department_menu()
            case 3:
                salary_menu()
            case 4:
                print("Exiting system...")
                break
            case _:
                print("Invalid choice ")


def employee_menu():
    print("\n---Employee Menu---")
    print("1 -> Add Employee")
    print("2 -> View All Employees")
    print("3 -> Search Employee by ID ")
    print("4 -> Search Employee by Name ")
    print("5 -> Count Employees in the Department ")
    print("6 -> Update Employee Details ")
    print("7 -> Update Employee Salary")
    print("8 -> Delete Employee ")
    print("9 -> Back ")
    choice = int(input("Enter Choice : "))
    print("\n")
    match choice:
        case 1:
            emp_id = int(input("Enter Employee ID : "))
            name = input("Enter Name : ")
            email = input("Enter Email : ")
            phone = int(input("Enter phone number : "))
            emp_type = input("Enter Employee Type : ")
            dept_id = int(input("Enter Department ID : "))

            emp.Add_employee(emp_id, name, email, phone, emp_type, dept_id)

            if emp_type.lower() == "permanent":
                basic = float(input("Enter Basic Salary : "))
                bonus = float(input("Enter Bonus : "))
                pf = float(input("Enter PF : "))

                emp.add_permanent_employee(emp_id, basic, bonus, pf)
            elif emp_type.lower() == "intern":
                duration = int(input("Enter Internship Duration(months): "))
                emp.add_intern_employee(emp_id, duration)
            else:
                print("Invalid Employee Type ")
        case 2:
            emp.get_Employees()
        case 3:
            emp_id = int(input("Enter Employee ID: "))
            emp.get_employee_by_id(emp_id)
        case 4:
            name = input("Enter Employee Name : ")
            emp.search_employee_by_name(name)
        case 5:
            print("Department Id ----- Department_Name ")
            print(" 1                        HR")
            print(" 2                        IT")
            print(" 3                        Finance")
            print(" 4                        Marketing")
            print(" 5                        Production")
            dept_ID = int(input("Enter Department ID : "))
            emp.count_employees(dept_ID)
        case 6:
            emp.confirm_and_Update_employee()
        case 7:
            empID = int(input("Enter Employee ID : "))
            emp.update_Salary(empID)
        case 8:
            id = int(input("Enter Employee ID to delete "))
            employee = emp.get_employee_by_id(emp_id)
            if employee:
                confirm = input(f"Delete {employee[1]} (ID: {employee[0]})? (y/n): ")

                if confirm.lower() == "yes":
                    emp.delete_employee(emp_id)
                else:
                    print("Deletion cancelled ")
            else:
                print("Employee not found ")

        case 9:
            print("Going back...")
            return
        case _:
            print("Invalid Choice ")


def department_menu():
    print("\n--- DEPARTMENT MENU ---")
    print("1 -> Add Department ")
    print("2 -> View  All Departments ")
    print("3 -> Search Department by Department ID ")
    print("4 -> Show total Number of Departments ")
    print("5 -> Show Department Employee : ")
    print("6 -> Back ")
    choice = int(input("Enter Choice : "))
    print("\n")

    match choice:
        case 1:
            dept_id = int(input("Enter Department ID : "))
            dept_name = input("Enter Department Name : ")
            dept.add_department(dept_id, dept_name)
            print("\n)")
        case 2:
            dept.get_departments()
            print("\n")
        case 3:
            dept_id = int(input("Enter department ID : "))
            dept.get_department_by_id(dept_id)
        case 4:
            dept.count_departments()
        case 5:
            print("Department Id ----- Department_Name ")
            print(" 1                        HR")
            print(" 2                        IT")
            print(" 3                        Finance")
            print(" 4                        Marketing")
            print(" 5                        Production")
            dept_ID = int(input("Enter Department ID : "))
            dept.show_department_employees(dept_ID)
        case 6:
            print("Going back...")
            return
        case _:
            print("Invalid Choice")


def salary_menu():
    print("\n--- SALARY MENU ---")
    print("1 -> View Salaries ")
    print("2 -> Salary Report")
    print("3 -> Highest Paid Employee")
    print("4 -> Individual Salary Report")
    print("5 -> Add Salary of New Employee ")
    print("6 -> Back")

    choice = int(input("Enter  your Choice : "))

    match choice:
        case 1:
            sal.get_all_Salaries()
        case 2:
            sal.get_salary_report()
        case 3:
            sal.highest_paid_Employee()
        case 4:
            print("\n\n")
            empID = int(input("Enter Employee ID : "))
            sal.get_salary_by_employee(empID)
        case 5:
            salID = int(input("Enter  New Salary ID : "))
            EmpID = int(input("Enter Employee ID : "))
            Basic = int(input("Enter Employee's Basic Salary : "))
            HRA = int(input("Enter HRA : "))
            DA = int(input("Enter DA : "))
            Bonus = int(input("Enter Bonus : "))
            Tax = int(input("Enter Tax "))
            PF = int(input("Enter PF : "))
            sal.add_salary(salID, EmpID, Basic, HRA, DA, Bonus, Tax, PF)
        case 6:
            print("Going back...")
            return
        case _:
            print("Invalid Choice")


main_menu()
