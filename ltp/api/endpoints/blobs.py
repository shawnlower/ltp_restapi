from flask import request
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from ..restplus import api
from ..serializers import blob
from ...database.models import Blob
from ...database import get_db

from datetime import datetime
import logging
log = logging.getLogger(__name__)

from ..blobstore import validate_hash

ns = api.namespace(
    'blobs', description='Raw upload objects (e.g.  video/audio')

"""
This is a simple 'blob-store' endpoint. It allows uploading arbitrary data to
LTP. It is implemented as a content addressable store, with each blob being
cryptographically hashed - the hash then forming the key used to identify the
object. This allows an Item to be created prior to the object being uploaded to
the object store.

This blob store may also implement a proxy resolver for hash URIs
https://github.com/hash-uri/hash-uri

Workflow:
    - POST /items  ## Create a new item. Any URL attributes can specify a known
                   ## location, e.g. http://<fqdn>/api/objects/<sha-256 hash>

    - POST /objects ## Create the new object at the known location.
"""


upload_parser = api.parser()

upload_parser.add_argument('X-Upload-Content-Length', location='headers',
                           required=True)
upload_parser.add_argument('X-Upload-Content-Type', location='headers')
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@ns.route('/')
class BlobCollection(Resource):

    @api.expect(upload_parser, validate=True)
    @api.response(201, 'Blob created')
    @api.marshal_with(blob, envelope="blob")
    def post(self):
        """
        Creates a new blob

        Example from bash:
        ```shell
        $ file=album_art.jpg
        $ sha=$(sha256sum $file | awk '{print $1}')
        $ curl -X POST -F file=@${file}
               --header 'Content-Type: multipart/form-data'
               --header "X-Upload-Content-Length: $(stat $file --printf=%s)"
               --header 'Accept: application/json'
               --header "X-Upload-Content-Hash: $sha"
               'http://localhost:8888/api/blobs/'
        ```
        """

        file = request.files['file']

        meta = {}
        # Look for meta info in file object
        if file.content_type:
            meta['content_type'] = file.content_type
        if file.content_length:
            meta['content_length'] = file.content_length

        missing_meta = []
        # Check for meta info in headers
        for key in ['content_type', 'content_length', 'content_hash']:

            header = 'x-upload-{}'.format(key.replace('_', '-'))

            if meta.get(key, None):
                # Already set above
                continue
            elif request.headers.get(header):
                # X-Upload-foo exists
                meta[key] = request.headers.get(header)
            else:
                missing_meta.append(header)

        if missing_meta:
            raise BadRequest("Missing meta-data headers: {}".format(
                ', '.join(missing_meta)))

        meta['created_at'] = datetime.utcnow().isoformat()

        blob_file = Blob(**meta)

        db = get_db()
        db.session.add(blob_file)
        db.session.commit()

        return (blob_file, 201)
