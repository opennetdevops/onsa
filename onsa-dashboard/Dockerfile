FROM ubuntu:18.04
EXPOSE ${EXPOSE}
RUN apt-get update -q
RUN apt-get -q install -y gnupg2
RUN apt-get -q install -y curl
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get -q install -y nodejs

# set working directory
RUN mkdir /usr/src/onsa-dash
WORKDIR /usr/src/onsa-dash

ENV PATH /usr/src/onsa-dash/node_modules/.bin:$PATH

# install and cache dependencies
COPY package.json /usr/src/onsa-dash/package.json
COPY ./src /usr/src/onsa-dash/src
COPY ./public /usr/src/onsa-dash/public
RUN npm install --silent
RUN npm install react-scripts@2.1.1 -g --silent