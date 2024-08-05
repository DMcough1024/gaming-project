import mysql.connector 
import json
import os
from functions import Ship, AtkBlock, AtkVals, print_ship, was_connection
   
allignment = {
    "United States": "Allies",
    "United Kingdom": "Allies",
    "Soviet Union": "Allies",
    "China": "Allies",
    "France": "Allies",
    "Australia": "Allies",
    "Canada": "Allies",
    "Greece": "Allies",
    "Poland": "Allies",
    "India": "Allies",
    "New Zealand": "Allies",
    "Netherlands": "Allies",
    "South Africa": "Allies",
    "Germany": "Axis",
    "Italy": "Axis",
    "Japan": "Axis",
    "Hungary": "Axis",
    "Romania": "Axis",
    "Bulgaria": "Axis",
    "Finland": "Axis",
    "Neutral": "Neutral",
}

atk_types = ["Gunnery1", "Gunnery2", "Gunnery3", "Antiair", "ASW", "Torpedo", "Bomb"]

def collect_values(cursor):
    e = None
    try:
        ship = Ship()
        ship.name = input("Name: ")
        ship.nation = input("Nation: ")
        if ship.nation == "us":
            ship.nation = "United States"
        elif ship.nation == "uk":
            ship.nation = "United Kingdom"
        elif ship.nation == "su":
            ship.nation = "Soviet Union"
        elif ship.nation == "ge":
            ship.nation = "Germany"
        elif ship.nation == "it":
            ship.nation = "Italy"
        elif ship.nation == "jp":
            ship.nation = "Japan"
        elif ship.nation == "fr":
            ship.nation = "France"
        elif ship.nation == "au":
            ship.nation = "Australia"
        ship.faction = allignment.get(ship.nation)
        if ship.faction is None:
            ship.faction = input("Alignment: ")
            allignment[ship.nation] = ship.faction
        ship.type = input("Type: ")
        if ship.type == '':
            ship.type = "Ship"
        ship.subtype = input("Subtype: ")
        ship.year = input("Year: ")
        ship.speed = input("Speed: ")
        if ship.speed == '':
            ship.speed = 2
        ship.flagship = input("Flagship: ")
        if ship.flagship == '':
            ship.flagship = 0
        ship.carrier_load = input("Carrier Load: ")
        if ship.carrier_load == '':
            ship.carrier_load = 0
        ship.points = input("Points: ")
        ship.armament = AtkBlock()
        for weapon in atk_types:
            chk = input("Does this ship have " + weapon + "? (a): ")
            if chk == 'a':
                atk = AtkVals()
                atk.r0 = input("Range 0: ")
                atk.r1 = input("Range 1: ")
                atk.r2 = input("Range 2: ")
                atk.r3 = input("Range 3: ")
                setattr(ship.armament, weapon, atk)
        ship.armor = input("Armor: ")
        ship.vital_armor = input("Vital Armor: ")
        ship.hull = input("Hull: ")
        add_ability = "a" 
        while add_ability == "a":
            ability_name = input("Ability: ")
            ability_text = check_ability(cursor, ability_name)
            if ability_text == "Cancel":
                continue
            ship.abilities[ability_name] = ability_text
            add_ability = input("Add another ability? (a): ")
        ship.set_name = input("Set Letter: ")
        ship.set_number = input("Set Number: ")
        if ship.set_name == "A" or ship.set_name == "1":
            id = 700 + int(ship.set_number)
            ship.set_name = "A"
        elif ship.set_name == "B" or ship.set_name == "2":
            id = 800 + int(ship.set_number)
            ship.set_name = "B"
        elif ship.set_name == "C" or ship.set_name == "3":
            id = 900 + int(ship.set_number)
            ship.set_name = "C"
        elif ship.set_name == "D" or ship.set_name == "4":
            id = 1000 + int(ship.set_number)
            ship.set_name = "D"
        elif ship.set_name == "E" or ship.set_name == "5":
            id = 1100 + int(ship.set_number)
            ship.set_name = "E"
        elif ship.set_name == "F" or ship.set_name == "6":
            id = 1200 + int(ship.set_number)
            ship.set_name = "F"
        elif ship.set_name == "G" or ship.set_name == "7":
            id = 1300 + int(ship.set_number)
            ship.set_name = "G"
        elif ship.set_name == "H" or ship.set_name == "8":
            id = 1400 + int(ship.set_number)
            ship.set_name = "H"
        else:
            id = 9999
        ship.set_name = "Forumini " + str(ship.set_name)
        ship.rarity = "Base"
        ship.producer = "Forumini"
        ship.class_name = check_class(cursor, ship)
    except Exception as e:
        print(e)
    return ship, id, e

