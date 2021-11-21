# PurBeurre Project
OC project n°10

Deploy a Django app on a server.
See https://github.com/RiwsPy/OC_P8
For more informations.


#### Languages:
* Python3.8
* HTML5
* CSS3
* Javascript

#### Tools:
* Django (version 3.2.7)
* Bootstrap (for design)
* PostgreSQL

#### API:
* OpenFoodFacts

### Prerequisites:
* Python3
* PostgreSQL
* pipenv


## Monitoring & automatic task manager
* Supervisor
* Travis
* newRelic
* Sentry
* Crontab


## Program flow: online use
This application is available in: 
http://165.232.112.10/


### Architecture:
- .env
- .gitignore
- .travis.yaml
- Procfile
- Pipfile
- Pipfile.lock
- manage.py
- PurBeurre/
    - settings/
        - __init_.py
        - development.py
        - production.py
        - travis.py
    - asgi.py
    - urls.py
    - wsgi.py
- catalogue/
    - fixtures/
    - tests/
        - db_product_mock.json
        - test_import_off.py
        - test_models.py
        - test_pages.py
    - admin.py
    - apps.py
    - forms.py
    - models.py
    - urls.py
    - views.py
- static/
    - css/
    - img/
    - js/
- templates/layouts/
    - 404.html
    - 500.html
    - base.html
    - header.html
    - mentions.html
    - message.html
    - product_presentation.html
    - search_form_nav.html
    - search.htmll
- user/
    - templates/
        - account.html
        - favorite.html
        - login.html
        - register.html
    - tests/
        - geckodriver.exe
        - test_functionnal.py
        - tests.py
    - admin.py
    - apps.py
    - forms.py
    - models.py
    - urls.py
    - views.py
