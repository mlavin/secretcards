Secret Cards
============

This is the source code for https://secret.cards. It's simple site for sending
anonymous, encrypted messages in cat pictures. If you would like to add a feature,
fix a bug, or simply see how it works then please continue reading.


Contributing
------------

This project is a fun way for me to play and experiment with various technologies.
If you would like to play and experiment with me, that would be great. This project
doesn't intent to solve any major world problem nor is it likely to make any amount
of money for it's contributors.

In that vein before making any large changes, please add an issue to discuss it first. Changes
which are likely to increase the maintainance burden of the site are likely to
be rejected. Please see the information below about the test suite and code
standards as well.


Project Setup
-------------

To begin work on the project you will need the following software installed

- Python 3.4 including pip and virtualenv. virtualenvwrapper is recommended.
- Postgres 9.0+
- git 1.7+

First fork and clone your copy of the repository::

    $ git clone git@github.com:<username>/secretcards.git
    $ cd secretcards

To setup your local environment you should create a virtualenv and install the necessary requirements::

    # Check that you have python3.4 installed
    $ which python3.4
    $ mkvirtualenv secretcards -p `which python3.4`
    (secretcards)$ make install

Configurable settings are managed with `django-dotenv <https://github.com/jpadilla/django-dotenv>`_.
It reads environment variables located in a file name ``.env`` in the top level directory of the project.
The previous command ``make install`` creates new ``.env`` file with a new ``SECRET_KEY`` value set.

Create the Postgres database and run the initial migrate::

    (secretcards)$ createdb -E UTF-8 {{ project_name }}
    (secretcards)$ python manage.py migrate

You should now be able to run the development server::

    (secretcards)$ python manage.py runserver


Running the Tests
-----------------

The ``Makefile`` for this project has a number of helpful commands for testing
and checking code quality. Below is a brief description of the commands:

- ``make test`` - Runs the full test suite and reports test coverage
- ``make lint`` - Runs a set of subcommands to check code quality

As noted above, ``make lint`` runs a number of subcommands to check the code quality.
These commands can also be run individually:

- ``make lint-py`` - Runs the code through ``flake8`` for static analysis
- ``make lint-migrations`` - Runs Django's checks for model changes without migrations
- ``make lint-django`` - Runs Django's system checks with the base settings
- ``make lint-deploy`` - Runs Django's system checks for deployment

You should ensure that ``make test`` and ``make lint`` both pass cleanly before
submitting a pull request with any changes you wish to include.


License
-------

This source code is available under the BSD license included in the repo. In
the distribution are the source files for jQuery, Underscore, Backbone, Materalize,
kbpgp, Pacifico font, Roboto font, Socicon icons, and Material Design icons
which are distributed under their respective licenses. The images included are
licensed under the Creative Commons Share Alike license.
