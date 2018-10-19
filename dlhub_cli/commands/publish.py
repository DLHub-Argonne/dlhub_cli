import json
import click

from dlhub_cli.printing import format_output
# from dlhub_cli.config import get_dlhub_client
from dlhub_cli.parsing import dlhub_cmd, index_argument


@dlhub_cmd('publish', help='Publish a model to DLHub.')
@click.option('--model',
              default=None, show_default=True,
              help='The model to publish.')
def publish_cmd(model):
    """
    Publish a model to DLHub.

    :param model: A particular model to publish
    :return:
    """
    format_output("Publishing {}".format(model))
    pass