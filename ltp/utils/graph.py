from ..database import get_db, get_ns

import json
import logging
from rdflib import BNode, ConjunctiveGraph, Graph, RDF, URIRef
import re
import string
from typing import Dict, Optional, Union
from urllib.error import HTTPError


logging.config.fileConfig('ltp/logging.cfg')
log = logging.getLogger(__name__)


class MissingObjectError(Exception):
    """
    Object does not exist
    """
    def __init__(self):
        self.msg = "Object not found."

class MissingNamespaceError(Exception):
    def __init__(self):
        self.msg = "Namespace not found"


def split_on_namespace(uri, g):
    """
    :param uri: The uri to match against
    :param g: A graph with namespace bindings for a given uri
    :return: [uri_base, term]
    """
    # Not sure if there's any valid case for multiple prefixes, but we'll use
    # the longest just in case

    matches = []
    if str(uri).startswith('http:'):
        # Return all namespaces starting with uri
        namespaces = [ns[1] for ns in g.namespaces()]
        matches = list(filter(lambda ns: str(uri).startswith(ns), namespaces))
        if not matches:
            raise(MissingNamespaceError)
        base = max(matches, key=len)
        _, _, term = uri.partition(base)
    else:
        base, term = uri.split(':', maxsplit=1)

    return [base, term]


