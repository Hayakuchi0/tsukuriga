FROM ubuntu

ENV PYTHONUNBUFFERED 1
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt update
RUN apt install -y build-essential libbz2-dev libdb-dev \
    libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
    libncursesw5-dev libsqlite3-dev libssl-dev zlib1g-dev \
    uuid-dev
RUN apt install -y python3.7 python3.7-dev python3.7-distutils
RUN apt install -y ffmpeg git curl

RUN mkdir /code
COPY . /code/
WORKDIR /code

RUN ln -s /usr/bin/python3.7 /usr/bin/python
RUN curl -kL https://bootstrap.pypa.io/get-pip.py | python
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile --dev

RUN python manage_dev.py migrate
