from indeed_scraper import get_indeed_data

# Definir las posiciones y las ubicaciones
positions = ["Data Analyst"]
locations = ["Spain"]

# Llamar a la función para cada combinación de posición y ubicación
for location in locations:
    for position in positions:
        print(f"Extrayendo datos para {position} en {location}")
        get_indeed_data(position, location)
