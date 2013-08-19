#!/usr/bin/env python
"""Using the Admin API to perform handy handy functions.


Ex:


"""
import argparse

from ConfigParser import ConfigParser
from ConfigParser import MissingSectionHeaderError
from os.path import expanduser
from os.path import exists as path_exists

from bookie_api import VERSION
from bookie_api import commands

RCFILE = expanduser('~/.bookierc')


class BookieConfig(object):
    attrs = ['api_key', 'api_url', 'username']

    def __init__(self, rcfile):
        self.cfg = ConfigParser()
        try:
            self.cfg.read(rcfile)
        except MissingSectionHeaderError:
            raise SyntaxError(
                'Make sure your rc file starts with [main] section heading.')

        assert set(self.attrs).issubset(
            set([c[0] for c in self.cfg.items('main')])), \
            'You must supply {0} in your .bookierc config file'.format(
                ", ".join(self.attrs))

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
    parser.add_argument(
        '--version',
        action='version',
        version=VERSION)

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_ping = subparsers.add_parser('ping')
    parser_ping.set_defaults(func=commands.ping)

    # add an applog subcommand
    parser_applog = subparsers.add_parser('applog')
    applog = parser_applog.add_subparsers()

    log_list = applog.add_parser(
        'list',
        help='List the recent applog entries.')
    log_list.add_argument(
        '-d', '--days',
        action='store',
        default=1,
        help='How many days of logs to fetch.')
    log_list.add_argument(
        '-s', '--status',
        action='store',
        default=None,
        help='What log status to filter down to.')
    log_list.add_argument(
        '-f', '--filter',
        action='store',
        default=None,
        help='Filter log messages for the text.')
    log_list.set_defaults(func=commands.applog)

    # add a bmark subcommand
    bmark_invites = subparsers.add_parser('bmark')
    bmarks = bmark_invites.add_subparsers()

    bmark_del = bmarks.add_parser(
        'delete',
        help='Delete a bmark from the system.')
    bmark_del.add_argument(
        'hash_id',
        action='store',
        default=None,
        help='Hash id of the bookmark to delete.')
    bmark_del.add_argument(
        '-u', '--username',
        action='store',
        default=None,
        help='Delete this bookmark from the specified user.')

    bmark_del.set_defaults(func=commands.del_bookmark)

    # add an invite subcommand
    parser_invites = subparsers.add_parser('invite')
    invites = parser_invites.add_subparsers()

    invite_list = invites.add_parser(
        'list',
        help='List the users and their invite counts.')
    invite_list.add_argument(
        '-u', '--username',
        action='store',
        default=None,
        help='Pull the invite count for the specified user.')
    invite_list.set_defaults(func=commands.invite_list)

    invite_set = invites.add_parser(
        'set',
        help='Set the number of invites a user has')
    invite_set.add_argument(
        '--username', '-u',
        dest='username',
        action='store',
        default=None,
        help='The username to set an invite count to.')
    invite_set.add_argument(
        '--invites', '-i',
        dest='invite_ct',
        action='store',
        default=None,
        help='How many invites to give this user.')
    invite_set.set_defaults(func=commands.invite_set)

    # Add an import subcommand.
    parser_imports = subparsers.add_parser('import')
    imports = parser_imports.add_subparsers()

    import_list = imports.add_parser(
        'list',
        help='List the imports.')
    import_list.set_defaults(func=commands.import_list)

    import_reset = imports.add_parser(
        'reset',
        help='Reset an import to start again.')
    import_reset.add_argument(
        '--id', '-i',
        dest='id',
        action='store',
        default=None,
        help='Which id of the import to reset?')
    import_reset.set_defaults(func=commands.import_reset)

    # Add space for a user subcommand.
    parser_users = subparsers.add_parser('user')
    users = parser_users.add_subparsers()

    user_list = users.add_parser(
        'list',
        help='List the users.')
    user_list.set_defaults(func=commands.user_list)

    users_add = users.add_parser(
        'add',
        help='Add a new user to the system manually.')
    users_add.add_argument(
        '--username', '-u',
        dest='username',
        action='store',
        default=None,
        required=True,
        help='The username of the new user.')
    users_add.add_argument(
        '--email', '-e',
        dest='email',
        action='store',
        default=None,
        required=True,
        help='The email address for the new user.')
    users_add.set_defaults(func=commands.user_add)

    users_del = users.add_parser(
        'delete',
        help='Remove a user from the system via admin api.')
    users_del.add_argument(
        '--username', '-u',
        dest='username',
        action='store',
        default=None,
        required=True,
        help='The username of the new user.')
    users_del.set_defaults(func=commands.del_user)

    # add an invite subcommand
    parser_readable = subparsers.add_parser('readable')
    readable = parser_readable.add_subparsers()
    readable_todo = readable.add_parser(
        'todo',
        help='List of the urls that need readable parsing.')
    readable_todo.set_defaults(func=commands.to_readable)
    readable_reindex = readable.add_parser(
        'reindex',
        help='Rebuild the fulltext index of bookmark content.')
    readable_reindex.set_defaults(func=commands.readable_reindex)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    cfg = parse_config(fetch_rc_file())
    args.func(cfg, args)


if __name__ == "__main__":
    main()
