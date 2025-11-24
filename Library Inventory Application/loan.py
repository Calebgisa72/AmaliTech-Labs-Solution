from datetime import datetime, timedelta
from data_store import books
from borrower import Borrower


class Loan:
    _charge_per_day: float = 300

    def __init__(self, book_id: int, borrower_name: str, borrower_telphone: str):
        books[book_id].mark_as_checked_out()
        self.book_id = book_id
        self.borrower = Borrower(borrower_name, borrower_telphone)
        self.loan_date = datetime.now()
        self.returned_date = None

    def __repr__(self) -> str:
        return (
            f"Loan | Book: {self.book_id} | Borrower: {self.borrower.name} "
            f"({self.borrower.telephone}) | Loaned: {self.loan_date.strftime('%Y-%m-%d %H:%M')}"
        )

    @staticmethod
    def calculate_overdue(loan_date):
        due_date = loan_date + timedelta(days=7)
        if datetime.now() > due_date:
            return datetime.now() - due_date
        return False

    def return_book(self) -> None:
        overdue = Loan.calculate_overdue(self.loan_date)

        if not overdue:
            print("Book returned on time.")
            books[self.book_id].mark_as_available()
            self.returned_date = datetime.now()
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
                break

            elif choice == "2":
                print(
                    "We kept the book, but it will be marked as returned when you pay!!"
                )
                break
