#!/usr/bin/env python

from ltp import app
from ltp import settings
from ltp.settings import Config

import argparse
import logging
import os

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run Flask interactively.')
    parser.add_argument('--config', help='Config file with app settings '
                        '(default: {})'.format(settings.DEFAULT_CONFIG))
    parser.add_argument('-e', '--environment', help='Set the environment '
                        '(e.g. testing). This uses the config overrides '
                        '(core:testing). [NOTE]: You should NOT use this to '
                        'separate prod/dev in the same file.')
    args = parser.parse_args()

    config_file = None
    if args.config:
        config_file = args.config
    elif 'LTP_CONFIG' in os.environ:
        config_file = os.environ['LTP_CONFIG']

    config = Config(file=config_file, env=args.environment)

    ltp_app = app.create_app(__name__, config)
    log.info('>>> Starting development server at http://{}/api/'.format(
        ltp_app.config['SERVER_NAME']))
    ltp_app.run()


if __name__ == '__main__':
    main()
