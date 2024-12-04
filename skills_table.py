import pandas as pd
import json

# Cargar el JSON en un DataFrame
json_file_path = 'joined_data.json'  # Cambia esto a la ruta de tu archivo JSON

# Leer el archivo JSON
with open("joined_data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convertir el JSON a un DataFrame
df = pd.DataFrame(data)

# Desglosar la lista de skills en filas individuales, manteniendo todas las apariciones
skills_df = df.explode('skills')

# Seleccionar solo las columnas necesarias para el análisis
skills_df = skills_df[['job_id','skills', 'country', 'role', 'title']]

# Guardar el resultado en un archivo CSV
skills_df.to_csv('skills_data_table.csv', index=False)

print("Archivo 'skills_data_table.csv' creado con éxito. Aquí tienes un adelanto:")
print(skills_df.head())
