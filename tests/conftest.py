import pytest

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
