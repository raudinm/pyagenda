#!/usr/bin/env python3
from setuptools import setup


def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except IOError:
        return ''


setup(
    name="pyagenda",
    version="0.0.1b4",
    author='Raudin Moreno',
    author_email='raudin247@gmail.com',
    description='Administracion de contacos telefonicos.',
    long_description=get_long_description(),
    url='https://github.com/raudin17/pyagenda',
    scripts=['agenda.py', 'contacto.py', 'menus.py', 'colores.py', 'main.py'],
    entry_points={
        'console_scripts': [
            'main = main:menu_principal'
        ]
    },
    license='License :: OSI Approved :: MIT License',
)
