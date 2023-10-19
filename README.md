# Firewall Rule Center

This project is a prototype of a REST API Backend for documenting simple Layer-3/Layer-4 network firewall rules. It should help administrators to keep the desired state of these rules in one place and provide this information as a single-source-of-truth. It was written by *Jakob Wölfl* as part of a bachelors thesis.


## Installing / Getting started

Pre-Requisites:

Debian:
```shell
sudo apt install build-essential python3.11-dev libldap2-dev libsasl2-dev slapd ldap-utils tox lcov valgrind default-libmysqlclient-dev
```

```shell
pip install -r requirements.txt
```


### Initial Configuration

TBD

## Features:

- REST API Backend providing following components/functions:
  - ***Rule***
    - Add new *Rule*
    - View all *Rule*s
    - View specific *Rule*
    - Update specific *Rule*
    - Delete specific *Rule*
    - Import *Rule*s from CSV
  - ***RuleSetRequest***
    - Add new *RuleSetRequest*
    - View all *RuleSetRequest*s
    - Approve/Refuse specific *RuleSetRequest*

All other functions are currently not implemented or available for staff-members via the admin panel.

## Configuration

TBD

## Contributing

TBD

## Links

TBD

## Licensing 

TBD