def check_ability(cursor, ability):
    # check if ability is already in db 
    sql = "SELECT text FROM abilities WHERE name = %s"
    val = (ability,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result is not None:
        text = result[0]
    else:
        add_ability = input("Add ability to database? (a): ")
        if add_ability == "a":
            text = input("Ability Text: ")
            sql = "INSERT INTO abilities (name, text) VALUES (%s, %s)"
            val = (ability, text)
            cursor.execute(sql, val)
        else:
            text = "Cancel"
    return text

def check_class(cursor, ship):
    class_name = input("Class Name: ")
    sql = "SELECT * FROM classes WHERE name = %s AND nation = %s"
    val = (class_name,ship.nation,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result is not None:
        return class_name
    else:
        class_type = ship.type
        class_subtype = ship.subtype
        class_modifiers = input("Type of " + ship.subtype + ": ")
        class_nation = ship.nation
        class_year = ship.year
        class_subtype = class_modifiers + " " + class_subtype
        sql = "INSERT INTO classes (name, type, subtype, nation, year) VALUES (%s, %s, %s, %s, %s)"
        val = (class_name, class_type, class_subtype, class_nation, class_year,)
        cursor.execute(sql, val)
        return class_name
    
def edit_ship(ship):
    edit_flag = 'a'
    while edit_flag == 'a':
        atr = input("Attribute to update: ")
        if atr == "armament":
            for weapon in atk_types:
                chk = input("Does this ship have " + weapon + "? (a): ")
                if chk == 'a':
                    atk = AtkVals()
                    atk.r0 = input("Range 0: ")
                    atk.r1 = input("Range 1: ")
                    atk.r2 = input("Range 2: ")
                    atk.r3 = input("Range 3: ")
                    setattr(ship.armament, weapon, atk)
        elif atr == "abilities":
            add_ability = "a" 
            while add_ability == "a":
                ability_name = input("Ability: ")
                ability_text = check_ability(cursor, ability_name)
                if ability_text == "Cancel":
                    continue
                ship.abilities[ability_name] = ability_text
                add_ability = input("Add another ability? (a): ")
        else:
            val = input("New value: ")
            setattr(ship, atr, val)
        print_ship(ship)
        edit_flag = input("Edit another attribute? (a): ")
    return ship

def add_ship(cursor, ship, id):
    try:
        e = None
        owned = 1
        sql = "INSERT INTO cards (id, Name, Points, Faction, Nation, type, subtype, Speed, Flagship, Carrier_Load, Armament, Armor, Vital_Armor, Hull, Set_Name, Set_Num, Rarity, producer, Ability_id, owned_count, class) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id, ship.name, ship.points, ship.faction, ship.nation, ship.type, ship.subtype, ship.speed, ship.flagship, ship.carrier_load, json.dumps(ship.armament.to_dict()), ship.armor, ship.vital_armor, ship.hull, ship.set_name, ship.set_number, ship.rarity, ship.producer, json.dumps(ship.abilities), owned, ship.class_name)
        cursor.execute(sql, val)
        print("Inserted " + str(id) + " " + ship.name)
    except mysql.connector.Error as e:
        if e.errno == 1062:
            print("Duplicate entry: " + str(id))
            id = input("Enter new ID: ")
            add_ship(cursor, ship, id)
    except Exception as e:        
        print(e)
    return

cursor, was = was_connection()
add_another = "a"
while add_another != "n":
    e = None
    ship, id, e = collect_values(cursor)
    if e is not None:
        add_another = input("Add another ship? (n to cancel): ")
        continue
    print_ship(ship)
    com_ship = input("Add ship to database? (a): ")
    if com_ship == "a":
        add_ship(cursor, ship, id)
        was.commit()
    else: 
        edit_flag = input("Edit ship? (a): ")
        while edit_flag == "a":
            ship = edit_ship(ship)
            print_ship(ship)
            com_ship = input("Add ship to database? (a): ")
            if com_ship == "a":
                add_ship(cursor, ship, id)
                was.commit()
                break
            else:
                print("Cancelled")
    
    add_another = input("Add another ship? (n to cancel): ")
    os.system('cls')
