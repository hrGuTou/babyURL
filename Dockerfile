FROM tiangolo/uwsgi-nginx:python3.7


RUN apk --update add bash nano
# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /var/www/babyURL/babyURL/static


COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt