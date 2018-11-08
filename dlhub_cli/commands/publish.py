import os
import click
import pickle as pkl

from dlhub_cli.config import get_dlhub_directory, get_dlhub_client, check_logged_in
from dlhub_cli.printing import format_output, safeprint
from dlhub_cli.parsing import dlhub_cmd


_LOGIN_MSG = (u"""\

You must be logged in to perform this function.

Login to the DLHub CLI with
  dlhub login
""")


@dlhub_cmd('publish', help='Publish a servable to DLHub.')
@click.option('--servable',
              default=None, show_default=True,
              help='The servable to publish.')
def publish_cmd(servable):
    """
    Publish a model to DLHub. Read the description file from the .dlhub directory
    and send a publication request to DLHub.

    :param servable: A particular servable to publish
    :return:
    """


    if not check_logged_in():
        safeprint(_LOGIN_MSG)
        return

    format_output("Publishing {}".format(servable))
    loaded_servable = None
    dlhub_directory = get_dlhub_directory()

    if servable:
        servable_path = os.path.join(dlhub_directory, servable + ".pkl")
        format_output(servable_path)
        try:
            with open(servable_path, 'rb') as fp:
                loaded_servable = pkl.load(fp)
        except IOError as e:
            format_output("I/O error({0}): {1}".format(e.errno, e))
        except FileNotFoundError as e:
            format_output("FileNotFound error ({0}) {1}:".format(e, servable))
        except Exception as e:
            format_output("Exception ({0})".format(e))

    if not loaded_servable:
        format_output("Failed to load servable.")
        return

    client = get_dlhub_client()
    res = client.publish_servable(loaded_servable)

    format_output("Task_id: {}".format(res))
