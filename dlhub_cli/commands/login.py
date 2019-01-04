import click
from dlhub_sdk.config import check_logged_in
from dlhub_sdk.utils.auth import do_login_flow


@click.command('login',
               short_help=('Log into Globus to get credentials for '
                           'the DLHub CLI'),
               help=('Get credentials for the DLHub CLI. '
                     "Necessary before any 'dlhub' commands which "
                     'require authentication to work'))
@click.option('--force', is_flag=True,
              help='Do a fresh login, ignoring any existing credentials')
def login_cmd(force):
    """Perform a globus login. If forced, start the flow regardless of if they are already logged in.

    Args:
        force (bool): Whether or not to force the login.
    """

    if force or not check_logged_in():
        do_login_flow()
