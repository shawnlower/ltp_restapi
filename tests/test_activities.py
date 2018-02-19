import json
import pytest
from pprint import pprint

from ltp.app import create_app
from ltp.settings import TestConfig

"""
Basic tests for flask app object
"""


##################
# Helper functions
##################

@pytest.fixture(scope="module")
def client():
    app = create_app(__name__, config=TestConfig)
    client = app.test_client()
    return client

def wrapped(response, testresult, request):
    def finalizer():
        if testresult.rep.failed:
            print(">>>> FAIL <<<<")
            print(response.data.decode("utf-8"))
    request.addfinalizer(finalizer)

##################
# Activities
##################

class TestActivity():

    def test_get_activity_success(self, testresult, request, client):
        """
        Simplest GET /activities/ invocation
        """
        path = "/api/activities/"

        response = client.get(path)
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 200
        assert json.loads(response.data)

    def test_create_activity_success(self, testresult, request, client):
        """
        Creating an activity should succeed
        """
        path = "/api/activities/"
        data = {
                "description": "test activity",
                "items": [ 
                    {"id": 0, "content_type": 'text/plain'}
                    ]
        }

        response = client.post(path, data=json.dumps(data), content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 201
        
    def test_create_activity_empty(self, testresult, request, client):
        """
        Creating an activity with no data should fail
        """
        path = "/api/activities/"
        data = { }

        response = client.post(path, data=data, content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert response.status_code == 400

    def test_create_activity_empty_items(self, testresult, request, client):
        """
        Creating an activity should succeed
        """
        path = "/api/activities/"
        data = {
                "description": "test activity",
                "items": [ ]
        }

        response = client.post(path, data=json.dumps(data), content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 400

    def test_activity_bad_json(self, testresult, request, client):
        """
        Create an activity with bad JSON
        """
        path = "/api/activities/"
        data = "abcabcd"

        response = client.post(path, data=data, content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert response.status_code == 400

    def test_create_activity_no_items(self, testresult, request, client):
        """
        Creating an activity with a description, but no items should fail
        """
        path = "/api/activities/"
        data = { "description": "test activity" }

        response = client.post(path, data=data, content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert response.status_code == 400

##################
# Items
##################

class TestItems():

    def test_get_item_success(self, testresult, request, client):
        """
        Simplest GET /items/ invocation
        """
        path = "/api/items/"

        response = client.get(path)
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 200
        assert json.loads(response.data)

    def test_create_item_success(self, testresult, request, client):
        """
        Creating an item should succeed
        """
        path = "/api/items/"
        data = {
                "description": "test item",
                "content_type": "text/plain",
        }

        response = client.post(path, data=json.dumps(data), content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 201
