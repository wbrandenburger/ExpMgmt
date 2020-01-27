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
import expmgmt.config.experiment
import expmgmt.config.settings_user
import expmgmt.utils.yaml

import click
import logging
import os
import shlex
import subprocess
import sys

import shutil
import tempfile
import yaml

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger('run')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def pass_settings(
        experiment
    ):

    # create a temporary file
    tmp_object = tempfile.mkstemp(
        prefix="expmgmt-{0}-{1}-".format(
            expmgmt.config.experiment._CURRENT_EXPERIMENT,
            experiment),
        suffix=".yaml"
    )

    # get user defined settings
    data =  expmgmt.config.settings_user.get_experiment_settings(
        experiment=experiment
    )
    # write user defined settings to tempory file
    expmgmt.utils.yaml.data_to_yaml(tmp_object[1], data)

    return tmp_object[1]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        arguments=[],
        experiment=expmgmt.config.settings_default._DEFAULT_EXP_NAME
    ):
    
    path = expmgmt.config.configfile.get(
        expmgmt.config.settings_default._MAIN_PROJ_FILE, required=False
    )

    if not os.path.exists(path):
        logger.warning("Running main experiment file: File {0} does not exist.".format(path))
        return

    # get temporary file with user defined settings
    tmp_settings_path = pass_settings(experiment)
    
    cmd_args = [
        "python", 
        path,
        tmp_settings_path
    ]
    if arguments:
        cmd_args.append(" ".join(arguments))
    cmd = " ".join(cmd_args)
    
    logger.debug("Running main experiment file {0}.".format(path))
    logger.debug("Call '{0}'".format(cmd))

    subprocess.call(cmd)
    
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
    "arguments", 
    nargs=-1
)
@click.option(
    "-e",
    "--experiment",
    help="Pass the settings of the current experiment defined in {0}".format(expmgmt.config.settings_default._ENV_PROJECT),
    type=click.Choice([expmgmt.config.settings_default._DEFAULT_EXP_NAME, *expmgmt.config.settings_user.get_experiments_name()]),
    default=expmgmt.config.settings_default._DEFAULT_EXP_NAME
)
def cli(
        arguments,
        experiment
    ):
    """Run an arbitrary shell command in the library folder"""

    run(
        arguments=arguments,
        experiment=experiment
    )
