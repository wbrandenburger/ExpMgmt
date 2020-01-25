"""
This command is to list contents of a library.

CLI Examples
^^^^^^^^^^^^

- List all document files associated will all entries:

    .. code:: bash

        papis list --file

    .. raw:: HTML

        <script type="text/javascript"
        src="https://asciinema.org/a/XwD0ZaUORoOonwDw4rXoQDkjZ.js"
        id="asciicast-XwD0ZaUORoOonwDw4rXoQDkjZ" async></script>

- List all document year and title with custom formatting:

    .. code:: bash

        papis list --format '{doc[year]} {doc[title]}'

    .. raw:: HTML

        <script type="text/javascript"
        src="https://asciinema.org/a/NZ8Ii1wWYPo477CIL4vZhUqOy.js"
        id="asciicast-NZ8Ii1wWYPo477CIL4vZhUqOy" async></script>

- List all documents according to the bibitem formatting (stored in a template
  file ``bibitem.template``):

    .. code:: bash

        papis list --template bibitem.template

    .. raw:: HTML

        <script type="text/javascript"
        src="https://asciinema.org/a/QZTBZ3tFfyk9WQuJ9WWB2UpSw.js"
        id="asciicast-QZTBZ3tFfyk9WQuJ9WWB2UpSw" async></script>

Python examples
^^^^^^^^^^^^^^^

.. code:: python

    # Import the run function from the list command

    from papis.commands.list import run as papis_list

    documents = papis_list(query='einstein', library='papis')

    for doc in documents:
        print(doc["url"])

    # etc...
    info_files = list(query='einstein', library='papis', info_files=True)

    # do something with the info file paths...

Cli
^^^
.. click:: papis.commands.list:cli
    :prog: papis list
"""

import expmgmt.config.configfile
import expmgmt.config.experiment

import os
import click

import logging

logger = logging.getLogger('list')

def run(
        exp=False,
    ):
    """Main method to the list command

    :return:: List different objects
    :rtype:  list
    """
    if experiment is None:
        experiment = expmgmt.config.experiment.get_exp():

    config = expmgmt.config.configfile.get_configuration()

    if experiment:
        return [
            { 
                "" : config[section]["exp-name"], 
                "" :  config[section]["local-dir"]
            } for section in config
            if "exp-name" in config[section]
        ]

@click.command("list")
@click.help_option('--help', '-h')
@papis.cli.query_option()
@click.option(
    "-i",
    "--info",
    help="Show the info file name associated with the document",
    default=False,
    is_flag=True
)
@click.option(
    "-d",
    "--dir",
    help="Show the folder name associated with the document",
    default=False,
    is_flag=True
)
@click.option(
    "-e",
    "--exp",
    help="List defined experiments",
    default=False,
    is_flag=True
)

def cli(
        dir,
        exp
        ):
    """List documents' properties"""

    if not exp and not dir:
        dir = True

    experiment = expmgmt.config.experiment.get_exp():

    objects = run(
        exp = experiment,
    )
    # for o in objects:
    #     click.echo(o)
    return
