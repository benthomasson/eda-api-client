#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Usage:
    basic_client [options] <server>

Options:
    -h, --help        Show this page
    --debug            Show debug logging
    --verbose        Show verbose logging
    --user=<u>       User [default: admin]
"""
from docopt import docopt
import logging
import sys
import requests
import getpass
import time
from requests.auth import HTTPBasicAuth

logger = logging.getLogger('basic_client')


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = docopt(__doc__, args)
    if parsed_args['--debug']:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    server = parsed_args['<server>']
    user = parsed_args['--user']
    basic = HTTPBasicAuth(user, getpass.getpass())
    start = time.time()
    r = requests.get(f'{server}/api/eda/v1/users/me/', verify=False, auth=basic)
    end = time.time()
    print(r.headers)
    print(r.text)
    print(f'time: {end-start}')

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
