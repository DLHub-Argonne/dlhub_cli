import click

from dlhub_cli.parsing import dlhub_cmd
from dlhub_cli.config import get_dlhub_client


@dlhub_cmd('whoami',
               help='Get the username of logged in user')
def whoami_cmd():
    """Perform a globus login. If forced, start the flow regardless of if they are already logged in.

    Args:
        force (bool): Whether or not to force the login.
    """

    client = get_dlhub_client()
    click.echo(client.get_username())
