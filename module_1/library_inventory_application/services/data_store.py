from typing import TYPE_CHECKING, Dict
from models.book import Book
from models.author import Author

if TYPE_CHECKING:
    from models.loan import Loan

books: Dict[int, Book] = {}
authors: Dict[int, Author] = {}
loans: Dict[int, "Loan"] = {}
