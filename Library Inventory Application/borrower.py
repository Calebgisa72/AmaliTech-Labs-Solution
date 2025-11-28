class Borrower:
    _next_id = 1

    @classmethod
    def generate_id(cls) -> int:
        bid = cls._next_id
        cls._next_id += 1
        return bid

    def __init__(self, name: str, telephone: str):
        self.borrower_id = Borrower.generate_id()
        self.name = name
        self.telephone = telephone

    def __repr__(self) -> str:
        return f"{self.borrower_id} - {self.name} - {self.telephone}"

    def to_dict(self) -> dict:
        return {
            "borrower_id": self.borrower_id,
            "name": self.name,
            "telephone": self.telephone,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Borrower":
        obj = cls.__new__(cls)
        obj.borrower_id = int(d.get("borrower_id", 0))
        obj.name = d.get("name", "")
        obj.telephone = d.get("telephone", "")
        return obj
