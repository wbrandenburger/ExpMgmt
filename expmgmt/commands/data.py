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
    "--data",
    help="Pass the trainings, test and validation of the specified dataset setting",
    nargs=2, 
    type=(
        click.Choice(["default",*expmgmt.config.settings.get_datasets()]), str
    ),
    default=("default","default")
)
def cli(
        data
    ):
    """List experiments' properties"""

    if data[0] == "default":
        data_setting = (
            expmgmt.config.config.get
            (expmgmt.config.settings._DEFAULT_DATASET),
            expmgmt.config.config.get(expmgmt.config.settings._DEFAULT_SETTING)
        )
    else:
        data_setting = data
        
        if not data_setting[1] in expmgmt.config.settings.get_dataset_settings(data_setting[0]):
            raise ValueError("Error: Invalid value for '-d' / '--data': invalid choice: {0}. (choose from {1})".format(
                data_setting[1], 
                expmgmt.config.settings.get_dataset_settings(data_setting[0])
                )
            ) # @todo[generalize]: also in expmgmt

    if data[1] == "default":
        data_setting = (data_setting[0], "")

    run(
        data_setting[0],
        data_setting[1]
    )