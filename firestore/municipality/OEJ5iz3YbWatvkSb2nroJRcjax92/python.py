import json

# Lee el archivo JSON
with open('emergencies.json', 'r') as archivo:
    data = json.load(archivo)

# Recorre cada mapa en la lista y agrega la clave "municipality_id" con el valor "1"
for item in data:
    item["municipality_id"] = "OEJ5iz3YbWatvkSb2nroJRcjax92"

# Escribe los datos actualizados de nuevo en el archivo JSON
with open('emergencies.json', 'w') as archivo:
    json.dump(data, archivo, indent=4)
