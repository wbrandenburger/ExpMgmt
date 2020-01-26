# ===========================================================================
#   configfile.py -------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.utils.configuration
import expmgmt.config.settings_default
import expmgmt.debug.exceptions
import expmgmt.config.experiment

from collections import OrderedDict
import configparser
import logging
import os
import sys

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
_CONFIGURATION = None  #: Global configuration object variable

logger = logging.getLogger("config")

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def set(key, val, section=None):
    """Set a key to val in some section and make these changes available
    everywhere.
    """
    config = get_configuration()
    if not config.has_section(section or "settings"):
        config.add_section(section or "settings")
    config[section or get_general_settings_name()][key] = str(val)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def general_get(key, section=None, data_type=None, required=False):
    # @todo[to change]: Changed required to False -> implications for default settings
    """General getter method that will be specialized for different modules.

    :param data_type: The data type that should be expected for the value of
        the variable.
    :type  data_type: DataType, e.g. int, src ...
    :param default: Default value for the configuration variable if it is not
        set.
    :type  default: It should be the same that ``data_type``
    :param extras: List of tuples containing section and prefixes
    """

    # initialize main variable
    method = None
    value = None

    config = get_configuration()
    expname = expmgmt.config.experiment.get_proj_name()  
    global_section = expmgmt.config.settings_default.get_general_settings_name() 
    specialized_key = section + "-" + key if section is not None else key
    extras = [(section, key)] if section is not None else []
    sections = [(global_section, specialized_key)] +\
        extras + [(expname, specialized_key)]
    
    settings_default = expmgmt.config.settings_default.get_settings_default()

    # Check data type for setting getter method
    if data_type == int:
        method = config.getint
    elif data_type == float:
        method = config.getfloat
    elif data_type == bool:
        method = config.getboolean
    else:
        method = config.get

    # Try to get key's value from configuration
    for extra in sections:
        sec = extra[0]
        whole_key = extra[1]
        if sec not in config.keys():
            continue
        if whole_key in config[sec].keys():
            value = method(sec, whole_key)

    if value is None and required is True:
        try:
            default = settings_default[
                section or global_section
            ][
                specialized_key if section is None else key
            ]
        except KeyError:
            raise expmgmt.debug.exceptions.DefaultSettingValueMissing(key) # @todo[to change]: create function and imnport 
        else:
            return default
    return value

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get(*args, **kwargs):
    """String getter
    """
    return general_get(*args, **kwargs)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_section(section, required=False):
    """Section getter
    """
    data = dict()
    config = get_configuration()

    if section in config.keys():
        return config[section]
    else:
        if required:
            raise expmgmt.debug.exceptions.DefaultSettingValueMissing(section) # @todo[to change]: missing section
    return data

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def getint(*args, **kwargs):
    """Integer getter

    >>> set('something', 42)
    >>> getint('something')
    42
    """
    return general_get(*args, data_type=int, **kwargs)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def getfloat(*args, **kwargs):
    """Float getter

    >>> set('something', 0.42)
    >>> getfloat('something')
    0.42
    """
    return general_get(*args, data_type=float, **kwargs)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def getboolean(*args, **kwargs):
    """Bool getter

    >>> set('add-open', True)
    >>> getboolean('add-open')
    True
    """
    return general_get(*args, data_type=bool, **kwargs)

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def getlist(key, **kwargs):
    """List getter

    :return:: A python list
    :rtype:  list
    :raises SyntaxError: Whenever the parsed syntax is either not a valid
        python object or a valid python list.
    """
    rawvalue = general_get(key, **kwargs)
    if isinstance(rawvalue, list):
        return rawvalue
    try:
        value = eval(rawvalue)
    except Exception as e:
        raise SyntaxError(
            "The key '{0}' must be a valid python object\n\t{1}".format(key, e)
        )
    else:
        if not isinstance(value, list):
            raise SyntaxError(
                "The key '{0}' must be a valid python list".format(key)
            )
        return value

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_configuration():
    """Get the configuration object, if no expmgmt configuration has ever been
    initialized, it initializes one. Only one configuration per process should
    ever be configured.

    :return:: Configuration object
    :rtype:  expmgmt.utils.configuration.Configuration
    """
    global _CONFIGURATION
    if _CONFIGURATION is None:
        logger.debug("Creating configuration")
        _CONFIGURATION = expmgmt.utils.configuration.Configuration()
        # Handle local configuration file, and merge it if it exists
        merge_configuration_from_path(get(expmgmt.config.settings_default._LOCAL_CONFIG), _CONFIGURATION)
    return _CONFIGURATION

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def merge_configuration_from_path(path, configuration):
    """
    Merge information of a configuration file found in `path`
    to the information of the configuration object stored in `configuration`.

    :param path: Path to the configuration file
    :type  path: str
    :param configuration: Configuration object
    :type  configuration: expmgmt.utils.configuration.Configuration
    """
    if not os.path.exists(path):
        logger.warning("Merging configuration: File {0} does not exist.".format(path))
        return
    logger.debug("Merging configuration from {0}".format(path))
    configuration.read(path)
    configuration.handle_includes()

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def reset_configuration():
    """Destroys existing configuration and return: a new one.

    :return:: Configuration object
    :rtype:  expmgmt.utils.configuration.Configuration
    """
    global _CONFIGURATION
    if _CONFIGURATION is not None:
        logger.warning("Overwriting previous configuration")
    _CONFIGURATION = None
    logger.debug("Resetting configuration")
    return get_configuration()

