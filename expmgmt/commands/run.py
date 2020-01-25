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

import click
import logging
import os

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger('run')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
    ):
    
    logger.debug("List all available experiments defined in configuration folder.".format(folder))

    print(expmgmt.config.configfile.get("main-file")) # @todo[to change]:

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
def cli(
    ):
    """Run an arbitrary shell command in the library folder"""

    run()
