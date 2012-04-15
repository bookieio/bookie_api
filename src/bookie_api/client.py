#!/usr/bin/env python
"""Using the Admin API to perform handy handy functions.


Ex:


"""
import argparse

from ConfigParser import ConfigParser
from ConfigParser import MissingSectionHeaderError
from os.path import expanduser
from os.path import exists as path_exists

from api import AdminApi
from bookie_api import VERSION
from bookie_api import commands

RCFILE = expanduser('~/.bookierc')

class BookieConfig(object):
    def __init__(self, rcfile):
        self.cfg = ConfigParser()
        try:
            self.cfg.read(rcfile)
        except MissingSectionHeaderError, exc:
            raise SyntaxError(
                'Make sure your rc file starts with [main] section heading.')

    def __getattr__(self, attr):
        return self.cfg.get('main', attr)


def fetch_rc_file():
    """Load the config data from your rc file.

    The rc file defaults to looking in ~/.bookierc

    :param allow_absent: If we don't care if the file exists...say we have a
    -f flag that specifies a config file, then just skip.

    """
    if not path_exists(RCFILE):
        raise IOError('Could not find a rc file at: ' + RCFILE)
    else:
        return RCFILE


def parse_config(config):
    """Process the config text into a config object we can use."""
    cfg = BookieConfig(config)
    return cfg


def parse_args():
    """Handle building what we want to do based on the arguments.

    Examples:
        api.py invites list
        api.py invites set -u username -c 10
        api.py accounts list --inactive
        api.py readable list --todo

    """
    desc = """Command line client for the Bookie bookmark service.

    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--version',
        action='version', version=VERSION)

    subparsers = parser.add_subparsers(help='sub-command help')

    # add an invite subcommand
    invite_help = "Get or set invite data."

    # create the parser for the "foo" command
    parser_invites = subparsers.add_parser('invite')
    invites = parser_invites.add_subparsers()

    invite_list = invites.add_parser('list',
        help='List the users and their invite counts.')
    invite_list.add_argument('-u', '--username', action='store', default=None,
            help='Pull the invite count for the specified user.')
    invite_list.set_defaults(func=commands.invite_list)

    invite_set = invites.add_parser('set',
        help='Set the number of invites a user has')
    invite_set.add_argument('--username', '-u',
        dest='username',
        action='store',
        default=None,
        help='The username to set an invite count to.')
    invite_set.add_argument('--invites', '-i',
        dest='invite_ct',
        action='store',
        default=None,
        help='How many invites to give this user.')
    invite_set.set_defaults(func=commands.invite_set)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    cfg = parse_config(fetch_rc_file())
    args.func(cfg, args)


if __name__ == "__main__":
    main()
