from abc import ABC, abstractmethod
from typing import Any, Dict
from .author import Author
from enum import Enum
from utils import format_time
from datetime import datetime


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
        self.genre: Genre = genre
        self.available: bool = available
        self.__year: int = datetime.now().year
        self.year = year

    @property
    def year(self) -> int:
        """Getter for the private year variable."""
        return self.__year

    @year.setter
    def year(self, value: int) -> None:
        """Setter that ensures the year is not a future year."""
        current_year = datetime.now().year

        if value > current_year:
            raise ValueError(f"Year cannot be in the future ({value}).")
        if value < 0:
            raise ValueError("Year cannot be negative.")

        self.__year = value

    @abstractmethod
    def book_info(self) -> Dict:
        pass

    @abstractmethod
    def update_book(self) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
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
        return f"{self.book_id} - {self.title} ({self.genre.value}) - {status}"

    def base_dict(self) -> Dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "year": self.year,
            "genre": self.genre.value,
            "available": bool(self.available),
        }


class Textbook(Book):
    def __init__(self, title: str, year: int, author: Author):
        super().__init__(title, year, Genre.TEXTBOOK)
        self.author = author

    def book_info(self) -> Dict:
        return {
            "book_id": self.book_id,
            "status": Book.check_availability(self.available),
            "title": self.title,
            "genre": Genre.TEXTBOOK.value,
            "year_of_publication": self.year,
            "author_details": {
                "author_id": self.author.author_id,
                "name": self.author.name,
                "nationality": self.author.nationality,
            },
        }

    def update_book(self, **kwargs) -> None:
        editable_fields = {"title", "year", "author"}

        for field, value in kwargs.items():
            if field in editable_fields:
                if field == "year":
                    self.year = value
                else:
                    setattr(self, field, value)
            else:
                print(f"Warning: '{field}' is not valid for Textbook.")

    def to_dict(self) -> Dict:
        base = self.base_dict()
        base.update({"author_id": self.author.author_id})
        return base

    @classmethod
    def from_dict(cls, d: Dict, author: Author):
        obj = cls.__new__(cls)
        obj.book_id = int(d["book_id"])
        obj.title = d["title"]
        obj.genre = Genre.TEXTBOOK
        obj.available = bool(d.get("available", True))

        obj.__year = datetime.now().year
        obj.year = int(d["year"])

        obj.author = author
        return obj


class Audiobook(Book):
    def __init__(self, title: str, year: int, duration_sec: int, narrator_name: str):
        super().__init__(title, year, Genre.AUDIOBOOK)
        self.duration_sec = duration_sec
        self.narrator_name = narrator_name

    def book_info(self) -> Dict:
        return {
            "book_id": self.book_id,
            "status": Book.check_availability(self.available),
            "title": self.title,
            "genre": Genre.AUDIOBOOK.value,
            "year_of_publication": self.year,
            "duration": format_time(self.duration_sec),
            "narrator_name": self.narrator_name,
        }

    def update_book(self, **kwargs) -> None:
        editable_fields = {"title", "year", "duration_sec", "narrator_name"}

        for field, value in kwargs.items():
            if field in editable_fields:
                if field == "year":
                    self.year = value
                else:
                    setattr(self, field, value)
            else:
                print(f"Warning: '{field}' is not valid for Audiobook.")

    def to_dict(self) -> Dict:
        base = self.base_dict()
        base.update(
            {
                "duration_sec": int(self.duration_sec),
                "narrator_name": self.narrator_name,
            }
        )
        return base

    @classmethod
    def from_dict(cls, d: Dict):
        obj = cls.__new__(cls)
        obj.book_id = int(d["book_id"])
        obj.title = d["title"]
        obj.genre = Genre.AUDIOBOOK
        obj.available = bool(d.get("available", True))

        obj.__year = datetime.now().year
        obj.year = int(d["year"])

        obj.duration_sec = int(d.get("duration_sec", 0))
        obj.narrator_name = d.get("narrator_name", "")
        return obj
