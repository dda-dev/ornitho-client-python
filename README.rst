Python Ornitho API Client
=========================

The following "ornitho controllers / calls" are implemented:

- taxonomic groups

  - List taxo groups
  - Get a single taxo group

- families

  - List families
  - Get a single family

- species

  - List species
  - Get a single species

- territorial units

  - List territorial units
  - Get a single territorial unit

- local admin units

  - List local admin units
  - Get a single local admin unit

- places

  - List places
  - Get a single place

- observers

  - List Observers
  - Get a single observer
  - Get an observer rights list
  - Get current observers info

- entities

  - List entities
  - Get a single entity

- protocol

  - List protocol
  - Get a single protocol
  - Get list of sites for protocol id
  - Get PDF for site id

- observations

  - List observations
  - Get a single observation
  - Create an observation
  - Update an observations (**WIP**)
  - Delete an observations
  - Search an observation
  - Search update or deletion since a given date
  - Delete a record
  - Delete a list

- fields

  - List fields
  - Get a single field options

- media

  - Get a single media

Not yet Implemented:

- local admin units

  - Search local admin units

- export organizations

  - List export organizations
  - Get a single export organization

- observations

  - Search closest observations
  - Search last observations
  - Search rare observations
  - Search my observations
  - Search observations from a list of observers
  - Search observations from a list of coordinates
  - Search resources linked to an observation
  - Create a new resources for an observation

- import files

  - List import files
  - Get a single import file

- import files/observations

  - List links for import files and observations
  - Get a single link between import file and observation

- validations

  - List validations
  - Get a single validation

- mortality information

  - List mortality informations

- bearded vulture birds

  - List all bearded vulture birds
  - Get a single bird

- bearded vulture information

  - List bearded vulture informations

- observations by polygon

  - List observations_by_polygon
  - Get a single family
  - Get a single group

- polygons

  - Get a single polygon
  - List polygons from a group
  - List polygon groups
  - List cache for a given polygon or group with a period
  - List form cache for a given polygon or group with a period
  - List species form cache for a given polygon or group with a period
  - List observer cache for a given polygon or group
  - List observer species cache for a given polygon or group

Installing
----------
The project is published on `PyPI <https://pypi.python.org/pypi/ornitho>`__, and can be install using pip or any other package manager:

``$ pip install ornitho``

Manual installation can be done with following command:

``$ pip install .``

Usage
-----
Before the client can be used  **consumer_key**, **consumer_secret**, **user_email**, **user_pw** and **api_base** must be set:

.. code-block:: python

    import ornitho

    ornitho.consumer_key = "CONSUMER_KEY"
    ornitho.consumer_secret = "CONSUMER_SECRET"
    ornitho.user_email = "USER_MAIL"
    ornitho.user_pw = "USER_PASSWORD"
    ornitho.api_base = "https://www.ornitho.de/api/"

The client can then be used.

Examples
~~~~~~~~~~~~~
Following code shows how to get all observation from ornitho.de between 01.10.2019 and 31.10.2019:

.. code-block:: python

    import os
    import ornitho

    ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
    ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
    ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
    ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
    ornitho.api_base = "https://www.ornitho.de/api/"
    
    resp = ornitho.Observation.search_all(period_choice="range", date_from="01.10.2019", date_to="31.10.2019")
    print(f"Found {len(resp)} observations between 01.10.2019 and 31.10.2019")
    
More examples can be found the `examples <https://github.com/dda-dev/ornitho-client-python/tree/master/examples>`__ folder.

Prerequisites
~~~~~~~~~~~~~

The project has been tested with the following python versions:

- Python 3.6
- Python 3.7
- Python 3.8

Collaborate
-----------

Any kind of help with the project will be well received, and there are
two main ways to give such help:

- Reporting errors and asking for extensions through the issues management
- or forking the repository and extending the project

Issues management
~~~~~~~~~~~~~~~~~

Issues are managed at the Github `project issues
tracker <https://github.com/dda-dev/ornitho-client-python/issues>`__, where
any Github user may report bugs or ask for new features.

Testing
~~~~~~~

The tests included with the project can be run with:

``$ pytest``

or with a coverage report:

``$ pytest --cov=ornitho tests/``

To test all supported Python versions, use tox:

``$ tox``

License
-------

The project has been released under the `MIT
License <https://opensource.org/licenses/MIT>`__.
