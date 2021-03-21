#!/usr/bin/env python3

import line
from argparse import ArgumentParser
from capture import record
from upload import upload


arg_parser = ArgumentParser(
    usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
)
arg_parser.add_argument('-p', '--port', default=8000, help='port')
options = arg_parser.parse_args()

line.app.run(port=options.port)

# record()
# upload()