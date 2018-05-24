#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modulo para gestionar los datos de los contactos"""
import re
from colores import Colores as c


class Contacto:
    """Clase principal para la gestion de datos de los contactos"""

    # expresion regular para filtrar emails validos
    regex_email = re.compile(r'''(
        [a-zA-Z0-9._%+-]+      # nombre de usuario
        @                      # simbolo @
        [a-zA-Z0-9.-]+         # nombre de dominio
        (\.[a-zA-Z]{2,4})      # punto lo que sea
        )''', re.VERBOSE)

    def __init__(self, nombre, apellido, edad, telefono, email):
        """Inicializador de instancias.

        Argumentos:
            nombre {str}
            apellido {str}
            edad {int}
            telefono {str}
            email {str}
        """
        self.nombre = nombre
        self.apellido = apellido

        try:
            self.edad = int(edad)
        except:
            c.error(
                "{}: No es una edad valida!!"
                .format(edad)
            )
            self.edad = ''

        # Verificar numero valido
        if self.telefono_valido(telefono):
            self.telefono = telefono
        else:
            c.error(
                "{}: No es un numero de telefono valido!!"
                .format(telefono)
            )
            self.telefono = ''

        if self.email_valido(email):
            self.email = email
        else:
            self.email = ''

    def __str__(self):
        """Rrepresentacion de la instancia Contacto.

        Retorno:
            str -- Nombre, apellido y telefono del contacto.
        """
        return "Contacto: {} {} - Tel: {}".format(self.nombre,
                                                  self.apellido, self.telefono)

    @classmethod
    def email_valido(cls, email):
        """Verifica que las entradas de emails sean validas.

        Argumento:
            email {str}

        Retorno:
            str -- True si encuentra una coincidencia valida.
        """

        coincidencias = []
        for grupos in cls.regex_email.findall(email):
            coincidencias.append(grupos[0])

        if len(coincidencias) > 0:
            return coincidencias[0]
        else:
            c.error(
                "{}: No es un email valido!!"
                .format(email)
            )
            return False

    @classmethod
    def telefono_valido(cls, telefono):
        """Verificador de numeros de telefono validos.

        Argumento:
            telefono {str}

        Retorno:
            bool -- True si pasa la verificacion, de lo contraio False.
        """

        if len(telefono) != 12:
            return False
        for i in range(0, 3):
            if not telefono[i].isdecimal():
                return False
        if telefono[3] != '-':
            return False
        for i in range(4, 7):
            if not telefono[i].isdecimal():
                return False
        if telefono[7] != '-':
            return False
        for i in range(8, 12):
            if not telefono[i].isdecimal():
                return False
        return True

    def obtener_datos(self):
        """Facilita la obtencion de los datos de la instancia
        para ser manipulados por la clase una instancia de la clase
        `Agenda`

        Retorno:
            list -- lista de atributos de la instancia Contacto
        """
        return list((
            self.nombre,
            self.apellido,
            self.edad,
            self.telefono,
            self.email
        ))

    def es_valido(self):
        """Verifica los atributos de un contacto

        Retorno:
            bool -- True si todos los atributos son validos
            de lo contrario False
        """

        return True if self.nombre != '' and \
            self.apellido != '' and self.edad != '' and \
            self.telefono != '' and self.email != '' else False
