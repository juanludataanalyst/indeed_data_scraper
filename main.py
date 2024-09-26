import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
from time import sleep
import traceback

from selenium.common.exceptions import TimeoutException




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
    chrome_options.add_argument(f"user-agent={user_agent}")  # Añadir el User-Agent

    print(f"Usando el siguiente User-Agent: {user_agent}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def move_mouse_to_center(driver):
    """Mueve el ratón al centro de la pantalla."""
    actions = ActionChains(driver)
    width = driver.execute_script("return window.innerWidth")
    height = driver.execute_script("return window.innerHeight")
    
    # Mover el ratón al centro de la ventana
    center_x = width // 2
    center_y = height // 2
    print(f"Moviendo ratón al centro de la ventana: ({center_x}, {center_y})")
    actions.move_by_offset(center_x, center_y).perform()
    sleep(1)

def simulate_mouse_movements(driver, max_movements=3):
    """Simula movimientos del ratón en la página asegurándose de no salir de los límites."""
    actions = ActionChains(driver)
    
    # Obtener el tamaño de la ventana para establecer límites
    width = driver.execute_script("return window.innerWidth")
    height = driver.execute_script("return window.innerHeight")
    
    current_x = width // 2  # Inicializa en el centro
    current_y = height // 2
    
    for _ in range(max_movements):  # Número de movimientos limitados a max_movements
        # Coordenadas aleatorias con límites para evitar salir de la pantalla
        x_offset = random.randint(-50, 50)  # Movimientos más controlados
        y_offset = random.randint(-50, 50)
        
        # Verificar que el nuevo movimiento esté dentro de los límites
        new_x = current_x + x_offset
        new_y = current_y + y_offset
        
        if 0 <= new_x <= width and 0 <= new_y <= height:
            current_x = new_x
            current_y = new_y
            print(f"Moviendo ratón por ({x_offset}, {y_offset}) a ({current_x}, {current_y})")
            actions.move_by_offset(x_offset, y_offset).perform()
            sleep(random.uniform(0.5, 1.0))
        else:
            print(f"Movimiento fuera de límites evitado: ({new_x}, {new_y}) está fuera de la pantalla.")

def simulate_random_scrolls(driver, max_scrolls=2):
    """Simula scrolls aleatorios en la página."""
    for _ in range(max_scrolls):  # Número de scrolls limitados a max_scrolls
        scroll_distance = random.randint(200, 500)  # Distancia de scroll reducida
        print(f"Scrolleando {scroll_distance} píxeles hacia abajo")
        
        # Realiza el scroll hacia abajo
        driver.execute_script(f"window.scrollBy(0, {scroll_distance})")
        sleep(random.uniform(1, 2))  # Pausa breve entre scrolls

def simulate_random_clicks(driver, max_clicks=2):
    """Simula clics en posiciones aleatorias fuera de los elementos."""
    actions = ActionChains(driver)
    
    for _ in range(max_clicks):  # Número de clics limitados a max_clicks
        # Coordenadas aleatorias dentro de la ventana
        x_offset = random.randint(100, driver.execute_script("return window.innerWidth") - 100)
        y_offset = random.randint(100, driver.execute_script("return window.innerHeight") - 100)
        print(f"Click en ({x_offset}, {y_offset})")
        
        # Mover el ratón a la posición aleatoria y hacer clic
        actions.move_by_offset(x_offset, y_offset).click().perform()
        sleep(random.uniform(0.5, 1.5))  # Pausa breve entre clics


# Función para generar la URL de búsqueda
def get_url(position, location, start):
    template = 'https://www.indeed.com/jobs?q={}&l={}&start={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location, start)
    return url

# Iniciar el scraping
for start in range(0, 230, 10):  # Ajusta el rango según la cantidad de páginas a scrapear
    driver = create_driver()  # Crear el driver con User-Agent aleatorio

    try:
        url = get_url('Data Analyst', 'United States', start)
        print(f"Accediendo a la URL: {url}")
        driver.get(url)
        move_mouse_to_center(driver)
        simulate_random_scrolls(driver)
        # Espera aleatoria para evitar detección
        sleep(random.uniform(5, 10))

        


        # Verificar que la página se ha cargado
        print(driver.title)

        jobs_data = []

        job_page = driver.find_element(By.ID, "mosaic-jobResults")
        jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for jj in jobs:
            job_title = jj.find_element(By.CLASS_NAME, "jobTitle")
            job_title.click()
            simulate_random_scrolls(driver)
            simulate_mouse_movements(driver)
            #job_description = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "jobDescriptionText")))

            try: 
                job_description = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "jobDescriptionText")))
            except TimeoutException:
                print("No se encontró la descripción, continuando con el siguiente trabajo.")
                continue  # Saltar al siguiente trabajo y no detener el proceso:


            
            company_location = jj.find_element(By.CSS_SELECTOR, ".company_location")
            company_name = company_location.text.strip()

            jobs_data.append({
                "title": job_title.text,
                "company": company_name,
                "description": job_description.text
            })

            # Espera aleatoria entre clics
            sleep(random.uniform(5, 10))


        # Guardar los datos en un archivo JSON
        json_file = f"US_data_analyst_{start}.json"
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(jobs_data, file, indent=4, ensure_ascii=False)

        print(f"Datos guardados en {json_file}")

    except Exception as e:
        print(f"Error procesando la página: {e}")
        traceback.print_exc()  # Agrega más detalles sobre el error

    finally:
        driver.quit()  # Cerrar el navegador después de cada iteración
