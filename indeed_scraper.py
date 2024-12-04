# indeed_scraper.py
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
import os
from datetime import date
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
    user_agent = random.choice(user_agents)
    chrome_options.add_argument(f"user-agent={user_agent}")
    print(f"Usando el siguiente User-Agent: {user_agent}")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def clear_browser_storage(driver):
    """
    Limpia cookies, sessionStorage y localStorage del navegador.
    """
    try:
        # Borrar cookies
        driver.delete_all_cookies()
        print("Cookies eliminadas.")
        
        # Borrar sessionStorage
        driver.execute_script("window.sessionStorage.clear();")
        print("sessionStorage limpiado.")
        
        # Borrar localStorage
        driver.execute_script("window.localStorage.clear();")
        print("localStorage limpiado.")
    except Exception as e:
        print(f"Error al limpiar el almacenamiento del navegador: {e}")


# Función para generar la URL de búsqueda
def get_url(position, location, start):
    # URL base por defecto para 'United States'
    base_url = 'https://www.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14'
    
    # Modificar la URL base según el país
    location_urls = {
        "spain": 'https://es.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14',
        "colombia": 'https://co.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14',
        "united kingdom": 'https://uk.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14',
        "canada": 'https://ca.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14',
        "germany": 'https://de.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14',
        "australia": 'https://au.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14',
        "singapore": 'https://sg.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14',
        "india": 'https://in.indeed.com/jobs?q={}&l={}&start={}&sort=date&fromage=14'
    }
    
    # Actualizar la URL base si el país está en el diccionario
    base_url = location_urls.get(location.lower(), base_url)

    return base_url.format(position.replace(' ', '+'), location.replace(' ', '+'), start)


def get_indeed_data(position, location):
    # Crear la carpeta de salida
    today = date.today()
    base_dir = os.path.join("data", f"{today}_{location}_{position}")
    os.makedirs(base_dir, exist_ok=True)

    start = 0
    while True:
        driver = create_driver()
        try:
            clear_browser_storage(driver)
            url = get_url(position, location, start)
            print(f"Accediendo a la URL: {url}")
            driver.get(url)

            # Intentar aceptar cookies si aparece el aviso
            try:
                cookies_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar') or contains(text(), 'Allow') or contains(text(), 'Accept')]"))
                )
                cookies_button.click()
                print("Cookies aceptadas.")
            except TimeoutException:
                print("No se encontró el aviso de cookies o ya estaba aceptado.")
                
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
                except NoSuchElementException:
                    salary = "No especificado"

                try:
                    employment_type = driver.find_element(By.XPATH, "//div[@aria-label='Tipo de empleo']").text
                except NoSuchElementException:
                    employment_type = "No especificado"

                jobs_data.append({
                    "title": job_title.text,
                    "company": company_name,
                    "description": job_description.text,
                    "salary": salary,
                    "employment_type": employment_type
                })

                sleep(random.uniform(5, 10))

            # Guardar los datos en un archivo JSON en la carpeta correspondiente
            json_file = os.path.join(base_dir, f"{today}_{position}_{location}_{start}.json")
            with open(json_file, mode='w', encoding='utf-8') as file:
                json.dump(jobs_data, file, indent=4, ensure_ascii=False)
            print(f"Datos guardados en {json_file}")

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Next Page"]')
                next_button.click()
                start += 10
            except NoSuchElementException:
                print("No hay más páginas.")
                break
        except Exception as e:
            print(f"Error procesando la página: {e}")
            traceback.print_exc()
        finally:
            driver.quit()