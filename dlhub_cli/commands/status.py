import click

from dlhub_cli.config import get_dlhub_client
from dlhub_cli.printing import format_output
from dlhub_cli.parsing import dlhub_cmd

HELP_STR = """\

  Check the status of a DLHub task.
\b
Options:
  --task TEXT    The UUID of a task.  [required]
  -h, --help     Show this message and exit.
  -v, --version  Show the version and exit."""


@dlhub_cmd('status', help='Check the status of a DLHub task.')
@click.option('--task',
              show_default=True, required=False,
              help='The UUID of a task.')
def status_cmd(task):
    """Use DLHub to query the status of a task.

    Args:
        task (string): The uuid the task
    Returns:
        (dict) the status of the task. Once complete this will include output.
    """

    if not any([task, False]):
        format_output(HELP_STR)
        return

    client = get_dlhub_client()
    res = client.get_task_status(task)

    format_output("{0}: {1}".format(task, res))
    return res
