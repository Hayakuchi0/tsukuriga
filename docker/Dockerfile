FROM ubuntu
MAINTAINER Hayakuchi <hayakuchi@hinesm.info>
ADD ./Pipfile /tmp/Pipfile
ADD ./depend.sh /tmp/depend.sh
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONIOENCODING=utf-8
RUN /tmp/depend.sh
ENTRYPOINT python3 /var/www/html/manage_dev.py makemigrations && python3 /var/www/html/manage_dev.py migrate && python3 /var/www/html/manage_dev.py runserver_plus 0.0.0.0:8000
VOLUME ["/var/www/html"]
EXPOSE 8000
