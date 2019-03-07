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
@click.argument('name', default=None)
@click.argument('method', default='')
def methods_cmd(name, method):
    """Print out the methods of a servable

    Args:
        name (string): DLHub name of the servable of the form <user>/<servable_name>
        method (str): Name of the method (optional)
    """

    # Check if name is proper format
    if len(name.split("/")) < 2:
        raise click.BadArgumentUsage('Please enter name in the form <user>/<servable_name>')
    if name.split("/")[0] == "" or name.split("/")[1] == "":
        raise click.BadArgumentUsage('Please enter name in the form <user>/<servable_name>')

    # If the method name is blank, make it None (for compatibility with client)
    if method == '':
        method = None

    # Get the DLHub client
    client = get_dlhub_client()

    # Get the method details
    method_details = client.describe_methods(name, method)

    # Print them in YAML format
    format_output(yaml.dump(method_details, default_flow_style=False))
