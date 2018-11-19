Quickstart
==========

Welcome to the DLHub Command Line Interface (CLI). This CLI simplifies interacting with the DLHub service and the deployed servables.

Installation
------------

The CLI is available on PyPI, but first make sure you have Python3.5+

>>> python3 --version

The CLI has been tested on Linux.


Installation using Pip
^^^^^^^^^^^^^^^^^^^^^^

While ``pip`` and ``pip3`` can be used to install the CLI we suggest the following approach
for reliable installation when many Python environments are avaialble.::

     $ python3 -m pip install dlhub_cli

     (to update a previously installed parsl to a newer version, use: python3 -m pip install -U dlhub_cli)


Installation using Conda
^^^^^^^^^^^^^^^^^^^^^^^^
1. Install Conda and setup python3.6 following the instructions `here <https://conda.io/docs/user-guide/install/macos.html>`_::

     $ conda create --name dlhub_py36 python=3.6
     $ source activate dlhub_py36

2. Install the CLI::

     $ python3 -m pip install dlhub_cli

     (to update a previously installed the cli to a newer version, use: python3 -m pip install -U parsl)

For Developers
--------------

1. Download Parsl::

    $ git clone https://github.com/DLHub-Argonne/dlhub_cli

2. Install::

    $ cd dlhub_cli
    $ python3 setup.py install

3. Use the CLI!

Requirements
------------

Parsl requires the following:

* Python 3.5+
