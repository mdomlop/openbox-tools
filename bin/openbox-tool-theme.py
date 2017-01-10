#!/usr/bin/python3
# Cambia el tema en el rc de openbox
# 2015.01.26.09.03

import xml.etree.ElementTree as ET
from os import environ, system, path
from sys import argv, stderr
from glob import glob

argc = len(argv)

home = environ['HOME']
rc = home + '/.config/openbox/rc.xml'
me = 'openbox-theme.py'


tree = ET.parse(rc)
root = tree.getroot()


def gen_error(string=''):
    print(string, file=stderr)
    exit(1)


def validate(theme):
    #theme = home + '/.themes/' + theme + '/openbox-3/themerc'
    theme = '/usr/share/themes/' + theme + '/openbox-3/themerc'
    if not path.isfile(theme):
        gen_error(theme + ' no es un tema válido.')


def set_theme(value):
    for theme in root.findall('theme'):
        theme.find('name').text = str(value)

    tree.write(rc)
    system('openbox --reconfigure')


def get_theme_names():
    #themes = glob(home + '/.themes/*/openbox-3') + glob('/usr/share/themes/*/openbox-3')
    #themes = glob(home + '/.themes/*/openbox-3')
    themes = glob('/usr/share/themes/*/openbox-3')
    names = [path.basename(path.dirname(i)) for i in themes]
    return(names)


def gen_menu():
    openbox = []
    icondir = environ['OPENBOX_ICONDIR']
    ext = '.png'

    openbox.append('<openbox_pipe_menu>')

    for i in root.findall('theme'):
        current = i.find('name').text

        execute = me + current
        check = '☑'
        openbox.append(
        '<item label="' + check + ' ' + current + '">'
        + '<action name="Execute"><execute>' + execute
        + '</execute></action></item>'
        + '<separator/>')

    for value in sorted(get_theme_names()):
        check = '☐'
        if value == current:
            continue
        execute = me + ' ' + value
        openbox.append(
        '<item label="' + check + ' ' + value + '">'
        + '<action name="Execute"><execute>' + execute
        + '</execute></action>'
        + '</item>')
    openbox.append('</openbox_pipe_menu>')

    return(openbox)


if argc == 1:
    '''Si no hay argumentos imprime el menú para openbox.'''
    menu = gen_menu()
    for i in menu:
        print(i)
elif argc == 2:
    '''Con un argumento aplica dicho argumento como tema.'''
    theme = argv[1]
    validate(theme)
    set_theme(theme)
else:
    gen_error('Sólo se permite de 0  a 1 argumentos.')
