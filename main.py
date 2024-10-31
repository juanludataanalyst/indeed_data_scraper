from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import random
import json
from time import sleep
import traceback

# Lista de User-Agents (todos de Google Chrome)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"
]

# Función para inicializar el navegador con un User-Agent aleatorio
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-features=EnableAutomation")
    chrome_options.add_argument("--window-size=1920,1080")
    # Seleccionar un User-Agent aleatorio de Google Chrome
    user_agent = random.choice(user_agents)
    chrome_options.add_argument(f"user-agent={user_agent}")

    print(f"Usando el siguiente User-Agent: {user_agent}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Función para generar la URL de búsqueda
def get_url(position, location, start):
    template = 'https://www.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location, start)
    return url

# Iniciar el scraping
start = 0  # Variable de inicio para la primera página
while True:
    driver = create_driver()  # Crear el driver con User-Agent aleatorio

    try:
        url = get_url('Data Analyst', 'United States', start)
        print(f"Accediendo a la URL: {url}")
        driver.get(url)

        # Verificar que la página se ha cargado
        print(driver.title)

        jobs_data = []

        job_page = driver.find_element(By.ID, "mosaic-jobResults")
        jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for jj in jobs:
            job_title = jj.find_element(By.CLASS_NAME, "jobTitle")
            job_title.click()

            try: 
                job_description = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "jobDescriptionText")))
            except TimeoutException:
                print("No se encontró la descripción, continuando con el siguiente trabajo.")
                continue

            company_location = jj.find_element(By.CSS_SELECTOR, ".company_location")
            company_name = company_location.text.strip()

            try:
                salary = driver.find_element(By.XPATH, "//h3[contains(text(), 'Sueldo')]/following-sibling::div").text
            except:
                salary = "No especificado"

            try:
                employment_type = driver.find_element(By.XPATH, "//div[@aria-label='Tipo de empleo']").text
            except:
                employment_type = "No especificado"

            jobs_data.append({
                "title": job_title.text,
                "company": company_name,
                "description": job_description.text,
                "salary": salary,
                "employment_type": employment_type
            })

            sleep(random.uniform(5, 10))

        # Guardar los datos en un archivo JSON
        json_file = f"US_data_analyst_{start}.json"
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(jobs_data, file, indent=4, ensure_ascii=False)

        print(f"Datos guardados en {json_file}")

        # Intentar encontrar el botón de "Next Page" para avanzar a la siguiente página
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Next Page"]')
            start += 10  # Incrementar la variable de inicio para la siguiente URL
        except NoSuchElementException:
            print("No hay más páginas.")
            break  # Terminar el bucle si no hay más páginas

    except Exception as e:
        print(f"Error procesando la página: {e}")
        traceback.print_exc()

    finally:
        driver.quit()

