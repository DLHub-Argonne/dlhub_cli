import click

from dlhub_cli.printing import format_output

from dlhub_cli.parsing import dlhub_cmd, index_argument


@dlhub_cmd('update', help='Update a servables metadata')
@click.option('--servable',
              default=None, show_default=True,
              help='The servable to update.')
def update_cmd(servable):
    """Update the servable

    Args:
        servable (string): The uuid of the servable to update
    Returns:
        (none) None.
    """
    format_output("Update {}".format(servable))
    pass