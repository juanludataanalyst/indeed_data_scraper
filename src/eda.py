import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar el JSON en un DataFrame
json_file_path = 'output_data/joined_data.json'  # Cambia esto a la ruta de tu archivo JSON

# Leer el archivo JSON
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convertir el JSON a un DataFrame
df = pd.DataFrame(data)

# Asignar tipos de datos
df['date'] = pd.to_datetime(df['date'])
df['salary'] = df['salary'].astype(str)

# Contar trabajos por país y rol
job_counts = df.groupby(['country', 'role']).size().reset_index(name='count')

# Crear un gráfico de barras
plt.figure(figsize=(12, 6))
sns.barplot(data=job_counts, x='count', y='country', hue='role', palette='viridis')

# Personalizar el gráfico
plt.title('Número de Trabajos por País y Rol')
plt.xlabel('Número de Trabajos')
plt.ylabel('País')
plt.legend(title='Rol')
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar el gráfico
plt.show()
