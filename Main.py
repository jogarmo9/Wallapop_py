from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os.path
from datetime import datetime

from Browser import get_browser
from Producto import Producto


def get_productos(driver):
    # Obtenemos las tarjetas
    cards = driver.find_elements_by_class_name(
        'ItemCard__data border-top-0 ItemCard__data--with-description'.replace(" ", "."))

    productos = []
    c = 1
    # Obtenemos el texto  de las tarjetas
    for i in cards:
        # Obtenemos el texto de la tarjeta
        card = i.text
        # Separamos el texto por saltos de linea
        card = card.split("\n")

        # Si el articulo esta reservado añadimos "Reservado" a la lista
        reservado, xpath = get_reserved_xpath(c, driver)

        producto = Producto(card[1], card[0], reservado, xpath)
        productos.append(producto)
        c += 1
    return productos


def get_reserved_xpath(position, driver):
    # Obtenemos si el articulo esta reservado o no
    # Obtenemos el xpath de la tarjeta empezando desde 1 hasta el numero de tarjetas
    xpath = "/html/body/tsl-root/tsl-public/div/div/tsl-search/div/tsl-search-layout/div/div[2]/div[1]/tsl-public-item-card-list/div/a[" + str(
        position) + "]"
    try:
        # Obtenemos el boton de reservar
        reservado = driver.find_element_by_xpath("/html/body/tsl-root/tsl-public/div/div/tsl-search/div/tsl-search-layout/div/div[2]/div/tsl-public-item-card-list/div/a["+str(
            position)+"]/tsl-public-item-card/div/tsl-svg-icon")
    except:
        reservado = False
    # Si el articulo esta reservado añadimos "Reservado" a la lista
    if reservado:
        reservado = "Reservado"
    else:
        reservado = "No Reservado"
    return reservado, xpath


def get_xpath(length: int) -> list:
    xpaths = []
    for i in range(1, length + 1):
        xpath = "/html/body/tsl-root/tsl-public/div/div/tsl-search/div/tsl-search-layout/div/div[2]/div[1]/tsl-public-item-card-list/div/a["+str(
            i)+"]"
        xpaths.append(xpath)
    return xpaths


def filter(productos: list):
    options = input("¿Deseas filtrar los articulos? (s/n): ")
    if options == "S" or options == "s":
        word = input("Introduce la palabra clave del titulo: ").lower()
        # Filtramos por titulo
        for i in range(len(productos)):
            titulo = i.get_titulo()
            if word not in titulo.lower():
                productos.remove(i)
    return productos


def create_csv(productos: list, date: str):
    # Eliminamos los articulos reservados
    option = input("¿Deseas eliminar los articulos reservados? (s/n): ")
    if option == "S" or option == "s":
        for i in range(len(productos)):
            if productos[i].get_reservado() == "Reservado":
                productos.remove(i)

    # Creamos el csv
    data = {"nombre": [], "precio": [], "reservado": [], "xpath": []}
    for producto in productos:
        data["nombre"].append(producto.get_nombre())
        data["precio"].append(producto.get_precio())
        data["reservado"].append(producto.get_reservado())
        data["xpath"].append(producto.get_xpath())

    df = pd.DataFrame(data)
    # Añaadimos la fecha
    #df["Fecha"] = date
    print(df)

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
    # Obtenemos el navegador
    driver = get_browser(url)
    # Obtenemos los productos
    productos = get_productos(driver)

    # Obtenemos la fecha
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    driver.quit()

    # Filtramos los productos por titulo
    productos = filter(productos)
    # Creamos el csv
    create_csv(productos, date)


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
        xpath = get_xpath()
        xpath_click(xpath)
    elif option == 3:
        exit()


if __name__ == '__main__':
    main()
