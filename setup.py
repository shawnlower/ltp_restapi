from setuptools import setup

setup(
    name='ltp',
    packages=['ltp'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'flask-restplus',
        'rdflib',
        'rdflib_jsonld',
        'rdflib-sqlalchemy'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'flake8'
    ],
)
