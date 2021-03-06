# ===========================================================================
#   experiment.py -----------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.config
import expmgmt.config.settings
import expmgmt.utils.experiment

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

    assert(isinstance(experiment, expmgmt.utils.experiment.Experiment))

    config = expmgmt.config.config.get_configuration()
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

    config = expmgmt.config.config.get_configuration()
    if expname not in config.keys():
        if os.path.isdir(expname):
            # Check if the path exists, then use this path as a new experiment
            logger.warning(
                "Since {0} exists, interpreting it as a experiment".format(
                    expname
                )
            ) # @log
            experiment_obj = expmgmt.utils.experiment.from_paths([expname])
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
            paths = [os.path.expanduser(config[name][ expmgmt.config.settings._LOCAL_DIR])]
        except KeyError:
            try:
                paths = eval(os.path.expanduser(config[name].get("local-dir")))  # @todo[to change]:
            except SyntaxError as e:
                raise Exception(
                    "To define a experiment you have to set either dir or dirs"
                    " in the configuration file.\n"
                    "Error: ({0})".format(e)
                )
        experiment_obj = expmgmt.utils.experiment.Experiment(expname, paths)
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
def get_proj_name():

    return get_exp().name

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_exp():
    """Get current experiment, if there is no experiment set before,
    the default experiment will be retrieved.
    If the `EXPMGMT_PROJECT` environment variable is defined, this is the
    experiment name (or path) that will be taken as a default.

    :return:: Current experiment
    :rtype:  expmgmt.experiment.Experiment
    """

    #global _CURRENT_EXPERIMENT
    #if _CURRENT_EXPERIMENT is None:
    set_exp_from_name(expmgmt.config.settings._PROJECT) 
    if _CURRENT_EXPERIMENT is None:
        # Do not put expmgmt.config.config.get because get is a special function that also needs the experiment to see if some key was overridden!
        exp = expmgmt.config.settings.get_settings_default(key=expmgmt.config.settings._DEFAULT_PROJ)
        set_exp_from_name(exp)

    assert(isinstance(_CURRENT_EXPERIMENT, expmgmt.utils.experiment.Experiment))
    return _CURRENT_EXPERIMENT