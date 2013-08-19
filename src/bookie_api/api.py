"""Api implementation in Python

"""
import json
import requests
from urllib import urlencode

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

    def _build_url(self, segment, data=None):
        """Generate the api url given the call we want to do."""
        if data:
            remove = []
            # First remove any None values from the qs.
            for key, val in data.iteritems():
                if val is None:
                    remove.append(key)
            for key in remove:
                del data[key]
            data['api_key'] = self.apikey
        else:
            data = {
                'api_key': self.apikey

            }
        qs = urlencode(data)
        return "{0}/{1}?{2}".format(self.apiurl, segment, qs)

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

    def applog(self, days, status, message_filter):
        """Fetch the applog entries we want to see."""
        segment = 'applog/list'
        req = requests.get(
            self._build_url(
                segment, {
                    'days': days,
                    'status': status,
                    'message': message_filter
                }
            )
        )

        data = json.loads(req.text)
        if req.status_code != 200:
            print data.get('error')
        else:
            logs = data['logs']
            t = self._build_table('user', 'status', 'message', 'payload')
            for l in logs:
                t.add_row([
                    l['user'],
                    l['status'],
                    l['message'],
                    l['payload']])
            print t

    def to_readable(self):
        """Return a list of urls that we need to parse for content."""
        segment = 'readable/todo'
        req = requests.get(self._build_url(segment))
        data = json.loads(req.text)
        urls = data.get('urls')

        t = self._build_table('username', 'imported', 'url')
        for u in urls:
            t.add_row([u['username'], u['stored'], u['url'].strip(" ")])
        print(t)

    def readable_reindex(self):
        """Reindex all bookmarks in the system."""
        segment = 'readable/reindex'
        req = requests.get(self._build_url(segment))
        data = json.loads(req.text)
        success = data.get('success')

        if success:
            print "Started"
        else:
            print "Error: " + str(success)

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

        t = self._build_table('id', 'status', 'username', 'file_path')
        for i in imports:
            t.add_row([i['id'], i['status'], i['username'], i['file_path']])

        print(t)

    def import_reset(self, import_id):
        """Reset the specified import"""
        segment = "imports/reset/{0}".format(import_id)
        req = requests.post(self._build_url(segment))
        data = json.loads(req.text)
        imp = data.get('import')

        t = self._build_table('id', 'status', 'username', 'file_path')
        t.add_row(
            [imp['id'], imp['status'], imp['username'], imp['file_path']])
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


class BmarkApi(object):
    """Wrapper for Bmark specific Api calls."""
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

    def delete(self, username, hash_id, is_admin=False):
        """Delete the user via the api call."""
        if not is_admin:
            segment = "{username}/bmark/{hash_id}"
        else:
            segment = "a/bmark/{username}/{hash_id}"

        print self._build_url(segment.format(
            username=username,
            hash_id=hash_id,
        ))

        req = requests.delete(self._build_url(segment.format(
            username=username,
            hash_id=hash_id,
        )))

        data = json.loads(req.text)
        if data.get('message', False):
            print "Delete Results: " + data.get(
                'message',
                'failure to load message from response')
        else:
            print "Delete Results ERROR: " + data.get(
                'error',
                'failure to load message from response')


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
            print "Ping Results: " + data.get(
                'message',
                'failure to load message from response')
        else:
            print "Ping Results ERROR: " + data.get(
                'error',
                'failure to load message from response')
