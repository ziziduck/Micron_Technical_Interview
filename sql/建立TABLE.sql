-- 1. 建立新的資料庫
CREATE DATABASE Micron 
GO

-- 2. 切換到新資料庫並建立練習表
USE Micron;
GO

-- 建立 TABLE
CREATE TABLE Employees (
    Emp_ID INT PRIMARY KEY IDENTITY(1001,1),
    Name NVARCHAR(50),
    Department NVARCHAR(50),
    Salary INT
);
GO

-- 刪除 TABLE
DROP TABLE Employees;