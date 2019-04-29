====
EXIT
====
This is a small Django project. It build a basic for a multiple choice game.

Setup
-----
Linux::

  python3 -m venv venv
  source venv/bin/activate

Windows::

  python -m venv venv
  venv\Scripts\activate

Install requirements::

  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt

Setup Django::

  python exit\manage.py migrate
  python exit\manage.py createsuperuser

Import some game data::

  python exit\manage.py import examples\questions-1.json
  python exit\manage.py import examples\exits.json

Run development server::

  python exit\manage.py runserver

Tools
-----
Check unused imported::

  python -m pip install flake8
  flake8 --select F401 exit
