from dlhub_sdk.client import DLHubClient

__all__ = (
    # option name constants
    'get_dlhub_client',
)

# The path to read and write servable definitions.
DLHUB_URL = "https://dlhub.org/"

CONF_SECTION_NAME = 'dlhub-cli'


def get_dlhub_client(force=False):
    """Get the DLHub client

    Returns:
        DLHubClient: DLHubClient with the proper credentials
    """

    return DLHubClient(force=force)
