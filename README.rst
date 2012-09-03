Bookie Api and Command Line Client
===================================

This is a python implementation of the `Bookie`_ api and a command line client
to interact with our Bookie installation.

Commands
--------
The initial commands are admin related I need to help run and operate the
https://bmark.us installation.


Getting Started
---------------
You need to create a `.bookierc` in your home directory with your username,
api key, and api url for the site.

::

    [main]
    username=admin
    api_key=12345678
    api_url=https://bmark.us/api/v1

Commands
--------

::

    # check out the help for each command level
    $ bookie --help
    $ bookie invite --help
    $ bookie invite set --help

    # check your configuration by making a ping request
    $ bookie ping

    # Invite commands
    $ bookie invite list

    # set 'someuser' to have 10 invites
    $ bookie invite set -u someuser -i 10

    # Import commands
    $ bookie import list

    # User Commands
    $ bookie user list
    $ bookie user add -u testing -e testing@gmail.com
    $ bookie user delete -u testing


.. _Bookie: http://github.com/mitechie/Bookie
