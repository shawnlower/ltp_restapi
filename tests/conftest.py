from ltp.app import create_app
from ltp.settings import Config

import os
import pytest
from tempfile import NamedTemporaryFile

@pytest.fixture
def testresult():
    class TestResult:
        pass
    return TestResult()


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    if call.when == "call":
        if "testresult" in item.fixturenames:
            rep = __multicall__.execute()
            item.funcargs["testresult"].rep = rep
            return rep


@pytest.fixture()
def client():
    config = Config(env='testing')
    # Enforce a temp file
    with NamedTemporaryFile(prefix='ltp_test.', suffix='.db') as file:
        print("Using: {} as temp DB".format(file.name))
        config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file.name
        app = create_app(__name__, config=config)
        yield app.test_client()


def wrapped(response, testresult, request):
    def finalizer():
        if testresult.rep.failed:
            print(">>> HEADERS: \n" + str(response.headers))
            print(">>> DATA: \n" + response.data.decode("utf-8"))
    request.addfinalizer(finalizer)
