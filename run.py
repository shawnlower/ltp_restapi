#!/usr/bin/env python

from ltp.app import create_app
from ltp import settings
from ltp.settings import Config

import click
from flask import Flask

import argparse
import logging
import os
import sys

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run Flask interactively.')
    parser.add_argument('-p', '--port', help='Port number to listen on.',
                        type=int, default=8888)
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

    config = Config(file=config_file, env=args.environment)
    app = create_app(__name__, config)

    log.info('>>> Starting development server at http://{}/api/'.format(
        app.config['SERVER_NAME']))
    return app.run(port=args.port)


if __name__ == '__main__':
    sys.exit(main())

# Used by flask, e.g.: 'flask shell', 'flask run'
app = create_app()

