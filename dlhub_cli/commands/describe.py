import click

from dlhub_cli.config import get_dlhub_client
from dlhub_cli.printing import format_output
from dlhub_cli.parsing import dlhub_cmd


HELP_STR = """\

  Describe a servable.
\b
Options:
  --id TEXT      The UUID of a servable.
  --name TEXT    The name of a servable.
  -h, --help     Show this message and exit.
  -v, --version  Show the version and exit."""


@dlhub_cmd('describe', help='Describe a servable.')
@click.option('--id',
              show_default=True, required=False,
              help='The UUID of a servable.')
@click.option('--name',
              show_default=True, required=False,
              help='The name of a servable.')
def describe_cmd(id, name):
    """Use DLHub to get a description of the servable.

    Args:
        id (string): The uuid of the servable
        name (string): The name of the servable
    Returns:
        (dict) a set of information regarding the servable
    """

    if not any([id, name]):
        format_output(HELP_STR)
        return

    client = get_dlhub_client()
    res = "Unable to describe a servable (name: {0}, id: {1})".format(name, id)
    if id:
        res = client.describe_servable(servable_id=id)
    elif name:
        res = client.describe_servable(servable_name=name)

    format_output("{0}".format(res))
    return res
