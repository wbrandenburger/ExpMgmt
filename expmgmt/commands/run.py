# ===========================================================================
#   run.py ------------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.config
import expmgmt.config.settings
import expmgmt.config.experiment
import expmgmt.utils.yaml
import expmgmt.utils.dictparser
import expmgmt.debug.exceptions

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
        data_set = None,
        setting = None,
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

    if  data_set == expmgmt.config.settings._DEFAULT_NAME:
        try:
            data_set = experiment_setting["data"]["data-set"]
            setting = experiment_setting["data"]["setting"]
        except KeyError:
            raise expmgmt.debug.exceptions.KeyErrorJson("data")

    if data_set and setting:
        experiment_setting.update(
            expmgmt.config.settings.get_dataset_setting_files(
                data_set, setting
            )
        )
        experiment_setting.update(
            expmgmt.config.settings.get_dataset_meta_settings(
                data_set, setting
            )
        )

    try:
        experiment_setting.pop("data", None)
    except KeyError:
        pass

    # write user defined settings to tempory file
    logger.info("Write experiment and data settings to file '{0}'".format(tmp_object[1]))
    expmgmt.utils.yaml.data_to_yaml(
        tmp_object[1], 
        expmgmt.utils.dictparser.DictParser(experiment_setting).interpolate()
    )

    return tmp_object[1]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        arguments=[],
        experiment=expmgmt.config.settings._DEFAULT_NAME,
        data_set = None,
        setting = None
    ):

    # get temporary file with user defined settings
    tmp_settings_path = pass_settings(experiment, data_set, setting)

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
    help="Experiment",
    type=str,
    default=expmgmt.config.settings._DEFAULT_NAME
)
@click.option(
    "-d",
    "--data_set",
    help="Pass the trainings, test and validation of the specified dataset setting",
    type=click.Choice([
        expmgmt.config.settings._DEFAULT_NAME,
        *expmgmt.config.settings.get_datasets()
        ]
    ),
    default=expmgmt.config.settings._DEFAULT_NAME
)
@click.option(
    "-s",
    "--setting",
    help="Pass the trainings, test and validation of the specified dataset setting",
    type=str,
    default=expmgmt.config.settings._DEFAULT_NAME
)
def cli(
        arguments,
        experiment,
        data_set,
        setting
    ):
    """Run an arbitrary shell command in the library folder"""

    if not setting in expmgmt.config.settings.get_dataset_settings(data_set):
        raise expmgmt.debug.exceptions.ArgumentError(
            setting, 
            expmgmt.config.settings.get_dataset_settings(data_set)
        )

    run(
        arguments=arguments,
        experiment=experiment,
        data_set=data_set, 
        setting=setting,
    )
