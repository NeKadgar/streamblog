# Dockerfile

# Pull base image
FROM python:3.8

# Set envoroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
COPY /server/req.txt /code/
RUN pip3 install -r /code/req.txt

# Copy project
COPY . /code/
RUN ls
RUN pip freeze