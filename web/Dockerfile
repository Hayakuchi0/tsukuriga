FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt update
RUN apt install -y ffmpeg git

RUN mkdir /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
WORKDIR /code

RUN pip install pipenv

ENV PIPENV_VENV_IN_PROJECT 1
RUN pipenv install --ignore-pipfile --dev
