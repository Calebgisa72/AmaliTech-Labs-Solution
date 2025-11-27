class Author():
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