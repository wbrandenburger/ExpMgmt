# ===========================================================================
#   run.py ------------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.config
import expmgmt.config.settings
import expmgmt.config.experiment
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
        experiment_setting.update(
            expmgmt.config.settings.get_dataset_meta_settings(
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

    # get temporary file with user defined settings
    tmp_settings_path = pass_settings(experiment, data_setting)

    path = expmgmt.config.config.get(
        expmgmt.config.settings._MAIN_PROJ_FILE, required=False
    )
    if not os.path.exists(path):
        logger.warning("Running main experiment file: File {0} does not exist.".format(path)) # @log
        cmd_args = [path, "run", tmp_settings_path]
    else:
        cmd_args = ["python", path, tmp_settings_path]

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
    type=str
)
@click.option(
    "-d",
    "--data_set",
    help="Pass the trainings, test and validation of the specified dataset setting",
    type=click.Choice(["default",*expmgmt.config.settings.get_datasets()]),
    default="default"
)
@click.option(
    "-s",
    "--setting",
    help="Pass the trainings, test and validation of the specified dataset setting",
    type=str,
    default="default"
)
@click.option(
    "--nodata",
    help="Pass no trainings, test and validation data",
    is_flag=True,
    default=False
)
def cli(
        arguments,
        experiment,
        data_set,
        setting,
        nodata
    ):
    """Run an arbitrary shell command in the library folder"""


    if not nodata:
        if data_set == "default":
            run_data_set = expmgmt.config.config.get(expmgmt.config.settings._DEFAULT_DATASET)
            run_setting =  expmgmt.config.config.get(expmgmt.config.settings._DEFAULT_SETTING)
        elif not data_set == "none":
            run_data_set = data_set
            run_setting = setting
            if not setting in expmgmt.config.settings.get_dataset_settings(run_data_set):
                raise ValueError("Error: Invalid value for '-d' / '--data_set': invalid choice: {0}. (choose from {1})".format(
                    setting, 
                    expmgmt.config.settings.get_dataset_settings(run_data_set)
                    )
                ) # @todo[generalize]: also in expmgmt
    else:
        run_data_set = None
        run_setting = None

    run(
        arguments=arguments,
        experiment=experiment,
        data_setting = (run_data_set, run_setting)
    )
