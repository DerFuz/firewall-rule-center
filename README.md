![FRC logo](docs/Logo.png)

# Firewall Rule Center

This project is a prototype of a REST API Backend for documenting simple Layer-3/Layer-4 network firewall rules. It should help administrators to keep the desired state of these rules in one place and provide this information as a single-source-of-truth. It was written by *Jakob Wölfl* as part of his bachelors' thesis.

The project was developed and tested with Python3.11 and Django 4.2.6



## Installing / Getting started

### Running it locally

1. Install required dependencies (for python-ldap and mysqlclient) 

    Debian:
```shell
sudo apt install build-essential python3.11-dev libldap2-dev libsasl2-dev slapd ldap-utils tox lcov valgrind default-libmysqlclient-dev pkg-config
```

2. Install Python packages

```shell
pip install -r requirements.txt
```

3. Generate Django `SECRET_KEY`
```shell
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

4. Adapt `.env`-File. Replace `SECRET_KEY` in environment variables and change other values according to your needs.

5. Verify that your configured database is online and reachable.
6. Run Django migrations and create default FRC usergroups and permissions.

```shell
python manage.py migrate
python manage.py create_frc_groups
```

7. Create Django Superuser
```shell
python manage.py createsuperuser
```

8. Run Django Developmentserver
```shell
python manage.py runserver
```

### Running it as a container

1. Generate Django `SECRET_KEY` - either you have django installed in your local python environment and run step 3 from above, or you use [Djecrety](https://djecrety.ir/) to generate the key once.

2. Adapt `.env`-File. Replace `SECRET_KEY` in environment variables and change other values according to your needs.

3. Build Container
```shell
docker build -t frc-backend -f Dockerfile .
```


## Features:

- REST API Backend provides following components/functions:
  - ***Rule***
    - Add new *Rule*
    - View all *Rules*
    - View specific *Rule*
    - Update specific *Rule*
    - Delete specific *Rule*
    - Import *Rules* from CSV
  - ***RuleSetRequest***
    - Add new *RuleSetRequest*
    - View all *RuleSetRequests*
    - View specific *RuleSetRequest*
    - Approve/Refuse specific *RuleSetRequest*
  - ***Firewall***
    - View all *Firewalls*
  - ***User***
    - View all *Users*
  - ***Authentication***
    - Tokenauthentication
    - JWT Authentication

For a comprehensive API description visit the OpenAPI Doc [here](backend/schema.yml) or when the application is running at `/api/schema/`, `/api/schema/redoc/` or `/api/schema/swagger-ui/`. (no custom descriptions and examples yet...)

All other functions are currently not implemented or available for staff-members via the admin panel.

## Licensing 

TBD