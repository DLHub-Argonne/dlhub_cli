import os
import json
import click
import pickle as pkl

from dlhub_cli.config import get_dlhub_client
from dlhub_cli.printing import format_output, safeprint
from dlhub_cli.parsing import dlhub_cmd

from dlhub_sdk.utils import unserialize_object

HELP_STR = """\

  Publish a servable to DLHub.
\b
Options:
  --local            A flag to signify publishing a servable in the local
                     directory. This requires a dlhub.json file exist locally.
  --repository TEXT  The repository to publish.
  -h, --help         Show this message and exit.
  -v, --version      Show the version and exit."""


@dlhub_cmd('publish', help='Publish a servable to DLHub.')
@click.option('--local', is_flag=True,
              help='A flag to signify publishing a servable in the local directory. '
                   'This requires a dlhub.json file exist locally.')
@click.option('--repository',
              default=None, show_default=True,
              help='The repository to publish.')
def publish_cmd(local, repository):
    """Publish a model to DLHub. Either a metadata description file for a local servable or a remote github address.
    The servable's metadata will be sent to the DLHub service.

    If using a local servable the files described in the
    metadata's 'files' field will be zipped into a tmp archive and staged to S3. An ingestion pipeline will then
    download the data from S3, build the servable, and publish the servable to DLHub.

    When using a repository the github url is passed to a specific publish_repo endpoint on DLHub. This will
    use repo2docker to build the servable and publish it.

    Args:
        servable (string): A particular servable to publish.
        repository (string): A github repository that will be built and published by DLHub.
    Returns:
        (string) Task uuid.
    """

    if not any([local, repository]):
        format_output(HELP_STR)
        return

    loaded_servable = None

    client = get_dlhub_client()
    res = None
    if local:
        # Read the dlhub.json
        config = None
        try:
            with open('dlhub.json', 'r') as json_data:
                config = json.load(json_data)
        except IOError as e:
            format_output("I/O error({0}): {1}".format(e.errno, e))
        except FileNotFoundError as e:
            format_output("FileNotFound error ({0})".format(e))
        except Exception as e:
            format_output("Exception ({0})".format(e))
        if not config:
            format_output("Failed to load servable.")
            return

        model = unserialize_object(config)
        res = client.publish_servable(model)
        format_output("Task_id: {}".format(res))

    elif repository:
        res = client.publish_repository(repository)
        format_output("Task_id: {}".format(res))
    return res