def make_pyclass(uri, base=None, graph=None,
                 format='application/rdf+xml,text/rdf+n3'):
    """
    Factory method for generating RDF based classes
    :param uri: String or rdflib.URIRef of a resource that can be dereferenced.
    :param graph: optional graph containing existing triples

    The resource specified must have RDF type information available
    """

    if not base:
        base = uri

    class RDFSchema():

        def __init__(self, source: Union[Dict, None, str, URIRef] = None):
            """
            Source can be any of the following:
            :param source: A URIRef that can be dereferenced
                           A JSON payload
                           A dict() object
            """
            self._id = None

            if not source:
                return

            if isinstance(source, dict):
                self._from_dict(source)
            elif isinstance(source, URIRef) or source.startswith('http'):
                self._from_uri(source)
            else:
                d = json.loads(source)
                self._from_dict(d)

            if not self._id:
                self._id = base + '/' + BNode().toPython()

        def _from_uri(self, uri: Union[URIRef, str]) -> None:
            """
            Populate the class instance based on a passed URI.
            The data may be able to be dereferenced from our graph, but
            if not, we can just have rdflib handle that for us.
            NOTE: If the subject is found in our graph, additional triples
            will not be dereferenced externally.

            :param uri: URIRef or string to be dereferenced
            """

            if not isinstance(uri, URIRef):
                uri = URIRef(uri)

            self._id = uri

            # Create a temp graph if we don't know the subject already
            if uri not in self._g.subjects():
                if uri.startswith(self._base):
                    raise(MissingObjectError)

                g = ConjunctiveGraph
                log.debug(f"Loading subject from {uri}.")
                g.load(uri)
                log.debug(f"Loaded subject from {uri} with {len(g)} triples.")
            else:
                g = self._g

            # Iterate through our properties
            c = 0  # Found counter
            for prop in self.property_map:
                res = list(set(g.objects(subject=uri,
                           predicate=self.property_map[prop])))
                print(prop, self.property_map[prop], res)

                if not res:
                    log.warning(f"Property {prop} not found.")
                    continue

                o = res[0]
                if len(res) > 1:
                    log.warning(f"Found multiple ({len(res)}) values for "
                                "{prop}. Using {o}.")
                if o:
                    setattr(self, prop, str(o))  # TODO: Get proper object type
                    c += 1
            setattr(self, '@id', self._id)
            log.debug(f"Found {c} properties.")

        def _from_dict(self, d):
            """
            Populate our class properties from a source dict
            """
            for k in d:
                # First make sure we're not a JSON-LD specific key
                if k not in self.property_map:
                    log.warn(f"Unknown key in source: {k}")
                    continue
                setattr(self, k, d[k])

            # Ensure we have a context
            if not getattr(self, '@context', None):
                setattr(self, '@context', str(get_ns()))

        def _to_dict(self):
            """
            Returns a dict populated with our properties
            """
            d = {}
            d['@context'] = self._uri
            d['@id'] = self._id
            for k in self.property_map:
                d[k] = getattr(self, k)
            return d

        def _to_json(self):
            return(json.dumps(self._to_dict()))

        def __getitem__(self, item):
            if item not in self.property_map:
                raise IndexError(f"{item} not found.")
            return getattr(self, item)

        def __setitem__(self, item, value):
            if item not in self.property_map:
                raise IndexError(f"{item} not found.")
            setattr(self, item, value)

        def __repr__(self):
            return "JSON of {}: {}".format(self._uri, self._to_dict())

        @classmethod
        def _init(cls, uri, graph=None, format=None):
            """
            - Accept an RDF URI
            - Use rdflib to parse it into a graph
            - Convert any properties into vars
            - Store a URI for any derived classes
            """
            cls._base = base

            if graph:
                cls._g = graph
            else:
                cls._g = ConjunctiveGraph()

            if isinstance(uri, str):
                cls._uri = URIRef(uri)
            elif isinstance(uri, URIRef):
                cls._uri = uri
            else:
                raise TypeError("Expected a string or URIRef for uri")

            # Dereference URL if necessary
            if cls._uri not in cls._g.subjects():
                cls._g.load(str(uri))
                print("Loaded graph with {} triples.".format(len(cls._g)))

            # Get the properties for the class
            cls.property_map = {}
            var_name = ''
            for prop in cls.get_properties():
                labels = cls.get_labels_for_type(prop)
                if labels:
                    var_name = labels[0]
                else:
                    try:
                        var_name = split_on_namespace(prop, cls._g)[1]
                    except MissingNamespaceError:
                        pass

                if not var_name:
                    var_name = str(prop).rpartition('/')[-1]

                # Ensure var names aren't don't begin with caps
                if re.match('^[A-Z]', var_name):
                    m = re.split('^([A-Z]+)', var_name)
                    var_name = m[1].lower() + m[2]

                # Strip invalid chars
                var_name = ''.join(c for c in var_name if c in
                                   string.ascii_letters +
                                   string.digits + '_')

                # Unlikely var name conflicts
                if var_name in cls.property_map:
                    n = 0
                    while True:
                        tmp = f"{var_name}_{n}"
                        if tmp not in cls.property_map:
                            var_name = tmp
                            break
                cls.property_map[var_name] = prop
                setattr(cls, var_name, None)

        @classmethod
        def get_labels_for_type(cls, rdf_t):
            for args in [{'lang': 'en'}, {'lang': ''}, {}]:
                labels = cls._g.preferredLabel(rdf_t, **args)
                if not labels:
                    return []

            return [label_v for (label_t, label_v) in labels]

        @classmethod
        def get_properties(cls):
            q = '''SELECT DISTINCT ?prop WHERE {
                    ?prop <http://schema.org/domainIncludes> ?uri .
                    }
            '''
            results = [p[0] for p in graph.query(q, initBindings={'uri':
                       cls._uri})]
            return results

        @classmethod
        def get(cls, query: Union[None, str, URIRef] = None):
            """
            Return one or more resources of a given type
            :param query: The resource(s) to look up.

            A query can be one of the following:
                URIRef: The full URIRef of an activity
                URI string: The URI as a string
                name/id: The final portion of a URI.
                    ex: get(LTP['Activity'])

            Example:
                >>> get(URIRef("http://example.com/items/Foo"))
                <class 'ltp.database.models.Item'>

                >>> get("http://example.com/items/Foo")
                <class 'ltp.database.models.Item'>

                >>> get("1234abcd")
                <class 'ltp.database.models.Activity'>
            """

            if not query:
                log.debug(f"Returning all items of type {str(cls._uri)}")
                return [cls(s) for s in cls._g.subjects(
                        predicate=RDF['type'], object=cls._uri)]

            if query.startswith('http:'):
                if isinstance(query, URIRef):
                    s = query
                else:
                    s = URIRef(query)
            else:
                s = URIRef(cls._base + '/' + query)

            try:
                return cls(s)
            except MissingObjectError:
                log.warning(f"Object: {uri} not found.")
                return None

        @classmethod
        def get_all(cls):
            """
            Return all resources of a given type. Alias of get()

            Example:
                >>> get_all()
                [<class 'ltp.database.models.Activity'>,
                 <class 'ltp.database.models.Activity'>
                 <class 'ltp.database.models.Activity'>]
            """
            return cls.get()

        @classmethod
        def get_one(cls, query: str):
            """
            Return one or more resources of a given type
            :param query: The resource(s) to look up.

            Examples:
                # Get an activity by UUID
                >>> get("6f5ace2bf9ba-4dad-91a2-011a20e700ca")
                <class 'ltp.database.models.Activity'>
            """
            items = cls.get(query)
            assert(len(items) == 1)
            return items[0]

        def save(self):
            """
            Commits object to database
            TODO: Handle unique items
            """
            d = dict(self._to_dict())
            # We already dereferenced during class creation, so we don't
            # want to pass the context URI (as that would cause us to fetch
            # it again. We can retrieve the context from our graph
            d['@context'] = self._embedded_context()
            d['@type'] = self._uri
            d['@id'] = self._id
            jsonld = json.dumps(d)
            self._g.parse(data=jsonld, format='json-ld')

        def _embedded_context(self):
            """
            Returns a dictionary mapping the properties to URIs
            """
            context = {}
            for key in self.property_map:
                context[key] = {
                    '@id': self.property_map[key]
                }
            return context

    R = RDFSchema
    R._init(uri, graph, format=format)
    return R


