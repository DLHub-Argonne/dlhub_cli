import json
import click

from dlhub_cli.printing import format_output
# from dlhub_cli.config import get_dlhub_client
from dlhub_cli.parsing import dlhub_cmd, index_argument


@dlhub_cmd('run', help='Invoke a servable')
@click.option('--servable',
              default=None, show_default=True,
              help='The servable to invoke.')
def run_cmd(servable):
    """
    Invoke the servable

    :param servable: The servable to invoke
    :return:
    """
    format_output("Running {}".format(servable))
    pass