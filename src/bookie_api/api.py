"""Api implementation in Python

"""
import json
import requests


class AdminApi(object):
    """Wrapper for Admin specific Api calls."""
    apikey = None
    server = None
    uesrname = None

    def __init__(self, username, apikey):
        """Init the admin api handler. Apikey is required.

        :param apikey: string that's the admin api key

        """
        self.apikey = apikey
        self.username = username
        self.server = 'https://bmark.us/api/v1/a'

    def _build_url(self, segment):
        """Generate the api url given the call we want to do."""
        return "{0}/{1}?api_key={2}".format(self.server, segment, self.apikey)

    def invite_status(self):
        """Fetch the list of users and their invite counts."""
        segment = "accounts/invites"
        req = requests.get(self._build_url(segment))
        data = json.loads(req.text)
        users = data.get('users')
        for u in users:
            print "{0}\t{1}".format(u[1], u[0])
