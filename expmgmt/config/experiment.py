# ===========================================================================
#   experiment.py -----------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.configfile
import expmgmt.config.settings_default
import expmgmt.experiment.experiment

import os
import logging

#   settings ----------------------------------------------------------------
# ---------------------------------------------------------------------------
_CURRENT_EXPERIMENT = None  #: Current experiment in use

logger = logging.getLogger("config")

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def set_exp(experiment):
    """Set experiment

    :param experiment: Experiment object
    :type  experiment: expmgmt.experiment.Experiment

    """

    global _CURRENT_EXPERIMENT

    assert(isinstance(experiment, expmgmt.experiment.experiment.Experiment))

    config = expmgmt.config.configfile.get_configuration()
    if experiment.name not in config.keys():
        config[experiment.name] = dict(dirs=experiment.paths)
    _CURRENT_EXPERIMENT = experiment

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def set_exp_from_name(expname):
    """Set experiment, notice that in principle experiment can be a full path.

    :param expname: Name of the experiment or some path to a folder
    :type  expname: str
    """

    assert(isinstance(expname, str))

    set_exp(
        get_exp_from_name(expname)
    )

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_exp_from_name(expname):

    assert(isinstance(expname, str))

    config = expmgmt.config.configfile.get_configuration()
    if expname not in config.keys():
        if os.path.isdir(expname):
            # Check if the path exists, then use this path as a new experiment
            logger.warning(
                "Since {0} exists, interpreting it as a experiment".format(
                    expname
                )
            )
            experiment_obj = expmgmt.experiment.experiment.from_paths([expname])
            name = experiment_obj.path_format()
            config[name] = dict(dirs=experiment_obj.paths)
        else:
            raise Exception(
                "Path or experiment '%s' does not seem to exist" % expname
            )
    else:
        name = expname
        if name not in config.keys():
            raise Exception('Experiment {0} not defined'.format(expname))
        try:
            paths = [os.path.expanduser(config[name][ expmgmt.config.settings_default._LOCAL_DIR])]
        except KeyError:
            try:
                paths = eval(os.path.expanduser(config[name].get("dirs")))  # @todo[to change]:
            except SyntaxError as e:
                raise Exception(
                    "To define a experiment you have to set either dir or dirs"
                    " in the configuration file.\n"
                    "Error: ({0})".format(e)
                )
        experiment_obj = expmgmt.experiment.experiment.Experiment(expname, paths)
    return experiment_obj

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_exp_dirs():
    """Get the directories of the current experiment

    :return:: A list of paths
    :rtype:  list
    """

    return get_exp().paths

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_exp_name():

    return get_exp().name

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_exp():
    """Get current experiment, if there is no experiment set before,
    the default experiment will be retrieved.
    If the `EXPMGMT_EXP` environment variable is defined, this is the
    experiment name (or path) that will be taken as a default.

    :return:: Current experiment
    :rtype:  expmgmt.experiment.Experiment
    """

    global _CURRENT_EXPERIMENT

    if os.environ.get(expmgmt.config.settings_default._ENV_EXP):
        logger.debug("Environment variable '{0}' found with value '{1}'".format(
            expmgmt.config.settings_default._ENV_EXP,
            os.environ.get(expmgmt.config.settings_default._ENV_EXP)
            )
        )
        set_exp_from_name(
            os.environ[expmgmt.config.settings_default._ENV_EXP]
        ) 

    if _CURRENT_EXPERIMENT is None:
        # Do not put expmgmt.config.configfile.get because get is a special function that also needs the experiment to see if some key was overridden!
        exp = expmgmt.config.settings_default.get_settings_default(key=expmgmt.config.settings_default._DEFAULT_EXP)
        set_exp_from_name(exp)

    assert(isinstance(_CURRENT_EXPERIMENT, expmgmt.experiment.experiment.Experiment))
    
    return _CURRENT_EXPERIMENT