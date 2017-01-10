#!/usr/bin/python3
# Cambia el valor de la etiqueta placement en el rc.xml de openbox

import xml.etree.ElementTree as ET
from os import environ, system
from sys import argv

argc = len(argv)

home = environ['HOME']
rc = home + '/.config/openbox/rc.xml'
me = 'openbox-tool-placement.py'

tree = ET.parse(rc)
root = tree.getroot()

valid_keys = {
    'policy': ('smart', 'undermouse'),
    'center':('yes', 'no'),
    'monitor': ('Any',)
    }

def validate(key, value):
    if key not in valid_keys:
        gen_error(key + ' no es una llave válida')
    if value not in valid_keys[key]:
        gen_error(value + ' no es un valor válido para ' + key)


def gen_error(string):
    print(string)
    exit(1)


def set_placement(key, value):
    for placement in root.findall('placement'):
        placement.find(key).text = str(value)

    tree.write(rc)
    system('openbox --reconfigure')


def gen_menu():
    openbox = []
    icondir = environ['OPENBOX_ICONDIR']
    ext = '.svg'

    openbox.append('<openbox_pipe_menu>')

    for key in valid_keys:
        openbox.append(
            '<menu id="obplacement-' + key
            + '" label="' + key
            + '" icon="' + icondir + '/' + 'terminal' + ext
            + '">')
        for placement in root.findall('placement'):
            current = placement.find(key).text
        for value in valid_keys[key]:
            check = '☐'
            if value == current:
                check = '☑'
            execute = me + ' ' + key + ' ' + value
            openbox.append(
                '<item label="' + check + ' ' + value +
        '"><action name="Execute"><execute>' + execute +
        '</execute></action></item>')
        openbox.append('</menu>')
    openbox.append('</openbox_pipe_menu>')

    return(openbox)


if argc == 1:
    menu = gen_menu()
    for i in menu:
        print(i)
elif argc == 3:
    validate(argv[1], argv[2])
    set_placement(argv[1], argv[2])
else:
    print('Fuck you')
