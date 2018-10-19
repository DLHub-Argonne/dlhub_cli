import json
import click

from dlhub_cli.printing import format_output
# from dlhub_cli.config import get_dlhub_client
from dlhub_cli.parsing import dlhub_cmd, index_argument


@dlhub_cmd('init', help='Initialize a DLHub repository')
@click.option('--model',
              default=None, show_default=True,
              help='The model to initialize.')
def init_cmd(model):
    """
    Initialize the model repository. Create the .dlhub directory (if it
    doesn't exist) and use the toolbox to generate a config file for the
    specific model.

    :param model: A particular model to initialize
    :return:
    """
    format_output("Initializing {}".format(model))
    pass