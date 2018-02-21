import json
import pytest
from pprint import pprint

from .conftest import wrapped

class TestItems():
    """
    Tests for /items/ endpoint
    """

    ITEM_GOOD_DATA = {
                "description": "test item",
                "content_type": "text/plain",
        }

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
        data = self.ITEM_GOOD_DATA

        response = client.post(path, data=json.dumps(data), content_type='application/json')
        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 201

    def test_create_item_get_single_item(self, testresult, request, client):
        """
        POST a new item, then ensure we can get it (and the content is right)
        """
        data = self.ITEM_GOOD_DATA

        path = "/api/items/"
        # Post our JSON
        response = client.post(path, data=json.dumps(data), content_type='application/json')

        retrieved_item = json.loads(response.data)['item']

        # GET the item we just posted
        path = "/api/items/{}".format(retrieved_item['id'])
        response = client.get(path)

        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 200

        # Verify the contents are the same, spare for a few keys
        ignore_keys = ('id', 'created_at', 'items')
        d1 = self.ITEM_GOOD_DATA.copy()
        d1 = dict((k, d1[k]) for k in d1 if not k in ignore_keys)

        d2 = retrieved_item.copy()
        d2 = dict((k, d1[k]) for k in d1 if not k in ignore_keys)

        assert d1 == d2

