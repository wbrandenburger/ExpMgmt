# ===========================================================================
#   data.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.settings

import click
import logging

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger('list')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        dataset = "none"
    ):
    """Main method to the list command
    """
    
    if dataset in expmgmt.config.settings.get_datasets():
        expmgmt.config.settings.set_dataset(
            dataset=dataset
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
    "-s",
    "--set_data",
    help="Set the setting files for the specified datasets",
    type=click.Choice(["none",*expmgmt.config.settings.get_datasets()]),
    default="none"
)
def cli(
        set_data,
    ):
    """List experiments' properties"""

    run(
        dataset = set_data
    )