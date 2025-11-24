from data_store import books, authors, loans
from book import Textbook, Audiobook
from author import Author
from loan import Loan
from utils import get_int


def list_all_books(withDetails: bool = False):
    if not books:
        print("\nNo books found.")
        return
    print("\n=== All Books ===")
    for b in books.values():
        if withDetails:
            print(f"\n{b.book_info()}")
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
    print("\n=== All Loans ===")
    for l in loans.values():
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
    name = input("Enter author name: ")
    nationality = input("Enter nationality: ")

    a = Author(name, nationality)
    authors[a.author_id] = a
    print(f"Author added successfully with ID {a.author_id}")


def add_book():
    print("\n=== Add Book ===")
    print("1. Textbook")
    print("2. Audiobook")

    choice = input("Choose book type: ")

    title = input("Enter title: ")
    year = get_int("Enter year of publication: ")

    if choice == "1":
        if not authors:
            print("No authors available. Add an author first!")
            return

        list_all_authors()
        a_id = get_int("\nEnter author ID: ")

        if a_id not in authors:
            print("Invalid author ID.")
            return

        book = Textbook(title, year, authors[a_id])

    elif choice == "2":
        duration = get_int("Enter duration in seconds: ")
        narrator = input("Enter narrator name: ")
        book = Audiobook(title, year, duration, narrator)

    else:
        print("Invalid choice.")
        return

    books[book.book_id] = book
    print(f"Book added successfully with ID {book.book_id}")


def loan_book():
    print("\n=== Loan Book ===")
    list_all_books()
    b_id = get_int("\nEnter book ID to loan: ")

    if b_id not in books:
        print("Invalid book ID.")
        return

    if not books[b_id].available:
        print("Book is already loaned out.")
        return

    borrower_name = input("Enter borrower's name: ")
    borrower_tel = input("Enter borrower's telephone: ")

    ln = Loan(b_id, borrower_name, borrower_tel)
    loans[b_id] = ln

    print("Book loaned successfully.")


def return_book():
    print("\n=== Return Book ===")
    if not loans:
        print("No active loans.")
        return

    list_all_loans()
    b_id = get_int("\nEnter book ID to return: ")

    if b_id not in loans:
        print("No loan found for this book.")
        return

    loans[b_id].return_book()
    # del loans[b_id]


def delete_book():
    print("\n=== Delete Book ===")
    list_all_books()
    b_id = get_int("\nEnter book ID to delete: ")

    if b_id not in books:
        print("Invalid book ID.")
        return

    if not books[b_id].available:
        print("Cannot delete a book that is loaned out!")
        return

    del books[b_id]
    print("Book deleted successfully.")


def edit_book():
    print("\n=== Edit Book ===")
    list_all_books()
    b_id = get_int("\nEnter book ID to edit: ")

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
                print("Invalid author ID. Author not changed.")

    elif isinstance(book, Audiobook):
        print("\nThis is an Audiobook.")
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
        print("Book updated successfully.")
    else:
        print("No changes applied.")


def main():
    print("---WELCOME TO LIBRARY INVENTORY---")
    while True:
        print("\n1. Add Book")
        print("2. Add Author")
        print("3. Loan a Book")
        print("4. Return a Book")
        print("5. Search Books")
        print("6. List All Books")
        print("7. List All Authors")
        print("8. List All Loans")
        print("9. Delete Book")
        print("10. Edit Book")
        print("11. Start with sample books and authors")
        print("12. Exit")
        print("========================================")

        choice = input("Enter choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            add_author()
        elif choice == "3":
            loan_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            search_books()
        elif choice == "6":
            list_all_books(withDetails=True)
        elif choice == "7":
            list_all_authors()
        elif choice == "8":
            list_all_loans()
        elif choice == "9":
            delete_book()
        elif choice == "10":
            edit_book()
        elif choice == "11":
            from data_store import sample_books

            sample_books()
            print("Sample authors and books added.")
        elif choice == "12":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
