import os
import pytest
from tempfile import NamedTemporaryFile

from ltp.app import create_app
from ltp.settings import Config

class TestConfig():
    """
    Tests for config setup
    """

    def test_config_from_default(self):
        """
        We should load the default config.ini regardless
        """
        app = create_app(__name__)
        # Additional key that should not be present unless defconfig is read
        assert 'BLOBSTORE_BACKEND' in app.config

    def test_config_overrides_defaults(self):
        """
        When we run the server with a config file, we expect those settings to take
        precedence.
        """
        config_content="""
            [core]
            SERVER_NAME = XXTESTINGXX

            [sqlalchemy]
            DATABASE_URI = sqlite:///:memory:?XXTESTXX
        """

        with NamedTemporaryFile("w", delete=False) as file:
            file.write(config_content)

        config = Config(file=file.name)

        app = create_app(__name__, config=config)

        assert app.config['SERVER_NAME'] == 'XXTESTINGXX'
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:?XXTESTXX'

        os.unlink(file.name)

