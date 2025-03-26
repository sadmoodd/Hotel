import Visitor

class Room:
    def __init__(self, num):
        self.is_free = True
        self.is_booked = False
        self.number = num
        self.has_visitor = False

    def bookRoom(self):
        if self.is_free:
            self.is_booked = True
            print(f"Room number {self.get_num()} is booked by:", self.returnVisitor())
            self.is_free = False
        else:
            print("This room is already booked")

    def addVisitor(self, visitor: "Visitor"):
        self.visitor = visitor
        self.has_visitor = True
        self.bookRoom()
    
    def returnVisitor(self) -> "Visitor": 
        if self.has_visitor:
            return self.visitor
        else:
            return print("This room has no a visitor")
    
    def get_num(self) -> int:
        return self.number

    def __str__(self):
        if self.has_visitor:
            return f"Room number {self.number}, Visitor: {str(self.returnVisitor)}"