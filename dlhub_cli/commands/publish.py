import os
import json
import uuid
import boto3
import click
import requests
import pickle as pkl

import dlhub_toolbox
import dlhub_client

from dlhub_cli.config import get_dlhub_directory, get_publish_url
from dlhub_cli.printing import format_output
from dlhub_cli.parsing import dlhub_cmd


def _stage_data(servable):
    """
    Stage data to the DLHub service.

    :param data_path: The data to upload
    :return str: path to the data on S3
    """
    s3 = boto3.resource('s3')

    # Get the list of things to upload
    upload_files = []

    # Figure out what to upload.
    data_path = servable.files['model']
    for dp in servable.files['other']:
        upload_files.append(dp)

    # Crawl if its a directory.
    if os.path.isdir(data_path):
        for (src_dir, dirname, filename) in os.walk(data_path):
            for f in filename:
                if f[0] == ".":  # Ignore hidden files
                    continue
                upload_files.append(os.path.join(src_dir, f))
    else:
        upload_files.append(data_path)

    # Generate a uuid to deposit the data
    dest_uuid = str(uuid.uuid4())
    dest_dir = 'servables/'
    bucket_name = 'dlhub-anl'

    # Upload to S3
    for sourcepath in upload_files:
        ext_path = sourcepath.split(data_path)[-1].strip("/")  # Take everything after parent dir
        destpath = os.path.join(dest_dir, dest_uuid, ext_path)  # Join destination with a uuid and path to file
        format_output("Uploading: {}".format(sourcepath))
        res = s3.Object(bucket_name, destpath).put(ACL="public-read", Body=open(sourcepath, 'rb'))

    staged_path = os.path.join("s3://", bucket_name, dest_dir, dest_uuid)
    return staged_path


@dlhub_cmd('publish', help='Publish a servable to DLHub.')
@click.option('--servable',
              default=None, show_default=True,
              help='The servable to publish.')
def publish_cmd(servable):
    """
    Publish a model to DLHub. Read the description file from the .dlhub directory
    and send a publication request to DLHub.

    :param servable: A particular servable to publish
    :return:
    """
    format_output("Publishing {}".format(servable))
    loaded_servable = None
    dlhub_directory = get_dlhub_directory()

    if servable:
        servable_path = os.path.join(dlhub_directory, servable + ".pkl")
        format_output(servable_path)
        try:
            with open(servable_path, 'rb') as fp:
                loaded_servable = pkl.load(fp)
        except IOError as e:
            format_output("I/O error({0}): {1}".format(e.errno, e))
        except FileNotFoundError as e:
            format_output("FileNotFound error ({0}) {1}:".format(e, servable))
        except Exception as e:
            format_output("Exception ({0})".format(e))

    if not loaded_servable:
        format_output("Failed to load servable.")
        return

    # Stage data for DLHub to access
    staged_path = _stage_data(loaded_servable)
    format_output(staged_path)

    # Publish to DLHub
    payload = loaded_servable.to_dict()
    payload['dlhub']['location'] = staged_path

    url = get_publish_url()
    response = requests.post(url, json=payload)
    format_output(response.text)
