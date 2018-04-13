from rdflib import ConjunctiveGraph, Graph, URIRef

import re
import string


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


def make_pyclass(uri, g=None, format='application/rdf+xml,text/rdf+n3'):
    """
    Factory method for generating RDF based classes
    :param uri: String or rdflib.URIRef of a resource that can be dereferenced.

    The resource specified must have RDF type information available
    """
    class RDFSchema():

        def __init__(self, source):
            """
            Source can be any of the following:
            :param source: A URIRef that can be dereferenced
                           A JSON payload
                           A dict() object
            """

        @classmethod
        def _init(cls, uri, g=None, format=None):
            """
            - Accept an RDF URI
            - Use rdflib to parse it into a graph
            - Convert any properties into vars
            - Store a URI for any derived classes
            """
            if type(uri) == str:
                cls._uri = URIRef(uri)
            elif type(uri) == URIRef:
                cls._uri = uri
            else:
                raise TypeError("Expected a string or URIRef for uri")

            if not g:
                g = Graph()
                g.load(str(uri))
                print("Loaded graph with {} triples.".format(len(g)))
            cls._g = g

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
                
                # print("Initial var name: " + var_name)
                # normalization ##
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
        def get_labels_for_type(rdf_t):
            for args in [{'lang': 'en'}, {'lang': ''}, {}]:
                labels = g.preferredLabel(rdf_t, **args)
                if not labels:
                    return []

            return [label_v for (label_t, label_v) in labels]

        @classmethod
        def get_properties(cls):
            q = '''SELECT DISTINCT ?prop WHERE {
                    ?prop <http://schema.org/domainIncludes> ?uri .
                    }
            '''
            results = [p[0] for p in g.query(q, initBindings={'uri':
                       cls._uri})]
            return results

    R = RDFSchema
    R._init(uri, g, format=format)
    return R

# We can either look for type information in an existing graph, or fetch it
# remotely
# If we supply a graph, we assume the former

# g = Graph()
# uri = SCHEMA['Thing']
# g.load(uri)

# Thing = make_pyclass(uri, g)
# [ i for i in dir(Thing) if not i.startswith('__')]

# Activity = make_pyclass(s, g)
