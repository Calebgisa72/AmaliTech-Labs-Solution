from typing import TYPE_CHECKING, Dict
from book import Book
from author import Author

if TYPE_CHECKING:
    from loan import Loan

books: Dict[int, Book] = {}
authors: Dict[int, Author] = {}
loans: Dict[int, "Loan"] = {}

def sample_books():
    books.clear()
    authors.clear()

    author1 = Author("Brian J. Jarrett.", "American")
    authors[author1.author_id] = author1

    from book import Textbook, Audiobook

    tb = Textbook("Into the Badlands", 2018, author1)
    books[tb.book_id] = tb

    ab = Audiobook("The Subtle Art of Not Giving", 2016, 34200, "Roger Wayne")
    books[ab.book_id] = ab
