"""Api implementation in Python

"""
import json
import requests

from prettytable import PrettyTable


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

    @classmethod
    def _build_table(cls, *args):
        """Create a pretty table with the list of fields supplied.

        :param fields: list of columns of data

        """
        table = PrettyTable(args)
        table.border = False
        table.header = False
        table.align = 'l'

        return table

    def invite_status(self):
        """Fetch the list of users and their invite counts."""
        segment = "accounts/invites"
        req = requests.get(self._build_url(segment))
        data = json.loads(req.text)
        users = data.get('users')
        t = self._build_table('invite_ct', 'username')
        for u in users:
            t.add_row([u[1], u[0]])

        print(t)

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

        t = self._build_table('status', 'username', 'file_path')
        for i in imports:
            t.add_row([i['status'], i['username'], i['file_path']])

        print(t)

    def user_list(self):
        """Fetch the list of users."""
        segment = "users/list"
        req = requests.get(self._build_url(segment))
        data = json.loads(req.text)
        users = data.get('users')

        t = self._build_table('username', 'name', 'email')
        for i in users:
            t.add_row([i['username'], i['name'], i['email']])

        print(t)

    def new_user(self, username, email):
        """Handle adding a new user to the system.

        """
        segment = "users/add"
        req = requests.post(self._build_url(segment), {
            'username': username,
            'email': email,
        })
        data = json.loads(req.text)

        if req.status_code != 200:
            print data.get('error')
        else:
            user = data
            print user['username'], user['random_pass']

    def del_user(self, username):
        """Remove a user from the system via the admin api."""
        segment = "users/delete/{0}".format(username)
        req = requests.delete(self._build_url(segment))
        data = json.loads(req.text)

        if req.status_code != 200:
            print data.get('error')
        else:
            print data['message']



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
