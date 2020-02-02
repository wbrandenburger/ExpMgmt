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
import expmgmt.config.config
import expmgmt.config.settings
import expmgmt.config.experiment
import expmgmt.config.settings
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
        experiment,
        data_setting = ()
    ):

    # create a temporary file
    tmp_object = tempfile.mkstemp(
        prefix="expmgmt-{0}-{1}-".format(
            expmgmt.config.experiment._CURRENT_EXPERIMENT,
            experiment),
        suffix=".yaml"
    )

    # get user defined settings
    experiment_setting =  expmgmt.config.settings.get_experiment_settings(
        experiment=experiment
    )

    if not data_setting == ():
        experiment_setting.update(
            expmgmt.config.settings.get_dataset_setting_files(
                *data_setting
            )
        )

    # write user defined settings to tempory file
    logger.info("Write experiment and data settings to file '{0}'".format(tmp_object[1]))
    expmgmt.utils.yaml.data_to_yaml(tmp_object[1], experiment_setting)

    return tmp_object[1]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        arguments=[],
        experiment=expmgmt.config.settings._DEFAULT_EXP_NAME,
        data_setting = ()
    ):
    
    path = expmgmt.config.config.get(
        expmgmt.config.settings._MAIN_PROJ_FILE, required=False
    )

    if not os.path.exists(path):
        logger.warning("Running main experiment file: File {0} does not exist.".format(path)) # @log
        return

    # get temporary file with user defined settings
    tmp_settings_path = pass_settings(experiment, data_setting)
    
    cmd_args = [
        "python", 
        path,
        tmp_settings_path
    ]

    if arguments:
        cmd_args.append(" ".join(arguments))
    cmd = " ".join(cmd_args)
    
    logger.debug("Running main experiment file {0}.".format(path)) # @log
    logger.debug("Call '{0}'".format(cmd)) # @log

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
    help="Pass the settings of the current experiment defined in {0}".format(expmgmt.config.settings._ENV_PROJECT),
    type=click.Choice([expmgmt.config.settings._DEFAULT_EXP_NAME, *expmgmt.config.settings.get_experiments_name()]),
    default=expmgmt.config.settings._DEFAULT_EXP_NAME
)
@click.option(
    "-d",
    "--data",
    help="Pass the trainings, test and validation of the specified dataset setting.",
    nargs=2, 
    type=(
        click.Choice(["none",*expmgmt.config.settings.get_datasets()]), str
    ),
    default=("none","")
)
def cli(
        arguments,
        experiment,
        data
    ):
    """Run an arbitrary shell command in the library folder"""

    data_setting = ()
    if not data[0] == "none":
        data_setting= data
        
        if not data_setting[1] in expmgmt.config.settings.get_dataset_settings(data_setting[0]):
            raise ValueError("Error: Invalid value for '-d' / '--data': invalid choice: {0}. (choose from {1})".format(
                data_setting[1], 
                expmgmt.config.settings.get_dataset_settings(data_setting[0])
                )
            )

    run(
        arguments=arguments,
        experiment=experiment,
        data_setting = data_setting
    )
