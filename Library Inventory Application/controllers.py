from services.data_store import books, authors, loans
from models.book import Textbook, Audiobook
from models.author import Author
from models.loan import Loan
from utils import get_int, get_non_empty_string
import services.storage as storage


def list_all_books(withDetails: bool = False):
    if not books:
        print("\nNo books found.")
        return
    print("\n=== All Books ===")
    for b in books.values():
        if withDetails:
            info = b.book_info()
            for k, v in info.items():
                print(f"{k.capitalize()}: {v}")
            print("-------------------")
        else:
            print(b)


def list_all_authors():
    if not authors:
        print("\nNo authors found.")
        return
    print("\n=== All Authors ===")
    for a in authors.values():
        print(a)


def list_all_loans():
    if not loans:
        print("\nNo loans found.")
        return

    print("\nShow loans:")
    print("1. Active loans only")
    print("2. All loans")

    choice = input("Choose (1/2): ").strip()

    if choice == "1":
        items = [l for l in loans.values() if l.status == "active"]
    else:
        items = list(loans.values())

    if not items:
        print("No loans match the selection.")
        return

    print("\n=== Loans ===")
    for l in items:
        print(l)


def search_books():
    print("\n=== Search Books ===")
    term = input("Enter title or part of title: ").lower()

    results = [b for b in books.values() if term in b.title.lower()]

    if not results:
        print("No matching books found.")
        return

    print("\nSearch Results:")
    for r in results:
        print(r)


def add_author():
    print("\n=== Add Author ===")
    name = get_non_empty_string("Enter author name: ")
    nationality = get_non_empty_string("Enter nationality: ")

    a = Author(name, nationality)
    authors[a.author_id] = a
    storage.save_authors()
    print(f"Author added successfully with ID {a.author_id}")


def add_book():
    print("\n=== Add Book ===")
    print("1. Textbook")
    print("2. Audiobook")

    choice = get_int("Choose book type: ")
    if choice is None:
        return  # ← important

    title = get_non_empty_string("Enter title: ")
    year = get_int("Enter year of publication: ")
    if year is None:
        return

    if choice == 1:
        if not authors:
            print("No authors available. Add an author first!")
            return

        list_all_authors()
        a_id = get_int("\nEnter author ID: ")
        if a_id is None:
            return

        if a_id not in authors:
            print("Invalid author ID.")
            return

        book = Textbook(title, year, authors[a_id])

    elif choice == 2:
        duration = get_int("Enter duration in seconds: ")
        if duration is None:
            return
        narrator = get_non_empty_string("Enter narrator name: ")
        book = Audiobook(title, year, duration, narrator)

    else:
        print("Invalid choice.")
        return

    books[book.book_id] = book
    storage.save_books()
    print(f"Book added successfully with ID {book.book_id}")


def loan_book():
    print("\n=== Loan Book ===")
    list_all_books()
    b_id = get_int("\nEnter book ID to loan: ")
    if b_id is None:
        return

    if b_id not in books:
        print("Invalid book ID.")
        return

    if not books[b_id].available:
        print("Book is already loaned out.")
        return

    borrower_name = get_non_empty_string("Enter borrower's name: ")
    borrower_tel = get_non_empty_string("Enter borrower's telephone: ")

    ln = Loan(b_id, borrower_name, borrower_tel)
    loans[ln.loan_id] = ln
    storage.save_loans()
    storage.save_books()
    print(f"Book loaned successfully. Loan ID: {ln.loan_id}")


def return_book():
    print("\n=== Return Book ===")
    if not loans:
        print("No loans available.")
        return

    list_all_loans()

    b_id = get_int("\nEnter book ID to return: ")
    if b_id is None:
        return

    found = None
    for l in loans.values():
        if l.book_id == b_id and l.status == "active":
            found = l
            break

    if not found:
        print("No active loan found for this book.")
        return

    found.return_book()
    storage.save_loans()
    storage.save_books()
    print("Book returned successfully.")


def delete_book():
    print("\n=== Delete Book ===")
    list_all_books()
    b_id = get_int("\nEnter book ID to delete: ")
    if b_id is None:
        return

    if b_id not in books:
        print("Invalid book ID.")
        return

    if not books[b_id].available:
        print("Cannot delete a book that is loaned out!")
        return

    del books[b_id]
    storage.save_books()
    print("Book deleted successfully.")


def edit_book():
    print("\n=== Edit Book ===")
    list_all_books()
    b_id = get_int("\nEnter book ID to edit: ")
    if b_id is None:
        return

    if b_id not in books:
        print("Invalid book ID.")
        return

    book = books[b_id]

    print("\nLeave a field blank to keep current value.\n")

    new_title = input(f"New title (current: {book.title}): ").strip()
    new_year_str = input(f"New year (current: {book.year}): ").strip()

    updates = {}

    if new_title:
        updates["title"] = new_title
    if new_year_str.isdigit():
        updates["year"] = int(new_year_str)

    from models.book import Textbook, Audiobook

    if isinstance(book, Textbook):
        list_all_authors()
        new_author_str = input(
            f"Enter new author ID (current: {book.author.author_id}): "
        ).strip()
        if new_author_str.isdigit():
            author_id = int(new_author_str)
            if author_id in authors:
                updates["author"] = authors[author_id]
            else:
                print("Invalid author ID. Author unchanged.")

    elif isinstance(book, Audiobook):
        new_duration = input(
            f"Enter new duration (sec) (current: {book.duration_sec}): "
        ).strip()
        new_narrator = input(
            f"Enter new narrator (current: {book.narrator_name}): "
        ).strip()

        if new_duration.isdigit():
            updates["duration_sec"] = int(new_duration)
        if new_narrator:
            updates["narrator_name"] = new_narrator

    if updates:
        book.update_book(**updates)
        storage.save_books()
        print("Book updated successfully.")
    else:
        print("No changes applied.")
