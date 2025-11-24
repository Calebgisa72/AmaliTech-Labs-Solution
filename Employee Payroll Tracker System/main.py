from employee import FullTimeEmployee, ContractEmployee, Intern
from data_store import employees, sample_employees
from payroll import generate_payslip, generate_all_payslips, print_payslip
from utils import get_int, get_float, show_all_employee_ids


def main():
    print("\n--- Employee Payroll Tracker ---")

    while True:
        print("\nSystem Menu:")
        print("1. Start with sample employees")
        print("2. Add an employee")
        print("3. List employees")
        print("4. Generate payslip for an employee")
        print("5. Generate payslips for all employees")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            sample_employees()
            print("Sample employees added.")
            continue

        if choice == "2":
            print("\nChoose role:")
            print("1. Full-time")
            print("2. Contract")
            print("3. Intern")
            role_choice = get_int("Role option: ")

            if role_choice == 1:
                name = input("Employee name: ").strip()
                salary = get_float("Monthly salary: ")
                bonus = get_float("Bonus (0 if none): ")
                overtime_hours = get_float("Overtime hours (0 if none): ")
                overtime_rate = get_float("Overtime rate per hour (0 if none): ")
                tax_rate = get_float("Tax rate (as decimal, e.g., 0.18 for 18%): ")
                emp = FullTimeEmployee(
                    name,
                    monthly_salary=salary,
                    bonus=bonus,
                    overtime_hours=overtime_hours,
                    overtime_rate=overtime_rate,
                    tax_rate=tax_rate,
                )
                employees[emp.employee_id] = emp
                print(f"Added Full-time employee with ID {emp.employee_id}")

            elif role_choice == 2:
                name = input("Employee name: ").strip()
                hourly = get_float("Hourly rate: ")
                hours = get_float("Hours worked: ")
                tax_rate = get_float("Tax rate (decimal): ")
                emp = ContractEmployee(name, hourly_rate=hourly, hours_worked=hours, tax_rate=tax_rate)
                employees[emp.employee_id] = emp
                print(f"Added Contract employee with ID {emp.employee_id}")

            elif role_choice == 3:
                name = input("Employee name: ").strip()
                stipend = get_float("Stipend amount (0 if unpaid): ")
                emp = Intern(name, stipend=stipend)
                employees[emp.employee_id] = emp
                print(f"Added Intern with ID {emp.employee_id}")

            else:
                print("Invalid role choice.")
            continue

        if choice == "3":
            show_all_employee_ids()
            continue

        if choice == "4":
            show_all_employee_ids()
            eid = get_int("Enter employee ID: ")
            if eid not in employees:
                print("Employee not found.")
                continue
            payslip = generate_payslip(employees[eid])
            print_payslip(payslip)
            continue

        if choice == "5":
            if not employees:
                print("No employees available.")
                continue
            payslips = generate_all_payslips(employees)
            for p in payslips:
                print_payslip(p)
            continue

        if choice == "6":
            print("Goodbye!")
            break

        print("Invalid choice.")


if __name__ == "__main__":
    main()
