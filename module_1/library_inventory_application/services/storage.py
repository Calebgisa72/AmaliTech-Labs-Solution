import json
import os
from typing import List, Dict, Any

from services.data_store import books, authors, loans
from models.author import Author
from models.book import Textbook, Audiobook, Book
from models.loan import Loan

DATA_DIR: str = os.path.join(os.getcwd(), "data")
BOOKS_FILE: str = os.path.join(DATA_DIR, "books.json")
AUTHORS_FILE: str = os.path.join(DATA_DIR, "authors.json")
LOANS_FILE: str = os.path.join(DATA_DIR, "loans.json")


def ensure_data_dir() -> None:
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


# ---------- Save functions ----------


def save_books() -> None:
    ensure_data_dir()
    book_list: List[Dict[str, Any]] = [b.to_dict() for b in books.values()]
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(book_list, f, indent=2, ensure_ascii=False)


def save_authors() -> None:
    ensure_data_dir()
    author_list: List[Dict[str, Any]] = [a.to_dict() for a in authors.values()]
    with open(AUTHORS_FILE, "w", encoding="utf-8") as f:
        json.dump(author_list, f, indent=2, ensure_ascii=False)


def save_loans() -> None:
    ensure_data_dir()
    loan_list: List[Dict[str, Any]] = [loan.to_dict() for loan in loans.values()]
    with open(LOANS_FILE, "w", encoding="utf-8") as f:
        json.dump(loan_list, f, indent=2, ensure_ascii=False)


# ---------- Load functions ----------


def load_authors() -> None:
    ensure_data_dir()
    if not os.path.exists(AUTHORS_FILE):
        return

    with open(AUTHORS_FILE, "r", encoding="utf-8") as f:
        raw: List[Dict[str, Any]] = json.load(f)

    authors.clear()
    max_id: int = 0

    for entry in raw:
        author = Author.from_dict(entry)
        authors[author.author_id] = author
        max_id = max(max_id, author.author_id)

    Author.next_id = max(Author.next_id, max_id + 1)


def load_books() -> None:
    ensure_data_dir()
    if not os.path.exists(BOOKS_FILE):
        return

    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        raw: List[Dict[str, Any]] = json.load(f)

    books.clear()
    max_id: int = 0

    for entry in raw:
        book: Book | None = None

        if entry.get("genre") == "Textbook":
            author = authors.get(entry.get("author_id"))
            if author is None:
                continue
            book = Textbook.from_dict(entry, author)

        elif entry.get("genre") == "Audiobook":
            book = Audiobook.from_dict(entry)

        if book is None:
            continue

        books[book.book_id] = book
        max_id = max(max_id, book.book_id)

    Book.next_id = max(Book.next_id, max_id + 1)


def load_loans() -> None:
    ensure_data_dir()
    if not os.path.exists(LOANS_FILE):
        return

    with open(LOANS_FILE, "r", encoding="utf-8") as f:
        raw: List[Dict[str, Any]] = json.load(f)

    loans.clear()
    max_id: int = 0

    for entry in raw:
        loan = Loan.from_dict(entry)
        loans[loan.loan_id] = loan
        max_id = max(max_id, loan.loan_id)

    Loan.next_id = max(Loan.next_id, max_id + 1)


def load_all() -> None:
    load_authors()
    load_books()
    load_loans()
