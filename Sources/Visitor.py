class Visitor:
    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname

    def get_name(self) -> str:
        return self.name 
    
    def get_surname(self) -> str: 
        return self.surname 
    
    def set_name(self, name: str):
        self.name = name

    def set_surname(self, surname: str):
        self.surname = surname

    def __str__(self):
        return f"Name: {self.name}, Surname: {self.surname}"