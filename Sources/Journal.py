import Hotel
import sqlite3

class Journal:
    def __init__(self):
        self.hotels = sqlite3.connect('hotels.db')
        self.conn = self.hotels.cursor()

    def addHotel(self, hotel: "Hotel"):
        self.hotels.append(hotel)

    def rmHotel(self, name: str):
        pass
