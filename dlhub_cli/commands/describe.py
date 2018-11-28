import click

from dlhub_cli.config import get_dlhub_client
from dlhub_cli.printing import format_output
from dlhub_cli.parsing import dlhub_cmd


@dlhub_cmd('describe', help='Describe a servable.')
@click.option('--id',
              show_default=True, required=False,
              help='The UUID of a servable.')
@click.option('--name',
              show_default=True, required=False,
              help='The name of a servable.')
def describe_cmd(id, name):
    """
    Use DLHub to get a description of the servable.

    :param id: The uuid of a servable
    :param name: The uuid of a servable
    :return:
    """

    client = get_dlhub_client()
    res = "Unable to describe a servable (name: {0}, id: {1})".format(name, id)
    if id:
        res = client.describe_servable(servable_id=id)
    elif name:
        res = client.describe_servable(servable_name=name)

    format_output("{0}".format(res))
