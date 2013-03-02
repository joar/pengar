import logging

from argparse import ArgumentParser

from . import commands

import config

_log = logging.getLogger(__name__)

def get_commands():
    return commands.__all__


def main():
    # Set up logging
    _log.setLevel(logging.INFO)
    logging.basicConfig()

    parser = ArgumentParser(epilog='Created with <3 by Joar Wandborg')
    parser.add_argument(
        'action',
        metavar='command',
        type=str,
        help='One of {0}'.format(', '.join(get_commands())))

    args = parser.parse_args()

    if args.action and hasattr(commands, args.action):
        return getattr(commands, args.action)()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
