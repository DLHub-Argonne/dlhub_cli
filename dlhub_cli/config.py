from dlhub_client.client import DLHub

# The path to read and write servable definitions.
DLHUB_DIRECTORY_PATH = '.dlhub'
DLHUB_URL = "https://dlhub.org/"



def get_publish_url():
    """
    Return the url to publish servables.

    :return str: publish url
    """
    pub_path = "{}api/v1/publish".format(DLHUB_URL)
    return pub_path

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
    client = DLHub()
    return client