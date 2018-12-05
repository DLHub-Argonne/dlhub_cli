Tutorial
==========

The DLHub CLI provides an easy-to-use interface for interacting with the DLHub serving to publish, find, and run servables.
This tutorial showcases many of the functions available through the CLI. The CLI thinly wraps the DLHub SDK.
Further documentation on the SDK can be found `here <https://dlhub-sdk.readthedocs.io/en/latest/?badge=latest>`_.
Once installed, the CLI can be accessed via the command 'dlhub'::

    $ dlhub

    Usage: dlhub [OPTIONS] COMMAND [ARGS]...

      CLI Client to the DLHub API

    Options:
      -h, --help     Show this message and exit.
      -v, --version  Show the version and exit.

    Commands:
      describe   Describe a servable.
      init       Initialize a DLHub servable
      login      Log into Globus to get credentials for the DLHub CLI
      logout     Logout of the DLHub CLI
      publish    Publish a servable to DLHub.
      run        Invoke a servable
      servables  List the available servables.
      status     Check the status of a DLHub task.
      update     Update a servables metadata


Authentication
^^^^^^^^^^^^^^

Before using the DLHub CLI to publish, find, or use models you must login.
DLHub is underpinned by Globus Auth and uses a Globus Native App login flow to authenticate users.
Using various CLI commands (e.g., run and publish) will initiate a DLHubClient and automatically start a login flow if you are not already logged in.
Once logged in the CLI will create a ~/.globus.cfg file to store your tokens. The login flow will first check whether valid credentials exist in this file and will start a flow if they cannot be used.

Logging In
----------

The login flow will present a URL for you to visit. This URL will ask you to login with Globus or a compatible identitiy provider.
Once logged in the authentication flow will present the requested scopes for the DLHub service. Agreeing to these scopes
will then generate a temporary token for you to copy and paste into the terminal.

Logging in can also be explicitly invoked with the 'login' command::

     $ dlhub login --force

     (the --force flag will initiate a login flow even when the user is already logged in.)


Logging Out
-----------

The logout process is initiated using the logout command. This will invalidate and remove the credentials stored in the
~/.globus.cfg file and will force subsequent commands to initiate a new login flow.::

     $ dlhub logout


Finding Servables
^^^^^^^^^^^^^^^^^
The CLI can be used to list the available servables accessible to the user. This command will provide a list of servables in (id, name) pairs::

     $ dlhub servables

Describing Servables
^^^^^^^^^^^^^^^^^^^^
The 'describe' command queries the service for additional information about a servable. This information includes details on how to invoke the servable, required inputs, and expected outputs.
The describe command can be passed either the servables text name or identifier::

     $ dlhub describe --id 5e21f7da-7788-406a-a0ac-805aa17811ff

or::

    $ dlhub describe --name mnist


Running Servables
^^^^^^^^^^^^^^^^^
Servables can be invoked through the CLI using the run command. The run command accepts flags to specify the servable
and input parameters. The servable flag requires the identifier of the servable. Input parameters should be well formated JSON strings.
The run command first attempts to json.loads() the input before using the DLHub SDK to invoke the servable. Output will be returned
as well formatted JSON documents.::

     $ dlhub run --servable 50358d8c-be7a-41bf-af76-a460223907fe --input '[{"composition": "Al"}]'

     Outputs:
        [
          {
            "composition": "Al",
            "composition_object": "gANjcHltYXRnZW4uY29yZS5jb21wb3NpdGlvbgpDb21wb3NpdGlvbgpxACmBcQF9cQIoWA4AAABh\nbGxvd19uZWdhdGl2ZXEDiVgHAAAAX25hdG9tc3EERz/wAAAAAAAAWAUAAABfZGF0YXEFfXEGY3B5\nbWF0Z2VuLmNvcmUucGVyaW9kaWNfdGFibGUKRWxlbWVudApxB1gCAAAAQWxxCIVxCVJxCkc/8AAA\nAAAAAHN1Yi4=\n"
          }
        ]

Publishing Servables
^^^^^^^^^^^^^^^^^^^^
Publishing a servable can be achieved by issuing a publish command using either a github repository or a local servable definition file.

Description Files
-----------------

Publishing a servable relies on a compatible metadata document. The publication process uses the metadata document to
determine which shim to use when loading and interacting the servable.

Details on this process can be found `here <https://dlhub-sdk.readthedocs.io/en/latest/?badge=latest>`_.

Publishing a Repository
-----------------------

Publishing a model can also be achieved by specifying a compliant github repository. The repository will need to include the
dlhub.json file already. The publication flow relies on repo2docker to construct an initial container image before using
the image as the basis for another container that includes the necessary DLHub modules (dlhub_sdk and parsl).

An example repository can be found here: https://github.com/ryanchard/dlhub_publish_example

The publication command will return a task identifier that can subsequently be used to query the status of publication tasks.:::

     $ dlhub publish --repository https://github.com/ryanchard/dlhub_publish_example

      Task_id: ff56599e-3377-4475-9684-0afd7f563aeb

Publishing a Local Servable
---------------------------

Publishing a local servable requires the servable have been initalized and the dlhub.json file already exist locally.
Once that file has been generated you can use the --local flag to initiate a publication for the local model.
Files mentioned within the dlhub.json document will be packaged into a temporary zip file then transmitted to the DLHub service
using the boto3 library, staging the data through an S3 bucket.::

    $ dlhub publish --local

Checking Publication Status
--------------

The status of a publication task can be queried using the status command. The status command requires the task id and will return
a JSON status document.::

    $ dlhub status --task ff56599e-3377-4475-9684-0afd7f563aeb

     ff56599e-3377-4475-9684-0afd7f563aeb: {'status': 'COMPLETE'}

