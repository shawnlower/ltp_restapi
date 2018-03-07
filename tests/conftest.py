import pytest

from ltp.app import create_app
from ltp.settings import Config


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


@pytest.fixture(scope="module")
def client():
    config = Config(env='testing')
    app = create_app(__name__, config=config)
    client = app.test_client()
    return client


def wrapped(response, testresult, request):
    def finalizer():
        if testresult.rep.failed:
            print(">>> HEADERS: \n" + str(response.headers))
            print(">>> DATA: \n" + response.data.decode("utf-8"))
    request.addfinalizer(finalizer)
