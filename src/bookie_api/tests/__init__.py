from nose.tools import eq_

from bookie_api.api import AdminApi


def test_api_url():
    """First simple test, check build_url"""
    api_url = 'https://bmark.us/api/v1'
    username = 'admin'
    api_key = '123456'
    segment = 'invite'
    api = AdminApi(api_url, username, api_key)

    eq_('https://bmark.us/api/v1/a/invite?api_key=123456',
        api._build_url(segment),
        'The build url should be generated correctly.')
