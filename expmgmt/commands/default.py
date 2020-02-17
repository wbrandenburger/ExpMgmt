# ===========================================================================
#   default.py --------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.commands
import expmgmt.config.settings
import expmgmt.config.experiment

import click
import colorama
import difflib
import logging
import os
import sys

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class MultiCommand(click.MultiCommand):

    #   settings ------------------------------------------------------------
    # -----------------------------------------------------------------------
    scripts = expmgmt.commands.get_scripts()
    logger = logging.getLogger('multicommand')

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def list_commands(self, ctx):
        """List all matched commands in the command folder and in path

        >>> mc = MultiCommand()
        >>> rv = mc.list_commands(None)
        >>> len(rv) > 0
        True
        """
        rv = [s for s in self.scripts.keys()]
        rv.sort()
        return rv

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def get_command(self, ctx, name):
        """Get the command to be run

        >>> mc = MultiCommand()
        >>> cmd = mc.get_command(None, 'add')
        >>> cmd.name, cmd.help
        ('add', 'Add...')
        >>> mc.get_command(None, 'this command does not exist')
        """
        try:
            script = self.scripts[name]
        except KeyError:            
            colorama.init() # general: colorama has to be activated 
            self.logger.error( 
                "{c.Fore.RED}{c.Style.BRIGHT}{c.Back.BLACK}"
                "Did you mean {0}?"
                "{c.Style.RESET_ALL}"
                .format(
                    " or ".join(
                        difflib.get_close_matches(name, self.scripts, n=2)
                    ),
                    c=colorama
                )
            ) # @log
            return None
        if script['plugin']:
            return script['plugin']

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
@click.group(
    cls=MultiCommand,
    invoke_without_command=True
)
@click.help_option(
    "-h",
    "--help" 
)
@click.version_option(
    version=expmgmt.__version__
)
@click.option(
    "-p",
    "--project",
    help="Set the current project.",
    type=click.Choice([*expmgmt.config.settings.get_projects_name()]),
    default=expmgmt.config.config.get("default-proj")
)
@click.option(
    "-v",
    "--verbose",
    help="Make the output verbose (equivalent to --log DEBUG)",
    default=False,
    is_flag=True
)
@click.option(
    "--log",
    help="Logging level",
    type=click.Choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO"
)
@click.option(
    "--color",
    type=click.Choice(["always", "auto", "no"]),
    default="auto",
    help="Prevent the output from having color"
)
def run(
        project,
        verbose,
        log,
        color
    ):

    if (
        color == "no" or 
        (color == "auto" and not sys.stdout.isatty())):
        # Turn off colorama (strip escape sequences from the output)
        colorama.init(strip=True)
    else:
        colorama.init()

    log_format = (
        colorama.Fore.YELLOW +
        '%(levelname)s' +
        ':' +
        colorama.Fore.GREEN +
        '%(name)s' +
        colorama.Style.RESET_ALL +
        ':' +
        '%(message)s'
    )

    if verbose:
        log = "DEBUG"
        log_format = '%(relativeCreated)d-'+log_format
    logging.basicConfig(
        level=getattr(logging, log),
        format=log_format
    )
    
    logger = logging.getLogger('default')
    logger.debug("Plattform '{0}' detected.".format(sys.platform)) # @log
    print("HUUTUSAR")
    expmgmt.config.settings.set_project(project)
