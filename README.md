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

Misc
----

- [http://schema.org/Organization](schema.org) is a repository of structured data
- [https://en.wikipedia.org/wiki/JSON-LD](JSON-LD (wikipedia))
- [https://datahub.io/](datahub.io) data platform + tools
- [https://old.datahub.io/dataset/nytimes-linked-open-data](datahub NYTimes dataset)
- [https://developer.nytimes.com/semantic_api.json](NYTimes Semantic API)
