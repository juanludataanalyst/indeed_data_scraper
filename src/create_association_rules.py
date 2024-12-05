import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import json

# Leer el CSV de habilidades
skills_df = pd.read_csv('output_data/skills_data_table.csv')

# Crear una tabla binaria donde cada fila es un título y cada columna una habilidad
skills_encoded = skills_df.groupby(['title', 'skills']).size().unstack(fill_value=0)
skills_encoded = skills_encoded.applymap(lambda x: 1 if x > 0 else 0)  # Convertir a formato binario

# Aplicar el algoritmo Apriori
frequent_itemsets = apriori(skills_encoded, min_support=0.1, use_colnames=True)

# Generar las reglas de asociación
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Crear una estructura simplificada para el JSON
simplified_rules = []

for _, row in rules.iterrows():
    antecedents = list(row['antecedents'])
    consequents = list(row['consequents'])
    
    # Agregar al JSON simplificado
    simplified_rules.append({
        "antecedents": antecedents,
        "consequents": consequents,
        "support": row['support'],
        "confidence": row['confidence'],
        "lift": row['lift']
    })

# Guardar el JSON simplificado
with open('output_data/summary_association_rules.json', 'w') as f:
    json.dump(simplified_rules, f, indent=4)

print("Archivo JSON simplificado creado.")
