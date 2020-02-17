# ===========================================================================
#   data.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.settings
import expmgmt.config.config

import click
import logging

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger('list')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        dataset,
        setting
    ):
    """Main method to the list command
    """
    
    log_setting  = setting if setting else "default" 
    logger.debug("Create setting '{0}' from dataset '{1}'".format(log_setting, dataset))

    if dataset in expmgmt.config.settings.get_datasets():
        expmgmt.config.settings.set_dataset(
            dataset=dataset,
            predefined=setting
        )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
@click.command(
    "data"
)
@click.help_option(
    "-h",
    "--help" 
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
def cli(
        data_set,
        setting
    ):
    """List experiments' properties"""

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

    if setting == "default":
        run_data_set = data_set
        run_setting = setting

    run(
        run_data_set,
        run_setting
    )