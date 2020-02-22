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
            dataset,
            setting
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
        data_set,
        setting
    ):
    """List experiments' properties"""

    if not setting in expmgmt.config.settings.get_dataset_settings(data_set):
        raise expmgmt.debug.exceptions.ArgumentError(
            setting, 
            expmgmt.config.settings.get_dataset_settings(data_set)
        )

    run(
        data_set,
        setting
    )