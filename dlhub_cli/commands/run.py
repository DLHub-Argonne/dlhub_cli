import json
import click

from dlhub_cli.printing import format_output, safeprint
from dlhub_cli.config import (get_dlhub_client, check_logged_in)
from dlhub_cli.parsing import dlhub_cmd


_LOGIN_MSG = (u"""\

You must be logged in to perform this function.

Login to the DLHub CLI with
  dlhub login
""")


@dlhub_cmd('run', help='Invoke a servable')
@click.option('--servable',
              default=None, show_default=True, required=False,
              help='The servable to invoke.')
@click.option('--servable-uuid',
              default=None, show_default=True, required=False,
              help='The uuid of the servable to invoke.')
@click.option('--input',
              default=None, show_default=True, required=False,
              help='Input to pass to the servable.')
@click.option('--test',
              is_flag=True,
              help='Flag whether or not to invoke the servable\'s test function.')
def run_cmd(servable, servable_uuid, input, test):
    """
    Invoke a servable.

    :param servable: The servable to invoke
    :param servable_uuid: The uuid of the servable to invoke
    :param input: Input to pass into the servable
    :param test: Whether or not to use the test function
    :return:
    """

    if not check_logged_in():
        safeprint(_LOGIN_MSG)
        return

    format_output("Running {}".format(servable))

    if test:
        format_output("Invoking test function")

    client = get_dlhub_client()

    data = json.loads(input)

    res = client.run(servable_uuid, data)

    format_output(res)