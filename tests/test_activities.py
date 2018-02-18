import pytest
from pprint import pprint

from ltp.app import create_app
from ltp.settings import TestConfig

"""
Basic tests for flask app object
"""

class TestActivity():

    @pytest.fixture(scope="class")
    def client(self):
        app = create_app(__name__, config=TestConfig)
        client = app.test_client()
        return client

    def wrapped(self, response, testresult, request):
        def finalizer():
            if testresult.rep.failed:
                print(">>>> FAIL <<<<")
                print(response.data.decode("utf-8"))
        request.addfinalizer(finalizer)

    def test_create_activity_success(self, testresult, request, client):
        """
        Creating an activity should succeed
        """
        path = "/api/activities/"
        data = {
                "description": "test activity",
                "items": [ 0,1,2 ]
        }
        response = client.post(path, data=data)
        self.wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 201
        
    def test_activity_empty(self, testresult, request, client):
        """
        Creating an activity with no data should fail
        """
        path = "/api/activities/"
        data = { }

        response = client.post(path, data=data)
        self.wrapped(response, testresult, request)

        status_code = response.status_code
        assert response.status_code == 400

    def test_activity_bad_json(self, testresult, request, client):
        """
        Create an activity with bad JSON
        """
        path = "/api/activities/"
        data = "abcabcd"

        response = client.post(path, data=data)
        self.wrapped(response, testresult, request)

        status_code = response.status_code
        assert response.status_code == 400

    def test_create_activity_no_items(self, testresult, request, client):
        """
        Creating an activity with a description, but no items should fail
        """
        path = "/api/activities/"
        data = { "description": "test activity" }

        response = client.post(path, data=data)
        self.wrapped(response, testresult, request)

        status_code = response.status_code
        assert response.status_code == 400
