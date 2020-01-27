
# ===========================================================================
#   settings_user.py --------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.configfile
import expmgmt.config.experiment
import expmgmt.config.settings_default
import expmgmt.utils.yaml

import logging
import os
import yaml

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
logger = logging.getLogger("config")

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_local_settings(default=True):

    if default:
        settings_file = expmgmt.config.configfile.get(expmgmt.config.settings_default._LOCAL_SETTINGS_DEFAULT)
        if not os.path.isfile(settings_file):
            logger.debug("Settings file {0} with default experiment does not exist".format(settings_file))
            return expmgmt.config.settings_default._settings_default_experiment

    else:
        settings_file = expmgmt.config.configfile.get(expmgmt.config.settings_default._LOCAL_SETTINGS_EXP)
        if not os.path.isfile(settings_file):
            logger.debug("Settings file {0} with experiment settings does not exist".format(settings_file))
            return

    # @todo[to change]: add logger
    data = expmgmt.utils.yaml.yaml_to_data(settings_file, raise_exception=True)
    return data

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_projects_name():
    
    config = expmgmt.config.configfile.get_configuration()

    return [
        config[section][expmgmt.config.settings_default._PROJ_NAME] for section in config if expmgmt.config.settings_default._PROJ_NAME in config[section]
    ]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_experiments_name():
    exp_settings = get_local_settings(default=False)
    
    if exp_settings is None:
        return [expmgmt.config.settings_default._DEFAULT_EXP_NAME]
    else:
        return [item["name"] for item in exp_settings]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_experiment_settings(
        experiment=expmgmt.config.settings_default._DEFAULT_EXP_NAME
    ):
    
    default_settings = get_local_settings()
    optional_default_settings = expmgmt.config.configfile.get_section(expmgmt.config.settings_default._DEFAULT_EXP_NAME)
    
    if optional_default_settings is not dict():
        default_settings.update(optional_default_settings)

    experiment_object = None
    if experiment in get_experiments_name():
        experiment_settings = get_local_settings(default=False)
        if experiment_settings is not None:
            for item in experiment_settings:
                if item["name"] == experiment:
                    default_settings.update(item)
                    return default_settings
    elif experiment != expmgmt.config.settings_default._DEFAULT_EXP_NAME:
        raise expmgmt.debug.exceptions.DefaultExperimentMissing(experiment)
    
    return default_settings