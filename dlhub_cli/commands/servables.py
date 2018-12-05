import click

from dlhub_cli.config import get_dlhub_client
from dlhub_cli.printing import format_output
from dlhub_cli.parsing import dlhub_cmd


@dlhub_cmd('servables', help='List the available servables.')
def servables_cmd():
    """List the available servables.

    Returns:
        (dict) the list of available servables as (uuid, name) pairs.
    """

    client = get_dlhub_client()
    res = client.list_servables()

    format_output("{0}".format(res))
    return res