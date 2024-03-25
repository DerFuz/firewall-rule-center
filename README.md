![FRC logo](docs/Logo.png)

# Firewall Rule Center

This project is a prototype of a REST API Backend for documenting simple Layer-3/Layer-4 network firewall rules. It should help administrators to keep the desired state of these rules in one place and provide this information as a single-source-of-truth. It was written by *Jakob Wölfl* as part of his bachelors' thesis.

The project was developed and tested with Python3.11 and Django 4.2.6

A corresponding prototype client is available [here](https://github.com/DerFuz/firewall-rule-center_client)

## Installing / Getting started

### Running it locally (development)

1. Install required dependencies (for [python-ldap](https://www.python-ldap.org/en/python-ldap-3.4.3/installing.html#debian)) 

    Debian:
```shell
sudo apt install build-essential python3.11-dev libldap2-dev libsasl2-dev slapd ldap-utils tox lcov valgrind
```

2. Install Python packages

```shell
pip install -r requirements.txt
```

3. Generate Django `SECRET_KEY`
```shell
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
or you use [Djecrety](https://djecrety.ir/) to generate the key once

4. Adapt `.env`-File. Replace `DJANGO_SECRET_KEY` in environment variables and change other values according to your needs.

5. Verify that your configured database is online and reachable.
6. Run Django migrations and create default FRC usergroups and permissions (permissions are documented [here](docs/permission_overview.png)).

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

2. Adapt `.env`-File. Replace `DJANGO_SECRET_KEY` in environment variables and change other values according to your needs.

3. Build Container
```shell
docker build -t frc-backend -f Dockerfile.prod .
```

---

We also provide a rudimentary [docker-compose-File](docker-compose.prod.yaml) for running the "production ready"-containers. The nginx-configuration that is used inside the backend-web-container is located [here](nginx/nginx.conf). Inside there TLS configuration could be provided for example.

## Configuration

| Name                                    | Default   | Description                                                                                                                                                                                                       |
| --------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DJANGO_DEBUG                            | False     | [DEBUG](https://docs.djangoproject.com/en/4.2/ref/settings/#debug)                                                                                            |
| DJANGO_ALLOWED_HOSTS                    | localhost | [ALLOWED_HOSTS](https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts)                                                                            |
| DJANGO_CORS_ALLOWED_ORIGINS             | \-        | [CORS_ALLOWED_ORIGINS](https://pypi.org/project/django-cors-headers/)                                                                                                                    |
| DJANGO_SECRET_KEY                       | \-        | [SECRET_KEY](https://docs.djangoproject.com/en/4.2/ref/settings/#secret-key)                                                                                  |
| DJANGO_LANGUAGE_CODE                    | \-        | [LANGUAGE_CODE](https://docs.djangoproject.com/en/4.2/ref/settings/#language-code)                                                                            |
| DJANGO_TIME_ZONE                        | \-        | [TIME_ZONE](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-TIME_ZONE)                                                            |
| DJANGO_CSRF_TRUSTED_ORIGINS             | \-        | [CSRF_TRUSTED_ORIGINS](https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins)                                                              |
| DJANGO_JWT_ACCESS_TOKEN_LIFETIME_MINS   | 5         | [ACCESS_TOKEN_LIFETIME](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#access-token-lifetime)      |
| DJANGO_JWT_REFRESH_TOKEN_LIFETIME_HOURS | 24        | [REFRESH_TOKEN_LIFETIME](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#refresh-token-lifetime)    |
| DJANGO_AUTH_LDAP_SERVER_URI             | \-        | [LDAP_SERVER_URI](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-server-uri)                                    |
| DJANGO_LDAP_TLS_REQUIRED                | False     | Enable TLS connection to LDAP server                                                                                                                                                                              |
| DJANGO_LDAP_CA_FILE_PATH                | \-        | Path to CA-File of LDAP certificate                                                                                                                                                                               |
| DJANGO_AUTH_LDAP_BIND_DN                | \-        | [AUTH_LDAP_BIND_DN](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-bind-dn)                                          |
| DJANGO_AUTH_LDAP_BIND_PASSWORD          | \-        | [AUTH_LDAP_BIND_PASSWORD](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-bind-password)                              |
| DJANGO_LDAP_USER_BASE_DN                | \-        | Base DN where user accounts reside                                                                                                                                                                                |
| DJANGO_LDAP_USER_FILTER                 | \-        | Filter for user accounts                                                                                                                                                                                          |
| DJANGO_LDAP_GROUP_BASE_DN               | \-        | Base DN where groups reside                                                                                                                                                                                       |
| DJANGO_LDAP_GROUP_FILTER                | \-        | Filter for groups                                                                                                                                                                                                 |
| DJANGO_AUTH_LDAP_USER_FLAGS_BY_GROUP    | \-        | [AUTH_LDAP_USER_FLAGS_BY_GROUP](https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-flags-by-group)<br>given as JSON |
| DJANGO_LDAP_LOGGING_LEVEL               | WARNING   | [https://django-auth-ldap.readthedocs.io/en/latest/logging.html](https://django-auth-ldap.readthedocs.io/en/latest/logging.html)                                                                                  |
| DJANGO_DATABASE_URL                     | \-        | [https://django-environ.readthedocs.io/en/latest/types.html#environ-env-db-url](https://django-environ.readthedocs.io/en/latest/types.html#environ-env-db-url)                                                    |

## Features

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

This project is licensed under the **MIT license**.
See [LICENSE](LICENSE) for more information.