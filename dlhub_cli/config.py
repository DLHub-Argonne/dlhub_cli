from dlhub_sdk.client import DLHubClient
import os
from configobj import ConfigObj
import globus_sdk
from dlhub_cli import version

__all__ = (
    # option name constants
    'DLHUB_RT_OPTNAME',
    'DLHUB_AT_OPTNAME',
    'DLHUB_AT_EXPIRES_OPTNAME',

    'write_option',
    'lookup_option',
    'remove_option',
    'internal_auth_client',

    'check_logged_in',

    'get_dlhub_directory',
    'get_dlhub_client',
)

# The path to read and write servable definitions.
DLHUB_DIRECTORY_PATH = '.dlhub'
DLHUB_URL = "https://dlhub.org/"

# DLHUB_SCOPE = 'https://auth.globus.org/scopes/56ceac29-e98a-440a-a594-b41e7a084b62/all'

CONF_SECTION_NAME = 'dlhub-cli'

CLIENT_ID = 'f47a891c-cfd0-443c-8db8-c72fb82fe3f7'
DLHUB_RT_OPTNAME = 'dlhub_refresh_token'
DLHUB_AT_OPTNAME = 'dlhub_access_token'
DLHUB_AT_EXPIRES_OPTNAME = 'dlhub_access_token_expires'

GLOBUS_ENV = os.environ.get('GLOBUS_SDK_ENVIRONMENT')
if GLOBUS_ENV:
    DLHUB_RT_OPTNAME = '{}_{}'.format(GLOBUS_ENV, DLHUB_RT_OPTNAME)
    DLHUB_AT_OPTNAME = '{}_{}'.format(GLOBUS_ENV, DLHUB_AT_OPTNAME)
    DLHUB_AT_EXPIRES_OPTNAME = '{}_{}'.format(GLOBUS_ENV,
                                               DLHUB_AT_EXPIRES_OPTNAME)
    CLIENT_ID = {
        'sandbox':      'f9e36a20-2e1a-49e5-ba67-34cc82ca8b29',
        'test':         '2aa543de-b6c6-4aa5-9d7b-ef28e3a28cd8',
        'staging':      '0811fdd3-0d3e-4b5e-b634-8d6c91d87f21',
        'preview':      '988ff3e0-3bcf-495a-9f12-3b3a309bdb36',
    }.get(GLOBUS_ENV, CLIENT_ID)


def get_config_obj(file_error=False):
    path = os.path.expanduser("~/.globus.cfg")

    return ConfigObj(path, encoding='utf-8', file_error=file_error)


def lookup_option(option):
    conf = get_config_obj()
    try:
        return conf[CONF_SECTION_NAME][option]
    except KeyError:
        return None


def write_option(option, value):
    """
    Write an option to disk -- doesn't handle config reloading
    """
    # deny rwx to Group and World -- don't bother storing the returned old mask
    # value, since we'll never restore it in the CLI anyway
    # do this on every call to ensure that we're always consistent about it
    os.umask(0o077)

    conf = get_config_obj()

    # add the section if absent
    if CONF_SECTION_NAME not in conf:
        conf[CONF_SECTION_NAME] = {}

    conf[CONF_SECTION_NAME][option] = value
    conf.write()


def remove_option(option):
    conf = get_config_obj()

    # if there's no section for the option we're removing, just return None
    try:
        section = conf[CONF_SECTION_NAME]
    except KeyError:
        return None

    try:
        opt_val = section[option]

        # remove value and flush to disk
        del section[option]
        conf.write()
    except KeyError:
        opt_val = None

    # return the just-deleted value
    return opt_val


def internal_auth_client():
    """
    Get the globus native app client.

    :return:
    """
    return globus_sdk.NativeAppAuthClient(CLIENT_ID, app_name=version.app_name)


# Ryan: From Search:
# def get_search_client():
#     def search_refresh_callback(token_response):
#         tkn = token_response.by_resource_server
#         token = tkn['search.api.globus.org']['access_token']
#         expires_at = tkn['search.api.globus.org']['expires_at_seconds']
#         write_option(SEARCH_AT_OPTNAME, token)
#         write_option(SEARCH_AT_EXPIRES_OPTNAME, expires_at)
#
#     refresh_token = lookup_option(SEARCH_RT_OPTNAME)
#     access_token = lookup_option(SEARCH_AT_OPTNAME)
#     access_token_expires = lookup_option(SEARCH_AT_EXPIRES_OPTNAME)
#
#     authorizer = None
#     if access_token_expires is not None:
#         authorizer = globus_sdk.RefreshTokenAuthorizer(
#             refresh_token, internal_auth_client(),
#             access_token, int(access_token_expires),
#             on_refresh=search_refresh_callback)
#
#     return globus_sdk.SearchClient(
#         authorizer=authorizer,
#         app_name='dlhub-cli v{}'.format(version.__version__))


def check_logged_in():
    """
    Check if the user is already logged in.

    :return:
    """
    search_rt = lookup_option(DLHUB_RT_OPTNAME)
    if search_rt is None:
        return False
    native_client = internal_auth_client()
    res = native_client.oauth2_validate_token(search_rt)
    return res['active']


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
    client = DLHubClient()
    return client
