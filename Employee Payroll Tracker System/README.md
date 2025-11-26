# Employee Payroll Tracker System

This project is a command-line **Employee Payroll Tracker System** built using Python and Object-Oriented Programming (OOP).  
It demonstrates principles such as **inheritance, abstraction, polymorphism, encapsulation, and modular application design**.

The system allows an administrator to:

- Add different types of employees  
- Generate payslips for individual employees  
- Generate payslips for all employees  
- List all registered employees  
- Use preloaded sample employees for quick testing  

Employee types supported:

- **Full-Time Employee**
- **Contract Employee**
- **Intern**

---

## Project Structure

### 1. Employee Management

The system supports three employee categories, each with customized pay calculations:

#### **FullTimeEmployee**
- Monthly salary  
- Bonus  
- Overtime hours & rate  
- Tax rate  
- Net pay calculation = *(salary + bonus + overtime) – tax*

#### **ContractEmployee**
- Hourly rate  
- Hours worked  
- Tax rate  
- Net pay calculation = *(hours × rate) – tax*

#### **Intern**
- Fixed stipend  
- Zero tax  
- Net pay = stipend

All employees automatically receive a unique employee ID.

---

### 2. Payroll System

Payroll processing includes:

- Generating a payslip for a single employee  
- Generating payslips for all employees  
- Printing payslip details cleanly in the console  

A payslip contains:
- Employee ID  
- Name  
- Role  
- Gross pay  
- Taxes  
- Net pay  
- Additional breakdown (salary, hours worked, bonus, etc.)

---

### 3. Example Features

- Start with sample employees  
-  Add new full-time, contract, or intern workers  
-  Validate numeric inputs  
-  View a list of all employees  
-  Generate detailed payslips  

---

## Setup Instructions

### **Requirements**
- Python **3.10+**
- Terminal / Command Prompt

---

## Running the Project

### **1. Clone the Repository**
```bash
git clone https://github.com/Calebgisa72/AmaliTech-Labs-Solution
cd "Employee Payroll Tracker System"
python main.py
```