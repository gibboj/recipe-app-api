FROM python:3.7-alpine
LABEL maintainer="kendra.gibbons@travelperk.com"

ENV PYTHONUNBUFFERED 1
# recommended on docker containers, Prevents buffering of output

COPY ./requirements.txt /requirements.txt
# copy file onto image

RUN apk add --update --no-cache postgresql-client jpeg-dev

#permenent dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

#temporary dependencies, only used for installing the pip packages

RUN pip install -r /requirements.txt
# install predefined requirements

RUN apk del .tmp-build-deps

RUN mkdir /app
# make an empty folder on docker image
WORKDIR /app
# this is the new default directory, any application is run from here
COPY ./app /app
# copy local code into docker image

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user

# make new user, that's only for running applications
# this is for security, we don't want to run as root
RUN chown -R user:user /vol/
# give the user access to the folder & subfolders
RUN chmod -R 755 /vol/web
# give user full rwx perms
USER user
