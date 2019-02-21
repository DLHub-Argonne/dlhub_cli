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
      describe   Get the description of a servable
      init       Initialize a DLHub servable.
      login      Log into Globus to get credentials for the DLHub CLI
      logout     Logout of the DLHub CLI
      methods    Print method information
      publish    Publish a servable to DLHub.
      run        Invoke a servable
      search     Search the servable index
      servables  List the available servables.
      status     Check the status of a DLHub task.
      whoami     Get the username of logged in user


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

The ``--force`` flag will initiate a login flow even when the user is already logged in.

Logging Out
-----------

The logout process is initiated using the logout command. This will invalidate and remove the credentials stored in
the ``~/.dlhub/credentials/`` directory and will force subsequent commands to initiate a new login flow.::

     $ dlhub logout


Finding Servables
^^^^^^^^^^^^^^^^^
The CLI can be used to list the available servables accessible to the user. This command will provide a list of
servables that are currently available in DLHub::

     $ dlhub servables

You can also search the index of DLHub servables with the 'search' command.
The 'search' command supports tags for common options, such as the owner::

    $ dlhub search --owner blaiszik_globusid

    Model Name       Owner              Publication Date    Type
    ---------------  -----------------  ------------------  -----------
    cherukara_phase  blaiszik_globusid  2019-02-19 15:21    Keras Model

Call ``dlhub search --help`` for a full listing of search tags.

.. TODO: Add a link to DLHub search docs when available

You can also provide a full query string using the DLHub query syntax::

    $ dlhub search dlhub.owner:blaiszik_globusid AND servable.type:"Keras Model"

    Model Name       Owner              Publication Date    Type
    ---------------  -----------------  ------------------  -----------
    cherukara_phase  blaiszik_globusid  2019-02-19 15:21    Keras Model

Describing Servables
^^^^^^^^^^^^^^^^^^^^
The 'describe' command queries the service for additional information about a servable.
This information includes details on how to invoke the servable, required inputs, and expected outputs.
The describe command requires the owner name and user name of the servable::

     $ dlhub describe dlhub.test_gmail 1d_norm

Use the 'methods' to return only information about the methods implemented by a servable::

    $ dlhub methods dlhub.test_gmail 1d_norm

    run:
      input:
        description: Array to be normed
        shape:
        - None
        type: ndarray
      output:
        description: Norm of the array
        type: number


Running Servables
^^^^^^^^^^^^^^^^^
Servables can be invoked through the CLI using the run command.
The run command accepts flags to specify the servable and input parameters.
The servable flag requires the identifier of the servable.
Input parameters should be correctly-formatted JSON strings.
The run command first attempts to json.loads() the input before using the DLHub SDK to invoke the servable.
Output will be returned as well formatted JSON documents.::

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
Publishing a servable can be achieved by issuing a publish command using either a GitHub repository or a local servable definition file.

Description Files
-----------------

Publishing a servable relies on a compatible metadata document. The publication process uses the metadata document to
determine which shim to use when loading and interacting the servable.

A guide for describing servables can be found in the
`DLHub SDK documentation <https://dlhub-sdk.readthedocs.io/en/latest/?badge=latest>`_.

Publishing a Repository
-----------------------

Publishing a model can also be achieved by specifying a compliant GitHub repository.
The repository will need to include the ``dlhub.json`` file already.
The publication flow relies on `repo2docker <https://repo2docker.readthedocs.io/en/latest/>`_
to construct a container with all of the required dependencies.

An example repository can be found here: https://github.com/ryanchard/dlhub_publish_example

The publication command will return a task identifier that can subsequently be used to query the status of publication tasks.:::

     $ dlhub publish --repository https://github.com/ryanchard/dlhub_publish_example

      Task_id: ff56599e-3377-4475-9684-0afd7f563aeb

Publishing a Local Servable
---------------------------

Publishing a local servable requires first generating the ``dlhub.json`` file and storing it on your system.
Once that file has been generated you can use the ``--local`` flag to initiate a publication for the local model.
Files mentioned within the dlhub.json document will be packaged into a temporary zip file
then transmitted to the DLHub service using HTTP::

    $ dlhub publish --local

Checking Publication Status
---------------------------

The status of a publication task can be queried using the status command. The status command requires the task id and will return
a JSON status document.::

    $ dlhub status --task ff56599e-3377-4475-9684-0afd7f563aeb

     ff56599e-3377-4475-9684-0afd7f563aeb: {'status': 'COMPLETE'}

