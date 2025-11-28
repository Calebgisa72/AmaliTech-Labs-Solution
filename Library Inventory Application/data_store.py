from typing import TYPE_CHECKING, Dict
from book import Book
from author import Author

if TYPE_CHECKING:
    from loan import Loan

books: Dict[int, Book] = {}
authors: Dict[int, Author] = {}
loans: Dict[int, "Loan"] = {}