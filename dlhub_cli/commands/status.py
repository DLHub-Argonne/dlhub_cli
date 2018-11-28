import click

from dlhub_cli.config import get_dlhub_client
from dlhub_cli.printing import format_output
from dlhub_cli.parsing import dlhub_cmd


@dlhub_cmd('status', help='Check the status of a DLHub task.')
@click.option('--task',
              show_default=True, required=True,
              help='The UUID of a task.')
def status_cmd(task):
    """
    Use DLHub to query the status of a task.

    :param task: The uuid of a task
    :return:
    """

    client = get_dlhub_client()
    res = client.get_task_status(task)

    format_output("{0}: {1}".format(task, res))
