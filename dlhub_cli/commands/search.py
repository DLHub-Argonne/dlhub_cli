"""Commands for basic searches from the commandline"""

import click
import pandas as pd
from datetime import datetime
from tabulate import tabulate

from dlhub_sdk.utils.search import DLHubSearchHelper, filter_latest

from dlhub_cli.parsing import dlhub_cmd
from dlhub_cli.config import get_dlhub_client


@dlhub_cmd('search',
           help='Search the servable index')
@click.option('--owner', help='Name of owner of the servable')
@click.option('--name', help='Name of the servable')
@click.option('--all', 'all_versions', help='Get all versions of each model',
              is_flag=True)
@click.option('--author', help='Search by author name. Must be in form "Last, First"',
              multiple=True)
@click.option('--domain', help='Domain of the servable (e.g., chemistry)',
              multiple=True)
@click.option('--doi', help='DOI of an associated publication')
@click.argument('query', nargs=-1)
def search_cmd(owner, name, all_versions, author, domain, doi, query):
    """Search command

    See above for argument details
    """

    # Get the client
    client = get_dlhub_client()

    # Start the query object
    query = DLHubSearchHelper(client._search_client, q="(" + " ".join(query), advanced=True)

    # Add the filters
    query.match_owner(owner)
    query.match_servable(servable_name=name)
    query.match_authors(author)
    query.match_domains(domain)
    query.match_doi(doi)

    # If no query strings are given, return an error
    if not query.initialized:
        click.echo('Error: No query specified. For options, call: dlhub search --help')
        click.get_current_context().exit(1)

    # Perform the query
    results = query.search()

    # If no results, return nothing
    if len(results) == 0:
        click.echo('No results')
        return

    # If desired, filter the entries
    if not all_versions:
        results = filter_latest(results)

    # Get only a subset of the data and print it as a table
    results_df = pd.DataFrame([{
        'Owner': r['dlhub']['owner'],
        'Model Name': r['dlhub']['name'],
        'Publication Date': datetime.fromtimestamp(int(r['dlhub']['publication_date']) /
                                                   1000).strftime('%Y-%m-%d %H:%M'),
        'Type': r['servable']['type']
    } for r in results])

    results_df.sort_values(['Owner', 'Model Name', 'Publication Date'],
                           ascending=[True, True, False], inplace=True)

    click.echo(tabulate(results_df.values, headers=results_df.columns))
