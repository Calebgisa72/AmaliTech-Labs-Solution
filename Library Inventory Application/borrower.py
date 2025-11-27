class Borrower:
    _next_id = 1

    @classmethod
    def generate_id(cls) -> int:
        bid = cls._next_id
        cls._next_id += 1
        return bid
    
    def __init__ (self, name: str, telephone: str):
        self.borrower_id = Borrower.generate_id()
        self.name = name
        self.telephone = telephone
    
    def __repr__(self) -> str:
        return f"{self.borrower_id} - {self.name} - {self.telephone}"