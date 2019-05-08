====
EXIT
====
This is a small Django project. The basic for a multiple choice game.

Setup
-----
Linux::

  $ python3 -m venv venv
  $ source venv/bin/activate

Windows::

  $ python -m venv venv
  $ venv\Scripts\activate

Install requirements::

  $ python -m pip install --upgrade pip
  $ python -m pip install -r requirements.txt

Setup Django::

  $ python manage.py migrate

Import some game data::

  $ python manage.py import examples --delete

Create super user (Optional)::

  $ python manage.py createsuperuser

Tools
-----
Run development server::

  $ python manage.py runserver

Check unused imported::

  $ python -m pip install flake8
  $ flake8 --select F401 exit

Tests::

  $ python -m pip install --upgrade tox
  $ python tests/manage.py test simplechoice
  $ tox
