"""Api implementation in Python

"""
import json
import requests


class AdminApi(object):
    """Wrapper for Admin specific Api calls."""
    apikey = None
    apiurl = None
    username = None

    def __init__(self, apiurl, username, apikey):
        """Init the admin api handler. Apikey is required.

        :param apikey: string that's the admin api key

        """
        self.apikey = apikey
        self.username = username
        apiurl = "{apiurl}/a".format(apiurl=apiurl)
        self.apiurl = apiurl

    def _build_url(self, segment):
        """Generate the api url given the call we want to do."""
        return "{0}/{1}?api_key={2}".format(self.apiurl, segment, self.apikey)

    def invite_status(self):
        """Fetch the list of users and their invite counts."""
        segment = "accounts/invites"
        req = requests.get(self._build_url(segment))
        data = json.loads(req.text)
        users = data.get('users')
        for u in users:
            print "{0}\t{1}".format(u[1], u[0])

    def invite_set(self, username, invite_ct):
        """Set the number of invites a user has available."""
        segment = "accounts/invites/{0}/{1}".format(
            username,
            invite_ct
        )
        req = requests.post(self._build_url(segment))
        if req.status_code == 200:
            resp = json.loads(req.text)
            updated_user = resp
            print "{0} updated to {1} invites.".format(
                updated_user.get('username'),
                updated_user.get('invite_ct'))
        else:
            raise LookupError('Invite set request died with: ' + str(req))

    def import_list(self):
        """Fetch the list of imports."""
        segment = "imports/list"
        req = requests.get(self._build_url(segment))
        data = json.loads(req.text)
        imports = data.get('imports')
        for i in imports:
            print "{0}\t{1}\t{2}".format(
                i['status'],
                i['username'],
                i['file_path'])


class UserApi(object):
    """Wrapper for User specific Api calls."""
    apikey = None
    apiurl = None
    username = None

    def __init__(self, apiurl, username, apikey):
        """Init the admin handler. Apikey is required.

        :param apikey: string that's the user's api key

        """
        self.apikey = apikey
        self.username = username
        self.apiurl = apiurl

    def _build_url(self, segment):
        """Generate the api url given the call we want to do."""
        return "{0}/{1}?api_key={2}".format(self.apiurl, segment, self.apikey)

    def ping(self):
        """Fetch the list of users and their invite counts."""
        segment = "{0}/ping".format(self.username)
        req = requests.get(self._build_url(segment))
        data = json.loads(req.text)
        if data.get('success', False):
            print "Ping Results: " + data.get('message',
                'failure to load message from response')
        else:
            print "Ping Results ERROR: " + data.get('error',
                'failure to load message from response')
