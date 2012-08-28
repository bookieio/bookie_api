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
