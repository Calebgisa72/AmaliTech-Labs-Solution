from abc import ABC, abstractmethod
from typing import Dict
from author import Author
from enum import Enum
from utils import format_time

class Genre(Enum):
    TEXTBOOK = "Textbook"
    AUDIOBOOK = "Audiobook"

class Book(ABC):
    next_id = 1

    @classmethod
    def generate_id(cls) -> int:
        bid = cls.next_id
        cls.next_id += 1
        return bid

    def __init__(self, title: str, year: int, genre: Genre, available: bool = True):
        self.book_id: int = Book.generate_id()
        self.title: str = title
        self.year: int = year
        self.available: bool = available
        self.genre: Genre = genre

    @abstractmethod
    def book_info(self) -> Dict:
        pass

    @abstractmethod   
    def update_book(self) -> None:
        pass

    def mark_as_checked_out(self) -> None:
        self.available = False

    def mark_as_available(self) -> None:
        self.available = True

    @staticmethod
    def check_availability(available):
        return "Available" if available else "Checked Out"

    def __str__(self) -> str:
        status = Book.check_availability(self.available)
        return f"{self.book_id} - {self.title} ({self.genre}) - {status}"

class Textbook(Book):
    def __init__(self, title: str, year: int, author: Author):
        super().__init__(title, year, Genre.TEXTBOOK)
        self.author = author

    def book_info(self) -> Dict:
        return {
            "book_id": self.book_id,
            "status": Book.check_availability(self.available),
            "title": self.title,
            "Genre": Genre.TEXTBOOK,
            "year_of_publication": self.year,
            "author_details": {
                "author_id": self.author.author_id,
                "name": self.author.name,
                "nationality": self.author.nationality,
            },
        }
        
    def update_book(self, **kwargs) -> None:
        editable_fields = {
            "title",
            "year",
            "author",
        }

        for field, value in kwargs.items():
            if field in editable_fields:
                setattr(self, field, value)
            else:
                print(f"Warning: '{field}' is not a valid field for Textbook and was ignored.")

class Audiobook(Book):
    def __init__(self, title: str, year: int, duration_sec: int, narrator_name: str):
        super().__init__(title, year, Genre.TEXTBOOK)
        self.duration_sec = duration_sec
        self.narrator_name = narrator_name
    
    def book_info(self) -> Dict:
        return {
            "book_id": self.book_id,
            "status": Book.check_availability(self.available),
            "title": self.title,
            "Genre": Genre.AUDIOBOOK,
            "year_of_publication": self.year,
            "duration_sec": format_time(self.duration_sec),
            "narrator_name": self.narrator_name,
        }
    
    def update_book(self, **kwargs) -> None:
        editable_fields = {
            "title",
            "year",
            "duration_sec",
            "narrator_name",
        }

        for field, value in kwargs.items():
            if field in editable_fields:
                setattr(self, field, value)
            else:
                print(f"Warning: '{field}' is not a valid field for Audiobook and was ignored.")

    
