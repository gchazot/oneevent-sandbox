FROM docker.io/python:3.9 AS builder

RUN apt-get update
RUN apt-get install -y build-essential libpq-dev
RUN pip install pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

ADD Pipfile Pipfile.lock /usr/src/

WORKDIR /usr/src

RUN pipenv sync

FROM docker.io/python:3.9-slim AS runtime

ARG USERNAME=oneevent
ARG USER_UID=1000

RUN useradd --no-create-home --uid $USER_UID --user-group $USERNAME

RUN apt-get update && apt-get -y install libxml2 libpq5 && apt-get clean

RUN mkdir -v /usr/src/.venv
COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

WORKDIR /usr/src/
COPY manage.py .
COPY uwsgi.conf .
COPY oneevent_site ./oneevent_site
COPY static ./static
COPY templates ./templates

RUN /usr/src/.venv/bin/python manage.py collectstatic

USER $USERNAME

CMD ["/usr/src/.venv/bin/uwsgi", "--ini", "/usr/src/uwsgi.conf", "--enable-threads"]
