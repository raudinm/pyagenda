#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modulo principal de la clase Agenda."""
import os
import csv
import time
import sys
from getpass import getuser
import pandas as pd
from colores import Colores as c
from contacto import Contacto


# ruta al archivo de la agenda
usuario = getuser()
if usuario == 'root':
    ruta_archivo = '/{}/.agenda.csv'.format(usuario)
else:
    ruta_archivo = '/home/{}/.agenda.csv'.format(usuario)


class Agenda:
    """Esta clase recibe una instancia de la clase Contacto."""

    def __init__(self, contacto):
        if not isinstance(contacto, Contacto):
            c.error("{}: No es un contacto valido!!".format(contacto))

            # Salir retornando un codigo de error
            sys.exit(1)

        else:
            self.contacto = contacto

    def __str__(self):
        """Modifica como se representa la instancia de Agenda
        y muestra la instancia de Contacto que esta siendo modificada.

        Retorno:
            str -- representacion en cadena de la instancia Contacto
                   que esta siendo manejada por la instancia Agenda
        """
        return "Procesando el contacto {} con el Telefono {}"\
            .format(
                self.contacto.nombre,
                self.contacto.telefono
            )

    @classmethod
    def crear_agenda(cls):
        """Crea la agenda si no existe ya en disco."""

        if not cls.existe_agenda(ruta_archivo):
            with open(ruta_archivo, 'w') as agenda:
                columnas = ["Nombre", "Apellido", "Edad", "Telefono", "Email"]
                cabezera = csv.writer(agenda)
                cabezera.writerow(columnas)

            c.success("Agenda creada con exito!!")

        else:
            print(
                c.CYAN + c.BOLD + '\n' +
                '[!] La agenda ya existe puedes agregar tus contactos' +
                c.ENDC
            )
            time.sleep(2)

    @classmethod
    def borrar_agenda(cls):
        """Elimina todo el contenido de la agenda si ya existe en disco."""

        while True:
            opcion = input(
                c.ROJO + c.BOLD +
                "{} {}"
                .format(
                    "[x] ADVERTENCIA: ESTAS SEGURO/A QUE",
                    "DESEAS BORRAR LA AGENDA ? [SI/NO]: "
                ) + c.ENDC
            )

            if opcion.lower() == 'si':
                if cls.existe_agenda(ruta_archivo):
                    with open(ruta_archivo, 'w') as agenda:
                        columnas = [
                            "Nombre", "Apellido", "Edad", "Telefono", "Email"
                        ]
                        cabezera = csv.writer(agenda)
                        cabezera.writerow(columnas)

                    print(c.VERDE, c.BOLD, "\n[-] Agenda borrada!!", c.ENDC)
                    time.sleep(2)
                    break

                else:
                    print(
                        c.AMARILLO + c.BOLD + '\n' +
                        '[!] La agenda no existe aun!!' + c.ENDC
                    )
                    time.sleep(2)
                    break

            elif opcion.lower() == 'no':
                c.success('No se elimino la agenda...')
                break

    @staticmethod
    def existe_agenda(archivo):
        """Este metodo verifica la existencia del archivo en el disco.

        Argumentos:
            archivo {str} -- Nombre del archivo que se va a verificar.

        Retorno:
            bool -- True si existe el archivo, False si no existe.
        """

        return True if os.path.exists(archivo) else False

    def agregar_registro(self):
        """Guardar el contacto en el archivo agenda."""

        if self.existe_agenda(ruta_archivo):
            with open(ruta_archivo, mode='a', newline='') as agenda:
                contacto = csv.writer(agenda)
                contacto.writerow(self.contacto.obtener_datos())

                c.success(
                    "El contacto {} ha sido agregado a la agenda."
                    .format(self.contacto.nombre)
                )

        else:
            c.error(
                "{str} {} porque la agenda aun no existe..."
                .format(
                    self.contacto.nombre,
                    str="No se pudo agregar al contacto"
                )
            )

    @classmethod
    def eliminar_registro(cls, indice=None):
        """Elimina un contacto de la agenda a traves de su indice.

        Keyword Arguments:
            indice {int} -- Si no se espesifica un valor no se utiliza
                            para realizar la buzqueda (default: {None})
        """

        if indice:
            try:
                int_indice = int(indice)
                if cls.existe_agenda(ruta_archivo):
                    with open(ruta_archivo, 'r') as agenda:
                        registros = pd.read_csv(agenda)

                        # eliminar el indice
                        registros.drop(
                            registros.index[int_indice], inplace=True
                        )
                        print(c.VERDE, c.BOLD, "\n[-] Contacto eliminado!")
                        time.sleep(2)
                        registros.to_csv(ruta_archivo, index=False)
                else:
                    c.error("La agenda aun no existe!!")
            except:
                c.error(
                    "El indice debe ser un numero entero\n" +
                    "y debe ser un contacto valido en la agenda."
                )

        else:
            c.error(
                "{str1} {str2}"
                .format(
                    str1="Es necesario un indice (id)",
                    str2="para eliminar un contacto..."
                )
            )

    @classmethod
    def listar_contactos(cls, orden):
        """Muestra la lista de contactos segun el orden espesificado.

        Argumentos:
            orden str -- Los strings admitidos son {txt}.
        """.format(txt="`Nombre`, `Apellido` o `Edad`")

        # el orden aceptado para listar los contactos debe
        # coincidir con un elemento dentro de la tupla `_orden`
        _orden = ("Nombre", "Apellido", "Edad")

        if cls.existe_agenda(ruta_archivo):
            with open(ruta_archivo, 'r') as agenda:
                registros = pd.read_csv(agenda)

                if orden in _orden:
                    ordenados = registros.sort_values(by=[orden])
                    if len(ordenados) > 0:
                        print(
                            "\n",
                            c.BOLD, c.CYAN,
                            ordenados,
                            c.ENDC
                        )
                    else:
                        c.error("No hay contactos en la agenda todavia.")

                else:
                    c.error("Orden admitdo: Nombre, Apellido o Edad.")
        else:
            c.error("La agenda aun no existe!!")

    @classmethod
    def modificar_registro(
                           cls, indice=None, nombre=None,
                           apellido=None, edad=None, telefono=None,
                           email=None
                        ):
        """Modifica un registro de acuerdo a los argumentos indicados
        si no se espesifica uno de los argumentos este conserva su valor
        original.

        Keyword Arguments:
            indice {int} -- (default: {None})
            nombre {str} -- (default: {None})
            apellido {str} -- (default: {None})
            edad {str} -- (default: {None})
            telefono {str} -- (default: {None})
            email {str} -- (default: {None})
        """

        try:
            int_indice = int(indice)

            if isinstance(int_indice, int):
                if cls.existe_agenda(ruta_archivo):
                    with open(ruta_archivo, 'r') as agenda:
                        registros = pd.read_csv(agenda)

                        # convertir los registros en un diccionario
                        # para modificar los datos necesarios
                        tmp_agenda = registros.to_dict()

                        # modificar los campos
                        tmp_agenda["Nombre"][int_indice] = nombre \
                            if nombre is not None and nombre != '' else \
                            tmp_agenda["Nombre"][int_indice]

                        tmp_agenda["Apellido"][int_indice] = apellido \
                            if apellido is not None and apellido != '' else \
                            tmp_agenda["Apellido"][int_indice]

                        tmp_agenda["Edad"][int_indice] = edad \
                            if edad is not None and edad != '' else \
                            tmp_agenda["Edad"][int_indice]

                        tmp_agenda['Telefono'][int_indice] = telefono \
                            if telefono is not None and telefono != '' else \
                            tmp_agenda["Telefono"][int_indice]

                        tmp_agenda['Email'][int_indice] = email \
                            if email is not None and email != '' else \
                            tmp_agenda['Email'][int_indice]

                        registros_nuevos = pd.DataFrame.from_dict(tmp_agenda)

                        # Reordenar las colunmas
                        reordenado = registros_nuevos.reindex(
                            columns=[
                                "Nombre", "Apellido",
                                "Edad", "Telefono", "Email"
                            ]
                        )

                        # guardar los registros en el archivo de la agenda
                        reordenado.to_csv(ruta_archivo, index=False)

                else:
                    c.error("La agenda aun no existe!!")
            else:
                c.error(
                    "El indice debe ser un numero entero\n" +
                    "y debe ser un contacto valido en la agenda."
                )

        except:
            c.error(
                "{str1} {str2}"
                .format(
                    str1="Es necesario un indice para",
                    str2="modificar un contacto..."
                )
            )

    @classmethod
    def buscar_registro(cls, filtro, busqueda):
        """Realiza una busueda dentro del archivo de agenda.

        Argumentos:
            filtro {str} -- filtra el campo por el que se realiza
                            la busqueda.
            busqueda {str} -- filtra el valor contenido en el campo
                              por el que se filtra la busqueda.
        """

        _filtros = ("Nombre", "Apellido", "Telefono")

        if cls.existe_agenda(ruta_archivo):
            with open(ruta_archivo, 'r') as agenda:
                registros = pd.read_csv(agenda)

                if filtro.title() in _filtros:
                    # filtrar la busqueda
                    coincidencia = registros[
                        registros[filtro.title()] == busqueda
                    ]

                    print("\n", c.BOLD, c.CYAN, coincidencia, c.ENDC) \
                        if len(coincidencia) > 0 else \
                        c.error("{} no existe!!".format(busqueda))

                else:
                    c.error("Filtro admitdo: Nombre, Apellido o Telefono.")
        else:
            c.error("La agenda aun no existe!!")
