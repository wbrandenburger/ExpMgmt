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
import os
import papis.config.utils
import papis.debug.exceptions
import logging
import click

logger = logging.getLogger('run')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(folder, command=[]):
    logger.debug("Changing directory into %s" % folder)
    os.chdir(os.path.expanduser(folder))
    try:
        commandstr = os.path.expanduser(
            papis.config.utils.get("".join(command))
        )
    except papis.debug.exceptions.DefaultSettingValueMissing:
        commandstr = " ".join(command)
    logger.debug("Command = %s" % commandstr)
    return os.system(commandstr)

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
    "run_command", 
    nargs=-1
)
def cli(run_command):
    """Run an arbitrary shell command in the library folder"""
    for folder in papis.config.utils.get_lib_dirs():
        run(folder, command=run_command)
