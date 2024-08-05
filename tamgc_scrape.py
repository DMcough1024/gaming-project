import requests
import re
import json
from bs4 import BeautifulSoup
from functions import AtkVals, AtkBlock, Ship, was_connection, print_ship

# Database columns to fill out

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

img_names = ["Gunnery1", "Gunnery2", "Gunnery3", "Antiair", "Torpedo", "ASW", "Bomb"]

def get_info(id): 
    URL = "http://was.tamgc.net/unit.php?ID=" + str(id)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    ship = Ship("", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")

    # Set basic tables
    content = soup.find("div", id="content")
    header_table = content.find("table")
    attack_table = header_table.find_next("table")
    armor_table = attack_table.find_next("table")
    adj_table = armor_table.find_next("table")

    # Scrape header table
    ship.name = header_table.find("td", class_="inv").get_text()
    ship.nation = header_table.find("td", class_="alt3").find("img").get("alt")
    ship.faction = allignment.get(ship.nation)
    if ship.faction is None:
        ship.faction = "Blank"
    class_var = "small " + ship.faction
    class_row = header_table.find("td", class_=class_var)
    ship.year = class_row.find("span", class_="right").get_text()
    full_type = class_row.find("span", class_="left").get_text()
    if '-' in full_type:
        full_type = full_type.split("-")
        ship.type = full_type[0]
        ship.subtype = full_type[1]
    else: 
        ship.type = full_type
        ship.subtype = ""
    class_var = "points " + ship.faction
    ship.points = header_table.find("td", class_=class_var).get_text()
    ship.speed = header_table.find(string=re.compile(r'Speed - ')).split(" - ")[1]
    flag = header_table.find("img", alt="Flagship")
    if flag is None:
        ship.flagship = 0
    else:
        ship.flagship = flag.parent.get_text().strip()
    carrier = header_table.find_all("img", alt="Carrier")
    ship.carrier_load = len(carrier)

    # Scrape attack table
    weapon_block = AtkBlock()
    for weapon in img_names:
        attack_row = attack_table.find("img", src=re.compile(weapon))
        if attack_row is None:
            continue
        else: 
            attack_row = attack_row.find_parent("tr")
            attack_row = attack_row.find_all("td")
            if attack_row[1].get_text() == '-': 
                r0 = None
            else: 
                r0 = attack_row[1].get_text()
            if attack_row[2].get_text() == '-': 
                r1 = None
            else:
                r1 = attack_row[2].get_text()
            if attack_row[3].get_text() == '-':
                r2 = None
            else:
                r2 = attack_row[3].get_text()
            if attack_row[4].get_text() == '-':
                r3 = None
            else:
                r3 = attack_row[4].get_text()
            Atk_Vals = AtkVals(r0, r1, r2, r3)
            setattr(weapon_block, weapon, Atk_Vals)
    ship.armament = weapon_block

    # Scrape armor table
    ship.armor = armor_table.find(string=" Armor ").find_next("td").get_text()
    ship.vital_armor = armor_table.find(string=" Vital Armor ").find_next("td").get_text()
    ship.hull = armor_table.find(string=" Hull Points ").find_next("td").get_text()

    # Scrape adj table
    table_data = adj_table.find_all("td")
    set_info = table_data[-1].get_text().split("-")
    ship.set_name = set_info[0].strip()
    set_num = set_info[1].strip()
    ship.set_number = set_num.split("/")[0]
    ship.rarity = set_info[2].strip()
    
    # find the next alt2 small

    ability_title = adj_table.find_all("td", class_="alt2 small")
    ability_text = adj_table.find_all("td", class_="alt3 ability")
    for i in range(len(ability_title)):
        ship.abilities[ability_title[i].get_text()[:-2]] = ability_text[i].get_text()

    return ship

def loop_data(cursor):
    i = 401
    while i < 410:
        e = None
        add_ship = True
        try:
            ship = get_info(i)
        except Exception as e:
            print(e)
            add_ship = False

        if add_ship:
            f = insert_ship(cursor, ship, i)
            if f is not None:
                if str(f).startswith("1062 (23000): Duplicate"):
                    print("Duplicate entry for " + str(i))
                else:
                    print(f)
                    print(i)
                    break
            else:
                print("Inserted " + str(i) + " " + ship.name)

        i += 1
    return

def insert_ship(cursor, ship, id):
    try:
        sql = "INSERT INTO cards (id, Name, Points, Faction, Nation, type, subtype, Speed, Flagship, Carrier_Load, Armament, Armor, Vital_Armor, Hull, Set_Name, Set_Num, Rarity, producer, Ability_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id, ship.name, ship.points, ship.faction, ship.nation, ship.type, ship.subtype, ship.speed, ship.flagship, ship.carrier_load, json.dumps(ship.armament.to_dict()), ship.armor, ship.vital_armor, ship.hull, ship.set_name, ship.set_number, ship.rarity, ship.producer, json.dumps(ship.abilities))
        cursor.execute(sql, val)
    except Exception as e:
        return e
    return None

# Start Main
cursor, mydb = was_connection()

loop_data(cursor)

mydb.commit()
cursor.close()
mydb.close()
