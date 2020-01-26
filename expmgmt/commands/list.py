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
import expmgmt.config.settings_user

import click
import logging
import os

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger('list')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        projects,
        project,
        exp_name
    ):
    """Main method to the list command

    :return:: List different objects
    :rtype:  list
    """

    config = expmgmt.config.configfile.get_configuration()

    if projects:
        return [{
            config[section][expmgmt.config.settings_default._EXP_NAME]: config[section][expmgmt.config.settings_default._LOCAL_DIR]
            }
            for section in config
            if "exp-name" in config[section]
        ]
    elif exp_name:
        return expmgmt.config.settings_user.get_experiment_settings(exp_name)
    else:
        return expmgmt.config.settings_user.get_experiments_name()
        
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
    "--projects",
    help="Show all available projects and their main directory (default).",
    default=False,
    is_flag=True
)
@click.option(
    "-p",
    "--project",
    help="Show the experiment names of a specified project",
    default=lambda: exp.config.configfile.get(expmgmt.config.settings_default._DEFAULT_EXP) if not os.environ.get(expmgmt.config.settings_default._ENV_EXP) else os.environ.get(expmgmt.config.settings_default._ENV_EXP) 

)
@click.option(
    "-e",
    "--experiment",
    help="Show the settings of the current experiment defined in {0}".format(expmgmt.config.settings_default._ENV_EXP),
    default=None
)
def cli(
        projects,
        project,
        experiment
    ):
    """List experiments' properties"""
 
    result = run(
        projects=projects,
        project=project,
        exp_name = experiment
    )

    result = [result] if not isinstance(result,list) else result
    for list_item in result:
        for item, value in list_item.items():
            print(item, value)
