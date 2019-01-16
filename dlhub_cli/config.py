from dlhub_sdk.client import DLHubClient

__all__ = (
    # option name constants
    'get_dlhub_client',
)

# The path to read and write servable definitions.
DLHUB_URL = "https://dlhub.org/"

CONF_SECTION_NAME = 'dlhub-cli'

DLHUB_CLIENT = DLHubClient


def get_dlhub_client():
    """Get the DLHub client

    Returns:
        (DLHubClient) the dlhub client.
    """

    return DLHUB_CLIENT.login()
