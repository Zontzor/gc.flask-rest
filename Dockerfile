FROM ubuntu:16.04

MAINTAINER Alex Kiernan

# Update OS
RUN apt-get update -y
RUN apt-get -y upgrade

# Install Python
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y libmysqlclient-dev

# Create app directory
COPY . /app
WORKDIR /app

# Update pip and install reqs
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose listening port
EXPOSE 5000

# Run server
ENTRYPOINT ["python"]
CMD ["runserver.py"]