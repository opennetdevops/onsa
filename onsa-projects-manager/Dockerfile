FROM ubuntu:18.04
MAINTAINER fibercorplabs@cv.fibercorp.com.ar
EXPOSE $EXPOSE
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev
COPY ./requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
COPY . /usr/src/app