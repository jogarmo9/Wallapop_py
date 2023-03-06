from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def get_browser(url):
    # Opciones de navegación
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome(driver_path, chrome_options=options)

    # Iniciarla en la pantalla 2
    driver.set_window_position(2000, 0)
    driver.maximize_window()
    time.sleep(1)
    # Obtenemos el navegador
    driver.get(url)

    time.sleep(2)
    # Obtenemos el boton de aceptar cookies
    WebDriverWait(driver, 8)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           'button#onetrust-accept-btn-handler')))\
        .click()
    return driver
