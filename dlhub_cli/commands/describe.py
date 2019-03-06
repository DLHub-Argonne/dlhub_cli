from datetime import datetime
import click
import yaml

from dlhub_cli.config import get_dlhub_client
from dlhub_cli.printing import format_output
from dlhub_cli.parsing import dlhub_cmd


_unwanted_fields = [
    ('dlhub', 'build_location'),
    ('dlhub', 'ecr_arn'),
    ('dlhub', 'ecr_uri'),
    ('dlhub', 'id'),
    ('dlhub', 'transfer_method'),
    ('dlhub', 'user_id')
]


def _remove_field(metadata, field):
    """Remove a certain field from the metadata

    Args:
        metadata (dict): Metadata to be pruned
        field ([string]): Coordinates of fields to be removed
    """

    if len(field) == 1:
        if field[0] in metadata:
            del metadata[field[0]]
    else:
        if field[0] in metadata:
            subset = metadata[field[0]]
            return _remove_field(subset, field[1:])


def _preprocess_metadata(metadata):
    """Clean up a metadata record to make it more useful to humans

    Args:
         metadata (metadata): Metadata record to be cleaned
    """
    # Prune internal-only fields
    for field in _unwanted_fields:
        _remove_field(metadata, field)

    # Turn Timestamp (epoch time in ms) into a String
    metadata['dlhub']['publication_date'] = \
        datetime.fromtimestamp(int(metadata['dlhub']['publication_date']) / 1000) \
        .strftime('%Y-%m-%d %H:%M')


@dlhub_cmd('describe', short_help="Get the description of a servable",
           help="""Get the description of a servable

           OWNER is the username of the owner of the servable, and NAME is the name of the servable.

           You can optionally specify both owner and servable name as a single argument using
           a "owner_name/servable_name" format
           """)
@click.argument('name', default=None)
def describe_cmd(name):
    """Use DLHub to get a description of the servable.

    Args:
        name (string): DLHub name of the servable of the form <user>/<servable_name>
    Returns:
        (dict) a set of information regarding the servable
    """

    # Check if name is proper format
    if len(name.split("/")) < 2:
        raise click.BadArgumentUsage('Please enter name in the form <user>/<servable_name>')

    # Retrieve the metadata
    client = get_dlhub_client()
    res = client.describe_servable(name)

    # Clean up the metadata fields
    _preprocess_metadata(res)

    # Print it to screen
    format_output(yaml.dump(res))
    return res
