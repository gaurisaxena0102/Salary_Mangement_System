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
(101,'Aarav Sharma','aarav101@gmail.com','9000000001','Permanent',3),
(102,'Riya Verma','riya102@gmail.com','9000000002','Intern',1),
(103,'Kabir Singh','kabir103@gmail.com','9000000003','Permanent',5),
(104,'Ananya Gupta','ananya104@gmail.com','9000000004','Intern',2),
(105,'Vivaan Mehta','vivaan105@gmail.com','9000000005','Permanent',4),
(106,'Diya Kapoor','diya106@gmail.com','9000000006','Intern',3),
(107,'Arjun Nair','arjun107@gmail.com','9000000007','Permanent',1),
(108,'Meera Iyer','meera108@gmail.com','9000000008','Intern',5),
(109,'Rohan Das','rohan109@gmail.com','9000000009','Permanent',2),
(110,'Sneha Joshi','sneha110@gmail.com','9000000010','Intern',4),

(111,'Rahul Jain','rahul111@gmail.com','9000000011','Permanent',5),
(112,'Neha Bansal','neha112@gmail.com','9000000012','Intern',3),
(113,'Aditya Roy','aditya113@gmail.com','9000000013','Permanent',1),
(114,'Pooja Shah','pooja114@gmail.com','9000000014','Intern',2),
(115,'Kunal Malhotra','kunal115@gmail.com','9000000015','Permanent',4),
(116,'Isha Arora','isha116@gmail.com','9000000016','Intern',5),
(117,'Siddharth Gupta','sid117@gmail.com','9000000017','Permanent',3),
(118,'Nikita Sinha','nikita118@gmail.com','9000000018','Intern',1),
(119,'Amit Tiwari','amit119@gmail.com','9000000019','Permanent',2),
(120,'Simran Kaur','simran120@gmail.com','9000000020','Intern',4),

(121,'Rohit Agarwal','rohit121@gmail.com','9000000021','Permanent',1),
(122,'Tanvi Desai','tanvi122@gmail.com','9000000022','Intern',5),
(123,'Yash Patel','yash123@gmail.com','9000000023','Permanent',3),
(124,'Kriti Sharma','kriti124@gmail.com','9000000024','Intern',2),
(125,'Manish Reddy','manish125@gmail.com','9000000025','Permanent',4),
(126,'Shreya Kulkarni','shreya126@gmail.com','9000000026','Intern',1),
(127,'Varun Chawla','varun127@gmail.com','9000000027','Permanent',5),
(128,'Aditi Mishra','aditi128@gmail.com','9000000028','Intern',3),
(129,'Harsh Vardhan','harsh129@gmail.com','9000000029','Permanent',2),
(130,'Priya Nanda','priya130@gmail.com','9000000030','Intern',4),

(131,'Dev Khanna','dev131@gmail.com','9000000031','Permanent',3),
(132,'Sanya Kapoor','sanya132@gmail.com','9000000032','Intern',1),
(133,'Arpit Saxena','arpit133@gmail.com','9000000033','Permanent',5),
(134,'Ritu Yadav','ritu134@gmail.com','9000000034','Intern',2),
(135,'Nikhil Bhatia','nikhil135@gmail.com','9000000035','Permanent',4),
(136,'Pallavi Sen','pallavi136@gmail.com','9000000036','Intern',3),
(137,'Aman Gill','aman137@gmail.com','9000000037','Permanent',1),
(138,'Tanya Mehra','tanya138@gmail.com','9000000038','Intern',5),
(139,'Deepak Chauhan','deepak139@gmail.com','9000000039','Permanent',2),
(140,'Neelam Rathi','neelam140@gmail.com','9000000040','Intern',4),

(141,'Gaurav Singh','gaurav141@gmail.com','9000000041','Permanent',5),
(142,'Komal Arora','komal142@gmail.com','9000000042','Intern',3),
(143,'Ankit Jain','ankit143@gmail.com','9000000043','Permanent',1),
(144,'Divya Goel','divya144@gmail.com','9000000044','Intern',2),
(145,'Rakesh Yadav','rakesh145@gmail.com','9000000045','Permanent',4),
(146,'Swati Mishra','swati146@gmail.com','9000000046','Intern',5),
(147,'Vikas Sharma','vikas147@gmail.com','9000000047','Permanent',3),
(148,'Neeraj Kumar','neeraj148@gmail.com','9000000048','Intern',1),
(149,'Sunil Verma','sunil149@gmail.com','9000000049','Permanent',2),
(150,'Kavita Singh','kavita150@gmail.com','9000000050','Intern',4);



