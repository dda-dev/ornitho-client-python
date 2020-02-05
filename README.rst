Python Ornitho API Client
=========================

The following "ornitho controllers / calls" are implemented:

- taxonomic groups

  - List taxo groups
  - Get a single taxo group

- species

  - List species
  - Get a single species

- places

  - List places
  - Get a single place

- observers

  - List Observers
  - Get a single observer

- observations

  - List observations
  - Get a single observation
  - Search an observation
  - Search update or deletion since a given date

Not yet Implemented:

- families
- territorial units
- local admin units
- entities
- export organizations
- fields
- media
- import files
- import files/observations
- validations
- mortality information
- bearded vulture birds
- bearded vulture information

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

The project has been tested in the following versions of the
interpreter:

- Python 3.6
- Python 3.7
- Python 3.8

All other dependencies are indicated in the Pipfile.

These can be installed with pipenv:

``$ pipenv install``

``$ pipenv install --dev``

Installing
~~~~~~~~~~
**Currently not published on pypi!**

.. The project will be offered as a `Pypi
   package <https://pypi.python.org/pypi/ornitho>`__, and using pip /
   pipenv is the preferred way to install it. For this use the following
   command:

   ``$ pip install ornitho``

Manual installation can be done with following command:

``$ python setup.py install``

Used Libraries
--------------
https://github.com/requests/requests-oauthlib

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

To test all supported Python versions, use tox:

``$ tox``

License
-------

The project has been released under the `MIT
License <https://opensource.org/licenses/MIT>`__.
