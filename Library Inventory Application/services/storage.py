import json
import os
from typing import List, Dict, Any

from services.data_store import books, authors, loans
from models.author import Author
from models.book import Textbook, Audiobook
from models.loan import Loan

DATA_DIR = os.path.join(os.getcwd(), "data")
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")
AUTHORS_FILE = os.path.join(DATA_DIR, "authors.json")
LOANS_FILE = os.path.join(DATA_DIR, "loans.json")


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# Save functions
def save_books():
    ensure_data_dir()
    book_list: List[Dict[str, Any]] = []
    for b in books.values():
        book_list.append(b.to_dict())
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(book_list, f, indent=2, ensure_ascii=False)


def save_authors():
    ensure_data_dir()
    author_list: List[Dict[str, Any]] = []
    for a in authors.values():
        author_list.append(a.to_dict())
    with open(AUTHORS_FILE, "w", encoding="utf-8") as f:
        json.dump(author_list, f, indent=2, ensure_ascii=False)


def save_loans():
    ensure_data_dir()
    loan_list: List[Dict[str, Any]] = []
    for l in loans.values():
        loan_list.append(l.to_dict())
    with open(LOANS_FILE, "w", encoding="utf-8") as f:
        json.dump(loan_list, f, indent=2, ensure_ascii=False)


# Load functions
def load_authors():
    ensure_data_dir()
    if not os.path.exists(AUTHORS_FILE):
        return
    with open(AUTHORS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    authors.clear()
    max_id = 0
    for entry in raw:
        a = Author.from_dict(entry)
        authors[a.author_id] = a
        if a.author_id > max_id:
            max_id = a.author_id
    # ensure next id
    Author.next_id = max_id + 1 if max_id >= Author.next_id else Author.next_id


def load_books():
    ensure_data_dir()
    if not os.path.exists(BOOKS_FILE):
        return
    # authors must be loaded already
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    books.clear()
    max_id = 0
    for entry in raw:
        b = None
        if entry.get("genre") == "Textbook":
            author_id = entry.get("author_id")
            author = authors.get(author_id)
            if author is None:
                continue
            b = Textbook.from_dict(entry, author)

        elif entry.get("genre") == "Audiobook":
            b = Audiobook.from_dict(entry)
        else:
            continue

        books[b.book_id] = b
        if b.book_id > max_id:
            max_id = b.book_id
    # set book next id
    from models.book import Book as BookClass
    BookClass.next_id = max_id + 1 if max_id >= BookClass.next_id else BookClass.next_id


def load_loans():
    ensure_data_dir()
    if not os.path.exists(LOANS_FILE):
        return
    with open(LOANS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    loans.clear()
    max_id = 0
    for entry in raw:
        l = Loan.from_dict(entry)
        loans[l.loan_id] = l
        if l.loan_id > max_id:
            max_id = l.loan_id
    # set loan next id
    from models.loan import Loan as LoanClass
    LoanClass.next_id = max_id + 1 if max_id >= LoanClass.next_id else LoanClass.next_id


def load_all():
    """
    Load authors, then books, then loans (authors required by books).
    """
    load_authors()
    load_books()
    load_loans()
