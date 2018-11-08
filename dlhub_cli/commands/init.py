import os
import json
import click
import pickle as pkl

from dlhub_cli.printing import format_output
from dlhub_cli.config import get_dlhub_directory
from dlhub_cli.parsing import dlhub_cmd


@dlhub_cmd('init', help='Initialize a DLHub servable')
@click.option('--servable',
              default=None, show_default=True,
              help='The servable to initialize.')
@click.option('--from-pickle', type=str,
              default=None, show_default=True,
              help='A schema pickle to initialize from.')
def init_cmd(servable, from_pickle):
    """
    Initialize a servable. Create the .dlhub directory (if it
    doesn't exist) and use the toolbox to generate a config file for the
    specific model.

    :param servable: A particular servable to initialize
    :return:
    """
    format_output("Initializing")

    # Load from a toolbox pickle file
    loaded_servable = None
    if from_pickle:
        try:
            with open(from_pickle, 'rb') as fp:
                loaded_servable = pkl.load(fp)
        except IOError as e:
            format_output("I/O error({0}): {1}".format(e.errno, e.strerror))
        except FileNotFoundError as e:
            format_output("FileNotFound error ({0}) {1}:".format(e.strerror), from_pickle)
        except Exception as e:
            format_output("Exception ({0})".format(e))

    if not loaded_servable:
        format_output('Failed to load servable.')
        return

    # Create the .dlhub dir if it doesn't exist
    dlhub_directory = get_dlhub_directory()
    if not os.path.exists(dlhub_directory):
        os.makedirs(dlhub_directory)

    # If it doesn't already have an id, generate one.
    if not loaded_servable.dlhub_id:
        loaded_servable.assign_dlhub_id()

    # Save both the json and pkl representations to the dlhub directory
    pkl_path = os.path.join(dlhub_directory, loaded_servable['dlhub']['name']+ ".pkl")
    json_path = os.path.join(dlhub_directory, loaded_servable['dlhub']['name'] + ".json")

    try:
        with open(pkl_path, 'wb') as fp:
            pkl.dump(loaded_servable, fp)
        with open(json_path, 'w') as fp:
            json.dump(loaded_servable.to_dict(save_class_data=True), fp)
            format_output("Created {0}".format(json_path))
    except IOError as e:
        format_output("I/O error({0}): {1}".format(e.errno, e))
    except Exception as e:
        format_output("Exception ({0})".format(e))
