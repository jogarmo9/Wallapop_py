class Producto:
    def __init__(self, nombre, precio, reservado, xpath):
        self.__nombre = nombre
        self.__precio = precio
        self.__reservado = reservado
        self.__xpath = xpath

    def get_all(self):
        return self.__nombre, self.__precio, self.__reservado, self.__xpath

    def get_xpath(self):
        return self.__xpath

    def get_nombre(self):
        return self.__nombre

    def get_precio(self):
        return self.__precio

    def get_reservado(self):
        return self.__reservado

    def set_reservado(self):
        self.__reservado = "Reservado"

    # def __str__(self):
    #   return "Producto: " + self.nombre + " Precio: " + str(self.precio) + " Reservado: " + self.reservado + " Xpath: " + self.xpath
