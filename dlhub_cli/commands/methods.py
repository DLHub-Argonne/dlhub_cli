import yaml
import click

from dlhub_cli.parsing import dlhub_cmd
from dlhub_cli.printing import format_output
from dlhub_cli.config import get_dlhub_client


@dlhub_cmd('methods', short_help='Print method information',
           help='''Print methods for a certain servable

           OWNER is the username of the servable owner, NAME is the name of the servable.
           METHOD is optional. If provided, this command will only print the information
           for the method with that name. Otherwise, it will print the information for all
           methods implemented by the servable.

           You can optionally specify the servable name is owner_name/model_name format
           ''')
@click.argument('owner', default=None)
@click.argument('name', default='')
@click.argument('method', default='')
def methods_cmd(owner, name, method):
    """Print out the methods of a servable

    Args:
        owner (str): Name of the servable's owner
        name (str): Name of the servable
        method (str): Name of the method (optional)
    """

    # Check if the owner sent model information in owner/model format
    if '/' in owner:
        # Get the owner and model name
        temp = owner.split('/')
        if len(temp) != 2:
            raise click.BadArgumentUsage('Expected owner_name/model_name format')

        # If "name" is provided, it is actually the method name
        if name != '':
            method = name

        owner, name = temp

    # Make sure the name was provided
    if name == '':
        raise click.BadArgumentUsage('Model name not provided')

    # If the method name is blank, make it None (for compatibility with client)
    if method == '':
        method = None

    # Get the DLHub client
    client = get_dlhub_client()

    # Get the method details
    method_details = client.describe_methods(owner, name, method)

    # Print them in YAML format
    format_output(yaml.dump(method_details, default_flow_style=False))
