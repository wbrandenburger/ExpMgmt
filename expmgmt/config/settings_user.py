
# ===========================================================================
#   settings_user.py --------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.configfile
import expmgmt.config.experiment

import logging
import os
import yaml

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
_LOCAL_SETTINGS = "local-settings"
_LOCAL_SETTINGS_DEFAULT = "local-settings-default"

# @todo[to change]: logging

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_local_settings(default=True):

    if default:
        settings_file = expmgmt.config.configfile.get(_LOCAL_SETTINGS_DEFAULT)
        if not os.path.isfile(settings_file):
            raise SyntaxError("Settings file {0} with default values does not exist".format(settings_file))
    else:
        settings_file = expmgmt.config.configfile.get(_LOCAL_SETTINGS)
        if not os.path.isfile(settings_file):
            # raise SyntaxWarning("Settings file {0} does not exist".format(settings_file))
            return None
    
    with open(settings_file) as f:
            object_list = yaml.load(f, Loader=yaml.FullLoader)

    return object_list

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_experiment_settings(expname):
    
    exp_settings = get_local_settings(default=False)

    exp_item = None
    if exp_settings is not None:
        for item in exp_settings:
            if item["name"] == expname:
                exp_item = item
                break

    default_settings = get_local_settings()

    if exp_item is not None:
        # raise expmgmt.debug.exceptions.DefaultSettingValueMissing(expname) # @todo[to change]: exception is actually used for ini and not json's
        default_settings.update(exp_item)

    return default_settings