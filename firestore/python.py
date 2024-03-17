import json
import ciso8601
from datetime import datetime

location_data = []
relatives_data = []

genders = {
    "M": 1,
    "H": 1,
    "F": 2,
    "NB": 3,
}

relations = {
    "family": 1,
    "friend": 2,
    "neighbor": 3,
    "other": 4,
}

roles = {
    "police": 1,
    "vecino": 2,
    "neighbor": 2,
}

# Lee el archivo JSON
with open('users_test.json', 'r', encoding="utf-8") as archivo:
    data = json.load(archivo)

# Recorre cada mapa en la lista y agrega la clave "municipality_id" con el valor "1"
for item in data:
    birth_date = item["birthday"]
    birth_date_split = birth_date.split('-')
    if len(birth_date_split[0]) == 2:
        birth_date = '-'.join(birth_date_split[::-1])
    item["birthdate"] = str(ciso8601.parse_datetime(birth_date).isoformat())

    if "location_data" in item:
        item["location_data"].pop("speed_accuracy")
        item["location_data"].pop("floor")
        item["location_data"].pop("timestamp")
        item["location_data"]["user_id"] = item["id"]
        location_data.append(item["location_data"])
        item.pop("location_data")

    item["gender_id"] = genders[item["gender"].upper()]
    item["role_id"] = roles[item["role"].lower()]

    if "back_dni_url" in item:
        item["back_dni"] = item["back_dni_url"]
        item.pop("back_dni_url")
    if "front_dni_url" in item:
        item["front_dni"] = item["front_dni_url"]
        item.pop("front_dni_url")

    item["dni"] = int(item["dni"])
    item["neighborhood_id"] = int(item["neighborhood_id"])
    item["address_street_name"] = item["address"]["road_name"]
    item["address_number"] = int(item["address"]["number"])
    item["dni"] = int(item["dni"])

    if "relatives" in item:
        for relative in item["relatives"]:
            relatives_data.append(
                {
                    "relation_id": relations[relative["relation"].lower()],
                    "accepted": True,
                    "receiver_id": relative["id"],
                    "sender_id": item["id"]
                }
            )
        item.pop("relatives")

    item.pop("municipality_name")
    item.pop("full_name")
    item.pop("firestore_id")
    item.pop("gender")
    item.pop("role")
    item.pop("birthday")
    item.pop("address")

# Escribe los datos actualizados de nuevo en el archivo JSON
with open('users.json', 'w', encoding="utf-8") as archivo:
    json.dump(data, archivo, ensure_ascii=False, indent=4)

# Escribe los datos actualizados de nuevo en el archivo JSON
with open('locations_fixed.json', 'w', encoding="utf-8") as archivo:
    json.dump(location_data, archivo, ensure_ascii=False, indent=4)

# Escribe los datos actualizados de nuevo en el archivo JSON
with open('relatives_fixed.json', 'w', encoding="utf-8") as archivo:
    json.dump(relatives_data, archivo, ensure_ascii=False, indent=4)
