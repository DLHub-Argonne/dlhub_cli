from dlhub_cli.parsing import main_func
from dlhub_cli.commands import (
    init_cmd, publish_cmd, update_cmd,
    run_cmd, ls_cmd, status_cmd, login_cmd,
    logout_cmd, servables_cmd, describe_cmd)

@main_func
def cli_root():
    """Root to add everything to.

    Returns:
        (none) None.
    """
    pass


cli_root.add_command(init_cmd)
cli_root.add_command(publish_cmd)
cli_root.add_command(run_cmd)
cli_root.add_command(status_cmd)
cli_root.add_command(login_cmd)
cli_root.add_command(logout_cmd)
cli_root.add_command(servables_cmd)
cli_root.add_command(describe_cmd)
# cli_root.add_command(update_cmd)
# cli_root.add_command(ls_cmd)