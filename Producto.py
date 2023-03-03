class Producto:
    def __init__(self, nombre, precio, reservado, xpath):
        self.__nombre = nombre
        self.__precio = precio
        self.__reservado = reservado
        self.__xpath = xpath

    def get_all(self):
        return self.nombre, self.precio, self.reservado, self.xpath

    def get_xpath(self):
        return self.xpath

    def get_nombre(self):
        return self.nombre

    def set_reservado(self):
        self.reservado = "Reservado"

    def __str__(self):
        return "Producto: " + self.nombre + " Precio: " + str(self.precio) + " Reservado: " + self.reservado + " Xpath: " + self.xpath
