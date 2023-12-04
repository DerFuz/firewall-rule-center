# Dockerfile for firewall-rule-center

# Stage to build python-ldap
FROM python:3.11-bookworm AS ldap-build

# dependencies for python-ldap
RUN apt-get update && apt-get install -y \
    build-essential python3-dev libldap2-dev \
    libsasl2-dev slapd ldap-utils tox lcov valgrind && \
    pip wheel --wheel-dir=/tmp python-ldap

# Stage to build mysqlclient
FROM ldap-build AS mysqlclient-build

# dependencies for python-ldap
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev && \
    pip wheel --wheel-dir=/tmp mysqlclient

# install telnet for testing purposes
RUN apt-get update && apt-get install -y telnet

FROM python:3.11-slim-bookworm
# install runtime libraries for python-ldap and mysqlclient (no prod libraries?)
RUN apt-get update && apt-get install -y libldap-2.5-0 default-libmysqlclient-dev

COPY --from=mysqlclient-build /tmp/*.whl /tmp
RUN pip install /tmp/*.whl

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY backend backend
WORKDIR /backend

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]