class Course:
    def __init__(self, code, title, level):
        self.code = code
        self.title = title
        self.level = level

    def __str__(self):
        return f"{self.code}: {self.level} : {self.title}"
