FROM python:3.7-alpine
LABEL maintainer="kendra.gibbons@travelperk.com"

ENV PYTHONUNBUFFERED 1
# recommended on docker containers, Prevents buffering of output

COPY ./requirements.txt /requirements.txt
# copy file onto image

RUN pip install -r /requirements.txt
# install predefined requirements

RUN mkdir /app
# make an empty folder on docker image
WORKDIR /app
# this is the new default directory, any application is run from here
COPY ./app /app
# copy local code into docker image

RUN adduser -D user
# make new user, that's only for running applications
# this is for security, we don't want to run as root
USER user
