# start from an official image
FROM python:3.8

MAINTAINER Pius Musyoki

# Python Domain
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# arbitrary location choice: you can change the directory
RUN mkdir -p /backend
WORKDIR /backend

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# copy our project code
COPY . /backend
RUN chmod a+x /backend/entrypoint.sh
RUN chmod a+x /backend/wait-for-it.sh

# define the default command to run when starting the container
ENTRYPOINT ["/backend/entrypoint.sh"]
