#!/usr/bin/env python3

import line
from line_create_rich_menu import create_rich_menu
from argparse import ArgumentParser

create_rich_menu()

arg_parser = ArgumentParser(
    usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
)
arg_parser.add_argument('-p', '--port', default=8000, help='port')
options = arg_parser.parse_args()

line.app.run(port=options.port, host="0.0.0.0")
