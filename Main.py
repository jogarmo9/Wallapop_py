from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os.path
from datetime import datetime


def get_browser(url):
    # Opciones de navegación
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver_path = './chromedriver.exe'
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


def get_PID(driver):
    # Obtenemos las tarjetas
    cards = driver.find_elements_by_class_name(
        'ItemCard__data border-top-0 ItemCard__data--with-description'.replace(" ", "."))
    # Obtenemos si el articulo esta reservado o no
    reserved = driver.find_elements(
        By.CSS_SELECTOR, "tsl-svg-icon[src*='/assets/icons/item-card/reserved.svg']")

    precio = []
    titulo = []
    #descripcion = []

    # Obtenemos el texto  de las tarjetas
    for i in cards:
        # Obtenemos el texto de la tarjeta
        card = i.text
        # Separamos el texto por saltos de linea
        card = card.split("\n")

        # Añadimos el texto a las listas
        precio.append(card[0])
        titulo.append(card[1])
        # descripcion.append(card[2])
    return precio, titulo  # , descripcion


def get_reserved(length, driver):
    # Obtenemos si el articulo esta reservado o no
    reservado = []
    xpaths = []
    for i in range(1, length + 1):
        # Obtenemos el xpath de la tarjeta empezando desde 1 hasta el numero de tarjetas
        xpath = "/html/body/tsl-root/tsl-public/div/div/tsl-search/div/tsl-search-layout/div/div[2]/div[1]/tsl-public-item-card-list/div/a[" + str(
            i) + "]"
        reserved = driver.find_elements_by_xpath(xpath)
        # Si el articulo esta reservado añadimos "Reservado" a la lista
        if reserved:
            reservado.append("Reservado")
        else:
            reservado.append("No Reservado")
        xpaths.append(xpath)
    return reservado, xpaths


def get_xpath(length: int) -> list:
    xpaths = []
    for i in range(1, length + 1):
        xpath = "/html/body/tsl-root/tsl-public/div/div/tsl-search/div/tsl-search-layout/div/div[2]/div[1]/tsl-public-item-card-list/div/a["+str(
            i)+"]"
        xpaths.append(xpath)
    return xpaths


# , descripcion: list):
def filter(titulo: list, precio: list, reservado: list, xpath: list):
    options = input("¿Deseas filtrar los articulos? (s/n): ")
    if options == "S" or options == "s":
        option = input(
            "¿Deseas filtrar por palabra clave en el titulo o en la descripcion? (t/d): ")
        if option == "T" or option == "t":
            word = input("Introduce la palabra clave: ").lower()
            # Filtramos por titulo
            for i in range(len(titulo)):
                if word not in titulo[i].lower():
                    titulo[i] = ""
                    precio[i] = ""
                    reservado[i] = ""
                    xpath[i] = ""

    return titulo, precio, reservado,  xpath


# , descripcion: list):
def create_csv(titulo: list, precio: list, reservado: list, date: str, url: str, xpath: list):
    # Creamos el csv
    df = pd.DataFrame(list(zip(titulo, precio, reservado, xpath)), columns=[
        'Titulo', 'Precio', 'Reservado', 'Xpath'])
    df = df[df.Titulo != ""]
    df = df[df.Precio != ""]
    df = df[df.Reservado != ""]

    df = df[df.Xpath != ""]
    df = df.reset_index(drop=True)

    # Añadimos date y url a DataFrame
    #df["Url"] = url

    option = input("¿Deseas eliminar los articulos reservados? (s/n): ")
    if option == "S" or option == "s":
        # Eliminamos los articulos reservados
        df = df[df.Reservado != "Reservado"]

    name = input("Introduce el nombre del csv de salida: ")
    if ".csv" not in name:
        name += ".csv"

    path = './csv/'
    isdir = os.path.isdir(path)
    if not isdir:
        os.mkdir(path)

    df.to_csv("./csv/"+name, index=False, encoding='utf-8')


def get_data():
    url = input("Introduce la url de wallapop que desees buscar: ")
    driver = get_browser(url)
    precio, titulo = get_PID(driver)
    reservado = get_reserved(len(precio), driver)
    xpath = get_xpath(len(precio))
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    driver.quit()
    titulo, precio, reservado, xpath = filter(
        titulo, precio, reservado, xpath)
    create_csv(titulo, precio, reservado,
               xpath, date, url)


def update_csv():
    name = input("Introduce el nombre del csv que desees actualizar: ")
    try:
        # Abrimos el archivo para leer y escribir
        f = open(name, 'r+', encoding='utf-8')
    except:
        print("El archivo no existe")
    else:
        for line in f:
            pass


def xpath_click(xpath: str, driver: webdriver):
    for i in xpath:
        driver.find_element_by_xpath(i).click()


def menu():
    print("Wallapop Scraper")
    print("="*50)
    print("1. Buscar articulos y crear csv")
    print("2. Actualizar csv")
    print("3.Buscar articulos del csv")
    print("4. Salir")
    print("="*50)
    option = input("Introduce una opcion: ")
    return int(option)


def main():
    option = menu()
    if option == 1:
        get_data()
    elif option == 2:
        name = input("Introduce el nombre del csv: ")
        update_csv(name)
    elif option == 3:
        name = input("Introduce el nombre del csv: ")
        xpath = get_xpath()
        xpath_click(xpath)
    elif option == 4:
        exit()


if __name__ == '__main__':
    main()
