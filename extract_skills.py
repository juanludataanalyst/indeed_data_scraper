import json
import re
import os
import hashlib

# Diccionario con tecnologías y sus variaciones

with open('skills_definition.json', 'r') as f:
  skills = json.load(f)

# Obtener el directorio de trabajo actual
current_directory = os.getcwd()

# Especificar el directorio de datos
data_directory = os.path.join(current_directory, 'data')

# Función para generar un identificador único basado en la descripción del trabajo
def generate_job_id(description):
    # Usa hashlib para generar un hash a partir de la descripción
    return hashlib.md5(description.encode('utf-8')).hexdigest()

# Función para procesar archivos JSON en un directorio específico
def process_json_files(directory):
    processed_data = []
    
    # Leer todos los subdirectorios en el directorio de datos
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        
        if os.path.isdir(subdir_path):
            # Extraer fecha, país y rol del nombre del directorio
            date, country, role = subdir.split('_')
            
            # Leer todos los archivos JSON en el subdirectorio
            for file_name in os.listdir(subdir_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(subdir_path, file_name)
                    
                    # Cargar el archivo JSON
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    except FileNotFoundError:
                        print(f"Error: El archivo {file_path} no se encontró.")
                        continue
                    except json.JSONDecodeError as e:
                        print(f"Error al leer el archivo JSON: {e}")
                        continue

                    # Compilar expresiones regulares para cada tecnología
                    patterns = {key: re.compile(r'\b(' + '|'.join(map(re.escape, variations)) + r')\b', re.IGNORECASE) for key, variations in skills.items()}

                    # Extraer tecnologías
                    def extract_technologies(description):
                        found_technologies = set()  # Usar un conjunto para evitar duplicados
                        for key, pattern in patterns.items():
                            if pattern.search(description):
                                found_technologies.add(key)  # Agregar solo la clave (tecnología)
                        return list(found_technologies)  # Convertir el conjunto de vuelta a una lista

                    # Procesar cada puesto en el JSON y crear una nueva estructura
                    for job in data:
                        title = job.get("title", "")
                        company = job.get("company", "")
                        description = job.get("description", "")
                        salary = job.get("salary", "No especificado")
                        employment_type = job.get("employment_type", "No especificado")
                        technologies = extract_technologies(description)

                        # Generar un job_id único basado en la descripción
                        job_id = generate_job_id(description)

                        # Extraer la ubicación de la empresa
                        location = company.split('\n')[1] if '\n' in company else "Ubicación no especificada"
                        company_cleaned = company.split('\n')[0] if '\n' in company else company

                        # Crear un nuevo diccionario para el puesto procesado
                        processed_job = {
                            "job_id": job_id,
                            "title": title,
                            "company": company_cleaned,
                            "location": location,
                            "skills": technologies,
                            "salary": salary,
                            "employment_type": employment_type,
                            "date": date,
                            "country": country,
                            "role": role
                        }
                        processed_data.append(processed_job)

    return processed_data

# Procesar todos los archivos JSON y guardar los resultados en un nuevo archivo
processed_data = process_json_files(data_directory)

# Guardar el nuevo JSON en un archivo
output_file_name = 'joined_data.json'
output_file_path = os.path.join(current_directory, output_file_name)

try:
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    print(f"Datos procesados guardados en: {output_file_path}")
except Exception as e:
    print(f"Error al guardar el archivo JSON: {e}")
