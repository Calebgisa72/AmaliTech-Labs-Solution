from datetime import datetime, timedelta
from typing import Optional

from services.data_store import books
from .borrower import Borrower


class Loan:
    next_id: int = 1
    _charge_per_day: float = 300.0

    loan_id: int
    book_id: int
    borrower: Borrower
    loan_date: datetime
    returned_date: Optional[datetime]
    status: str

    @classmethod
    def generate_id(cls) -> int:
        lid = cls.next_id
        cls.next_id += 1
        return lid

    def __init__(self, book_id: int, borrower_name: str, borrower_telephone: str):
        books[book_id].mark_as_checked_out()

        self.loan_id = Loan.generate_id()
        self.book_id = book_id
        self.borrower = Borrower(borrower_name, borrower_telephone)
        self.loan_date = datetime.now()
        self.returned_date = None
        self.status = "active"

    def __repr__(self) -> str:
        returned = (
            self.returned_date.strftime("%Y-%m-%d %H:%M")
            if self.returned_date is not None
            else "N/A"
        )
        return (
            f"Loan {self.loan_id} | Book: {self.book_id} | Borrower: {self.borrower.name} "
            f"({self.borrower.telephone}) | Loaned: {self.loan_date.strftime('%Y-%m-%d %H:%M')} "
            f"| Returned: {returned} | Status: {self.status}"
        )

    @staticmethod
    def calculate_overdue(loan_date: datetime) -> Optional[timedelta]:
        due_date = loan_date + timedelta(days=7)
        if datetime.now() > due_date:
            return datetime.now() - due_date
        return None

    def return_book(self) -> None:
        if self.status != "active":
            print("This loan has already been returned.")
            return

        overdue = Loan.calculate_overdue(self.loan_date)

        if overdue is None:
            print("Book returned on time.")
            books[self.book_id].mark_as_available()
            self.returned_date = datetime.now()
            self.status = "returned"
            return

        days_overdue: int = overdue.days
        charge: float = days_overdue * Loan._charge_per_day

        print(f"Overdue: {days_overdue} days | Charge: {charge} FRW")

        while True:
            print("\n1. Charge Paid")
            print("2. Charge Not Paid")
            choice = input("Select: ")

            if choice == "1":
                print("Charge settled. Book returned.")
                books[self.book_id].mark_as_available()
                self.returned_date = datetime.now()
                self.status = "returned"
                break

            if choice == "2":
                print("Book kept until charge is paid. Status remains active.")
                break

    def to_dict(self) -> dict:
        return {
            "loan_id": self.loan_id,
            "book_id": self.book_id,
            "borrower": self.borrower.to_dict(),
            "loan_date": self.loan_date.isoformat(),
            "returned_date": (
                self.returned_date.isoformat() if self.returned_date else None
            ),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Loan":
        obj = cls.__new__(cls)

        obj.loan_id = int(d["loan_id"])
        obj.book_id = int(d["book_id"])
        obj.borrower = Borrower.from_dict(d["borrower"])
        obj.loan_date = datetime.fromisoformat(d["loan_date"])
        obj.returned_date = (
            datetime.fromisoformat(d["returned_date"])
            if d.get("returned_date")
            else None
        )
        obj.status = d.get("status", "active")

        return obj
