from datetime import datetime, timedelta
from services.data_store import books
from .borrower import Borrower


class Loan:
    next_id = 1
    _charge_per_day: float = 300

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
            if self.returned_date
            else "N/A"
        )
        return (
            f"Loan {self.loan_id} | Book: {self.book_id} | Borrower: {self.borrower.name} "
            f"({self.borrower.telephone}) | Loaned: {self.loan_date.strftime('%Y-%m-%d %H:%M')} | Returned: {returned} | Status: {self.status}"
        )

    @staticmethod
    def calculate_overdue(loan_date):
        due_date = loan_date + timedelta(days=7)
        if datetime.now() > due_date:
            return datetime.now() - due_date
        return False

    def return_book(self) -> None:
        if self.status != "active":
            print("This loan has already been returned.")
            return

        overdue = Loan.calculate_overdue(self.loan_date)

        if not overdue:
            print("Book returned on time.")
            books[self.book_id].mark_as_available()
            self.returned_date = datetime.now()
            self.status = "returned"
            return

        days_overdue = overdue.days
        charge = days_overdue * Loan._charge_per_day

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

            elif choice == "2":
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
        # don't mark book checked out again
        obj = cls.__new__(cls)
        obj.loan_id = int(d.get("loan_id", 0))
        obj.book_id = int(d.get("book_id", 0))
        obj.borrower = Borrower.from_dict(d.get("borrower", {}))
        loan_date_str = d.get("loan_date", None)
        if loan_date_str:
            obj.loan_date = datetime.fromisoformat(loan_date_str)
        else:
            obj.loan_date = datetime.now()
        returned = d.get("returned_date")
        obj.returned_date = datetime.fromisoformat(returned) if returned else None
        obj.status = d.get("status", "active")
        return obj
