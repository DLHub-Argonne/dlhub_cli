import os
import re
import click

from string import Template
from subprocess import Popen, PIPE
from dlhub_cli.parsing import dlhub_cmd
from dlhub_cli.printing import format_output


# Path of the templates
template_path = os.path.join(os.path.dirname(__file__), 'init_templates')


# Check name
def validate_name(ctx, param, name):
    if name is None:
        raise click.BadParameter('--name is required. Call --help to see syntax')
    if re.match('^\\S+$', name) is None:
        raise click.BadParameter('Name must not contain whitespace')
    return name


def validate_authors(ctx, param, authors):
    if authors is not None:
        for author, affil in authors:
            if re.match('^.*, .*$', author) is None:
                raise click.BadParameter('Authors must be listed as "Last, First"')
    return authors


@dlhub_cmd('init', help='Initialize a DLHub servable.'
                        ' Creates a Python script to generate model description from a template.')
@click.option('--force', is_flag=True,
              help='Whether to overwrite an existing file')
@click.option('--filename', default="describe_servable.py",
              help='Name of the Python script generated by init')
@click.option('--author', multiple=True, type=(str, str),
              default=(('Author, A.', 'Argonne'),),
              help='Name and affiliation of an author. Author names must be "Last, First". '
                   'Use quotation marks for multiple words in names and affiliations',
              callback=validate_authors)
@click.option('--title', help='Short, descriptive title for the servable',
              default='A short title for the servable')
@click.option('--name', help='Short name for the servable',
              callback=validate_name)
@click.option('--skip-run', help='Skip executing the dlhub.json file',
              is_flag=True)
def init_cmd(force, filename, author, title, name, skip_run):
    """
    Initial step in creating a DLHub servable

    Creates a Python script that a user can edit to create a description for a servable

    Args:
        force (bool): Whether to overwrite an existing template file
        filename (string): Name of the template file to create
        author ([string]): List of authors and affiliations
        title (string): Title for the servable
        name (string): Name of the servable
        skip_run (bool): Whether the skip executing the init script
    """

    format_output("Initializing")

    # Check if a file would be overwritten
    if os.path.isfile(filename) and not force:
        format_output("There is already a file named '{}'. Use --force to overwrite".format(filename))
        return 1

    # Prepare a dict of objects to be replaced
    subs = {
        'authors': '[{}]'.format(', '.join('"{}"'.format(x[0]) for x in author)),
        'affiliations': '[{}]'.format(', '.join('["{}"]'.format(x[1]) for x in author)),
        'title': title,
        'name': name
    }

    # Copy the template to the directory and make substitutions
    with open(filename, 'w') as fo:
        with open(os.path.join(template_path, 'describe_servable.py.template')) as fi:
            for line in fi:
                newline = Template(line).substitute(subs).rstrip()
                print(newline, file=fo)

    format_output('...Saved settings file as {}'.format(filename))

    # Unless skipped, run the new file
    if not skip_run:
        proc = Popen(['python', filename], shell=True, cwd=os.getcwd(),
                     stderr=PIPE)
        if proc.wait() != 0:
            format_output('WARNING: Script failed to run. Error details:')
            for line in proc.stderr:
                format_output(line.decode().rstrip())
        else:
            print('...Saved model description as dlhub.json')

    return
