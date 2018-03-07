from configparser import ConfigParser
import logging
import os
from pprint import pprint, pformat

log = logging.getLogger(__name__)
logging.config.fileConfig('ltp/logging.cfg')

DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), 'config.ini')


class Config(object):

    def __init__(self, file=None, skip_defaults=False, env=None):
        """
        Sets up a config object for use with Flask using an ini file as the
        source. For non-core/flask settings, the config option is constructed
        from the section name and the item, e.g.:

            [sqlalchemy]
            database_uri = ':memory:'

        Is accessed as:

            config = Config()
            config.SQLALCHEMY_DATABASE_URI

        Flask settings and anything else in the [core] section is left as-is

        :param str file: INI file containing settings (e.g. for prod/qa)
        :param bool skip_defaults: Don't load config.ini from settings package
        :param str env: Use a specific environment (e.g. testing)
        """
        self._config = dict()

        if not skip_defaults:
            self.update(DEFAULT_CONFIG)
            if env:
                self.update(DEFAULT_CONFIG, env=env)

        if file:
            self.update(file)
            log.debug("Loaded config: {}".format(file))
            if env:
                self.update(file, env=env)
                log.debug("Updated for env: {}".format(env))

        log.debug("Config initialized with: \n{}".format(
            pformat(self._config)))

    def update(self, file, env=None):
        cp = ConfigParser()
        if not cp.read(file):
            raise IOError("Unable to load settings from {}".format(file))

        # Find relevant sections. If we've specified an environment (env)
        # then we want all sections [section:env] as well as core.
        # If not, we want the inverse.

        config = {}
        for section in cp.sections():
            s_name = section.partition(':')[0]
            s_env = section.partition(':')[2]
            if env and s_env == env:
                config[s_name] = dict(cp[section])
            if not env and not s_env:
                config[section] = dict(cp[section])

        # Merge contents
        for section in config:
            for item in config[section]:
                if section == 'core':
                    # Core / flask settings:
                    key = item.upper()
                else:
                    # Other settings:
                    key = section.upper() + '_' + item.upper()

                self.set(key, config[section][item])

    def set(self, key, value):
        """
        Setter to track updates in dict (e.g. for logging)
        """
        self._config[key] = value
        setattr(self, key, value)
