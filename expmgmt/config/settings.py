# ===========================================================================
#   settings_default.py -----------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.config
import expmgmt.config.experiment
import expmgmt.utils.yaml
import expmgmt.utils.structures

from collections import OrderedDict
import logging
import os
import sys
import yaml

from pathlib import Path # @todo[to change]: https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
_GENERAL_SETTINGS_NAME = "settings"
_DEFAULT_PROJ_NAME = "project"
_DEFAULT_EXP_NAME = "default"

_ENV_PROJECT = "EXPMGMT_PROJECT"

_DEFAULT_PROJ = "default-proj"
_PROJ_NAME = "name"

_LOCAL_DIR = "local-dir"
_LOCAL_CONFIG = "local-config"
_LOCAL_SETTINGS_EXP = "local-experiments"

_MAIN_PROJ_FILE = "proj-file"

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
        _LOCAL_SETTINGS_EXP : "${{{0}}}\{1}-experiments.json".format(_LOCAL_DIR, _DEFAULT_PROJ_NAME),
    }
}

_settings_default_experiment = {
    "name": _DEFAULT_EXP_NAME
}

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_settings(file, description="", required=False):

    if not os.path.isfile(file):
        logger.debug("File {0} {1} does not exist".format(file, description)) # @log

    return expmgmt.utils.yaml.yaml_to_data(file, raise_exception=True)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_projects_name():
    
    config = expmgmt.config.config.get_configuration()

    return [
        config[section][_PROJ_NAME] for section in config if _PROJ_NAME in config[section]
    ]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_experiments_name():
    exp_settings = get_settings(expmgmt.config.config.get(expmgmt.config.settings._LOCAL_SETTINGS_EXP))
    
    if exp_settings is None:
        return [_DEFAULT_EXP_NAME]
    else:
        return [item["name"] for item in exp_settings]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_experiment_settings(
        experiment=_DEFAULT_EXP_NAME
    ):
    
    settings = get_settings(expmgmt.config.config.get(expmgmt.config.settings._LOCAL_SETTINGS_EXP))
    if settings is None:
        raise ValueError("Nothing to process")

    if experiment in get_experiments_name():
        default_setting = expmgmt.utils.structures.get_dict_elements(settings, 
            "name", [_DEFAULT_EXP_NAME, experiment], update=True)

        expmgmt.utils.structures.update_dict(default_setting, expmgmt.config.config.get_section(_DEFAULT_EXP_NAME))
    elif experiment != _DEFAULT_EXP_NAME:
        raise expmgmt.debug.exceptions.DefaultExperimentMissing(experiment)
    
    return default_setting

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data_settings(
        experiment="vaihingen",
        fullpath=True,
        sort=True
    ):
    data_config_file = expmgmt.config.config.get("data-config")


    from configparser import ConfigParser, ExtendedInterpolation
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(data_config_file)


    settings = expmgmt.utils.yaml.yaml_to_data(config[experiment]["local-config"], raise_exception=True)

    for item in settings.keys():
        data_tensor = get_data_tensor(settings[item], fullpath=fullpath,sort=sort)
        with open(os.path.join(config[experiment]["settings-dir"],"{0}.txt ".format(item)),"w+") as f:
            for line in data_tensor:
                f.write(" ".join("{}".format(x) for x in line)+"\n")
    return  

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_file_list(path, fullpath=True, sort=True):
    file_list = sorted(os.listdir(path)) if sort else os.listdir(path)
    file_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    return  [os.path.join(path,f) for f in file_list] if fullpath else  file_list
    
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_pattern_list(path, regex, group, sort=True):
    import re
    pattern = re.compile(regex)
    return [pattern.search(f).group(group) for f in get_file_list(path,sort=sort)]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_pattern_list_related_to_regex_list(path, regex, group, regex_list, fullpath=False, sort=True):
    import re
    
    file_list = get_file_list(path, fullpath=fullpath, sort=sort)

    result_file_list = [None]*(len(file_list))
    for c_regex, item in enumerate(regex_list):
        pattern = re.compile(regex.replace("%(ref)s",item))
        for c_files, f in enumerate(file_list):
            result_search = pattern.search(f)
            if result_search:
                result_file_list[c_regex] = file_list[c_files]

    return result_file_list

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data_tensor(object, fullpath=False, sort=True):
    
    if isinstance(object, list) and len(object)>0:
        obj_iter = iter(object)
        obj_item = next(obj_iter)

        lists = list()
        lists.append(get_file_list(obj_item["dir"], fullpath=fullpath, sort=sort))

        regex_list = get_pattern_list(obj_item["dir"], obj_item["regex"],obj_item["group"], sort=sort)

        while True:
            try:
                obj_item = next(obj_iter)
            except StopIteration:
                # if StopIteration is raised, break from loop
                break
            lists.append(get_pattern_list_related_to_regex_list(obj_item["dir"], obj_item["regex"], obj_item["group"], regex_list, fullpath=fullpath, sort=sort))

    
    return [data_tuple for data_tuple in zip(*lists)]


