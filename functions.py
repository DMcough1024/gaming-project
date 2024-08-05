import mysql.connector
import json

class Ship:
    def __init__(self, name=None, points=None, faction=None, nation=None, type=None, subtype=None, year=None, speed=None, flagship=None, carrier_load=None, armament=None, armor=None, vital_armor=None, hull=None, set_name=None, set_number=None, rarity=None, class_name=None):
        self.name = name
        self.points = points
        self.faction = faction
        self.nation = nation
        self.type = type
        self.subtype = subtype
        self.year = year
        self.speed = speed
        self.flagship = flagship
        self.carrier_load = carrier_load
        self.armament = armament
        self.armor = armor
        self.vital_armor = vital_armor
        self.hull = hull
        self.set_name = set_name
        self.set_number = set_number
        self.rarity = rarity
        self.producer = "Wizards of the Coast"
        self.abilities = {}
        self.class_name = class_name

class AtkVals: 
    def __init__(self, r0=None, r1=None, r2=None, r3=None):
        self.r0 = r0
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3

    def to_dict(self):
        return {
            'r0': self.r0,
            'r1': self.r1,
            'r2': self.r2,
            'r3': self.r3
        }
    
def was_connection():
    mydb = mysql.connector.connect(
        host="98.226.164.218",
        port="33060",
        user="",
        password="",
        database=""
    )
    cursor = mydb.cursor()
    return cursor, mydb

class AtkBlock:
    def __init__(self, Gunnery1=None, Gunnery2=None, Gunnery3=None, Antiair=None, Torpedo=None, ASW=None, Bomb=None):
        self.Gunnery1 = Gunnery1 or AtkVals()
        self.Gunnery2 = Gunnery2 or AtkVals()
        self.Gunnery3 = Gunnery3 or AtkVals()
        self.Antiair = Antiair or AtkVals()
        self.Torpedo = Torpedo or AtkVals()
        self.ASW = ASW or AtkVals()
        self.Bomb = Bomb or AtkVals()

    def to_dict(self):
        return {
            'Gunnery1': self.Gunnery1.to_dict(),
            'Gunnery2': self.Gunnery2.to_dict(),
            'Gunnery3': self.Gunnery3.to_dict(),
            'Antiair': self.Antiair.to_dict(),
            'Torpedo': self.Torpedo.to_dict(),
            'ASW': self.ASW.to_dict(),
            'Bomb': self.Bomb.to_dict()
        }
    
def print_ship(ship):
    print("Name: " + ship.name)
    print("Points: " + ship.points)
    print("Faction: " + ship.faction)
    print("Nation: " + ship.nation)
    print("Type: " + ship.type)
    print("Subtype: " + ship.subtype)
    print("Year: " + str(ship.year))
    print("Speed: " + str(ship.speed))
    print("Flagship: " + str(ship.flagship))
    print("Carrier Load: " + str(ship.carrier_load))
    print("Armament:")
    print(json.dumps(ship.armament.to_dict(), indent=4))
    print("Armor: " + str(ship.armor))
    print("Vital Armor: " + str(ship.vital_armor))
    print("Hull: " + str(ship.hull))
    print("Set Name: " + ship.set_name)
    print("Set Number: " + str(ship.set_number))
    print("Rarity: " + ship.rarity)
    print("Producer: " + ship.producer)
    print("Abilities: ")
    print(json.dumps(ship.abilities, indent=4))
    return
