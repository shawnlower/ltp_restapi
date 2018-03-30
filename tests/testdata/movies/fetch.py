#!/usr/bin/python3

from rdflib import Graph, URIRef
from urllib.parse import quote, urlparse

url = 'http://dbpedia.org/resource/Category:Films_set_in_colonial_Australia'
g = Graph()
g.parse(url)

triples = list(g.triples((None,
                     URIRef('http://purl.org/dc/terms/subject'),
                     URIRef(url))))
print("Loaded {} films.".format(len(list(triples))))
path = '/home/shawn/projects/rest-app/rest-app.git/tests/testdata/movies/movies_set_in_colonial_australia/'
for film, _, _ in triples:
    url_parsed = urlparse(film)
    if '&' in url_parsed.path:
        url = url_parsed.geturl().replace('&', quote('&'))
    else:
        url = url_parsed.geturl()

    filename = film.split('/')[-1]
    print("{} -> {}".format(film, filename))
    g = Graph()
    try:
        g.parse(url)
    except Exception as e:
        print("Failed to parse {}".format(url))
        continue

    try:
        with open("{}/{}.json".format(path, filename), 'wb') as f:
            f.write(g.serialize(format='json-ld'))
    except Exception as e:
        print("Failed to serialize/write file: {}".format(e))
