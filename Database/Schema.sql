create database Salary_Management;
use Salary_Management;

-- DEPARTMENT TABLE
CREATE TABLE DEPARTMENT (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(20) NOT NULL
);

-- EMPLOYEE TABLE
CREATE TABLE EMPLOYEE (
    EmployeeID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    EmpType VARCHAR(20) CHECK (EmpType IN ('Permanent', 'Intern')),
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES DEPARTMENT(DepartmentID)
);

-- PERMANENT EMPLOYEE TABLE
CREATE TABLE PERMANENT_EMPLOYEE (
    EmployeeID INT PRIMARY KEY,
    BasicSalary DECIMAL(10,2) CHECK (BasicSalary >= 0),
    Bonus DECIMAL(10,2) CHECK (Bonus >= 0),
    PF DECIMAL(10,2) CHECK (PF >= 0),
    FOREIGN KEY (EmployeeID)
    REFERENCES EMPLOYEE(EmployeeID)
    ON DELETE CASCADE
);

-- INTERN TABLE
CREATE TABLE INTERN (
    EmployeeID INT PRIMARY KEY,
    Internship_Duration INT CHECK (Internship_Duration > 0),
    FOREIGN KEY (EmployeeID)
    REFERENCES EMPLOYEE(EmployeeID)
    ON DELETE CASCADE
);

-- SALARY TABLE
CREATE TABLE SALARY (
    SalaryID INT PRIMARY KEY,
    EmployeeID INT UNIQUE,
    BasicSalary DECIMAL(10,2) CHECK (BasicSalary >= 0),
    HRA DECIMAL(10,2) CHECK (HRA >= 0),
    DA DECIMAL(10,2) CHECK (DA >= 0),
    Bonus DECIMAL(10,2) CHECK (Bonus >= 0),
    Tax DECIMAL(10,2) CHECK (Tax >= 0),
    PF DECIMAL(10,2) CHECK (PF >= 0),
    FOREIGN KEY (EmployeeID)
    REFERENCES EMPLOYEE(EmployeeID)
    ON DELETE CASCADE
);

-- ENTERING DATA

INSERT INTO DEPARTMENT VALUES
(1, 'HR'),
(2, 'IT'),
(3, 'Finance'),
(4, 'Marketing'),
(5, 'Production');

INSERT INTO EMPLOYEE VALUES
(101, 'Rahul Sharma', 'rahul@gmail.com', '9876543210', 'Permanent', 2),
(102, 'Anita Verma', 'anita@gmail.com', '9876543211', 'Intern', 1),
(103, 'Karan Mehta', 'karan@gmail.com', '9876543212', 'Permanent', 3),
(104, 'Sneha Singh', 'sneha@gmail.com', '9876543213', 'Intern', 4),
(105, 'Amit Patel', 'amit@gmail.com', '9876543214', 'Permanent', 2);

INSERT INTO PERMANENT_EMPLOYEE VALUES
(101, 50000, 5000, 2000),
(103, 60000, 6000, 2500),
(105, 55000, 5500, 2200);

INSERT INTO INTERN VALUES
(102, 6),
(104, 3);

INSERT INTO SALARY VALUES
(1, 101, 50000, 10000, 5000, 5000, 3000, 2000),
(2, 102, 15000, 2000, 1000, 0, 500, 0),
(3, 103, 60000, 12000, 6000, 6000, 3500, 2500),
(4, 104, 12000, 1500, 800, 0, 400, 0),
(5, 105, 55000, 11000, 5500, 5500, 3200, 2200);

-- ALL EMPLOYEES DETAILS
SELECT e.EmployeeID, e.Name, e.EmpType, d.DepartmentName,
       s.BasicSalary, s.HRA, s.DA
FROM EMPLOYEE e
LEFT JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
LEFT JOIN SALARY s ON e.EmployeeID = s.EmployeeID;

-- VIEW PERMANENT EMPLOYEES
SELECT e.EmployeeID, e.Name, p.BasicSalary, p.Bonus, p.PF, e.EmpType
FROM EMPLOYEE e
JOIN PERMANENT_EMPLOYEE p ON e.EmployeeID = p.EmployeeID;

-- VIEW INTERNS
SELECT e.EmployeeID, e.Name, i.Internship_Duration, e.Emptype
FROM EMPLOYEE e
JOIN INTERN i ON e.EmployeeID = i.EmployeeID; 

-- CALCULATE NET SALARY REPORT
SELECT e.EmployeeID, e.Name, s.BasicSalary, s.HRA, s.DA, s.Bonus, s.Tax, s.PF,
		(s.basicSalary + s.HRA + s.DA + s.Bonus - s.tax - s.pf) AS NET_SALARY 
FROM Salary s
LEFT JOIN Employee e on s.employeeID=e.EmployeeID;

-- CALCULATE ONLY NET SALARY
SELECT e.EmployeeID, e.Name,
       (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS NetSalary
FROM EMPLOYEE e
JOIN SALARY s ON e.EmployeeID = s.EmployeeID;

-- HIGHEST PAID EMPLOYEE
SELECT e.EmployeeID, e.Name,
       (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS NetSalary
FROM EMPLOYEE e
JOIN SALARY s ON e.EmployeeID = s.EmployeeID
ORDER BY NetSalary DESC
LIMIT 1;

-- DEPARTMENT WISE TOTAL SALARY EXPENSES
SELECT d.DepartmentName,
       SUM(s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS TotalExpense
FROM EMPLOYEE e
JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
JOIN SALARY s ON e.EmployeeID = s.EmployeeID
GROUP BY d.DepartmentName;

-- EMPLOYEE IN A SPECIFIC DEPARTMENT
SELECT e.EmployeeID, e.Name, d.DepartmentName
FROM EMPLOYEE e
JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
WHERE d.DepartmentName = 'IT';

-- TOTAL PERMANENT AND INTERN EMPLOYEES
SELECT EmpType, COUNT(*) AS Total
FROM EMPLOYEE
GROUP BY EmpType;

-- INTERNS WITH DURATION GREATER THAN 3 MONTHS
SELECT e.Name, i.Internship_Duration
FROM EMPLOYEE e
JOIN INTERN i ON e.EmployeeID = i.EmployeeID
WHERE i.Internship_Duration > 3;

-- DEPARTMENT WISE SALARY REPORT
SELECT d.DepartmentName,
       SUM(s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS TotalSalary,
      ROUND( AVG(s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF)) AS AvgSalary
FROM EMPLOYEE e
JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
JOIN SALARY s ON e.EmployeeID = s.EmployeeID
GROUP BY d.DepartmentName;

-- HIGHEST PAID EMPLOYEE IN EACH DEPARTMENT
SELECT d.DepartmentName, e.EmployeeID, e.Name,
       (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF) AS Net_Salary
FROM EMPLOYEE e
JOIN DEPARTMENT d ON e.DepartmentID = d.DepartmentID
JOIN SALARY s ON e.EmployeeID = s.EmployeeID
WHERE (e.DepartmentID, 
       (s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF)) IN (
       
    SELECT e.DepartmentID,
           MAX(s.BasicSalary + s.HRA + s.DA + s.Bonus - s.Tax - s.PF)
    FROM EMPLOYEE e
    JOIN SALARY s ON e.EmployeeID = s.EmployeeID
    GROUP BY e.DepartmentID
);

