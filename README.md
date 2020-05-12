No free view, no review
=======================

[![Build Status](https://travis-ci.com/dissemin/no-free-view-no-review.svg?token=vbDxkTY7k7fuYEqBFHjD&branch=master)](https://travis-ci.com/dissemin/no-free-view-no-review)
[![Coverage Status](https://coveralls.io/repos/dissemin/no-free-view-no-review/badge.svg?branch=master&service=github)](https://coveralls.io/github/dissemin/no-free-view-no-review?branch=master)

Sign the pledge: https://nofreeviewnoreview.org/

This is a [CAPSH](https://association.dissem.in/) project.

This simple app is powered by Django. To run it, clone the repository, and run:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "from .dev import *" > nfvnr/settings/__init__.py
python manage.py migrate
python manage.py runserver
```

To deploy it on a web server, see [Django's docs](https://docs.djangoproject.com/en/3.0/howto/deployment/).

Configuring ORCID login
-----------------------

Create a superuser to access the admin interface:

```
python manage.py createsuperuser
```

Create an ORCID Sandbox account at https://sandbox.orcid.org/

Create OAuth credentials at https://sandbox.orcid.org/developer-tools (enable the public API for that).
This gives you a pair of client ID and client secret.

Log into the admin interface at http://localhost:8000/admin/ with your superuser credentials created above.

Create a new social application at http://127.0.0.1:8000/admin/socialaccount/socialapp/add/

Select orcid.org as provider
Input the client ID and secret in the first two text fields.
Add the example.com site to the list of allowed sites
Save the social app.

For production, do the same with https://orcid.org/ instead of https://sandbox.orcid.org/.
