from employee import FullTimeEmployee, ContractEmployee, Intern
from data_store import employees, sample_employees
from utils.utils import get_int, get_float, show_all_employee_ids
from utils.payroll import generate_payslip, generate_all_payslips, print_payslip


def choose_role():
    while True:
        print("\nChoose role:")
        print("1. Full-time")
        print("2. Contract")
        print("3. Intern")

        role = get_int("Role option (or 'q' to quit): ")

        if role is None:
            return None

        if role in (1, 2, 3):
            return role

        print("Invalid choice.")


def add_employee():
    role = choose_role()
    if role is None:
        return

    name = input("Employee name (or 'q' to quit): ").strip()
    if name.lower() == "q":
        print("Returning to menu...")
        return

    if role == 1:  # Full-time
        salary = get_float("Monthly salary: ")
        if salary is None:
            return

        bonus = get_float("Bonus (0 if none): ")
        if bonus is None:
            return

        overtime_hours = get_float("Overtime hours: ")
        if overtime_hours is None:
            return

        overtime_rate = get_float("Overtime rate: ")
        if overtime_rate is None:
            return

        tax_rate = get_float("Tax rate (decimal): ")
        if tax_rate is None:
            return

        emp = FullTimeEmployee(
            name,
            monthly_salary=salary,
            bonus=bonus,
            overtime_hours=overtime_hours,
            overtime_rate=overtime_rate,
            tax_rate=tax_rate,
        )

    elif role == 2:  # Contract
        hourly = get_float("Hourly rate: ")
        if hourly is None:
            return

        hours = get_float("Hours worked: ")
        if hours is None:
            return

        tax_rate = get_float("Tax rate (decimal): ")
        if tax_rate is None:
            return

        emp = ContractEmployee(
            name, hourly_rate=hourly, hours_worked=hours, tax_rate=tax_rate
        )

    else:  # Intern
        stipend = get_float("Stipend amount (0 if unpaid): ")
        if stipend is None:
            return

        emp = Intern(name, stipend=stipend)

    employees[emp.employee_id] = emp
    print(f"Employee added successfully with ID {emp.employee_id}")


def list_employees():
    show_all_employee_ids()


def generate_single_payslip():
    show_all_employee_ids()
    eid = get_int("Enter employee ID: ")

    if eid is None:
        return

    if eid not in employees:
        print("Employee not found.")
        return

    payslip = generate_payslip(employees[eid])
    print_payslip(payslip)


def generate_every_payslip():
    if not employees:
        print("No employees available.")
        return

    payslips = generate_all_payslips(employees)

    for p in payslips:
        print_payslip(p)
