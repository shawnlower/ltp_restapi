Requirements
============

- Python 3
- flask
- pytest
- swagger

Getting Started
===============
```
$ virtualenv-3.6 venv
$ . ./venv/bin/activate
$ python -m setup build
```

TODO
====
- [ ] Remove unused fields (id, created_at) from POST
- [ ] Enforce JSON-LD on items
- [ ] Create schemas for items/activities
- [ ] Search/Filtering
- [ ] Relationships
- [ ] Support [https://tools.ietf.org/html/rfc6902](JSON PATCH rfc6902)

Resources
=========

Framework
---------

- Source
[https://github.com/noirbizarre/flask-restplus](github.com/noirbizarre/flask-restplus)

- Docs
  [http://flask-restplus.readthedocs.org](flask-restplus.readthedocs.org)

- Building beautiful REST APIs using Flask, Swagger UI and Flask-RESTPlus
  Michał Karzyński, EuroPython 2016
  http://michal.karzynski.pl/blog/2016/08/22/europython-2016-presentation/

- [https://rdflib.readthedocs.io/en/stable/intro_to_graphs.html](RDFlib: Intro to Graphs)
- [https://github.com/RDFLib/rdflib-sqlalchemy](github:rdflib-sqlalchemy)
- [https://github.com/RDFLib/rdflib-jsonld](github:rdflib-jsonld)
- [https://github.com/digitalbazaar/jsonld.js](github:jsonld.js)
  *NOTE:* links to use JSON CLI tools & reference documentation
- [https://pypi.python.org/pypi/PyLD/0.4.7](PyPI: PyLD)

UI / Visualization
------------------

- [https://github.com/scienceai/jsonld-vis]('Turn JSON-LD into pretty graphs.')
  Also as seen on the [https://json-ld.org/playground/](JSON-LD playground)
- [https://bokeh.pydata.org/en/latest/docs/user_guide/graph.html#layout-providers](Bokeh Plots)
- [https://demo.bokehplots.com/apps/movies](Bokeh plots demo: IMDB explorer) 
- [https://networkx.github.io/documentation/stable/](NetworkX)
- [https://mrnoutahi.com/2016/01/09/Tree-manipulation-with-ETE/](ETE is for Trees)
  *not the actual title*. Blog post on py visualization. ASCII

Misc
----

- [https://json-ld.org/playground/](json-ld playground)
- [https://en.wikipedia.org/wiki/Semantic_integration](wiki:Semantic_integration)
- [https://www.obitko.com/tutorials/ontologies-semantic-web/rdf-elements.html](Ontologies and Semantic Web)
- [https://en.wikipedia.org/wiki/JSON-LD](JSON-LD (wikipedia))
- [https://www.w3.org/TR/ldp-bp/](W3.org: Linked-data Best Practices)
- [https://indico.cern.ch/event/44/contributions/1942542/attachments/940358/1333580/BabikSemanticWeb.pdf](Deep Integration of Python with Semantic Web Technologies)

Data Sources
------------
- [https://datahub.io/](datahub.io) data platform + tools
- [https://old.datahub.io/dataset/nytimes-linked-open-data](datahub NYTimes dataset)
- [https://developer.nytimes.com/semantic_api.json](NYTimes Semantic API)
- [https://stackoverflow.com/questions/19453072/importing-dbpedias-class-hierarchy](StackOverflow: DBpedia question w/ links)
- [http://wiki.dbpedia.org/develop/datasets](DBpedia Datasets)
- [https://www.mediawiki.org/wiki/Extension:Semantic_Hierarchy](MediaWiki)


Grammars / ontology related
---------------------------
- [http://xmlns.com/foaf/spec/#sec-glance](FOAF)
- [https://en.wikipedia.org/wiki/RDF_Schema](wiki:RDF_Schema)
- [http://schema.org/Organization](schema.org) is a repository of structured data
- [http://schema.org/docs/schema_org_rdfa.html](Full RDFa from schema.org)
- [http://prefix.cc/](namespace lookup for RDF developers)
- [https://www.w3.org/2011/rdfa-context/rdfa-1.1](W3.org: RDFa pre-defined prefixes)
  Prefixes that can be used as contexts w/o explicitly defining within HTML
- [http://lov.okfn.org/dataset/lov/](Linked Open Vocabularies)
