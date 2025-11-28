class Author:
    _next_id = 1

    @classmethod
    def generate_id(cls) -> int:
        aid = cls._next_id
        cls._next_id += 1
        return aid

    def __init__(self, name: str, nationality: str) -> None:
        self.author_id = Author.generate_id()
        self.name = name
        self.nationality = nationality

    def __repr__(self) -> str:
        return f"{self.author_id} - {self.name} - {self.nationality}"

    def to_dict(self) -> dict:
        return {
            "author_id": self.author_id,
            "name": self.name,
            "nationality": self.nationality,
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'Author':
        # create instance without advancing id again
        obj = cls.__new__(cls)
        obj.author_id = int(d["author_id"])
        obj.name = d["name"]
        obj.nationality = d.get("nationality", "")
        return obj