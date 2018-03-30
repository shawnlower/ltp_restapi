#
# Run me with ipython -i <filename>
#

import rdflib
from rdflib import URIRef, BNode, Graph
from rdflib.plugin import register, Parser

from glob import glob
import os

path = 'movies_set_in_colonial_australia'

register('json-ld', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')


files = glob(path + '/*')

g = Graph()

assert(os.path.exists(files[0]))

for file in files:
    print("graph size: {}".format(len(list(g))))
    g.parse(data=open(file).read(), format='json-ld')


