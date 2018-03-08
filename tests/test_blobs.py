from io import BytesIO
from .conftest import wrapped

import json


class TestBlobs():
    """
    Tests for /blobs/ endpoint
    """

    BLOB_GOOD_DATA = {
        "headers": {
            "x-upload-content-length": 8,
            "x-upload-content-hash":
            '916f0027a575074ce72a331777c3478d6513f786a591bd892da1a577bf2335f9',
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

        data = {'file': (BytesIO(b'test data'), 'test.txt')}
        headers = self.BLOB_GOOD_DATA['headers']

        response = client.post(path, data=data, headers=headers)

        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 201

        r_blob = json.loads(response.data)['blob']
        orig_headers = self.BLOB_GOOD_DATA['headers']

        assert orig_headers['x-upload-content-length'] == \
            r_blob['content_length']
        assert orig_headers['x-upload-content-hash'] == r_blob['content_hash']
        assert r_blob['content_type']
        assert r_blob['created_at']
        assert r_blob['id'] > 0

    def test_create_blob_fail_bad_hash(self, testresult, request, client):
        """
        Creating a blob without the correct headers should fail
        """

        path = "/api/blobs/"

        data = {'file': (BytesIO(b'test data'), 'test.txt')}
        headers = self.BLOB_GOOD_DATA['headers']
        headers['x-upload-content-hash'] = 'XXX BAD HASH XXX'

        response = client.post(path, data=data, headers=headers)

        wrapped(response, testresult, request)

        status_code = response.status_code
        assert status_code == 201
