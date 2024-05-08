#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Usage:
    session_client [options] <server>

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

logger = logging.getLogger('session_client')


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
    s = requests.Session()
    s.verify = False
    print(s.cookies.get_dict())
    start = time.time()
    r = s.get(f'{server}/api/eda/v1/auth/session/login/')
    end = time.time()
    print(f'csrf time: {end-start}')
    print(r.headers)
    print(r.text)
    print(s.cookies.get_dict())
    s.headers.update({'X-CSRFToken': s.cookies.get_dict()['csrftoken']})
    password = getpass.getpass()
    start = time.time()
    r2 = s.post(f'{server}/api/eda/v1/auth/session/login/', data=dict(username=user, password=password))
    end = time.time()
    print(f'auth time: {end-start}')
    print(r2.headers)
    print(r2.text)
    print(s.cookies.get_dict())
    start = time.time()
    r = s.get(f'{server}/api/eda/v1/users/me/')
    end = time.time()
    print(r.headers)
    print(r.text)
    print(f'me time: {end-start}')

    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
