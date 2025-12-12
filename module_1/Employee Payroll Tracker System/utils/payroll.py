from typing import Dict, List
from employee import Employee

def generate_payslip(emp: Employee) -> Dict:
    """
    Generate payslip for a single employee instance by calling its calculate_pay().
    Returns the payslip dictionary returned by the employee.
    """
    return emp.calculate_pay()

def generate_all_payslips(employees: Dict[int, Employee]) -> List[Dict]:

    payslips = []
    for emp in employees.values():
        payslips.append(generate_payslip(emp))
    return payslips


def print_payslip(payslip: Dict) -> None:
    print("\n--- Payslip ---")
    print(f"ID: {payslip['employee_id']}  Name: {payslip['name']}  Role: {payslip['role']}")
    print(f"Gross Pay: {payslip['gross_pay']:.2f}")
    print(f"Taxes: {payslip['taxes']:.2f}")
    print(f"Net Pay: {payslip['net_pay']:.2f}")
    print("Details:")
    for k, v in payslip["details"].items():
        print(f"  - {k}: {v}")
    print("----------------")

