FROM python:3.6.7
ADD . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 8000
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENV PYTHONUNBUFFERED 1