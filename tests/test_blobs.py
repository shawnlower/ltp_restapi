from collections import OrderedDict
from io import StringIO, BytesIO
import json
import pytest
from pprint import pprint

from .conftest import wrapped

class TestBlobs():
    """
    Tests for /blobs/ endpoint
    See also:
     - https://github.com/pallets/flask/blob/master/examples/minitwit/tests/test_minitwit.py
    """

    BLOB_GOOD_DATA = {
        "headers": {
            "x-upload-content-length": 8,
            "x-upload-content-hash":
                '916f0027a575074ce72a331777c3478d6513f786a591bd892da1a577bf2335f9',
        },
        'data': {
            'file': (BytesIO(b'test data'), 'test.txt')
        }
    }

    def test_create_blob_fail_noheaders(self, testresult, request, client):
        """
        Creating a blob without the correct headers should fail
        """
        path = "/api/blobs/"

        response = client.post(path, data={
            'file': (BytesIO(b'test data'), 'test.txt')})

        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 400

    def test_create_blob_success(self, testresult, request, client):
        """
        Creating a blob should succeed
        """
        path = "/api/blobs/"

        response = client.post(path, 
                        headers = self.BLOB_GOOD_DATA['headers'],
                        data = self.BLOB_GOOD_DATA['data'])

        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 201

        r_blob = json.loads(response.data)['blob']
        orig_headers = self.BLOB_GOOD_DATA['headers']

        assert orig_headers['x-upload-content-length'] == r_blob['content_length']
        assert orig_headers['x-upload-content-hash'] == r_blob['content_hash']
        assert r_blob['content_type']
        assert r_blob['created_at']
        assert r_blob['id'] > 0

    def test_create_blob_fail_bad_hash(self, testresult, request, client):
        """
        Creating a blob without the correct headers should fail
        """

        assert "Test Not implemented" == '  :-(  '
