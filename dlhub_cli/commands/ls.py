import os
import json

from dlhub_cli.printing import format_output
from dlhub_cli.config import get_dlhub_directory
from dlhub_cli.parsing import dlhub_cmd, index_argument


@dlhub_cmd('ls', help='List servables in this directory')
def ls_cmd():
    """
    List servables that have been init'd in this directory.

    :return:
    """
    format_output("Servables:")

    dlhub_directory = get_dlhub_directory()

    # List the set of servables in the dlhub directory.
    servables = [serv_file for serv_file in os.listdir(dlhub_directory) if serv_file.endswith('.json')]

    for serv in servables:
        res = serv.split(".json")[0]
        format_output(res)
