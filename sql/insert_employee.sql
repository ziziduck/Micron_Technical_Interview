-- sql/insert_employee.sql
INSERT INTO Employees (Name, Department, Salary) 
VALUES (:name, :dept, :salary);