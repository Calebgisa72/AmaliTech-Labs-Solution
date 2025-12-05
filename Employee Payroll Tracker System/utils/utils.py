from typing import Dict
from data_store import employees

def get_int(prompt: str):
    """
    Gets an integer input.
    - User has 2 tries
    - User can type 'q' to quit early (returns None)
    """
    tries = 2
    while tries > 0:
        value = input(prompt).strip()

        if value.lower() == "q":
            print("Returning to menu...")
            return None

        try:
            return int(value)
        except ValueError:
            tries -= 1
            print(f"Invalid integer! You have {tries} tries left.")

    print("Too many failed attempts. Returning to menu...")
    return None


def get_float(prompt: str):
    tries = 2
    while tries > 0:
        value = input(prompt).strip()

        if value.lower() == "q":
            print("Returning to menu...")
            return None

        try:
            return float(value)
        except ValueError:
            tries -= 1
            print(f"Invalid number! You have {tries} tries left.")

    print("Too many failed attempts. Returning to menu...")
    return None


def show_all_employee_ids():
    print("\nAvailable Employees:")
    if not employees:
        print("  (none)")
        return
    for emp in employees.values():
        print(emp)
