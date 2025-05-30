# Codigo para hacer Web Scrapping en Airbnb
# Autor: Leandro Puig Lomez

# Librerias
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# ---------------------
# Funciones
# ---------------------

# ---------------------
# Parametros de entrada
# ---------------------
main_url = "https://www.airbnb.com.ar/"
ciudad   = "Pinamar"
nombre_archivo = "datos_Pinamar"

# ---------------------
# Seccion 1: Coneguir URL de la ciudad
# ---------------------
# Driver
options = Options()
# options.add_argument("--headless")
driver  = webdriver.Chrome(options=options)

# Variables de uso repetido
wait    = WebDriverWait(driver, 10)

# Pagina principal
driver.get(main_url)
sleep(5)

# Cerrar Pop Ups
try:
    close_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(@aria-label, "Close") or contains(@aria-label, "close") or contains(@aria-label, "Cerrar") or contains(@aria-label, "cerrar")]')
        )
    )
    close_btn.click()
except:
    pass

# Escribir la ciudad
search_input = driver.find_element(By.ID, "bigsearch-query-location-input")
search_input.click()
sleep(1)
search_input.send_keys(ciudad)
sleep(1)
search_input.send_keys(Keys.ENTER)
sleep(1)
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

# Clickear boton Buscar
element = driver.find_element(By.CSS_SELECTOR, '[data-testid="structured-search-input-search-button"]')
element.click()
sleep(5)

# Por chequeo, ir a la primer pagina
try:
    boton_pag1 = driver.find_element(By.XPATH, '//a[text()="1"]')
except:
    # boton_pag1 = driver.find_element(By.CSS_SELECTOR, 'button[aria-current="page"]')
    boton_pag1 = driver.find_element(By.XPATH, '//button[text()="1"]')

if boton_pag1.is_enabled():
    boton_pag1.click()
    sleep(5)


# ---------------------
# Seccion 2: Colleccionar Data
# ---------------------
datos = []
stop_switch = False
while not stop_switch:
    lista_publicaciones = driver.find_elements(By.CSS_SELECTOR, '[itemprop="itemListElement"]')
    for publicacion in lista_publicaciones:
        titulo      = publicacion.find_element(By.CSS_SELECTOR, 'meta[itemprop="name"]').get_attribute('content')
        url         = publicacion.find_element(By.CSS_SELECTOR, 'meta[itemprop="url"]').get_attribute('content')
        descripcion = publicacion.text

        datos.append({
            'titulo': titulo,
            'url': url,
            'descripcion': descripcion
        })

    try:
        boton_siguiente = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Siguiente"]')
    except:
        boton_siguiente = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Siguiente"]')
    if boton_siguiente.is_enabled():
        boton_siguiente.click()
        sleep(3)
    else:
        stop_switch = True


# ---------------------
# Seccion 2: Procesar Datos
# ---------------------
# TODO: Procesar y crear la base de datos. Input: datos
df = pd.DataFrame(datos)

# ---------------------
# Seccion 2: Crear Datos
# ---------------------
df.to_pickle(nombre_archivo + ".pkl")
df.to_csv(nombre_archivo + ".csv", index=False, encoding="utf-8")


