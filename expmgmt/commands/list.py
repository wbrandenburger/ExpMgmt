# ===========================================================================
#   list.py -----------------------------------------------------------------
# ===========================================================================
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

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.configfile
import expmgmt.config.experiment
import expmgmt.config.settings_default

import click
import logging
import os

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger('list')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        exp=True,
    ):
    """Main method to the list command

    :return:: List different objects
    :rtype:  list
    """

    config = expmgmt.config.configfile.get_configuration()

    if exp:
        return [
            "{0}:\t {1}".format(config[section][expmgmt.config.settings_default._EXP_NAME], config[section][expmgmt.config.settings_default._LOCAL_DIR])
            for section in config
            if "exp-name" in config[section]
        ]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
@click.command(
    "list"
)
@click.help_option(
    "-h",
    "--help" 
)
@click.option(
    "-e",
    "--exp",
    help="List defined experiments",
    default=True,
    is_flag=True
)
def cli(
        exp
    ):
    """List documents' properties"""
 
    for o in run(exp = exp):
        click.echo(o)
