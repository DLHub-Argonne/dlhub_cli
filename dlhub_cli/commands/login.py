import click
import platform
from dlhub_cli.printing import safeprint
from dlhub_cli.config import (
    DLHUB_AT_OPTNAME, DLHUB_AT_EXPIRES_OPTNAME, DLHUB_RT_OPTNAME,
    lookup_option, write_option,
    internal_auth_client, check_logged_in)


SEARCH_ALL_SCOPE = 'urn:globus:auth:scope:search.api.globus.org:all'

_SHARED_EPILOG = ("""\

Logout of the DLHub CLI with
  dlhub logout
""")

_LOGIN_EPILOG = (u"""\

You have successfully logged in to the DLHub CLI
""") + _SHARED_EPILOG

_LOGGED_IN_RESPONSE = ("""\
You are already logged in!

You may force a new login with
  dlhub login --force
""") + _SHARED_EPILOG


def _store_config(token_response):
    """
    Store the tokens on disk.

    :param token_response:
    :return:
    """
    tkn = token_response.by_resource_server

    search_at = tkn['search.api.globus.org']['access_token']
    search_rt = tkn['search.api.globus.org']['refresh_token']
    search_at_expires = tkn['search.api.globus.org']['expires_at_seconds']

    write_option(DLHUB_RT_OPTNAME, search_rt)
    write_option(DLHUB_AT_OPTNAME, search_at)
    write_option(DLHUB_AT_EXPIRES_OPTNAME, search_at_expires)

    safeprint(_LOGIN_EPILOG)


def _revoke_current_tokens(native_client):
    for token_opt in (DLHUB_RT_OPTNAME, DLHUB_AT_OPTNAME):
        token = lookup_option(token_opt)
        if token:
            native_client.aotuh2_revoke_token(token)


def _do_login_flow():
    """
    Do the globus native client login flow.
    :return:
    """

    # get the NativeApp client object
    native_client = internal_auth_client()

    label = platform.node() or None
    native_client.oauth2_start_flow(
        requested_scopes=SEARCH_ALL_SCOPE,
        refresh_tokens=True, prefill_named_grant=label)
    linkprompt = 'Please log into Globus here'
    safeprint('{0}:\n{1}\n{2}\n{1}\n'
              .format(linkprompt, '-' * len(linkprompt),
                      native_client.oauth2_get_authorize_url()))
    auth_code = click.prompt(
        'Enter the resulting Authorization Code here').strip()
    tkn = native_client.oauth2_exchange_code_for_tokens(auth_code)
    _revoke_current_tokens(native_client)
    _store_config(tkn)


@click.command('login',
               short_help=('Log into Globus to get credentials for '
                           'the DLHub CLI'),
               help=('Get credentials for the DLHub CLI. '
                     "Necessary before any 'dlhub' commands which "
                     'require authentication to work'))
@click.option('--force', is_flag=True,
              help='Do a fresh login, ignoring any existing credentials')
def login_cmd(force):
    """
    Perform a globus login. If forced, start the flow regardless of if they are already logged in.
    :param force:
    :return:
    """
    if not force and check_logged_in():
        safeprint(_LOGGED_IN_RESPONSE)
        return

    _do_login_flow()