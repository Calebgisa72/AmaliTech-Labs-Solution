from typing import Dict
from employee import Employee, FullTimeEmployee, ContractEmployee, Intern

employees: Dict[int, Employee] = {}

# Function that generate sample employees
def sample_employees():
    employees.clear() # First clear the employee dictionary

    ft = FullTimeEmployee("Caleb Gisa", monthly_salary=3000.0, bonus=200.0, overtime_hours=10, overtime_rate=15.0, tax_rate=0.18)
    employees[ft.employee_id] = ft

    ct = ContractEmployee("Mugisha Pacifique", hourly_rate=25.0, hours_worked=120, tax_rate=0.10)
    employees[ct.employee_id] = ct

    it = Intern("Mico Benjamin", stipend=300.0)
    employees[it.employee_id] = it