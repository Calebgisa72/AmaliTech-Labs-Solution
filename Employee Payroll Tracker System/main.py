import controllers as ctrl
from data_store import sample_employees


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

        elif choice == "2":
            ctrl.add_employee()

        elif choice == "3":
            ctrl.list_employees()

        elif choice == "4":
            ctrl.generate_single_payslip()

        elif choice == "5":
            ctrl.generate_every_payslip()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
