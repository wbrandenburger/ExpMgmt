# ===========================================================================
#   list.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.config
import expmgmt.config.settings
import expmgmt.utils.format

import click
import logging
import os

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger('list')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        projects,
        experiments,
        experiment
    ):
    """Main method to the list command

    :return:: List different objects
    :rtype:  list
    """
    
    if projects:
        expmgmt.utils.format.print_data(expmgmt.config.settings.get_projects_name())
    elif experiments:
        expmgmt.utils.format.print_data(expmgmt.config.settings.get_experiments_name())
    else:
        expmgmt.utils.format.print_data(expmgmt.config.settings.get_experiment_settings(experiment=experiment))

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
@click.command(
    "list"
)
@click.help_option(
    "-h",
    "--help" 
)
@click.option(
    "--projects",
    help="Show all available projects and their main directory (default).",
    is_flag=True,
    default=False
)
@click.option(
    "--experiments",
    help="Show the experiment names of current project",
    is_flag=True,
    default=False
)
@click.option(
    "-e",
    "--experiment",
    help="Show the settings of the current experiment defined in {0}".format(expmgmt.config.settings._ENV_PROJECT),
    type=click.Choice([expmgmt.config.settings._DEFAULT_EXP_NAME, *expmgmt.config.settings.get_experiments_name()]),
    default=expmgmt.config.settings._DEFAULT_EXP_NAME
)
def cli(
        projects,
        experiments,
        experiment
    ):
    """List experiments' properties"""
 
    result = run(
        projects=projects,
        experiments=experiments,
        experiment = experiment
    )