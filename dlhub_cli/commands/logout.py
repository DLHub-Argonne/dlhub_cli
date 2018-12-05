import click

from dlhub_cli.config import get_dlhub_client

@click.command('logout',
               short_help='Logout of the DLHub CLI',
               help=('Logout of the DLHub CLI. '
                     'Removes your Globus tokens from local storage, '
                     'and revokes them so that they cannot be used anymore'))
@click.confirmation_option(prompt='Are you sure you want to logout?',
                           help='Automatically say "yes" to all prompts')
def logout_cmd():
    """Logout of the dlhub client.

    Returns:
        (None) None
    """
    client = get_dlhub_client()

    client.logout()