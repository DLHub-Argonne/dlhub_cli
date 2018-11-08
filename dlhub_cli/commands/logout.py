import click

import globus_sdk

from dlhub_cli.printing import safeprint
from dlhub_cli.config import (
    DLHUB_AT_OPTNAME, DLHUB_AT_EXPIRES_OPTNAME, DLHUB_RT_OPTNAME,
    lookup_option, remove_option,
    internal_auth_client)


_RESCIND_HELP = """\
Rescinding Consents
-------------------
The logout command only revokes tokens that it can see in its storage.
If you are concerned that logout may have failed to revoke a token,
you may want to manually rescind the DLHub CLI consent on the
Manage Consents Page:
    https://auth.globus.org/consents
"""


_LOGOUT_EPILOG = """\
You are now successfully logged out of the DLHub CLI.
You may also want to logout of any browser session you have with Globus:
  https://auth.globus.org/v2/web/logout
Before attempting any further CLI commands, you will have to login again using
  globus-search login
"""


@click.command('logout',
               short_help='Logout of the DLHub CLI',
               help=('Logout of the DLHub CLI. '
                     'Removes your Globus tokens from local storage, '
                     'and revokes them so that they cannot be used anymore'))
@click.confirmation_option(prompt='Are you sure you want to logout?',
                           help='Automatically say "yes" to all prompts')
def logout_cmd():
    safeprint(u'Logging out of DLHub CLI\n')

    native_client = internal_auth_client()

    # remove tokens from config and revoke them
    # also, track whether or not we should print the rescind help
    print_rescind_help = False
    for token_opt in (DLHUB_RT_OPTNAME, DLHUB_AT_OPTNAME):
        # first lookup the token -- if not found we'll continue
        token = lookup_option(token_opt)
        if not token:
            safeprint(('Warning: Found no token named "{}"! '
                       'Recommend rescinding consent').format(token_opt))
            print_rescind_help = True
            continue
        # token was found, so try to revoke it
        try:
            native_client.oauth2_revoke_token(token)
        # if we network error, revocation failed -- print message and abort so
        # that we can revoke later when the network is working
        except globus_sdk.NetworkError:
            safeprint(('Failed to reach Globus to revoke tokens. '
                       'Because we cannot revoke these tokens, cancelling '
                       'logout'))
            click.get_current_context().exit(1)
        # finally, we revoked, so it's safe to remove the token
        remove_option(token_opt)

    # remove expiration time, just for cleanliness
    remove_option(DLHUB_AT_EXPIRES_OPTNAME)

    # if print_rescind_help is true, we printed warnings above
    # so, jam out an extra newline as a separator
    safeprint(("\n" if print_rescind_help else "") + _LOGOUT_EPILOG)

    # if some token wasn't found in the config, it means its possible that the
    # config file was removed without logout
    # in that case, the user should rescind the CLI consent to invalidate any
    # potentially leaked refresh tokens, so print the help on that
    if print_rescind_help:
        safeprint(_RESCIND_HELP)