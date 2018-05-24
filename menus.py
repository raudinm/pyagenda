#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Este modulo establece la forma en que se presenta la aplicacion
al usuario.
"""
from getpass import getuser
from os import name, system
from time import sleep
from agenda import Agenda
from contacto import Contacto
from colores import Colores as c


def portada():
    """Muestra portada del programa en pantalla
    el usuario activo y la version del programa."""

    system('cls') if name == 'nt' else system('clear')
    usuario = getuser() if name != 'nt' else "Usuario Windows -_-"

    print(c.CYAN, """
   /$$$$$$$             /$$$$$$                                  /$$
  | $$__  $$           /$$__  $$                                | $$
  | $$  \ $$/$$   /$$ | $$  \ $$ /$$$$$$  /$$$$$$ /$$$$$$$  /$$$$$$$ /$$$$$$
  | $$$$$$$| $$  | $$ | $$$$$$$$/$$__  $$/$$__  $| $$__  $$/$$__  $$|____  $$
  | $$____/| $$  | $$ | $$__  $| $$  \ $| $$$$$$$| $$  \ $| $$  | $$ /$$$$$$$
  | $$     | $$  | $$ | $$  | $| $$  | $| $$_____| $$  | $| $$  | $$/$$__  $$
  | $$     |  $$$$$$$ | $$  | $|  $$$$$$|  $$$$$$| $$  | $|  $$$$$$|  $$$$$$$
  |__/      \____  $$ |__/  |__/\____  $$\_______|__/  |__/\_______/\_______/
            /$$  | $$           /$$  \ $$
           |  $$$$$$/          |  $$$$$$/
            \______/            \______/

    {} {} :)                                           {}
    """.format(
            c.CURSIVA + c.VERDE + "Hola" + c.ENDC,
            c.AMARILLO + usuario + c.ENDC,
            c.CURSIVA + c.VERDE + c.BOLD +
            "Version " + c.ENDC + c.CYAN +
            "0.0.1b4" + c.ENDC
        ), c.ENDC
    )


def ver_contactos():
    """Muestra un submenu que permite filtrar la forma en que
    se muestran los contactos, por Nombre, Apellido o Edad"""

    while True:
        print(c.VERDE, c.BOLD, """
        Antes de ver los contactos puedes filtrarlos por Nombre,
        Apellido o por Edad.

        """, c.ENDC)

        opcion = input(c.CYAN + "[DESEAS CONTINUAR?][SI/NO]: " + c.ENDC)

        if opcion.lower() == 'si':
            filtro = input(
                c.VERDE + "Filtro [Nombre(default)]: " +
                c.ENDC
            )

            if filtro.title() in ("Nombre", "Apellido", "Edad"):
                Agenda.listar_contactos(filtro.title())

            elif filtro == '':
                Agenda.listar_contactos("Nombre")

            else:
                c.error(
                    "Solo Nombre[default], Apellido o Edad son permitidos!"
                )

        elif opcion.lower() == 'no':
            print(
                c.AMARILLO, "\n[!] Regresando al menu anterior...",
                c.ENDC
            )
            sleep(1.5)
            break
        else:
            c.error("Solo puedes responder Si o No.")


def solicitar_contacto():
    """Esta funcion estara en ejecucion hasta que el usuario
    no quiera seguir ingresando contactos a la agenda"""

    while True:
        print(c.VERDE, c.BOLD, """
        A continuacion debes proporcionar informacion sobre el contacto,
        asegurate de ingresar la info correcta, ejemplo: 8090000000 no es
        un numero valido en esta agenda el formato debe ser 809-000-0000
        y para correos usuario@dominio.lo-que-sea

        """, c.ENDC)

        opcion = input(c.CYAN + "[DESEAS CONTINUAR?][SI/NO]: " + c.ENDC)

        if opcion.lower() == 'si':
            nombre = input(c.VERDE + "[NOMBRE]: " + c.ENDC)
            apellido = input(c.VERDE + "[APELLIDO]: " + c.ENDC)
            edad = input(c.VERDE + "[EDAD]: " + c.ENDC)
            telefono = input(c.VERDE + "[TELEFONO]: " + c.ENDC)
            email = input(c.VERDE + "[CORREO]: " + c.ENDC)

            contacto = Contacto(
                nombre, apellido, edad, telefono, email
            )

            if contacto.es_valido():
                Agenda(contacto).agregar_registro()
                opcion2 = input(
                    c.CYAN + "\n" + "[AGREGAR OTRO?][SI/NO]: " + c.ENDC
                )

                if opcion2.lower() == 'si':
                    continue
                elif opcion2.lower() == 'no':
                    print(
                        c.AMARILLO, "\n[!] Regresando al menu anterior...",
                        c.ENDC
                    )
                    sleep(1.5)
                    break
                else:
                    c.error("Solo puedes responder Si o No.")

            else:
                c.error("Contacto no valido, por favor intenta de nuevo!!")

        elif opcion.lower() == 'no':
            print(c.AMARILLO, "\n[!] Regresando al menu anterior...", c.ENDC)
            sleep(1.5)
            break

        else:
            c.error("Solo puedes responder Si o No.")


def busqueda_personalizada():
    """Realiza una busqueda por parametros dentro de la agenda."""

    while True:
        print(c.VERDE, c.BOLD, """
        En este submenu puedes realizar una busqueda por Nombre,
        Apellido o el numero de Telefono.

        NOTA: Mayusculas y minusculas cuentan.

        """, c.ENDC)

        opcion = input(c.CYAN + "[DESEAS CONTINUAR?][SI/NO]: " + c.ENDC)

        if opcion.lower() == 'si':
            filtro = input(
                c.VERDE + "Filtrar por campo [Nombre(default)]: " + c.ENDC
            )

            busqueda = input(c.VERDE + "[A quien buscas?]: " + c.ENDC)

            Agenda.buscar_registro("Nombre", busqueda) if filtro == '' else \
                Agenda.buscar_registro(filtro, busqueda)

        elif opcion.lower() == 'no':
            print(
                c.AMARILLO, "\n[!] Regresando al menu anterior...",
                c.ENDC
            )
            sleep(1.5)
            break

        else:
            c.error("Solo puedes responder Si o No.")


def eliminar_contacto():
    """Activa la opcion de eliminar un contacto a traves de su indice."""

    while True:
        print("""
        {}ADVERTENCIA!!, no es posible recuperar contactos borrados.{}

        {}Para eliminar un contacto debes introducir su id, asegurate de
        saberlo antes de proceder.{}
        """.format(c.ROJO + c.BOLD, c.ENDC, c.VERDE + c.BOLD, c.ENDC))

        opcion = input(c.CYAN + "[DESEAS CONTINUAR?][SI/NO]: " + c.ENDC)

        if opcion.lower() == 'si':
            indice = input(c.VERDE + "[ID]: " + c.ENDC)

            Agenda.eliminar_registro(indice)

        elif opcion.lower() == 'no':
            print(
                c.AMARILLO, "\n[!] Regresando al menu anterior...",
                c.ENDC
            )
            sleep(1.5)
            break

        else:
            c.error("Solo puedes responder Si o No.")


def modificar_contacto():
    """Activa la opcion de modificar un contacto en la agenda."""

    while True:
        print("""
        {}Aqui puedes modificar un contacto atraves de su indice(id)
        asegurate de saber el indice correcto antes de modificar.{}

        {}NOTA: Los cambios no son reversibles.{}
        """.format(c.VERDE + c.BOLD, c.ENDC, c.ROJO + c.BOLD, c.ENDC))

        opcion = input(c.CYAN + "[DESEAS CONTINUAR?][SI/NO]: " + c.ENDC)

        if opcion.lower() == 'si':
            indice = input(c.VERDE + "[ID]: " + c.ENDC)
            nombre = input(c.VERDE + "[NOMBRE]: " + c.ENDC)
            apellido = input(c.VERDE + "[APELLIDO]: " + c.ENDC)
            edad = input(c.VERDE + "[EDAD]: " + c.ENDC)
            telefono = input(c.VERDE + "[TELEFONO]: " + c.ENDC)
            email = input(c.VERDE + "[CORREO]: " + c.ENDC)

            if indice != '' and nombre != '' and apellido != '' and \
                    edad != '' and telefono != '' and email != '':

                modificado = Contacto(nombre, apellido, edad, telefono, email)
                if modificado.es_valido():
                    Agenda.modificar_registro(
                        indice, *modificado.obtener_datos()
                    )
                    c.success(
                        "El contacto con el ID {} se ha modificado!"
                        .format(indice)
                    )

                else:
                    c.error("Verifica los datos, algo anda mal.")
            else:
                c.error("Faltan datos, el contacto no se ha modificado!!")

        elif opcion.lower() == 'no':
            print(
                c.AMARILLO, "\n[!] Regresando al menu anterior...",
                c.ENDC
            )
            sleep(1.5)
            break

        else:
            c.error("Solo puedes responder Si o No.")


def menu_principal():
    """Menu principal de la agenda donde puede interactuarse
    con las opciones principales del programa."""

    while True:
        portada()

        print("""
        ------------------- MENU PRINCIPAL ---------------------

        1 - {uno}
        2 - {dos}
        3 - {tres}
        4 - {cuatro}
        5 - {cinco}
        6 - {seis}
        7 - {siete}
        8 - Salir
        """.format(
                uno=c.VERDE + "[+] Generar el archivo de la agenda." + c.ENDC,

                dos=c.ROJO +
                "[x] Borrar todo el contenido de la agenda." + c.ENDC,

                tres=c.VERDE + "[+] Agregar un nuevo contacto" + c.ENDC,
                cuatro=c.CYAN + "[-] Ver lista de contactos." + c.ENDC,

                cinco=c.AMARILLO +
                "[!] Realizar una busqueda personalizada." + c.ENDC,

                seis=c.ROJO + "[x] Eliminar un contacto." + c.ENDC,
                siete=c.AZUL + "[!=] Modificar un contacto." + c.ENDC
            )
        )

        # capturar la opcion elegida en el menu principal
        opcion = input(c.CYAN + "[ESCOGE UNA OPCION]: " + c.ENDC)

        if opcion.isdecimal():
            if opcion == '1':
                Agenda.crear_agenda()

            elif opcion == '2':
                Agenda.borrar_agenda()

            elif opcion == '3':
                solicitar_contacto()

            elif opcion == '4':
                ver_contactos()

            elif opcion == '5':
                busqueda_personalizada()

            elif opcion == '6':
                eliminar_contacto()

            elif opcion == '7':
                modificar_contacto()

            elif opcion == '8':
                c.success("Cerrando la agenda...")
                break

            else:
                c.error("Opcion desconocida!!")
        else:
            c.error("Caracteres alfabeticos no son bienvenidos aqui!!")
