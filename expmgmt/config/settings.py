# ===========================================================================
#   settings_default.py -----------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.configfile
import expmgmt.config.experiment
import expmgmt.utils.yaml

from collections import OrderedDict
import logging
import os
import sys
import yaml

from pathlib import Path # @todo[to change]: https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
_GENERAL_SETTINGS_NAME = "settings"

_ENV_PROJECT = "EXPMGMT_PROJECT"

_DEFAULT_PROJ = "default-proj"
_PROJ_NAME = "proj-name"
_LOCAL_DIR = "local-dir"
_LOCAL_CONFIG = "local-config"
_LOCAL_SETTINGS_EXP = "local-settings-experiments"
_LOCAL_SETTINGS_DEFAULT = "local-settings-default"

_MAIN_PROJ_FILE = "main-proj-file"

_DEFAULT_PROJ_NAME = "project"
_DEFAULT_EXP_NAME = "default"

_PROJECT_DIR = "projects"
_SCRIPT_DIR = "scripts"

_OVERRIDE_VARS = {
    "folder": None,
    "file": None,
    "scripts": None
}

logger = logging.getLogger("config")

#   lambda's ----------------------------------------------------------------
# ---------------------------------------------------------------------------
get_env = lambda x: os.environ.get(x)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_config_dirs():
    """Get expmgmt configuration directories where the configuration
    files might be stored

    :return:: Folder where the configuration files might be stored
    :rtype:  list
    """

    dirs = []

    if os.environ.get('XDG_CONFIG_DIRS'):
        # get_config_home should also be included on top of XDG_CONFIG_DIRS
        dirs += [
            os.path.join(d, 'expmgmt') for d in
            os.environ.get('XDG_CONFIG_DIRS').split(':')
        ]

    # Take XDG_CONFIG_HOME and ~/.expmgmt for backwards compatibility
    dirs += [
        os.path.join(get_config_home(), 'expmgmt'),
        os.path.join(os.path.expanduser('~'), '.expmgmt')
    ]

    return dirs

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_config_folder():
    """Get folder where the configuration files are stored,
    e.g. ``~/expmgmt``. It is XDG compatible, which means that if the
    environment variable ``XDG_CONFIG_HOME`` is defined it will use the
    configuration folder ``XDG_CONFIG_HOME/expmgmt`` instead.

    :return:: Folder where the configuration files are stored
    :rtype:  str
    """

    config_dirs = get_config_dirs()

    for config_dir in config_dirs:
        if os.path.exists(config_dir):
            return config_dir

    # If no folder is found, then get the config home
    return os.path.join(get_config_home(), "expmgmt")

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_config_home():
    """Get the base directory relative to which user specific configuration
    files should be stored.

    :return:: Configuration base directory
    :rtype:  str
    """

    xdg_home = os.environ.get('XDG_CONFIG_HOME')

    if xdg_home:
        return os.path.expanduser(xdg_home)
    else:
        return os.path.join(os.path.expanduser('~'), '.config')

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_config_file():
    """Get the path of the main configuration file,
    e.g. /home/user/.config/expmgmt/config
    """

    global _OVERRIDE_VARS

    if _OVERRIDE_VARS["file"] is not None:
        config_file = _OVERRIDE_VARS["file"]
    else:
        config_file = os.path.join(
            get_config_folder(), "config.ini"
        )

    logger.debug("Getting config file %s" % config_file) # @log

    return config_file

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_configpy_file():
    """Get the path of the main python configuration file,
    e.g. /home/user/.config/expmgmt/config.py
    """

    return os.path.join(get_config_folder(), "config.py")

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def set_config_file(filepath):
    """Override the main configuration file path
    """

    global _OVERRIDE_VARS

    logger.debug("Setting config file to %s" % filepath) # @log

    _OVERRIDE_VARS["file"] = filepath

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_scripts_folder():
    """Get folder where the scripts are stored,
    e.g. /home/user/.config/expmgmt/scripts
    """

    return os.path.join(
        get_config_folder(), _SCRIPT_DIR, 
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_projects_folder():
    """Get folder where the projects are stored,
    e.g. /home/user/.config/expmgmt/projects
    """

    return os.path.join(
        get_config_folder(), _PROJECT_DIR, _DEFAULT_PROJ_NAME
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_general_settings_name():
    """Get the section name of the general settings

    :return:: Section's name
    :rtype:  str

    >>> get_general_settings_name()
    'settings'
    """
    return _GENERAL_SETTINGS_NAME

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_settings_default(section="", key=""):
    """Get the default settings for all non-user variables
    in expmgmt.

    If section and key are given, then the setting
    for the given section and the given key are returned.

    If only ``key`` is given, then the setting
    for the ``general`` section is returned.

    :param section: Particular section of the default settings
    :type  section: str
    :param key: Setting's name to be queried for.
    :type  key: str

    """
    global _settings_default
    
    # the first entry of an OrderedDict will always be the general
    # settings which is preferable for automatic documentation
    if _settings_default is None:
        _settings_default = OrderedDict()
        import expmgmt.config.settings
        _settings_default.update({
            get_general_settings_name(): get_settings_default(),
        })

    if not section and not key:
        return _settings_default
    elif not section:
        return _settings_default[get_general_settings_name()][key]
    else:
        return _settings_default[section][key]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_default_opener():
    """Get the default file opener for the current system
    
    :return: Default file opener
    :type: str
    """
    if sys.platform.startswith("darwin"):
        return "open"
    elif os.name == 'nt':
        return "start"
    elif os.name == 'posix':
        return "xdg-open"

#   settings ----------------------------------------------------------------
# --------------------------------------------------------------------------- 
_settings_default = { # default settings
    get_general_settings_name(): {
        _DEFAULT_PROJ: _DEFAULT_PROJ_NAME
    },
    _DEFAULT_PROJ_NAME: {
        _PROJ_NAME : _DEFAULT_PROJ_NAME,
        _LOCAL_DIR: get_projects_folder(),
        _LOCAL_CONFIG: "${{{0}}}\{1}.ini".format(_LOCAL_DIR, _DEFAULT_PROJ_NAME),
        _LOCAL_SETTINGS_DEFAULT : "${{{0}}}\{1}-default.json".format(_LOCAL_DIR, _DEFAULT_PROJ_NAME),
        _LOCAL_SETTINGS_EXP : "${{{0}}}\{1}-experiments.json".format(_LOCAL_DIR, _DEFAULT_PROJ_NAME)
    }
}

_settings_default_experiment = {
    "name": _DEFAULT_EXP_NAME
}

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_local_settings(default=True):

    if default:
        settings_file = expmgmt.config.configfile.get(expmgmt.config.settings._LOCAL_SETTINGS_DEFAULT)
        if not os.path.isfile(settings_file):
            logger.debug("Settings file {0} with default experiment does not exist".format(settings_file)) # @log
            return expmgmt.config.settings._settings_default_experiment

    else:
        settings_file = expmgmt.config.configfile.get(expmgmt.config.settings._LOCAL_SETTINGS_EXP)
        if not os.path.isfile(settings_file):
            logger.debug("Settings file {0} with experiment settings does not exist".format(settings_file)) # @log
            return

    data = expmgmt.utils.yaml.yaml_to_data(settings_file, raise_exception=True)
    return data

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_projects_name():
    
    config = expmgmt.config.configfile.get_configuration()

    return [
        config[section][_PROJ_NAME] for section in config if _PROJ_NAME in config[section]
    ]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_experiments_name():
    exp_settings = get_local_settings(default=False)
    
    if exp_settings is None:
        return [_DEFAULT_EXP_NAME]
    else:
        return [item["name"] for item in exp_settings]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_experiment_settings(
        experiment=_DEFAULT_EXP_NAME
    ):
    
    default_settings = get_local_settings()
    optional_default_settings = expmgmt.config.configfile.get_section(_DEFAULT_EXP_NAME)
    
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
    elif experiment != _DEFAULT_EXP_NAME:
        raise expmgmt.debug.exceptions.DefaultExperimentMissing(experiment)
    
    return default_settings