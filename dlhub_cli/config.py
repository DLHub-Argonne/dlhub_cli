from dlhub_sdk.client import DLHubClient

__all__ = (
    # option name constants

    'get_dlhub_directory',
    'get_dlhub_client',
)

# The path to read and write servable definitions.
DLHUB_DIRECTORY_PATH = '.dlhub'
DLHUB_URL = "https://dlhub.org/"

CONF_SECTION_NAME = 'dlhub-cli'

DLHUB_CLIENT = DLHubClient()

def get_dlhub_directory():
    """
    Standardize the dlhub directory path for each command.

    :return str: path to the directory
    """
    return DLHUB_DIRECTORY_PATH


def get_dlhub_client():
    """
    Get the DLHub client

    :return:
    """

    return DLHUB_CLIENT
