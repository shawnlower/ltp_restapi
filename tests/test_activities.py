import json
import pytest
from pprint import pprint

from .conftest import wrapped


class TestActivities():
    """
    Tests for /activities/ endpoint
    """

    ACTIVITY_GOOD_DATA = {
        "description": "test activity",
        "items": [
            {"id": 0, "content_type": 'text/plain'}
        ]
    }

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

    def test_create_activity_get_single_activity(self, testresult, request, client):
        """
        POST a new activity, then ensure we can get it (and the content is right)
        """
        data = self.ACTIVITY_GOOD_DATA

        path = "/api/activities/"
        # Post our JSON
        response = client.post(path, data=json.dumps(
            data), content_type='application/json')

        activity_id = json.loads(response.data)['activity']['id']

        # GET the activity we just posted
        path = "/api/activities/{}".format(activity_id)
        response = client.get(path)

        retrieved_activity = json.loads(response.data)['activity']

        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 200

        # Verify the contents are the same, spare for a few keys
        # NOTE: we're skipping the 'items' entirely
        ignore_keys = ('id', 'created_at', 'items')
        d1 = self.ACTIVITY_GOOD_DATA.copy()
        d1 = dict((k, d1[k]) for k in d1 if not k in ignore_keys)

        d2 = retrieved_activity.copy()
        d2 = dict((k, d1[k]) for k in d1 if not k in ignore_keys)

        assert d1 == d2

    def test_create_activity_success(self, testresult, request, client):
        """
        Creating an activity should succeed
        """
        path = "/api/activities/"
        data = self.ACTIVITY_GOOD_DATA

        response = client.post(path, data=json.dumps(
            data), content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 201

    def test_create_activity_empty(self, testresult, request, client):
        """
        Creating an activity with no data should fail
        """
        path = "/api/activities/"
        data = {}

        response = client.post(
            path, data=data, content_type='application/json')
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
            "items": []
        }

        response = client.post(path, data=json.dumps(
            data), content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 400

    def test_activity_bad_json(self, testresult, request, client):
        """
        Create an activity with bad JSON
        """
        path = "/api/activities/"
        data = "abcabcd"

        response = client.post(
            path, data=data, content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert response.status_code == 400

    def test_create_activity_no_items(self, testresult, request, client):
        """
        Creating an activity with a description, but no items should fail
        """
        path = "/api/activities/"
        data = {"description": "test activity"}

        response = client.post(
            path, data=data, content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert response.status_code == 400
