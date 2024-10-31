from indeed_scraper import get_indeed_data

# Definir las posiciones y la ubicación
positions = ["Data Analyst", "Data Engineer", "Data Scientist"]
location = "United States"

# Llamar a la función para cada posición
for position in positions:
    print(f"Extrayendo datos para {position} en {location}")
    get_indeed_data(position, location)
