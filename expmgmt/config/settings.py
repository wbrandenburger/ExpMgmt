# ===========================================================================
#   settings_default.py -----------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.config
import expmgmt.config.experiment
import expmgmt.utils.yaml
import expmgmt.utils.structures
import expmgmt.data.data

from collections import OrderedDict
import logging
import os
import sys
import yaml

from pathlib import Path # @todo[to change]: https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
_PROJECT = "project"

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def set_project(project):
    global _PROJECT
    _PROJECT = project

_GENERAL_SETTINGS_NAME = "settings"
_DEFAULT_PROJ_NAME = "project"
_DEFAULT_EXP_NAME = "default"
_DEFAULT_SET_NAME = "default"

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

_DATASET = None
_DEFAULT_DATASET = "default-dataset"
_DEFAULT_SETTING = "default-setting"
_META_DATA = ["type"]

_settings_default = None

logger = logging.getLogger("config")

#   lambda's ----------------------------------------------------------------
# ---------------------------------------------------------------------------
get_env = lambda x: os.environ.get(x)
get_env_project = lambda: os.environ.get(_ENV_PROJECT)

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
def get_scripts():
    
    file_list = [os.path.splitext(f)[0] for f in os.listdir(get_scripts_folder()) if os.path.isfile(os.path.join(get_scripts_folder(), f))]

    if file_list == list():
        raise ValueError("The predefined task folder seems to be empty.")

    return file_list

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
    print(expmgmt.config.config.get(expmgmt.config.settings._LOCAL_SETTINGS_EXP))
    exp_settings = get_settings(expmgmt.config.config.get(expmgmt.config.settings._LOCAL_SETTINGS_EXP))
    print(exp_settings)
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
def get_data(path):
    #print(path)
    with open(path) as f:
        return [line.split() for line in f]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_dataset(dataset):

    from configparser import ConfigParser, ExtendedInterpolation

    data_config_file = expmgmt.config.config.get("data-config")
    with open(data_config_file) as f:
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.readfp(f)
        sections = config.sections()
        
        return get_settings(config[dataset]["local-config"], description="", required=True)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def set_dataset_config():
    
    from configparser import ConfigParser, ExtendedInterpolation
    global _DATASET

    data_config_file = expmgmt.config.config.get("data-config")
    with open(data_config_file) as f:
        _DATASET = ConfigParser(interpolation=ExtendedInterpolation())
        _DATASET.readfp(f)
    
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_dataset_setting(dataset):
    if not _DATASET:
        set_dataset_config()

    return get_settings(_DATASET[dataset]["local-config"], description="", required=True)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_datasets():
    if not _DATASET:
        set_dataset_config()
    
    sections = _DATASET.sections()
    datasets = list()
    for section in sections:
        items = _DATASET.items(section)
        for item in items:
            if item[0] == "name":
                datasets.append(item[1])

    return datasets

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_dataset_settings(dataset):
    if not _DATASET:
        set_dataset_config()

    result = list()
    for dataset in get_datasets():
        dataset_obj = get_dataset_setting(dataset)
        if isinstance(dataset_obj,dict):
            for setting in dataset_obj.keys():
                result.append(setting)
    return result

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_dataset_setting_files(dataset, setting):
    if not _DATASET:
        set_dataset_config()

    setting_obj = get_dataset_setting(dataset)[setting]

    result = {"dataset": dataset, "setting": setting}
    for setting_type in setting_obj.keys():
        if not setting_type == "meta":
            result[setting_type] = (os.path.join(get_dataset_settings_dir(dataset),"{0}-{1}.txt".format(setting, setting_type)))
    return result

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_dataset_settings_dir(dataset):
    if not _DATASET:
        set_dataset_config()

    return _DATASET[dataset]["settings-dir"]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_dataset_meta_settings(dataset, setting):
    if not _DATASET:
        set_dataset_config()
        
    meta_settings = get_dataset_setting(dataset)["default"]["meta"]
    meta_settings.update(get_dataset_setting(dataset)[setting]["meta"])
    return meta_settings

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def set_dataset(
        dataset,
        predefined = "",
        sort=True
    ):
    dataset_obj = get_dataset_setting(dataset)

    data = dict()
    dataset_settings = dataset_obj.keys()
    if predefined:
        dataset_settings = [predefined]
    for setting in dataset_settings:
        setting_obj = dataset_obj[setting]
        
        for setting_type in setting_obj.keys():

            setting_type_obj = setting_obj[setting_type]
            if setting_type == "meta":
                x=1 # @todo[change]:  
            else: 
                path = os.path.join(get_dataset_settings_dir(dataset),"{0}-{1}.txt".format(setting, setting_type))
                if predefined and (not setting_type in data.keys()):
                    data[setting_type] = get_data(os.path.join(get_dataset_settings_dir(dataset),"default-{0}.txt".format(setting_type)))

                if not setting_type in data.keys():
                    data[setting_type] = get_data_tensor(setting_type_obj, sort=sort)
                    with open(path, "w+") as f:
                        for line in data[setting_type]:
                            f.write(" ".join("{}".format(x) for x in line)+"\n")
                else:
                    data_tensor = data[setting_type].copy()
                    for item in setting_type_obj:
                            task_func = getattr(expmgmt.data.data, item["func"])
                            data_tensor = task_func(data_tensor, *item["parameter"])

                    with open(path, "w+") as f:
                        for line in data_tensor:
                            f.write(" ".join("{}".format(x) for x in line)+"\n")
    return  

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_file_list(path, sort=True):
    path = path if isinstance(path, list) else [path]

    file_list = list()
    for item in path:   
        file_list.extend([os.path.join(item, f) for f in os.listdir(item) if os.path.isfile(os.path.join(item, f))])
        
    return file_list
    
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_pattern_list(path, regex, group, sort=True):
    import re
    pattern = re.compile(regex)
    return [pattern.search(f).group(group) for f in get_file_list(path,sort=sort)]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_pattern_list_related_to_regex_list(path, regex, group, regex_list, sort=True):
    import re
    
    file_list = get_file_list(path, sort=sort)

    result_file_list = [None]*(len(regex_list))
    for c_regex, item in enumerate(regex_list):
        pattern = re.compile(regex.replace("%(ref)s",item))
        # logger.debug("Search for pattern {0} '{1}' in folder '{2}'".format(regex.replace("%(ref)s",item),item, path)) # @log
        for c_files, f in enumerate(file_list):
            result_search = pattern.search(f)
            
            if result_search:
                result_file_list[c_regex] = file_list[c_files]

    return result_file_list        
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data_tensor(object, sort=True):
    
    if isinstance(object, list) and len(object)>0:
        obj_iter = iter(object)
        obj_item = next(obj_iter)

        lists = list()
        metadata = dict
        lists.append(get_file_list(obj_item["dir"], sort=sort))

        regex_list = get_pattern_list(obj_item["dir"], obj_item["regex"],obj_item["group"], sort=sort)

        while True:
            try:
                obj_item = next(obj_iter)
            except StopIteration:
                # if StopIteration is raised, break from loop
                break
            lists.append(get_pattern_list_related_to_regex_list(obj_item["dir"], obj_item["regex"], obj_item["group"], regex_list, sort=sort))

    
    return [data_tuple for data_tuple in zip(*lists)]


