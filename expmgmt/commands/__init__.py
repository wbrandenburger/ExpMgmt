# ===========================================================================
#   __init__.py -------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.utils.configuration
import expmgmt.plugin

import glob
import logging
import os
import re
from stevedore import extension

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
commands_mgr = None

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def _create_commands_mgr():
    global commands_mgr

    if commands_mgr is not None:
        return

    commands_mgr = extension.ExtensionManager(
        namespace='expmgmt.command',
        invoke_on_load=False,
        verify_requirements=True,
        propagate_map_exceptions=True,
        on_load_failure_callback=expmgmt.plugin.stevedore_error_handler
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_scripts():
    global commands_mgr
    _create_commands_mgr()
    scripts_dict = dict()
    for command_name in commands_mgr.names():
        scripts_dict[command_name] = dict(
            command_name=command_name,
            path=None,
            plugin=commands_mgr[command_name].plugin
        )
    return scripts_dict
