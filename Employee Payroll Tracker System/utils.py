from typing import Dict
from data_store import employees
from employee import Employee

def get_int(prompt: str, error: str = "Please enter a valid integer!") -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(error)


def get_float(prompt: str, error: str = "Please enter a valid number!") -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(error)


def show_all_employee_ids():
    print("\nAvailable Employees:")
    if not employees:
        print("  (none)")
        return
    for emp in employees.values():
        print(emp)
