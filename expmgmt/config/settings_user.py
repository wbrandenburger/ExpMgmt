
# ===========================================================================
#   settings_user.py --------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.configfile
import expmgmt.config.experiment
import expmgmt.utils.yaml

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
            return None
    # @todo[to change]: add logger
    data = expmgmt.utils.yaml.yaml_to_data(settings_file, raise_exception=True)
    return data

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_experiments_name():
    exp_settings = get_local_settings(default=False)
    return [{
        expmgmt.config.experiment._CURRENT_EXPERIMENT: item["name"]
        }
        for item in exp_settings
    ]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_experiment_settings(
        experiment="default"
    ):
    
    exp_settings = get_local_settings(default=False)

    exp_item = None
    if exp_settings is not None:
        for item in exp_settings:
            if item["name"] == experiment:
                exp_item = item
                break

    default_settings = get_local_settings()
    optional_default_settings = expmgmt.config.configfile.get_section("default")
    
    if optional_default_settings is not dict():
        default_settings.update(optional_default_settings)

    if exp_item is not None:
        # raise expmgmt.debug.exceptions.DefaultSettingValueMissing(experiment) # @todo[to change]: exception is actually used for ini and not json's
        default_settings.update(exp_item)

    return default_settings