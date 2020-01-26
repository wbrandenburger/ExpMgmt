# ===========================================================================
#   run.py ------------------------------------------------------------------
# ===========================================================================
"""
This command is useful to issue commands in the directory of your library.

CLI Examples
^^^^^^^^^^^^

    - List files in your directory

    .. code::

        papis run ls

    - Find a file in your directory using the ``find`` command

    .. code::

        papis run find -name 'document.pdf'

Python examples
^^^^^^^^^^^^^^^

.. code::python

    from papis.commands.run import run

    run(library='papers', command=["ls", "-a"])

Cli
^^^
.. click:: papis.commands.run:cli
    :prog: papis run
"""
#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.configfile
import expmgmt.config.settings_default

import click
import logging
import os
from subprocess import call


#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger('run')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        arguments=[]
    ):
    
    path = expmgmt.config.configfile.get(
        expmgmt.config.settings_default._MAIN_EXP_FILE, required=False
    )

    if not os.path.exists(path):
        logger.warning("Running main experiment file: File {0} does not exist.".format(path))
        return

    logger.debug("Running main experiment file {0}.".format(path))
    
    call(["python", path, ])
    
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
@click.command(
    "run", 
    context_settings=dict(ignore_unknown_options=True)
)
@click.help_option(
    "-h",
    "--help" 
)
@click.argument(
    "--arguments", 
    nargs=-1
)

def cli(
        arguments
    ):
    """Run an arbitrary shell command in the library folder"""

    run(arguments=arguments)
