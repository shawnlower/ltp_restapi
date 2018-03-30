from rdflib import URIRef, RDF

import logging

log = logging.getLogger(__name__)

def find_existing(source_graph, subject, rdf_type, search_graph):
    """
    Find any any existing triples in g2 that match all (p,o) of g1

    example:
        # Does a given movie exist in graph g2, possibly with a
        # different subject URI?
        movie = URIRef('http://dbpedia.org/resource/'
                       'For_the_Term_of_His_Natural_Life_(1908_film)')

        t_movie = URIRef('http://schema.org/Movie')
        g1 = Graph()
        g1.parse(movie)
        match = compare_graph(g1, movie, t_movie, g2)
    """
    for candidate_subject in search_graph.subjects(
            predicate=RDF['type'], object=rdf_type):
        matched = True
        # Iterate through all triples from our source
        for (p, o) in source_graph[subject]:
            if (candidate_subject, p, o) not in search_graph:
                matched = False
                break
        if matched:
            log.debug("Subject: {} matches".format(candidate_subject))
            return candidate_subject


