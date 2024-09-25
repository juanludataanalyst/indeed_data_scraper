from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

# Configurar opciones de Chrome (opcional)
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Esto es opcional, ejecuta Chrome en modo headless (sin interfaz gráfica)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Descargar e inicializar el ChromeDriver automáticamente
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)



def get_url(position, location, start):
    """Generate url from position, location and page"""
    template = 'https://www.indeed.com/jobs?q={}&l={}&start={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location, start)
    return url

# Abrir el navegador y realizar scraping en múltiples páginas
for start in range(0, 330, 10):
    print("\n\n\n\n\n")
    print("Iteracion numero: ",start)
    print("\n\n\n\n\n")
    url = get_url('Data Analyst', 'United States', str(start))
    print(f"Accediendo a la URL: {url}")

    # Abrir la página web (Indeed.com)
    driver.get(url)

    # Imprimir el título de la página para confirmar que se ha cargado correctamente
    print(driver.title)


    jobs_data = []

    try:
        job_page = driver.find_element(By.ID, "mosaic-jobResults")
        jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")  # return a list
        
        for jj in jobs:
            job_title = jj.find_element(By.CLASS_NAME, "jobTitle")
            job_description = driver.find_element(By.ID, "jobDescriptionText")
            company_location = jj.find_element(By.CSS_SELECTOR, ".company_location")
            company_name = company_location.text.strip()
           
            print("Role")
            print("\n\n\n\n\n")
            print(job_title.text)
            print("\n\n\n\n\n")
            print("Company Name")
            print(company_name)
            print("\n\n\n\n\n")
            print("Description")
            print("\n\n\n\n\n")
            print(job_description.text)
            

            jobs_data.append([job_title.text, company_name, job_description.text])
            
            
            job_title.click()

            from time import sleep
            sleep(3)

          # Guardar los datos en un CSV para la iteración actual
         # Guardar los datos en un archivo JSON para la iteración actual
        json_file = f"iteracion_{start}.json"
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(jobs_data, file, indent=4, ensure_ascii=False)

        print(f"Datos guardados en {json_file}")


        

    except Exception as e:
        print(f"Error procesando la página: {e}")
    
# Cerrar el navegador
driver.quit()
