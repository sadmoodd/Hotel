import Room

class Hotel:
    # pass
    def __init__(self, name: str):
        self.name = name
        self.rooms = {}
        self.workers = []

    def get_name(self, name):
        return self.name

    def addRoom(self, room: "Room"):
        if room.has_visitor:
            self.rooms.setdefault(room, room.returnVisitor())
        else:
            self.rooms.setdefault(room, "Empty (Don't booked)")

    def get_rooms(self):
        for key, value in self.rooms.items():
            print("Room number:",key.get_num(),"; Visitor:", value)

    # TODO add methods: get_booked_rooms, get_empty_rooms

    def get_empty_rooms(self):
        print("Empty rooms ->")
        empty_rooms_found = False  # Флаг для отслеживания, найдены ли пустые комнаты
        for key, values in self.rooms.items():
            if not key.has_visitor:  # Проверка на наличие посетителя
                print("Room number:", key.get_num())
                empty_rooms_found = True
        if not empty_rooms_found:
            print("No empty rooms found.")

            
    def get_booked_rooms(self):
        print("Booked rooms ->")
        booked_room_forund = False
        for key, values in self.rooms.items():
            if values != "Empty (Don't booked)":
                print(f"Room number: {key.get_num()} ; Visitor: {key.returnVisitor()}")
                booked_room_forund = True
        if not booked_room_forund:
            print("No booked rooms found.")


    def updateRooms(self):
        for key, values in self.rooms.items():
            if values == "Empty (Don't booked)" and key.has_visitor:
                self.rooms[key] = key.returnVisitor()