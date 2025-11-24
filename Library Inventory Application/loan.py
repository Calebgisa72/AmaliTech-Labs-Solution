from datetime import datetime, timedelta
from data_store import books


class Loan:
    _charge_per_day: float = 300

    def __init__(self, book_id: int, borrower_id: int):
        self.book_id = book_id
        self.borrower_id = borrower_id
        self.loan_date = datetime.now()

    def __repr__(self) -> str:
        return f"Book ID: {self.book_id} | Borrower ID: {self.borrower_id} | Loan Date: {self.loan_date.strftime('%Y-%m-%d %H:%M:%S')}"

    def return_book(self) -> None:
        overdue = Loan.calculate_overdue(self.loan_date)
        if not overdue:
            print("Book returned on time. No overdue charges.")
            books[self.book_id].mark_as_available()
            self.returned_date = datetime.now()
        else:
            days_overdue: int = overdue.days
            charge: float = days_overdue * Loan._charge_per_day
            print(
                f"The book is overdue by {days_overdue} days. Overdue charge: {charge} FRW."
            )
            while True:
                print("\nChoose Option:")
                print("1. Borrower paid the charge")
                print("2. Not paid yet")
                choice = input("Enter your choice (1 or 2): ")
                if choice == "1":
                    print("Charge paid. Book returned successfully.")
                    books[self.book_id].mark_as_available()
                    self.returned_date = datetime.now()
                    break
                if choice == "2":
                    print(
                        "We kept the book, but it will be marked as returned when you pay!!."
                    )
                    break

    @staticmethod
    def calculate_overdue(loan_date):
        if datetime.now() > loan_date + timedelta(days=7):
            return datetime.now() - loan_date + timedelta(days=7)
        return False
