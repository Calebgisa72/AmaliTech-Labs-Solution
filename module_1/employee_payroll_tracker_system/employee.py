from abc import ABC, abstractmethod


class Employee(ABC):

    _next_id = 1

    @classmethod
    def generate_id(cls) -> int:
        eid = cls._next_id
        cls._next_id += 1
        return eid

    def __init__(self, name: str, role: str):
        self.employee_id: int = Employee.generate_id()
        self.name: str = name
        self.role: str = role

    @abstractmethod
    def calculate_pay(self) -> dict:
        """
        Return a dictionary with computed payslip values.
        Subclasses must override this.
        Example return keys: gross_pay, taxes, net_pay, details
        """
        pass

    def __str__(self) -> str:
        return f"{self.employee_id} - {self.name} ({self.role})"


class FullTimeEmployee(Employee):
    """
    overview:    Represents a full-time employee with salary, bonus, overtime, and tax details.
    attributes:
    """

    def __init__(
        self,
        name: str,
        monthly_salary: float,
        bonus: float = 0.0,
        overtime_hours: float = 0.0,
        overtime_rate: float = 0.0,
        tax_rate: float = 0.15,
    ):
        super().__init__(name, "Full-time")
        self.monthly_salary = float(monthly_salary)
        self._bonus = 0.0
        self._tax_rate = 0.0

        self.bonus = bonus
        self.overtime_hours = float(overtime_hours)
        self.overtime_rate = float(overtime_rate)
        self.tax_rate = tax_rate

    @property
    def bonus(self) -> float:
        return self._bonus

    @bonus.setter  # Validates the bonus to be non-negative
    def bonus(self, value: float):
        if value < 0:
            raise ValueError("Bonus cannot be negative.")
        self._bonus = float(value)

    @property
    def tax_rate(self) -> float:
        return self._tax_rate

    @tax_rate.setter
    def tax_rate(self, value: float) -> None:
        if not (0.0 <= float(value) <= 1.0):
            raise ValueError("Tax rate must be between 0.0 and 1.0 (Ex: 0.15 for 15%).")
        self._tax_rate = float(value)

    def calculate_pay(self) -> dict:
        """
        Compute gross pay = salary + bonus + overtime
        taxes = gross_pay * tax_rate
        net_pay = gross - taxes
        Returns a payslip dictionary.
        """
        overtime_pay = self.overtime_hours * self.overtime_rate
        gross = self.monthly_salary + self.bonus + overtime_pay

        taxes = round(gross * self.tax_rate, 2)
        net = round(gross - taxes, 2)

        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "role": self.role,
            "gross_pay": round(gross, 2),
            "taxes": taxes,
            "net_pay": net,
            "details": {
                "monthly_salary": round(self.monthly_salary, 2),
                "bonus": round(self.bonus, 2),
                "overtime_hours": round(self.overtime_hours, 2),
                "overtime_rate": round(self.overtime_rate, 2),
            },
        }


class ContractEmployee(Employee):
    """
    Contract staff:
    - hourly_rate
    - hours_worked
    - tax_rate
    """

    def __init__(
        self,
        name: str,
        hourly_rate: float,
        hours_worked: float = 0.0,
        tax_rate: float = 0.10,
    ):
        super().__init__(name, "Contract")
        self.hourly_rate = float(hourly_rate)
        self.hours_worked = float(hours_worked)
        self._tax_rate = 0.0
        self.tax_rate = tax_rate

    @property
    def tax_rate(self) -> float:
        return self._tax_rate

    @tax_rate.setter
    def tax_rate(self, value: float):
        if not (0.0 <= float(value) <= 1.0):
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        self._tax_rate = float(value)

    def calculate_pay(self) -> dict:
        gross = round(self.hourly_rate * self.hours_worked, 2)
        taxes = round(gross * self.tax_rate, 2)
        net = round(gross - taxes, 2)
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "role": self.role,
            "gross_pay": gross,
            "taxes": taxes,
            "net_pay": net,
            "details": {
                "hourly_rate": round(self.hourly_rate, 2),
                "hours_worked": round(self.hours_worked, 2),
            },
        }


class Intern(Employee):
    """
    Intern: fixed stipend or unpaid (stipend default 0)
    Typically no taxes or very small tax (we'll keep taxes 0 by default).
    """

    def __init__(self, name: str, stipend: float = 0.0):
        super().__init__(name, "Intern")
        self.stipend = float(stipend)

    def calculate_pay(self) -> dict:
        gross = round(self.stipend, 2)
        taxes = 0.0
        net = gross
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "role": self.role,
            "gross_pay": gross,
            "taxes": taxes,
            "net_pay": net,
            "details": {"stipend": gross},
        }
