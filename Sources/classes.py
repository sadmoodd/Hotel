class RoomType:
    pass


class Equipment:
    pass


class Worker:
    # def __init__(self):
    pass
        
import Room as r, Visitor as v, Hotel as h



r1 = r.Room(1)
v1 = v.Visitor("Name", "Surname")

r1.addVisitor(v1)
#print(r1.returnVisitor())

r1.get_num()
    
r2 = r.Room(2)


hotel = h.Hotel("Hotel 1")
hotel.addRoom(r1)
hotel.addRoom(r2)


print()

v2 = v.Visitor("Ivan", "Ivanov")

r2.addVisitor(v2)
hotel.updateRooms()
# hotel.get_rooms()
print()

print()
r3 = r.Room(3)
hotel.addRoom(r3)
v3 = v.Visitor("Petr", "Petrov")
r3.addVisitor(v3)
hotel.updateRooms()
print()
hotel.get_rooms()

# hotel.get_rooms()

hotel.get_empty_rooms()
hotel.get_booked_rooms()