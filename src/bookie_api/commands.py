from bookie_api.api import AdminApi
from bookie_api.api import UserApi


# #############
# User Commands
# #############
def ping(cfg, args):
    """Perform a ping to check config."""
    api = UserApi(cfg.api_url, cfg.username, cfg.api_key)
    api.ping()


# ###############
# Admin Commands
# ###############
def invite_list(cfg, args):
    """Handle the invite list call."""
    api = AdminApi(cfg.api_url, cfg.username, cfg.api_key)
    api.invite_status()


def invite_set(cfg, args):
    """Handle the invite set call to add invites to a user."""
    api = AdminApi(cfg.api_url, cfg.username, cfg.api_key)
    api.invite_set(args.username, args.invite_ct)


def import_list(cfg, args):
    """Fetch some data """
    api = AdminApi(cfg.api_url, cfg.username, cfg.api_key)
    api.import_list()


def user_list(cfg, args):
    """List the users in the system."""
    api = AdminApi(cfg.api_url, cfg.username, cfg.api_key)
    api.user_list()

def user_add(cfg, args):
    """Add a new user to the system."""
    api = AdminApi(cfg.api_url, cfg.username, cfg.api_key)
    api.new_user(args.username, args.email)

def del_user(cfg, args):
    """Remove a user from the system."""
    api = AdminApi(cfg.api_url, cfg.username, cfg.api_key)
    api.del_user(args.username)
