# ===========================================================================
#   configuration.py --------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import expmgmt.config.settings

from configparser import ConfigParser, ExtendedInterpolation
import logging
import os
import sys

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class Configuration(ConfigParser):

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(self):
        
        # innitialization
        ConfigParser.__init__(self, interpolation=ExtendedInterpolation())

        self.logger = logging.getLogger("config")

        # get folder where the configuration files are stored and the path of the main configuration file
        self.dir_location = expmgmt.config.settings.get_config_folder()
        self.file_location = expmgmt.config.settings.get_config_file()

        # get folder where the scripts are stored
        self.scripts_location = expmgmt.config.settings.get_scripts_folder()

        # get folder where the experiments are stored
        self.experiments_location = expmgmt.config.settings.get_projects_folder()

        self.initialize()

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def handle_includes(self):
        """Include all defined configuration files in section 'include'.

        The specified file in field 'additional-configuration-file' in the following example will be read if it exists.

        ::
            [include]
            additional-configuration-file = A:\\.config\\additional-configuration-file.ini
        """

        # if sectiuon 'include' is not defined return
        if not "include" in self.keys():
            return
            
        # read additional configuration files if exists
        for name in self["include"]:
            self.logger.debug("Including {0}".format(name))  # @log
            fullpath = os.path.expanduser(self.get("include", name))
            if os.path.exists(fullpath):
                self.read(fullpath)
            else:
                self.logger.warning(
                    "{0} not included because it does not exist".format(
                        fullpath
                    )
                ) # @log

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def initialize(self):

        #   create directory structure --------------------------------------

        # create configuration folder, e.g. /home/user/.config
        if not os.path.exists(self.dir_location):
            self.logger.warning(
                'Creating configuration folder in %s' % self.dir_location
            ) # @log
            os.makedirs(self.dir_location)

        # create scripts and experiments folder, e.g. /home/user/.config/scripts and /home/user/.config/experiments
        if not os.path.exists(self.scripts_location):
            os.makedirs(self.scripts_location)
        if not os.path.exists(self.experiments_location):
            os.makedirs(self.experiments_location)

        #   create configuration file ---------------------------------------
        #   execute additional script files ---------------------------------
        if os.path.exists(self.file_location):
            # read configurations file if it exists
            self.logger.debug(
                'Reading configuration from {0}'.format(self.file_location)
            ) # @log
            self.read(self.file_location)
            self.handle_includes()
        else:
            # create configuration file, e.g. /home/user/.config/config.ini with default settings 
            default_info = expmgmt.config.settings.get_settings_default()
            for section in default_info:
                self[section] = {}
                for field in default_info[section]:
                    self[section][field] = default_info[section][field]
            with open(self.file_location, "w") as configfile:
                self.write(configfile)

        #   execute additional script files ---------------------------------
        configpy = expmgmt.config.settings.get_configpy_file()
        if os.path.exists(configpy):
            self.logger.debug('Executing {0}'.format(configpy)) # @log
            with open(configpy) as fd:
                exec(fd.read())
