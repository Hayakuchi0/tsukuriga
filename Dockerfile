FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install pipenv
COPY Pipfile /code/
RUN pipenv install --system --ignore-pipfile --dev
RUN apt update && apt install -y ffmpeg
COPY . /code/
RUN python manage_dev.py migrate
