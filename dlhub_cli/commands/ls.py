import json
import click

from dlhub_cli.printing import format_output
# from dlhub_cli.config import get_dlhub_client
from dlhub_cli.parsing import dlhub_cmd, index_argument


@dlhub_cmd('ls', help='List servables in this directory')
def ls_cmd():
    """
    List servables in this directory.

    :return:
    """
    format_output("ls things")
    pass