INSERT INTO PERMANENT_EMPLOYEE VALUES
(101,50000,5000,2000),
(103,60000,6000,2500),
(105,55000,5500,2200),
(107,52000,4000,2000),
(109,58000,5000,2500),
(111,65000,7000,3000),
(113,60000,6000,2500),
(115,55000,5500,2200),
(117,58000,5000,2500),
(119,60000,6000,2500),

(121,70000,8000,3500),
(123,65000,7000,3000),
(125,60000,6000,2500),
(127,62000,6000,2500),
(129,58000,5000,2500),

(131,55000,5500,2200),
(133,60000,6000,2500),
(135,58000,5000,2500),
(137,62000,6000,2500),
(139,60000,6000,2500),

(141,58000,5000,2500),
(143,60000,6000,2500),
(145,55000,5500,2200),
(147,62000,6000,2500),
(149,58000,5000,2500);

INSERT INTO INTERN VALUES
(102,6),(104,6),(106,6),(108,6),(110,6),
(112,6),(114,6),(116,6),(118,6),(120,6),
(122,6),(124,6),(126,6),(128,6),(130,6),
(132,6),(134,6),(136,6),(138,6),(140,6),
(142,6),(144,6),(146,6),(148,6),(150,6);

INSERT INTO SALARY VALUES
(1,101,50000,10000,5000,5000,3000,2000),
(2,102,30000,5000,2000,1000,500,0),
(3,103,60000,12000,6000,6000,3500,2500),
(4,104,32000,6000,2500,1000,800,0),
(5,105,55000,11000,5500,5500,3200,2200),
(6,106,31000,5000,2000,1000,500,0),
(7,107,52000,10000,5000,4000,3000,2000),
(8,108,30000,5000,2000,1000,500,0),
(9,109,58000,11000,5000,5000,3000,2500),
(10,110,31000,5000,2000,1000,500,0),

(11,111,65000,13000,6000,7000,4000,3000),
(12,112,30000,5000,2000,1000,500,0),
(13,113,60000,12000,6000,6000,3500,2500),
(14,114,31000,5000,2000,1000,500,0),
(15,115,55000,11000,5500,5500,3200,2200),
(16,116,30000,5000,2000,1000,500,0),
(17,117,58000,11000,5000,5000,3000,2500),
(18,118,32000,6000,2500,1000,800,0),
(19,119,60000,12000,6000,6000,3500,2500),
(20,120,30000,5000,2000,1000,500,0),

(21,121,70000,14000,7000,8000,4500,3500),
(22,122,30000,5000,2000,1000,500,0),
(23,123,65000,13000,6000,7000,4000,3000),
(24,124,31000,5000,2000,1000,500,0),
(25,125,60000,12000,6000,6000,3500,2500),
(26,126,30000,5000,2000,1000,500,0),
(27,127,62000,12000,6000,6000,3500,2500),
(28,128,30000,5000,2000,1000,500,0),
(29,129,58000,11000,5000,5000,3000,2500),
(30,130,30000,5000,2000,1000,500,0),

(31,131,55000,11000,5500,5500,3200,2200),
(32,132,30000,5000,2000,1000,500,0),
(33,133,60000,12000,6000,6000,3500,2500),
(34,134,31000,5000,2000,1000,500,0),
(35,135,58000,11000,5000,5000,3000,2500),
(36,136,30000,5000,2000,1000,500,0),
(37,137,62000,12000,6000,6000,3500,2500),
(38,138,30000,5000,2000,1000,500,0),
(39,139,60000,12000,6000,6000,3500,2500),
(40,140,30000,5000,2000,1000,500,0),

(41,141,58000,11000,5000,5000,3000,2500),
(42,142,30000,5000,2000,1000,500,0),
(43,143,60000,12000,6000,6000,3500,2500),
(44,144,31000,5000,2000,1000,500,0),
(45,145,55000,11000,5500,5500,3200,2200),
(46,146,30000,5000,2000,1000,500,0),
(47,147,62000,12000,6000,6000,3500,2500),
(48,148,30000,5000,2000,1000,500,0),
(49,149,58000,11000,5000,5000,3000,2500),
(50,150,30000,5000,2000,1000,500,0);

--  VIEW ALL EMPLOYEES DETAILS
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

