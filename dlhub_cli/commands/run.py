import json
import click

from dlhub_cli.printing import format_output, safeprint
from dlhub_cli.config import (get_dlhub_client)
from dlhub_cli.parsing import dlhub_cmd

# @click.option('--servable-uuid',
#               default=None, show_default=True, required=False,
#               help='The uuid of the servable to invoke.')
# @click.option('--test',
#               is_flag=True,
#               help='Flag whether or not to invoke the servable\'s test function.')

@dlhub_cmd('run', help='Invoke a servable')
@click.option('--servable',
              default=None, show_default=True, required=False,
              help='The servable to invoke.')
@click.option('--input',
              default=None, show_default=True, required=False,
              help='Input to pass to the servable.')
def run_cmd(servable, input):
    """Invoke a servable. The input data will be read with json.loads(input) and passed to the servable.

    Args:
        servable (string): The servable to invoke
        input (dict): Input to pass into the servable
    Returns:
        (dict) resulting data. The output from executing the servable.
    """

    client = get_dlhub_client()

    data = json.loads(input)

    res = client.run(servable, data)

    format_output(res)
    return res